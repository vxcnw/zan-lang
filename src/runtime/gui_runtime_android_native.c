/* gui_runtime_android_native.c -- NativeActivity window/event/present shell
 * (ZAN_GUI_ANDROID_NATIVE).
 *
 * Part of the gui_runtime translation unit: #include'd by gui_runtime.c in
 * a fixed order; not compiled standalone. Plays the role gui_runtime_sdl.c
 * plays for SDL builds and gui_runtime_ohos.c plays for HAP builds: owns
 * the zan_gui_* window/event/present exports, SDL-free.
 *
 * The APK shell is android.app.NativeActivity (a framework class -- zero
 * Java activity code). NDK's android_native_app_glue hosts the app thread:
 * the shell's ANativeActivity_onCreate is provided by the glue archive
 * (linked into libmain.so alongside the module), which spawns the thread
 * that runs android_main(); that thread pumps ALooper for lifecycle
 * commands and the AInputQueue, translates them into the same flat event
 * ring the SDL/OHOS shells use, and blocks in android_main until the Zan
 * program's main() returns. All GL/EGL work happens on this app thread
 * (present) -- input events arrive on the same thread via the looper, so
 * there is no cross-thread GL hazard and no need for SDL's event-watch
 * queue dance.
 *
 * Touch gesture synthesis (slop->drag->wheel, tap->click, fling coast) is
 * a port of the SDL shell's finger layer via the OHOS shell's version, so
 * all three phones scroll identically.
 *
 * Present goes through EGL: the composed CPU surface uploads as one
 * texture (dirty rects on the subrect path) and draws over the attached
 * ANativeWindow. Lifecycle surface loss (APP_CMD_TERM_WINDOW, every
 * background cycle) marks detached; present no-ops until the next
 * APP_CMD_INIT_WINDOW, which pushes the repaint-wake event.
 *
 * IME: NativeActivity offers show/hide soft input natively
 * (ANativeActivity_showSoftInput); committed text needs the GameTextInput
 * static lib (or a small Java InputConnection) -- a later layer. v1
 * shows/hides the keyboard so single-line entry works where the IME
 * commits through key events; rich composing text waits for the JNI
 * bridge.
 */

#ifdef ZAN_GUI_ANDROID_NATIVE

#include <EGL/egl.h>
#include <GLES3/gl3.h>
#include <android/native_activity.h>
#include <android/native_window.h>
#include <android/input.h>
#include <android/keycodes.h>
#include <android/looper.h>
#include <android/configuration.h>
#include <android/window.h>
#include <android/log.h>

#include "android_native_app_glue.h"

static void zan_alog(const char *fmt, ...) __attribute__((format(printf,1,2)));
static void zan_alog(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    __android_log_vprint(ANDROID_LOG_ERROR, "zanShell", fmt, ap);
    va_end(ap);
}
#define ZAN_LOG(...) zan_alog(__VA_ARGS__)
#ifdef ZAN_SHELL_TRACE
#define ZAN_TRACE(...) ZAN_LOG(__VA_ARGS__)
#else
#define ZAN_TRACE(...) ((void)0)
#endif

/* ---- app record ---------------------------------------------------------
 * The glue hands us one android_app; the Zan-facing hwnd is the address of
 * this record, exactly like the SDL shell hands back SDL_Window* and the
 * OHOS shell its window record. */
typedef struct {
    ANativeWindow *nw;    /* NULL while no surface (background cycle) */
    int w, h;             /* attached surface size, device pixels */
    int attached;
    int closed;           /* Close() seen: present becomes a no-op */

    /* EGL present state; created on attach / first present. All calls run
     * on the glue app thread, so plain fields need no lock. */
    EGLDisplay egl_dpy;
    EGLSurface egl_surf;
    EGLContext egl_ctx;
    ANativeWindow *surf_nw;  /* the surface's window (rotation rebuilds) */
    GLuint     gl_prog;
    GLuint     gl_tex;
    GLuint     gl_vbo;
    int        tex_w, tex_h;

    struct android_app *app;   /* back-pointer for IME + window flags */
    int destroy_wait;          /* main() entered with no surface yet */
} zan_anw_t;

static zan_anw_t g_anw;
#define ZAN_ANW_HWND ((iptr)&g_anw)

static int  g_window_width  = 0;
static int  g_window_height = 0;
static int  g_dpi           = 96;

/* ---- event ring --------------------------------------------------------
 * Same flat event protocol as the SDL/OHOS shells: e[0] kind, e[1] x,
 * e[2] y, e[3] button, e[4] code (keycode / wheel delta), e[5] mods,
 * e[6] flag. Kinds that matter here: 1 move, 2 down, 3 up, 4 key, 6 char,
 * 7 resized, 8 close, 13 wheel, 14 force-repaint. */
typedef struct { int e[8]; iptr win; } zan_aev_t;
#define ZAN_AQ_CAP 512
static zan_aev_t g_aq[ZAN_AQ_CAP];
static int g_aq_head = 0, g_aq_tail = 0;
static pthread_mutex_t g_aq_lock = PTHREAD_MUTEX_INITIALIZER;

static int g_pending_event[8];
static iptr g_event_win = 0;
static long long g_ev_seq = 0;

/* Plain moves coalesce (freshest x/y wins) and wheel floods coalesce by
 * SUMMING deltas -- the SDL/OHOS shell contract. */
