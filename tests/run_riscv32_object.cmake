# Bare-metal riscv32 (ESP32-C3) object emission check.
#
# Invoked by ctest as:
#   cmake -DZANC=<zanc> -DSRC=<case.zan> -DOUT=<case.o> -P run_riscv32_object.cmake
#
# The compiler's job for a freestanding target ends at the object file -- the
# target SDK owns startup code and linking. So the check is: zanc --target
# riscv32 produces an ELF32 little-endian RISC-V object (e_machine = EM_RISCV
# = 243 = 0xF3). Read as raw hex so the test needs nothing but cmake.

execute_process(
  COMMAND "${ZANC}" "${SRC}" --target riscv32 -o "${OUT}"
  ERROR_VARIABLE _err
  RESULT_VARIABLE _rc
  WORKING_DIRECTORY "${WORKDIR}")

if(NOT _rc EQUAL 0)
  message(FATAL_ERROR "run_riscv32_object: zanc --target riscv32 failed (rc=${_rc})\n${_err}")
endif()

if(NOT EXISTS "${OUT}")
  message(FATAL_ERROR "run_riscv32_object: no object written to ${OUT}")
endif()

file(READ "${OUT}" _hex HEX)
string(TOUPPER "${_hex}" _hex)

# e_ident: 7F 45 4C 46 = \x7fELF
string(SUBSTRING "${_hex}" 0 6 _magic)
if(NOT _magic STREQUAL "7F454C")
  message(FATAL_ERROR
    "run_riscv32_object: ${OUT} is not an ELF object (magic=${_magic})")
endif()

# EI_CLASS = 1 (ELF32)
string(SUBSTRING "${_hex}" 8 2 _class)
if(NOT _class STREQUAL "01")
  message(FATAL_ERROR
    "run_riscv32_object: ${OUT} is not ELF32 (EI_CLASS=${_class})")
endif()

# e_machine (LE) = 0x00F3 = EM_RISCV -> file bytes F3 00
string(SUBSTRING "${_hex}" 36 4 _mach)
if(NOT _mach STREQUAL "F300")
  message(FATAL_ERROR
    "run_riscv32_object: ${OUT} is not RISC-V (e_machine=${_mach})")
endif()
