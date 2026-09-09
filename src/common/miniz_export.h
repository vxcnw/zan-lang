/* miniz_export.h -- visibility shim for the vendored miniz subset.
 *
 * Upstream miniz generates this header from its CMake build; we vendor the
 * sources raw, so ship the plain variant: no DLL import/export decoration,
 * every public symbol has default visibility. */
#ifndef MINIZ_EXPORT_H
#define MINIZ_EXPORT_H

#define MINIZ_EXPORT

#endif /* MINIZ_EXPORT_H */