static void aq_push_locked(int kind, int x, int y, int button, int code, int mods) {
    int last = (g_aq_tail + ZAN_AQ_CAP - 1) % ZAN_AQ_CAP;
    int has_last = (g_aq_head != g_aq_tail);
    if (kind == 1 && has_last && g_aq[last].e[0] == 1) {
        g_aq[last].e[1] = x; g_aq[last].e[2] = y;
        return;
    }
    if (kind == 13 && has_last && g_aq[last].e[0] == 13) {
        g_aq[last].e[1] = x; g_aq[last].e[2] = y;
        g_aq[last].e[4] += code;
        return;
    }
    int next = (g_aq_tail + 1) % ZAN_AQ_CAP;
    if (next == g_aq_head) return; /* full: drop */
    zan_aev_t *z = &g_aq[g_aq_tail];
    z->e[0] = kind; z->e[1] = x; z->e[2] = y; z->e[3] = button;
    z->e[4] = code; z->e[5] = mods; z->e[6] = 0; z->e[7] = 0;
    z->win = ZAN_ANW_HWND;
    g_aq_tail = next;
}

static void aq_push_flag_locked(int kind, int x, int y, int button, int code, int mods) {
    aq_push_locked(kind, x, y, button, code, mods);
    if (g_aq_head != g_aq_tail) {
        int last = (g_aq_tail + ZAN_AQ_CAP - 1) % ZAN_AQ_CAP;
        g_aq[last].e[6] = 1;
    }
}

static int aq_pop(void) {
    pthread_mutex_lock(&g_aq_lock);
    if (g_aq_head == g_aq_tail) { pthread_mutex_unlock(&g_aq_lock); return 0; }
    zan_aev_t *z = &g_aq[g_aq_head];
    for (int i = 0; i < 8; i++) g_pending_event[i] = z->e[i];
    g_event_win = z->win;
    g_aq_head = (g_aq_head + 1) % ZAN_AQ_CAP;
    g_ev_seq++;
    pthread_mutex_unlock(&g_aq_lock);
    return 1;
}

/* ---- lifecycle feed (glue app thread) ---------------------------------- */

static void anw_attach(ANativeWindow *nw) {
    int w = ANativeWindow_getWidth(nw);
    int h = ANativeWindow_getHeight(nw);
    pthread_mutex_lock(&g_aq_lock);
    g_anw.nw = nw;
    g_anw.w = w; g_anw.h = h;
    g_anw.attached = 1;
    g_window_width = w;
    g_window_height = h;
    aq_push_locked(7, w, h, 0, 0, 0);
    /* Surface (re)attached: every pixel is undefined, and an idle app in
     * WaitEvent would keep sleeping (the OHOS shell's kind-14 contract). */
    aq_push_locked(14, 0, 0, 0, 0, 0);
    pthread_mutex_unlock(&g_aq_lock);
}

static void anw_detach(void) {
    pthread_mutex_lock(&g_aq_lock);
    g_anw.attached = 0;
    g_anw.nw = NULL;
    pthread_mutex_unlock(&g_aq_lock);
}

/* ---- touch gesture synthesis (OHOS shell port) --------------------------
 * The first finger's drag beyond an 8 px slop becomes Win32-scale wheel
 * events (kind 13) that move content 1:1 with the finger; a tap under the
 * slop is a full synthesized click at the anchor; finger-up with residual
 * speed coasts (fling) through a 16 ms thread until exponential friction
 * eats it. Formulas verbatim from gui_runtime_ohos.c. */
static i64 ant_tick_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (i64)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

#define ANT_TOUCH_SLOP2   64.0f   /* (8 px)^2: below this, still a tap */
#define ANT_TOUCH_HIST    8       /* release-velocity ring buffer */
#define ANT_FLING_START_PX_S 250.0f
#define ANT_FLING_STOP_PX_S  120.0f
#define ANT_FLING_TAU_MS     400.0f

static int   g_tg_down, g_tg_drag;
static float g_tg_ax, g_tg_ay;
static float g_tg_x, g_tg_y;
static float g_tg_acc;
static long long g_tg_ht[ANT_TOUCH_HIST];
static float g_tg_hy[ANT_TOUCH_HIST];
static int   g_tg_hn, g_tg_hi;

static int   g_fling_active;
static float g_fling_v;
static float g_fling_acc;
static int   g_fling_x, g_fling_y;
static long long g_fling_last;
static pthread_t g_fling_thr;
static int g_fling_thr_up;

static void *fling_thread(void *arg) {
    (void)arg;
    for (;;) {
        int live;
        pthread_mutex_lock(&g_aq_lock);
        live = g_fling_active;
        if (live) {
            long long now = ant_tick_ms();
            float dt = (float)(now - g_fling_last) / 1000.0f;
            g_fling_last = now;
            if (dt > 0) {
                g_fling_v *= expf(-dt * 1000.0f / ANT_FLING_TAU_MS);
                g_fling_acc += g_fling_v * dt * 288.0f / (float)g_dpi;
                int delta = (int)g_fling_acc;
                if (delta != 0) {
                    g_fling_acc -= (float)delta;
                    aq_push_locked(13, g_fling_x, g_fling_y, 0, delta, 0);
                }
            }
            if (fabsf(g_fling_v) < ANT_FLING_STOP_PX_S) g_fling_active = 0;
        }
        pthread_mutex_unlock(&g_aq_lock);
        if (!live) break;
        struct timespec ts = { 0, 16 * 1000 * 1000 };
        nanosleep(&ts, NULL);
    }
    g_fling_thr_up = 0;
    return NULL;
}

static void fling_cancel_locked(void) { g_fling_active = 0; }

