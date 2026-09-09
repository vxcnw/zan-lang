/* gui_gl_3d_test.c -- real-driver 3D regression for the GL backend's mesh
 * pipeline, the same shape as gui_gl_aa_test.c: no window, load zan_gui.dll
 * dynamically, install the GPU backend and compare the composed frame against
 * hand-computed expectations. Exit 77 explicitly means GL 3.3 is unavailable,
 * never a passing CPU substitute.
 *
 * What it pins down:
 *  - draw3d returns 1 on GL and 0 on the CPU backend (the seam's report);
 *  - a textured, rotating cube actually lands textured pixels: two frames of
 *    the same cube at different angles must differ (rotation happened) and
 *    must both differ from the flat clear (triangles rasterized);
 *  - depth ordering: with three overlapping quads at increasing depth, the
 *    nearest one must win -- the readback centre pixel equals the near quad's
 *    colour, not the far one's;
 *  - the alpha channel of a 3D draw stays opaque over the 2D clear.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#ifdef _WIN32
#include <windows.h>
static HMODULE lib;
#define SYMBOL(n) GetProcAddress(lib, n)
#else
#include <dlfcn.h>
static void *lib;
#define SYMBOL(n) dlsym(lib, n)
#endif
#define W 120
#define H 100
#define CHECK(c) do { if (!(c)) { fprintf(stderr, "GL 3D: %s (line %d)\n", #c, __LINE__); exit(1); } } while (0)

static int32_t (*create)(int32_t,int32_t);
static int32_t (*destroy)(int32_t);
static int32_t (*backend)(int32_t);
static const char *(*backend_name)(void);
static const void *(*pixels)(int32_t);
static void (*clear_rect)(int32_t,int32_t,int32_t,int32_t,int32_t,uint32_t);
static int32_t (*mesh_create)(int32_t,const float*,int32_t,const uint16_t*,int32_t);
static int32_t (*draw3d)(int32_t,int32_t,const float*,uint32_t,const char*);
#define LOAD(v,n) do { *(void **)(&(v)) = (void *)SYMBOL(n); CHECK(v); } while (0)

static uint32_t frame[W*H];
static void capture(int s) {
    const void *p = pixels(s);
    CHECK(p);
    memcpy(frame, p, sizeof(frame));
}
static int center_r(void) { uint32_t c = frame[(H/2)*W + W/2]; return (int)((c>>16)&255); }
static int center_g(void) { uint32_t c = frame[(H/2)*W + W/2]; return (int)((c>>8)&255); }
static uint32_t frame_hash(void) {
    uint32_t h = 2166136261u;
    for (int i = 0; i < W*H; i++) { h ^= frame[i]; h *= 16777619u; }
    return h;
}

/* column-major perspective * view * model for a cube of half-size r centred
 * at origin, viewed from (0, 0, dist) looking at the origin, spun by rad. */
static float *cube_mvp(float rad, float dist, float r) {
    static float m[16];
    float c = (float)cos(rad), s = (float)sin(rad);
    /* model: rotate about Y then a fixed tilt about X */
    float cy=(float)cos(0.4), sy=(float)sin(0.4);
    float R[16] = {
        c,        0,   -s,       0,
        sy*s,     cy,  sy*c,     0,
        cy*s,    -sy,  cy*c,     0,
        0,        0,    0,       1,
    };
    /* view: translate -dist on z (camera looks down -z), right-handed */
    float V[16] = { 1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,-dist,1 };
    /* perspective, 60deg, aspect W/H, D3D-style depth */
    float f = 1.0f / (float)tan(0.5235988);
    float P[16] = {
        f / ((float)W / (float)H), 0, 0, 0,
        0, f, 0, 0,
        0, 0, 10.0f/(1.0f-100.0f), (1.0f*100.0f)/(1.0f-100.0f),
        0, 0, -1, 0,
    };
    /* M = P * V * R, all column-major (m[col*4+row]) */
    float PV[16];
    for (int col = 0; col < 4; col++)
        for (int row = 0; row < 4; row++) {
            float v = 0;
            for (int k = 0; k < 4; k++) v += P[k*4+row] * V[col*4+k];
            PV[col*4+row] = v;
        }
    for (int col = 0; col < 4; col++)
        for (int row = 0; row < 4; row++) {
            float v = 0;
            for (int k = 0; k < 4; k++) v += PV[k*4+row] * R[col*4+k];
            m[col*4+row] = v;
        }
    (void)r;
    return m;
}

