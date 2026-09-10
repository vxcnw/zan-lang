package dev.zan.app;

import android.app.Activity;
import android.app.Application;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;

/**
 * Zan runtime host: asks for the storage permissions the in-app
 * FilePicker/Upload components need to browse shared storage. Declared as
 * the manifest {@code application android:name}, so no shell Activity code
 * changes; the request fires once, when the first activity is created
 * (runtime grants on API 23+, media-scoped grants on API 33+).
 */
public class ZanApp extends Application
        implements Application.ActivityLifecycleCallbacks {

    private static final int ZAN_PERM_REQUEST = 4242;
    private boolean asked = false;

    @Override
    public void onCreate() {
        super.onCreate();
        registerActivityLifecycleCallbacks(this);
    }

    @Override
    public void onActivityCreated(Activity a, Bundle savedInstanceState) {
        if (asked) { return; }
        asked = true;
        String[] perms;
        if (Build.VERSION.SDK_INT >= 33) {
            perms = new String[]{
                "android.permission.READ_MEDIA_IMAGES",
                "android.permission.READ_MEDIA_VIDEO",
                "android.permission.READ_MEDIA_AUDIO"};
        } else {
            perms = new String[]{
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.WRITE_EXTERNAL_STORAGE"};
        }
        boolean need = false;
        for (String p : perms) {
            if (a.checkSelfPermission(p) != PackageManager.PERMISSION_GRANTED) {
                need = true;
            }
        }
        if (need) {
            a.requestPermissions(perms, ZAN_PERM_REQUEST);
        }
    }

    @Override public void onActivityStarted(Activity a) { }
    @Override public void onActivityResumed(Activity a) { }
    @Override public void onActivityPaused(Activity a) { }
    @Override public void onActivityStopped(Activity a) { }
    @Override public void onActivitySaveInstanceState(Activity a, Bundle out) { }
    @Override public void onActivityDestroyed(Activity a) { }
}