static void fling_start(float v, int x, int y) {
    if (fabsf(v) < ANT_FLING_START_PX_S) return;
    pthread_mutex_lock(&g_aq_lock);
    g_fling_v = v;
    g_fling_acc = 0;
    g_fling_x = x; g_fling_y = y;
    g_fling_last = ant_tick_ms();
    g_fling_active = 1;
    int need = !g_fling_thr_up;
    g_fling_thr_up = 1;
    pthread_mutex_unlock(&g_aq_lock);
    if (need && pthread_create(&g_fling_thr, NULL, fling_thread, NULL) != 0)
        g_fling_thr_up = 0;
}

/* One pointer of a motion event. Multi-pointer pinch/rotate is a later
 * layer; the SDL shell's finger layer was single-pointer too. */
static void ant_touch(int action, int x, int y) {
    static int px = 0, py = 0;
    if (x < 0 && y < 0) { x = px; y = py; }
    px = x; py = y;

    if (action == 0) {
        pthread_mutex_lock(&g_aq_lock);
        fling_cancel_locked();
        g_tg_down = 1; g_tg_drag = 0; g_tg_acc = 0;
        g_tg_x = g_tg_ax = (float)x;
        g_tg_y = g_tg_ay = (float)y;
        g_tg_hn = 1; g_tg_hi = 1 % ANT_TOUCH_HIST;
        g_tg_ht[0] = ant_tick_ms(); g_tg_hy[0] = g_tg_y;
        /* Press at finger-down (hold gestures, press-state feedback);
         * a plain move precedes it so hover/enter state settles first. */
        aq_push_locked(1, (int)g_tg_ax, (int)g_tg_ay, 0, 0, 0);
        aq_push_locked(2, (int)g_tg_ax, (int)g_tg_ay, 0, 0, 0);
        pthread_mutex_unlock(&g_aq_lock);
        return;
    }
    if (action == 1 && g_tg_down) {
        pthread_mutex_lock(&g_aq_lock);
        float fx = (float)x, fy = (float)y;
        if (!g_tg_drag) {
            float dx = fx - g_tg_ax, dy = fy - g_tg_ay;
            if (dx * dx + dy * dy < ANT_TOUCH_SLOP2) {
                pthread_mutex_unlock(&g_aq_lock);
                return;
            }
            g_tg_drag = 1;
        }
        /* Finger travel -> wheel deltas in the /120 scale; dragging up
         * must scroll DOWN (content follows the finger), i.e. negative. */
        g_tg_acc += (fy - g_tg_y) * 288.0f / (float)g_dpi;
        int delta = (int)g_tg_acc;
        if (delta != 0) {
            g_tg_acc -= (float)delta;
            aq_push_locked(13, x, y, 0, delta, 0);
        }
        g_tg_ht[g_tg_hi] = ant_tick_ms(); g_tg_hy[g_tg_hi] = fy;
        g_tg_hi = (g_tg_hi + 1) % ANT_TOUCH_HIST;
        if (g_tg_hn < ANT_TOUCH_HIST) g_tg_hn++;
        g_tg_x = fx; g_tg_y = fy;
        if (delta == 0) aq_push_flag_locked(1, x, y, 0, 0, 0);
        pthread_mutex_unlock(&g_aq_lock);
        return;
    }
    if (action == 2 && g_tg_down) {
        g_tg_down = 0;
        pthread_mutex_lock(&g_aq_lock);
        if (g_tg_drag) {
            aq_push_flag_locked(3, (int)g_tg_x, (int)g_tg_y, 0, 0, 0);
            pthread_mutex_unlock(&g_aq_lock);
            int last = (g_tg_hi + ANT_TOUCH_HIST - 1) % ANT_TOUCH_HIST;
            int old = last;
            for (int k = 0; k < g_tg_hn; k++) {
                int idx = (last - k + ANT_TOUCH_HIST) % ANT_TOUCH_HIST;
                if (g_tg_ht[idx] + 120 < g_tg_ht[last]) break;
                old = idx;
            }
            long long span = g_tg_ht[last] - g_tg_ht[old];
            if (span > 0 && g_tg_hn >= 2) {
                float v = (g_tg_hy[last] - g_tg_hy[old]) * 1000.0f
                          / (float)span;
                fling_start(v, (int)g_tg_x, (int)g_tg_y);
            }
        } else {
            int ax = (int)g_tg_ax, ay = (int)g_tg_ay;
            aq_push_locked(3, ax, ay, 0, 0, 0);
            pthread_mutex_unlock(&g_aq_lock);
        }
        return;
    }
}

/* AInputEvent -> event ring, from the glue's input-queue callback
 * (app thread). Returns 1 when consumed. */
