set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR armv6)

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM "NEVER")
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY "ONLY")
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE "ONLY")

set(GENERATE_HEX "arm-none-eabi-objcopy -O ihex")


add_compile_definitions(STM32 STM32C0)

# cpu/fpu flags
set(CPU_FLAGS "-mcpu=cortex-m0plus -mthumb -mabi=aapcs")
set(FPU_FLAGS "-mfloat-abi=soft")

# c/c++ flags
# keep every function in a separate section, this allows linker to discard unused ones
set(C_FLAGS "-D__STACK_SIZE=8192 -D__HEAP_SIZE=8192 -fshort-enums -fdata-sections -ffunction-sections -Wall")
#-fno-builtin
set(CXX_FLAGS "${C_FLAGS} -fno-rtti -fno-exceptions -fno-use-cxa-atexit")

# linker flags
# let linker dump unused sections, use newlib in nano version, add standard libs at end so that their symbols get found
# https://interrupt.memfault.com/blog/how-to-write-linker-scripts-for-firmware
# use target_link_directories to let the linker find link.ld
set(LINKER_FLAGS "-Wl,--gc-sections -Wl,--undefined=SystemInit -specs=nano.specs -specs=nosys.specs")

# set flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${CPU_FLAGS} ${FPU_FLAGS} ${C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CPU_FLAGS} ${FPU_FLAGS} ${CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${LINKER_FLAGS}")
