import os
from conan import ConanFile
from conan.tools.files import save, load, copy
from conan.tools.cmake import CMake


class Project(ConanFile):
    name = "coco-toolchain"
    description = "User toolchain for CMake"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "platform": [None, "ANY"]}
    default_options = {
        "platform": None}
    exports_sources = "conanfile.py", "cmake/*"


    # get type (native or family of MCUs, default is native)
    def getType(self):
        p = str(self.options.platform);
        types = [
              'nrf52', # Cortex-M4F
              'nrf54', # Cortex-M33F
              'stm32f0', # Cortex-M0
              'stm32l0', 'stm32c0', 'stm32g0', # Cortex-M0+
              'stm32f1', 'stm32l1', # Cortex-M3
              'stm32f3', 'stm32f4', 'stm32l4', 'stm32g4', # Cortex-M4F
              'stm32h5', 'stm32u3', 'stm32u5' # Cortex-M33F
        ]
        for t in types:
            if p.startswith(t):
               return t;
        return 'native'

    def build(self):
        # generate variables.cmake (gets added as additional custom cmake toolchain file)
        # https://docs.conan.io/1/reference/conanfile/tools/files/basic.html#conan-tools-files-save
        platform = str(self.options.platform)
        content = f"set(PLATFORM \"{platform}\")"
        save(self, "cmake/generated/variables.cmake", content)

    def package(self):
        # install user toolchain from build directory into package directory
        copy(self, pattern="*", src=os.path.join("cmake", self.getType()), dst=os.path.join(self.package_folder, "cmake/coco"))
        copy(self, pattern="*", src="cmake/generated", dst=os.path.join(self.package_folder, "cmake/coco"))

    def package_info(self):
        # https://docs.conan.io/1/systems_cross_building/cross_building.html#conan-v1-24-and-newer
        # https://docs.conan.io/1/reference/conanfile/tools/cmake/cmaketoolchain.html#conf

        # add custom cmake toolchain files
        t = os.path.join(self.package_folder, "cmake/coco/toolchain.cmake")
        v = os.path.join(self.package_folder, "cmake/coco/variables.cmake")
        self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", [t, v])

        # compiler dependent flags
        settings_target = getattr(self, 'settings_target', None)
        if settings_target != None:
            if settings_target.compiler == "gcc":
                self.conf_info.define("tools.build:cxxflags", ["-fcoroutines", "-fconcepts", "-Wno-literal-suffix"])
            if settings_target.compiler == "clang":
                self.conf_info.define("tools.build:cxxflags", ["-fcoroutines-ts", "-Wno-user-defined-literals"])
            if settings_target.compiler == "msvc":
                self.conf_info.define("tools.build:cxxflags", ["/wd4455", "/Zc:__cplusplus"])