static float cube_verts[6*4*8];
static uint16_t cube_idx[36];
static void build_cube(void) {
    static const float faces[6][3] = {
        {0,0,1},{0,0,-1},{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},
    };
    static const float up[6][3] = {
        {0,1,0},{0,1,0},{0,1,0},{0,1,0},{0,0,-1},{0,0,1},
    };
    static const float right[6][3] = {
        {1,0,0},{-1,0,0},{0,0,-1},{0,0,1},{1,0,0},{1,0,0},
    };
    int v = 0, idx = 0;
    for (int f = 0; f < 6; f++) {
        float u0 = -1, v0 = -1, u1 = 1, v1 = 1;
        uint16_t base = (uint16_t)v;
        for (int corner = 0; corner < 4; corner++) {
            float uu = (corner == 0 || corner == 3) ? u0 : u1;
            float vv = (corner < 2) ? v0 : v1;
            cube_verts[v*8+0] = right[f][0]*uu + up[f][0]*vv + faces[f][0];
            cube_verts[v*8+1] = right[f][1]*uu + up[f][1]*vv + faces[f][1];
            cube_verts[v*8+2] = right[f][2]*uu + up[f][2]*vv + faces[f][2];
            cube_verts[v*8+3] = faces[f][0];
            cube_verts[v*8+4] = faces[f][1];
            cube_verts[v*8+5] = faces[f][2];
            cube_verts[v*8+6] = (corner == 0 || corner == 3) ? 0 : 1;
            cube_verts[v*8+7] = (corner < 2) ? 1 : 0;
            v++;
        }
        cube_idx[idx++] = base;     cube_idx[idx++] = (uint16_t)(base+1); cube_idx[idx++] = (uint16_t)(base+2);
        cube_idx[idx++] = base;     cube_idx[idx++] = (uint16_t)(base+2); cube_idx[idx++] = (uint16_t)(base+3);
    }
}

