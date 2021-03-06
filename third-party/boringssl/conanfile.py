import os
from conans import ConanFile, CMake
from conans import tools

class BoringsslConan(ConanFile):
    name = "boringssl"
    version = "0.1"
    license = "https://github.com/google/boringssl/blob/master/LICENSE"
    author = "Jay Zhang <wangyoucao577@gmail.com>"
    url = "https://github.com/google/boringssl"
    description = "BoringSSL is a fork of OpenSSL that is designed to meet Google's needs."
    topics = ("boringssl", "openssl", "ssl", "tls", "encryption", "security")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "src/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):

        cmakeArgs = []
        if self.settings.os == "Android":
            android_ndk_home = tools.get_env("ANDROID_NDK_HOME")
            if android_ndk_home is None:
                print("ANDROID_NDK_HOME is not set")
                os.exit(1)
            cmakeArgs.append("-DCMAKE_TOOLCHAIN_FILE={}/build/cmake/android.toolchain.cmake".format(android_ndk_home))
        elif self.settings.os == "iOS":
            cmakeArgs.append("-DCMAKE_OSX_SYSROOT={}".format(self.settings.os.sdk))
            cmakeArgs.append("-DCMAKE_OSX_ARCHITECTURES={}".format(tools.to_apple_arch(self.settings.arch)))

        cmake = CMake(self, generator="Ninja")
        cmake.verbose = True
        cmake.configure(source_folder="src", args=cmakeArgs)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src/boringssl/include", keep_path=True)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["boringssl"]
