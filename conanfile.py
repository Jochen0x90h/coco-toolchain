import os
from conans import ConanFile, tools
from conan.tools.files import save


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


    def getType(self):
        p = str(self.options.platform);
        if p == 'None' or p == 'native' or p == 'emu':
           return 'native'
        if p.startswith('nrf52'):
           return 'nrf52'
        if p.startswith('stm32f0'):
           return 'stm32f0'

    def isArm(self):
        t = self.getType()
        return t == 'nrf52' or t.startswith('stm32')

    def build(self):
        # https://docs.conan.io/1/reference/conanfile/tools/files/basic.html#conan-tools-files-save
        platform = str(self.options.platform)
        content = f"set(PLATFORM \"{platform}\")"
        save(self, "cmake/generated/variables.cmake", content)

    def package(self):
        # install user toolchain from build directory into package directory
        self.copy("*", src=os.path.join("cmake", self.getType()), dst="cmake/coco")
        self.copy("*", src="cmake/generated", dst="cmake/coco")

    def package_info(self):
        # https://docs.conan.io/1/systems_cross_building/cross_building.html#conan-v1-24-and-newer
        # https://docs.conan.io/1/reference/conanfile/tools/cmake/cmaketoolchain.html#conf

        # export platform
        #self.user_info.platform = self.options.platform

        # add custom cmake toolchains
        t = os.path.join(self.package_folder, "cmake/coco/toolchain.cmake")
        v = os.path.join(self.package_folder, "cmake/coco/variables.cmake")
        self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", [t, v])

        if self.isArm():
            # set compiler executables
            executables = {}
            cc = self.env.get("ARM_CC", None)
            if cc != None:
                executables['c'] = cc
            cxx = self.env.get("ARM_CXX", None)
            if cxx != None:
                executables['cpp'] = cxx
            self.conf_info.define("tools.build:compiler_executables", executables)

        # compiler dependent flags
        settings_target = getattr(self, 'settings_target', None)
        if settings_target != None:
            if settings_target.compiler == "gcc":
                self.conf_info.define("tools.build:cxxflags", ["-fcoroutines", "-fconcepts", "-Wno-literal-suffix"])
            if settings_target.compiler == "clang":
                self.conf_info.define("tools.build:cxxflags", ["-fcoroutines-ts", "-Wno-user-defined-literals"])
            if settings_target.compiler == "Visual Studio":
                self.conf_info.define("tools.build:cxxflags", ["/wd4455"])