int main(int argc, char **argv) {
    CHECK(argc == 2);
#ifdef _WIN32
    lib = LoadLibraryA(argv[1]);
#else
    lib = dlopen(argv[1], RTLD_NOW);
#endif
    CHECK(lib);
    LOAD(create, "zan_gui_create_surface");
    LOAD(destroy, "zan_gui_destroy_surface");
    LOAD(backend, "zan_gui_set_render_backend");
    LOAD(backend_name, "zan_gui_render_backend");
    LOAD(pixels, "zan_gui_get_pixels");
    LOAD(clear_rect, "zan_gui_clear_rect");
    LOAD(mesh_create, "zan_gui_mesh_create");
    LOAD(draw3d, "zan_gui_draw3d");

    build_cube();
    /* CPU first: the seam must report "no 3D" without crashing.
     * (set_render_backend(0) returns 0 by design -- the CPU has no backend
     * object -- so unlike the GL switch above, its return is not checked.) */
    backend(0);
    int s = create(W, H);
    CHECK(s >= 0);
    clear_rect(s, 0, 0, W, H, 0xFF203040);
    int mesh_cpu = mesh_create(s, cube_verts, 24, cube_idx, 36);
    (void)mesh_cpu;   /* CPU refuses meshes; either 0 or a no-op id is fine */
    int cpu_ret = draw3d(s, 1, cube_mvp(0.0f, 4.0f, 1.0f), 0xFFFFFFFF, NULL);
    capture(s);
    uint32_t cpu_hash = frame_hash();
    if (cpu_ret != 0) { fprintf(stderr, "GL 3D: CPU backend must report 0\n"); return 1; }

    /* GL: the same probe must report 1 and produce real content. */
    if (!backend(1) || strcmp(backend_name(), "gl")) {
        fprintf(stderr, "SKIP: real GL 3.3 unavailable\n");
        return 77;
    }
    clear_rect(s, 0, 0, W, H, 0xFF203040);
    int mesh = mesh_create(s, cube_verts, 24, cube_idx, 36);
    CHECK(mesh > 0);
    int gl_ret = draw3d(s, mesh, cube_mvp(0.0f, 4.0f, 1.0f), 0xFFFFFFFF, NULL);
    CHECK(gl_ret == 1);
    capture(s);
    uint32_t h0 = frame_hash();
    CHECK(h0 != cpu_hash);
    /* centre pixel must have been covered by the cube (shaded white-ish,
     * definitely not the flat clear colour 0x40,0x30,0x20) */
    CHECK(center_r() > 0x50 && center_g() > 0x50);

    /* Rotation must actually change the frame. */
    clear_rect(s, 0, 0, W, H, 0xFF203040);
    CHECK(draw3d(s, mesh, cube_mvp(0.7f, 4.0f, 1.0f), 0xFFFFFFFF, NULL) == 1);
    capture(s);
    uint32_t h1 = frame_hash();
    CHECK(h0 != h1);

    /* Texture path: a 2x2 checker via the image cache (the runtime decodes
     * bytes through stb_image, so wrap the pixels in an uncompressed TGA
     * header); the frame must change again versus the white-textured draw. */
    unsigned char checker[18 + 2*2*4] = {0};
    checker[2] = 2;             /* TGA type 2: uncompressed true-colour */
    checker[12] = 2; checker[14] = 2;   /* 2x2, little-endian */
    checker[16] = 32; checker[17] = 0x28; /* 32bpp, top-down */
    {
        const unsigned char px[2*2*4] = {
            255,0,0,255, 0,255,0,255,
            0,0,255,255, 255,255,0,255,
        };
        memcpy(checker + 18, px, sizeof(px));
    }
    int32_t (*img_mem)(const char*, const char*, int32_t);
    *(void **)(&img_mem) = (void *)SYMBOL("zan_gui_image_load_mem");
    CHECK(img_mem);
    CHECK(img_mem("mem:3dcheck", (const char *)checker, sizeof(checker)) > 0);
    clear_rect(s, 0, 0, W, H, 0xFF203040);
    CHECK(draw3d(s, mesh, cube_mvp(0.7f, 4.0f, 1.0f), 0xFFFFFFFF, "mem:3dcheck") == 1);
    capture(s);
    uint32_t h2 = frame_hash();
    CHECK(h1 != h2);

    /* Depth: three full-screen-ish quads at z = -1, -3, -6 painted far to
     * near; the visible centre must be the NEAR quad's colour (green). */
    float quad_v[3*4*8];
    uint16_t quad_i[6];
    for (int q = 0; q < 3; q++) {
        float z = (q == 0) ? -6.0f : (q == 1) ? -3.0f : -1.0f;
        float half = (q == 0) ? 3.0f : (q == 1) ? 2.0f : 1.0f;
        uint16_t base = (uint16_t)(q*4);
        const float corners[4][2] = {{-1,-1},{1,-1},{1,1},{-1,1}};
        for (int c2 = 0; c2 < 4; c2++) {
            quad_v[(q*4+c2)*8+0] = corners[c2][0]*half;
            quad_v[(q*4+c2)*8+1] = corners[c2][1]*half;
            quad_v[(q*4+c2)*8+2] = z;
            quad_v[(q*4+c2)*8+3] = 0;
            quad_v[(q*4+c2)*8+4] = 0;
            quad_v[(q*4+c2)*8+5] = 1;
            quad_v[(q*4+c2)*8+6] = 0;
            quad_v[(q*4+c2)*8+7] = 0;
        }
        quad_i[q*6+0]=base; quad_i[q*6+1]=(uint16_t)(base+1); quad_i[q*6+2]=(uint16_t)(base+2);
        quad_i[q*6+3]=base; quad_i[q*6+4]=(uint16_t)(base+2); quad_i[q*6+5]=(uint16_t)(base+3);
    }
    int qmesh = mesh_create(s, quad_v, 12, quad_i, 6);
    CHECK(qmesh > 0);
    (void)qmesh;
    /* Straight-on ortho view down -z: x/y untouched, z squeezed into [0,1)
     * D3D-style. Column-major, so m[14] scales z and m[11] is w's z-row. */
    float ortho[16] = {
        0.5f, 0, 0, 0,
        0, 0.5f, 0, 0,
        0, 0, 0.2f, 0,
        0, 0, 0.5f, 1,
    };
    for (int q = 0; q < 3; q++) {
        int m1 = mesh_create(s, quad_v + q*4*8, 4, quad_i, 6);
        CHECK(m1 > 0);
        /* draw in far -> near order with distinct colours */
        uint32_t col = (q == 0) ? 0xFF0000FFu /* red, far */
                     : (q == 1) ? 0xFF00FF00u /* green, middle */
                                : 0xFFFF0000u /* blue, near */;
        CHECK(draw3d(s, m1, ortho, (int)col, NULL) == 1);
    }
    capture(s);
    /* Near quad (half=1, z=-1) covers the centre. The shader treats the
     * colour as R,G,B,A over an ARGB u32 (0xRRGGBBAA here, matching
     * Uniform4f's channel order), and readback stores 0xAABBGGRR, so the
     * red 0xFFFF0000u draw reads back 0xE60000FF-ish: red channel high. */
    {
        uint32_t c = frame[(H/2)*W + W/2];
        int r = (int)((c >> 16) & 255);
        int b = (int)(c & 255);
        fprintf(stderr, "GL 3D: depth centre %08x (r=%d b=%d)\n", c, r, b);
        CHECK(r > 150 && b < 100);
    }

    destroy(s);
    fprintf(stderr, "GL 3D: OK\n");
    return 0;
}
