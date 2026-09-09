/* Empty stub shared object for toolchain\ohos-<arch>\libEGL.so and
 * libGLESv3.so. They exist only so a cross link records the DT_NEEDED
 * dependency of the GUI driver's EGL present path (a dlopened OHOS library
 * relocates against its own dependency group); at run time the app process
 * supplies the real libraries, and no EGL symbol is referenced at link time.
 * Built by scripts\build_cross_rt.cmd; not committed (*.so is git-ignored). */
typedef int zan_ohos_stub_translation_unit_is_not_empty;
