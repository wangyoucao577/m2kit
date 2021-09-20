from conans import ConanFile, CMake


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
        cmake = CMake(self, generator="Ninja")
        #cmake.verbose = True
        cmake.configure(source_folder="src")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

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