static int32_t ant_input(struct android_app *app, AInputEvent *ev) {
    (void)app;
    if (AInputEvent_getType(ev) == AINPUT_EVENT_TYPE_MOTION) {
        int action = AMotionEvent_getAction(ev) & AMOTION_EVENT_ACTION_MASK;
        float fx = AMotionEvent_getX(ev, 0);
        float fy = AMotionEvent_getY(ev, 0);
        int x = (int)fx, y = (int)fy;
        switch (action) {
        case AMOTION_EVENT_ACTION_DOWN:
            ant_touch(0, x, y);
            return 1;
        case AMOTION_EVENT_ACTION_MOVE:
            ant_touch(1, x, y);
            return 1;
        case AMOTION_EVENT_ACTION_UP:
        case AMOTION_EVENT_ACTION_CANCEL:
            ant_touch(2, x, y);
            return 1;
        default:
            /* POINTER_DOWN / POINTER_UP etc.: keep the primary pointer's
             * position flowing so held gestures don't stall. */
            if (g_tg_down) ant_touch(1, x, y);
            return 1;
        }
    }
    if (AInputEvent_getType(ev) == AINPUT_EVENT_TYPE_KEY) {
        int32_t kc = AKeyEvent_getKeyCode(ev);
        int32_t act = AKeyEvent_getAction(ev);
        if (act != AKEY_EVENT_ACTION_DOWN) return 1;
        if (kc == AKEYCODE_BACK) {
            /* Back = close the app window, like the SDL shell's ESC-to-
             * quit path: kind 8 ends the App loop (Form.Run breaks). */
            pthread_mutex_lock(&g_aq_lock);
            g_anw.closed = 1;
            aq_push_locked(8, 0, 0, 0, 0, 0);
            pthread_mutex_unlock(&g_aq_lock);
            return 1;
        }
        if (kc == AKEYCODE_DEL || kc == AKEYCODE_FORWARD_DEL) {
            pthread_mutex_lock(&g_aq_lock);
            aq_push_locked(6, 0, 0, 0, 8, 0);
            pthread_mutex_unlock(&g_aq_lock);
            return 1;
        }
        if (kc == AKEYCODE_ENTER || kc == AKEYCODE_NUMPAD_ENTER) {
            pthread_mutex_lock(&g_aq_lock);
            aq_push_locked(6, 0, 0, 0, 13, 0);
            pthread_mutex_unlock(&g_aq_lock);
            return 1;
        }
        /* Printable ASCII arrives through the soft keyboard's key events on
         * most IMEs: map the A-Z/0-9/space band, everything else to the
         * GameTextInput bridge (later layer). */
        if (kc >= AKEYCODE_SPACE && kc <= AKEYCODE_Z) {
            static const char *map =
                " ??##  abcdefghijklmnop   0123456789  ";
            /* AKEYCODE_SPACE=62, digits 7..16, letters 29..54 */
            (void)map;
            int ch = 0;
            if (kc == AKEYCODE_SPACE) ch = ' ';
            else if (kc >= AKEYCODE_0 && kc <= AKEYCODE_9)
                ch = '0' + (kc - AKEYCODE_0);
            else if (kc >= AKEYCODE_A && kc <= AKEYCODE_Z)
                ch = 'a' + (kc - AKEYCODE_A);
            if (ch) {
                pthread_mutex_lock(&g_aq_lock);
                aq_push_locked(6, 0, 0, 0, ch, 0);
                pthread_mutex_unlock(&g_aq_lock);
                return 1;
            }
        }
        return 1;
    }
    return 0;
}

static void fling_cancel_public(void);

static void ant_pump_looper(void);

static void ant_cmd(struct android_app *app, int32_t cmd) {
    switch (cmd) {
    case APP_CMD_INIT_WINDOW:
        pthread_mutex_lock(&g_aq_lock);
        g_anw.destroy_wait = 0;
        pthread_mutex_unlock(&g_aq_lock);
        anw_attach(app->window);
        break;
    case APP_CMD_TERM_WINDOW:
        /* Fires on EVERY background cycle. Queue nothing (kind 8 would end
         * the app loop); present no-ops while detached and the INIT_WINDOW
         * that follows pushes kind 14 to repaint. */
        anw_detach();
        break;
    case APP_CMD_WINDOW_RESIZED:
        if (app->window) {
            int w = ANativeWindow_getWidth(app->window);
            int h = ANativeWindow_getHeight(app->window);
            pthread_mutex_lock(&g_aq_lock);
            g_anw.w = w; g_anw.h = h;
            g_window_width = w; g_window_height = h;
            aq_push_locked(7, w, h, 0, 0, 0);
            aq_push_locked(14, 0, 0, 0, 0, 0);
            pthread_mutex_unlock(&g_aq_lock);
        }
        break;
    case APP_CMD_GAINED_FOCUS:
        pthread_mutex_lock(&g_aq_lock);
        aq_push_locked(14, 0, 0, 0, 0, 0);
        pthread_mutex_unlock(&g_aq_lock);
        break;
    case APP_CMD_LOST_FOCUS:
        fling_cancel_public();
        break;
    default:
        break;
    }
}

static void fling_cancel_public(void) {
    pthread_mutex_lock(&g_aq_lock);
    fling_cancel_locked();
    pthread_mutex_unlock(&g_aq_lock);
}

/* ---- android_main: the glue app thread becomes the Zan app thread -------
 * The glue's ANativeActivity_onCreate (in the same .so) spawned this
 * thread; when this function returns, the glue asks the activity to
 * finish. DPI comes from the activity's AConfiguration (density is
 * denominated in 160dpi like OHOS; the Gui runtime keeps the desktop
 * 96-dpi base -- see zan_gui_ohos_set_dpi for the math). */

static char g_files_dir[512] = "/data/local/tmp";

static void ant_set_dpi(struct android_app *app) {
    if (!app->config) return;
    int32_t d = AConfiguration_getDensity(app->config);
    /* DENSITY_NONE(0)/DENSITY_ANY(0xFFFE)/DENSITY_NONE(0xFFFF) carry no
     * scale; treat them as the 160 baseline. */
    if (d > 0 && d < 0xFF00) {
        g_dpi = (int)((long)d * 96 / 160);
    }
}

/* Rust-free C entry the module links: the Zan program's main(). */
int main(int argc, char **argv);

