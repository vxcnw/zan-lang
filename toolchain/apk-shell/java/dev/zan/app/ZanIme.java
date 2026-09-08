package dev.zan.app;

import android.app.Activity;
import android.content.Context;
import android.text.InputType;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.BaseInputConnection;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputConnection;
import android.view.inputmethod.InputMethodManager;

/**
 * Hidden IME host for the NativeActivity shell. NativeActivity has no view
 * of its own, so a soft keyboard has nothing to bind an InputConnection to
 * and every commitText-based IME (all CJK keyboards, most Latin ones) goes
 * unheard. On first open this adds a 1px focusable view to the content
 * view; the keyboard binds to it and committed text lands in
 * {@link #zanCommit} -> the native event ring (kind-6, one event per
 * codepoint). show()/hide() are invoked from the native shell's
 * zan_gui_set_ime_open, on the UI thread.
 */
public class ZanIme {
    private static View view;

    public static void show(final Activity a) {
        a.runOnUiThread(new Runnable() { public void run() {
            if (view == null) {
                ViewGroup content =
                    (ViewGroup) a.findViewById(android.R.id.content);
                if (content == null) { return; }
                View v = new View(a) {
                    @Override public InputConnection onCreateInputConnection(
                            EditorInfo outAttrs) {
                        outAttrs.inputType = InputType.TYPE_CLASS_TEXT;
                        outAttrs.imeOptions =
                            EditorInfo.IME_FLAG_NO_FULLSCREEN |
                            EditorInfo.IME_FLAG_NO_EXTRACT_UI;
                        return new BaseInputConnection(this, true) {
                            @Override public boolean commitText(
                                    CharSequence text, int newPosition) {
                                send(text.toString());
                                return true;
                            }
                            /* Pinyin etc. keep the pre-commit string in the
                             * connection; forward it so the focused widget
                             * can render a dim preview. An empty string
                             * clears the preview. */
                            @Override public boolean setComposingText(
                                    CharSequence text, int newCursorPosition) {
                                sendComposing(text == null ? ""
                                                           : text.toString());
                                return true;
                            }
                            /* The IME folds the composing string into a
                             * commit (or abandons it): drop the preview. */
                            @Override public boolean finishComposingText() {
                                sendComposing("");
                                return true;
                            }
                            /* IMEs erase through the connection when they
                             * manage the text themselves; surface each erase
                             * as the backspace control the native side maps
                             * (codepoint 8 = kind-6 backspace). */
                            @Override public boolean deleteSurroundingText(
                                    int before, int after) {
                                for (int i = 0; i < before; i++) {
                                    send("\b");
                                }
                                return true;
                            }
                        };
                    }
                };
                v.setFocusable(true);
                v.setFocusableInTouchMode(true);
                content.addView(v, new ViewGroup.LayoutParams(1, 1));
                view = v;
            }
            view.requestFocus();
            InputMethodManager imm = (InputMethodManager)
                a.getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) {
                imm.showSoftInput(view, InputMethodManager.SHOW_IMPLICIT);
            }
        }});
    }

    public static void hide(final Activity a) {
        a.runOnUiThread(new Runnable() { public void run() {
            if (view == null) { return; }
            InputMethodManager imm = (InputMethodManager)
                a.getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) {
                imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
            }
            view.clearFocus();
        }});
    }

    /** Implemented in the native shell (gui_runtime_android_native.c),
     * bound via RegisterNatives at init. */
    public static native void zanCommit(String s);

    /** Native half of the composing preview; see zanCommit. */
    public static native void zanSetComposing(String s);

    /** A commit that cannot reach the native side must not kill the app
     * (an unbound native is a log, not a crash). */
    private static void send(String s) {
        try {
            android.util.Log.i("ZanIme", "commit: [" + s + "]");
            zanCommit(s);
        } catch (UnsatisfiedLinkError e) {
            android.util.Log.w("ZanIme", "zanCommit not bound: " + e);
        }
    }

    private static void sendComposing(String s) {
        try {
            zanSetComposing(s);
        } catch (UnsatisfiedLinkError e) {
            android.util.Log.w("ZanIme", "zanSetComposing not bound: " + e);
        }
    }
}