void android_main(struct android_app *app) {
    app->onAppCmd = ant_cmd;
    app->onInputEvent = ant_input;
    g_anw.app = app;

    ant_set_dpi(app);

    const char *files = app->activity ? app->activity->internalDataPath : NULL;
    if (files && files[0]) {
        snprintf(g_files_dir, sizeof(g_files_dir), "%s", files);
        if (chdir(g_files_dir) != 0) {
            /* keep going: relative logs land wherever cwd allows */
        }
    }

    /* Keep the screen on while the app runs (games / dashboards); the
     * framework clears it when the activity dies. */
    if (app->activity) {
        ANativeActivity_setWindowFlags(app->activity,
            AWINDOW_FLAG_KEEP_SCREEN_ON, 0);
    }

    /* If the surface already exists (fast startup), attach now instead of
     * waiting for a queued INIT_WINDOW replay. */
    if (app->window) anw_attach(app->window);
    else {
        /* No surface yet: replay the INIT_WINDOW the activity queued
         * before android_main ran (the glue pre-drained its queue).
         * Calling the cmd directly is safe -- the glue thread is this
         * thread, blocked inside main() below. */
        ant_pump_looper();
        if (!app->window) {
            pthread_mutex_lock(&g_aq_lock);
            g_anw.destroy_wait = 1;
            pthread_mutex_unlock(&g_aq_lock);
        }
    }

    char *arg0 = "zan";
    char *argv[1] = { arg0 };
    main(1, argv);
    /* Returning ends the glue's app thread; the activity finishes. */
}

/* ---- present (EGL) ------------------------------------------------------ */

static const char *k_ant_vs =
    "attribute vec2 a_pos;\n"
    "varying vec2 v_uv;\n"
    "void main() {\n"
    "    gl_Position = vec4(a_pos, 0.0, 1.0);\n"
    "    v_uv = vec2(a_pos.x * 0.5 + 0.5, 0.5 - a_pos.y * 0.5);\n"
    "}\n";
static const char *k_ant_fs =
    "precision mediump float;\n"
    "uniform sampler2D u_tex;\n"
    "varying vec2 v_uv;\n"
    "void main() {\n"
    "    vec4 c = texture2D(u_tex, v_uv);\n"
    "    gl_FragColor = vec4(c.b, c.g, c.r, c.a);\n"
    "}\n";

static GLuint ant_compile(GLenum type, const char *src) {
    GLuint sh = glCreateShader(type);
    glShaderSource(sh, 1, &src, NULL);
    glCompileShader(sh);
    GLint ok = 0;
    glGetShaderiv(sh, GL_COMPILE_STATUS, &ok);
    if (!ok) { glDeleteShader(sh); return 0; }
    return sh;
}

static int ant_gl_surface(zan_anw_t *w) {
    if (!w->nw) return 1;
    if (!w->egl_dpy) {
        w->egl_dpy = eglGetDisplay(EGL_DEFAULT_DISPLAY);
        if (w->egl_dpy == EGL_NO_DISPLAY || !eglInitialize(w->egl_dpy, NULL, NULL))
            return 1;
    }
    const EGLint cfg_attrs[] = {
        EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
        EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
        EGL_RED_SIZE, 8, EGL_GREEN_SIZE, 8, EGL_BLUE_SIZE, 8, EGL_ALPHA_SIZE, 8,
        EGL_NONE
    };
    EGLConfig cfg = NULL;
    EGLint n = 0;
    if (!eglChooseConfig(w->egl_dpy, cfg_attrs, &cfg, 1, &n) || n < 1)
        return 1;
    if (!w->egl_surf || w->nw != w->surf_nw) {
        if (w->egl_surf) {
            eglMakeCurrent(w->egl_dpy, EGL_NO_SURFACE, EGL_NO_SURFACE,
                           EGL_NO_CONTEXT);
            eglDestroySurface(w->egl_dpy, w->egl_surf);
            w->egl_surf = EGL_NO_SURFACE;
        }
        w->egl_surf = eglCreateWindowSurface(w->egl_dpy, cfg,
                                             (EGLNativeWindowType)w->nw, NULL);
        if (w->egl_surf == EGL_NO_SURFACE) return 1;
        w->surf_nw = w->nw;
    }
    if (!w->egl_ctx) {
        const EGLint ctx_attrs[] = { EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE };
        w->egl_ctx = eglCreateContext(w->egl_dpy, cfg, EGL_NO_CONTEXT, ctx_attrs);
        if (w->egl_ctx == EGL_NO_CONTEXT) return 1;
    }
    if (!eglMakeCurrent(w->egl_dpy, w->egl_surf, w->egl_surf, w->egl_ctx))
        return 1;
    return 0;
}

static int ant_gl_program(zan_anw_t *w) {
    if (w->gl_prog) { return 0; }
    GLuint vs = ant_compile(GL_VERTEX_SHADER, k_ant_vs);
    GLuint fs = ant_compile(GL_FRAGMENT_SHADER, k_ant_fs);
    if (!vs || !fs) return 1;
    w->gl_prog = glCreateProgram();
    glAttachShader(w->gl_prog, vs);
    glAttachShader(w->gl_prog, fs);
    glLinkProgram(w->gl_prog);
    glDeleteShader(vs); glDeleteShader(fs);
    GLint linked = 0;
    glGetProgramiv(w->gl_prog, GL_LINK_STATUS, &linked);
    if (!linked) return 1;

    static const GLfloat quad[] = { -1,-1, 1,-1, -1,1, 1,1 };
    glGenBuffers(1, &w->gl_vbo);
    glBindBuffer(GL_ARRAY_BUFFER, w->gl_vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(quad), quad, GL_STATIC_DRAW);
    GLint loc = glGetAttribLocation(w->gl_prog, "a_pos");
    glEnableVertexAttribArray((GLuint)loc);
    glVertexAttribPointer((GLuint)loc, 2, GL_FLOAT, GL_FALSE, 0, NULL);
    glGenTextures(1, &w->gl_tex);
    glUseProgram(w->gl_prog);
    glUniform1i(glGetUniformLocation(w->gl_prog, "u_tex"), 0);
    return 0;
}

/* Dirty rects: partial-band frames upload only the changed subrects; the
 * texture persists across frames (contract as the OHOS EGL path). */
#define ZAN_ANT_DIRTY_MAX 512
static i32 g_dirty[ZAN_ANT_DIRTY_MAX * 4];
static int g_dirty_count;
static int g_dirty_overflow;

EXPORT i32 zan_gui_present_dirty_add(i32 x, i32 y, i32 w, i32 h) {
    if (w <= 0 || h <= 0) return 0;
    if (g_dirty_count >= ZAN_ANT_DIRTY_MAX) { g_dirty_overflow = 1; return 0; }
    g_dirty[g_dirty_count * 4 + 0] = x;
    g_dirty[g_dirty_count * 4 + 1] = y;
    g_dirty[g_dirty_count * 4 + 2] = w;
    g_dirty[g_dirty_count * 4 + 3] = h;
    g_dirty_count++;
    return 0;
}

static void ant_dirty_reset(void) { g_dirty_count = 0; g_dirty_overflow = 0; }

static void ant_texture(zan_anw_t *w, const zan_surface_t *s) {
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, w->gl_tex);
    if (w->tex_w != s->width || w->tex_h != s->height) {
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, s->width, s->height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, NULL);
        w->tex_w = s->width;
        w->tex_h = s->height;
        glPixelStorei(GL_UNPACK_ROW_LENGTH, s->stride);
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, s->width, s->height,
                        GL_RGBA, GL_UNSIGNED_BYTE, s->pixels);
        glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    } else if (g_dirty_count > 0 && !g_dirty_overflow) {
        glPixelStorei(GL_UNPACK_ROW_LENGTH, s->stride);
        for (int i = 0; i < g_dirty_count; i++) {
            i32 x = g_dirty[i * 4 + 0], y = g_dirty[i * 4 + 1];
            i32 cw = g_dirty[i * 4 + 2], ch = g_dirty[i * 4 + 3];
            if (x < 0) { cw += x; x = 0; }
            if (y < 0) { ch += y; y = 0; }
            if (x + cw > s->width) { cw = s->width - x; }
            if (y + ch > s->height) { ch = s->height - y; }
            if (cw <= 0 || ch <= 0) continue;
            glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, cw, ch,
                            GL_RGBA, GL_UNSIGNED_BYTE,
                            (const uint8_t *)s->pixels
                                + ((size_t)y * (size_t)s->stride + (size_t)x) * 4);
        }
        glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    } else {
        glPixelStorei(GL_UNPACK_ROW_LENGTH, s->stride);
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, s->width, s->height,
                        GL_RGBA, GL_UNSIGNED_BYTE, s->pixels);
        glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    }
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
}

EXPORT i32 zan_gui_present(iptr hwnd_val, i32 surface_id) {
    (void)hwnd_val;
    if (surface_id < 0 || surface_id >= g_surface_count ||
        !g_surfaces[surface_id]) return 1;
    if (!g_anw.attached || !g_anw.nw || g_anw.closed) return 1;
    zan_surface_t *s = g_surfaces[surface_id];

    if (ant_gl_surface(&g_anw) != 0) {
        ant_dirty_reset(); return 1;
    }
    if (ant_gl_program(&g_anw) != 0) {
        ant_dirty_reset(); return 1;
    }
    ant_texture(&g_anw, s);
    ant_dirty_reset();
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
    eglSwapBuffers(g_anw.egl_dpy, g_anw.egl_surf);
    return 0;
}

/* ---- window management (phone: no chrome) ------------------------------- */

EXPORT iptr zan_gui_create_window(const char *title, i32 width, i32 height) {
    (void)title; (void)width; (void)height; /* the NativeActivity decides */
    return ZAN_ANW_HWND;
}
EXPORT i32 zan_gui_show_window(iptr hwnd_val)         { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_minimize(iptr hwnd_val)            { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_toggle_maximize(iptr hwnd_val)     { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_close_window(iptr hwnd_val) {
    (void)hwnd_val;
    pthread_mutex_lock(&g_aq_lock);
    g_anw.closed = 1;
    aq_push_locked(8, 0, 0, 0, 0, 0);
    pthread_mutex_unlock(&g_aq_lock);
    /* Ask the activity to finish: the glue posts EXIT; the framework's
     * NativeActivity tears the surface down on its own. */
    if (g_anw.app && g_anw.app->activity) {
        ANativeActivity_finish(g_anw.app->activity);
    }
    return 0;
}
EXPORT i32 zan_gui_destroy_window(iptr hwnd_val) {
    (void)hwnd_val;
    pthread_mutex_lock(&g_aq_lock);
    g_anw.attached = 0;
    g_anw.nw = NULL;
    pthread_mutex_unlock(&g_aq_lock);
    return 0;
}
EXPORT i32 zan_gui_is_maximized(iptr hwnd_val)     { (void)hwnd_val; return 0; }
EXPORT i32 zan_gui_window_visible(iptr hwnd_val)   { (void)hwnd_val; return g_anw.attached; }
EXPORT i32 zan_gui_window_focused(iptr hwnd_val)   { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_titlebar_height(void)           { return 0; }
EXPORT i32 zan_gui_caption_button_width(void)      { return 0; }
EXPORT i32 zan_gui_set_caption_buttons(iptr h, i32 n) { (void)h; (void)n; return 0; }
EXPORT i32 zan_gui_set_window_pos(iptr h, i32 x, i32 y) { (void)h; (void)x; (void)y; return 0; }
EXPORT i32 zan_gui_center_window(iptr hwnd_val)    { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_set_topmost(iptr h, i32 on)     { (void)h; (void)on; return 0; }
EXPORT i32 zan_gui_set_title(iptr h, const char *t) { (void)h; (void)t; return 0; }
EXPORT i32 zan_gui_set_cursor(i32 cursor_type)     { (void)cursor_type; return 0; }

/* ---- event pump --------------------------------------------------------- */

EXPORT i32 zan_gui_poll_event(void) {
    memset(g_pending_event, 0, sizeof(g_pending_event));
    /* The poll path is the hot idle path for a redraw-pending loop
     * (App.ProcessEvent's needsRedraw branch): lifecycle commands sitting
     * in the glue queue must be drained here too, or APP_CMD_INIT_WINDOW
     * never runs, attached stays 0, and an app that gates on IsVisible
     * spins forever before its first frame. */
    ant_pump_looper();
    if (aq_pop()) { return 0; }
    return 1;
}

static long long g_wait_spins;

/* The glue drives ALooper only inside android_main, and this thread IS
 * android_main's thread -- blocked in the Zan program's main() right now.
 * Nobody else drains the lifecycle/input queues while the Zan loop is
 * parked in wait_event, so pump them ourselves: ant_pump_looper() runs
 * the glue's source callbacks (which translate into the event ring)
 * before every ring check. The SDL shell solved the same shape with an
 * event watch on its own thread; the OHOS shell with shell-thread feeds;
 * here the shell is in-process and the pump is just a function call. */
static void ant_pump_looper(void) {
    struct android_app *app = g_anw.app;
    if (!app) return;
    int ident;
    int events;
    struct android_poll_source *source;
    while ((ident = ALooper_pollOnce(0, NULL, &events,
                                     (void **)&source)) >= 0) {
        if (source && source->process) source->process(app, source);
        if (ident == LOOPER_ID_MAIN && app->destroyRequested != 0) {
            pthread_mutex_lock(&g_aq_lock);
            g_anw.closed = 1;
            aq_push_locked(8, 0, 0, 0, 0, 0);
            pthread_mutex_unlock(&g_aq_lock);
            return;
        }
    }
}

EXPORT i32 zan_gui_wait_event(void) {
    memset(g_pending_event, 0, sizeof(g_pending_event));
    for (;;) {
        ant_pump_looper();
        if (aq_pop()) { return 0; }
        /* Before first attach: block in the looper itself. The glue's
         * MAIN looper wakes on lifecycle commands (INIT_WINDOW among
         * them), so this sleeps until the surface actually exists --
         * no 4 ms spin burning CPU on a black screen. */
        if (g_anw.destroy_wait && g_anw.app) {
            int events;
            struct android_poll_source *source;
            int ident = ALooper_pollOnce(-1, NULL, &events,
                                         (void **)&source);
            if (ident == LOOPER_ID_MAIN && source && source->process)
                source->process(g_anw.app, source);
            if (g_anw.app->destroyRequested != 0) {
                pthread_mutex_lock(&g_aq_lock);
                g_anw.closed = 1;
                aq_push_locked(8, 0, 0, 0, 0, 0);
                pthread_mutex_unlock(&g_aq_lock);
                return 0;
            }
            if (aq_pop()) { return 0; }
            continue;
        }
#ifdef ZAN_SHELL_TRACE
        if ((++g_wait_spins % 500) == 0)
            ZAN_TRACE("wait spin %lld", g_wait_spins);
#endif
        struct timespec ts = { 0, 4 * 1000 * 1000 }; /* 4 ms */
        nanosleep(&ts, NULL);
    }
}

EXPORT i32 zan_gui_wait_event_timeout(i32 ms) {
    memset(g_pending_event, 0, sizeof(g_pending_event));
    ant_pump_looper();
    if (aq_pop()) { return 0; }
    int remain = (ms < 0) ? 0 : ms;
    while (remain > 0) {
        long step = (remain > 8) ? 8 : (long)remain;
        struct timespec ts = { 0, step * 1000 * 1000 };
        nanosleep(&ts, NULL);
        remain -= (int)step;
        ant_pump_looper();
        if (aq_pop()) { return 0; }
    }
    return 1;
}

EXPORT i32 zan_gui_wake(void) { return 0; }

EXPORT i32 zan_gui_inject_event(
    iptr hwnd_val, i32 kind, i32 x, i32 y, i32 button, i32 keycode, i32 mods) {
    (void)hwnd_val;
    pthread_mutex_lock(&g_aq_lock);
    aq_push_locked((int)kind, (int)x, (int)y, (int)button, (int)keycode,
                   (int)mods);
    pthread_mutex_unlock(&g_aq_lock);
    return 0;
}
EXPORT i32 zan_gui_inject_pending(void) {
    return (g_aq_tail - g_aq_head + ZAN_AQ_CAP) % ZAN_AQ_CAP;
}

EXPORT i32 zan_gui_event_kind(void)    { return g_pending_event[0]; }
EXPORT i64 zan_gui_event_seq(void)     { return g_ev_seq; }
EXPORT i32 zan_gui_event_x(void)       { return g_pending_event[1]; }
EXPORT i32 zan_gui_event_y(void)       { return g_pending_event[2]; }
EXPORT i32 zan_gui_event_button(void)  { return g_pending_event[3]; }
EXPORT i32 zan_gui_event_keycode(void) { return g_pending_event[4]; }
EXPORT i32 zan_gui_event_mods(void)    { return g_pending_event[5]; }
EXPORT i32 zan_gui_event_flag(void)    { return g_pending_event[6]; }
EXPORT iptr zan_gui_event_hwnd(void)   { return g_event_win; }

EXPORT i32 zan_gui_window_width(void)  { return g_window_width; }
EXPORT i32 zan_gui_window_height(void) { return g_window_height; }
EXPORT i32 zan_gui_client_width(iptr hwnd_val)  { (void)hwnd_val; return g_window_width; }
EXPORT i32 zan_gui_client_height(iptr hwnd_val) { (void)hwnd_val; return g_window_height; }

/* ---- platform services --------------------------------------------------- */

EXPORT i32 zan_gui_get_dpi_scale(void) { return (i32)(g_dpi * 100 / 96); }

EXPORT i64 zan_gui_get_tick_ms(void) { return ant_tick_ms(); }
EXPORT void zan_gui_sleep_ms(i32 ms) {
    if (ms > 0) {
        struct timespec ts = { ms / 1000, (long)(ms % 1000) * 1000 * 1000 };
        nanosleep(&ts, NULL);
    }
}

EXPORT const char *zan_gui_android_files_dir(void) { return g_files_dir; }

/* JNI reach for gui_runtime_android.c's WebView bridge (v1: env for the
 * calling thread + the activity jobject; real WebView plumbing is a later
 * layer -- the hooks exist so the bridge links either way). */
static JNIEnv *zan_anw_bridge_env(void) {
    struct android_app *app = g_anw.app;
    if (!app || !app->activity) return NULL;
    JavaVM *vm = app->activity->vm;
    JNIEnv *env = NULL;
    if ((*vm)->GetEnv(vm, (void **)&env, JNI_VERSION_1_6) == JNI_OK)
        return env;
    if ((*vm)->AttachCurrentThread(vm, &env, NULL) == JNI_OK)
        return env;
    return NULL;
}

static jobject zan_anw_bridge_activity(void) {
    struct android_app *app = g_anw.app;
    return app && app->activity ? (jobject)app->activity->clazz : NULL;
}

EXPORT i32 zan_gui_set_clipboard(const char *utf8) { (void)utf8; return 1; }
EXPORT const char *zan_gui_get_clipboard(void)     { return ""; }
EXPORT int  zan_gui_drop_pending(void)             { return 0; }
EXPORT const char *zan_gui_drop_take(void)         { return ""; }
EXPORT void zan_gui_set_ime_pos(i32 x, i32 y)      { (void)x; (void)y; }

/* Soft keyboard show/hide through the framework (the part NativeActivity
 * does natively). Committed text waits for the GameTextInput bridge. */
EXPORT i32 zan_gui_set_ime_open(i32 on) {
    struct android_app *app = g_anw.app;
    if (!app || !app->activity) return 1;
    if (on) {
        ANativeActivity_showSoftInput(app->activity,
            ANATIVEACTIVITY_SHOW_SOFT_INPUT_FORCED);
    } else {
        ANativeActivity_hideSoftInput(app->activity,
            ANATIVEACTIVITY_HIDE_SOFT_INPUT_NOT_ALWAYS);
    }
    return 0;
}

EXPORT i32 zan_gui_enable_glass(iptr hwnd_val, i32 tint_argb) {
    (void)hwnd_val; (void)tint_argb; return 1; /* unsupported: app keeps CPU bg */
}
EXPORT i32 zan_gui_disable_glass(iptr hwnd_val)    { (void)hwnd_val; return 0; }
EXPORT i32 zan_gui_set_opacity(iptr h, i32 percent) { (void)h; (void)percent; return 0; }

EXPORT i32 zan_gui_write_file(const char *path, const char *utf8) {
    if (!path || !utf8) return 1;
    FILE *f = fopen(path, "wb");
    if (!f) return 1;
    size_t n = strlen(utf8);
    size_t w = fwrite(utf8, 1, n, f);
    fclose(f);
    return w == n ? 0 : 1;
}

/* GameKit GPU-scene hooks: report unsupported on this backend. */
EXPORT i32 zan_gui_adopt_sdl_window(iptr hwnd_val)                  { (void)hwnd_val; return 1; }
EXPORT i32 zan_gui_scene_set_renderer(iptr hwnd_val, iptr rend)     { (void)hwnd_val; (void)rend; return 1; }
EXPORT i32 zan_gui_scene_upload(iptr hwnd_val, const void *bgra, i32 w, i32 h) {
    (void)hwnd_val; (void)bgra; (void)w; (void)h; return 1;
}
EXPORT i32 zan_gui_scene_present(iptr hwnd_val, i32 surface_id) {
    (void)hwnd_val; (void)surface_id; return 1;
}

#endif /* ZAN_GUI_ANDROID_NATIVE */
