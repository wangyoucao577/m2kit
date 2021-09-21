import os
from conans import ConanFile, AutoToolsBuildEnvironment
from conans import tools


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.4"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Ffmpeg here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = "src/*"
    requires = "boringssl/0.1"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        configureArgs=[]
        if self.settings.build_type == "Debug":
            configureArgs.append("--enable-debug")

        if self.settings.os == "Android":
            android_ndk_home = tools.get_env("ANDROID_NDK_HOME")
            if android_ndk_home is None:
                print("ANDROID_NDK_HOME is not set")
                os.exit(1)

            # decide host_tag, default to linux
            host_tag = "linux-x86_64"   
            if tools.detected_os() == "Darwin":
                host_tag = "darwin-x86_64"
            elif tools.detected_os() == "Windows":
                host_tag = "windows-x86_64"
            android_ndk_toolchain_path = android_ndk_home + "/toolchains/llvm/prebuilt/{}".format(host_tag)
            configureArgs.append("--enable-cross-compile")
            configureArgs.append("--target-os=android")
            configureArgs.append("--sysroot={}/sysroot".format(android_ndk_toolchain_path))
            if self.settings.arch == "armv7":
                configureArgs.append("--arch=arm")
                configureArgs.append("--cross-prefix={}/bin/arm-linux-androideabi-".format(android_ndk_toolchain_path))
                configureArgs.append("--cc={}/bin/armv7a-linux-androideabi{}-clang".format(android_ndk_toolchain_path, self.settings.os.api_level))
            elif self.settings.arch == "armv8":
                configureArgs.append("--arch=aarch64")
                configureArgs.append("--cross-prefix={}/bin/aarch64-linux-android-".format(android_ndk_toolchain_path))
                configureArgs.append("--cc={}/bin/aarch64-linux-android{}-clang".format(android_ndk_toolchain_path, self.settings.os.api_level))
            elif self.settings.arch == "x86":
                configureArgs.append("--arch=x86")
                configureArgs.append("--cross-prefix={}/bin/i686-linux-android-".format(android_ndk_toolchain_path))
                configureArgs.append("--cc={}/bin/i686-linux-android{}-clang".format(android_ndk_toolchain_path, self.settings.os.api_level))
            elif self.settings.arch == "x86_64":
                configureArgs.append("--arch=x86_64")
                configureArgs.append("--cross-prefix={}/bin/x86_64-linux-android-".format(android_ndk_toolchain_path))
                configureArgs.append("--cc={}/bin/x86_64-linux-android{}-clang".format(android_ndk_toolchain_path, self.settings.os.api_level))
            else:
                print("arch {} is not support".format(self.settings.arch))
                os.exit(1)

        else:
            configureArgs.append("--cc="+str(self.settings.compiler))
            configureArgs.append("--cxx="+str(self.settings.compiler))


        # deps is a list of package names, for example ["boringssl"]
        for d in self.deps_cpp_info.deps:
            for p in self.deps_cpp_info[d].include_paths:
                configureArgs.append("--extra-cflags=-I"+p)
            for p in self.deps_cpp_info[d].lib_paths:
                configureArgs.append("--extra-ldflags=-L"+p)

        configureArgs.append("--enable-openssl")        
        configureArgs.append("--extra-libs=-pthread")   

        with tools.chdir("./src/ffmpeg-4.4/"):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=configureArgs, build=False, host=False)
            autotools.make()
            autotools.install()

    # def package(self):
    #     self.copy("*.h", dst="include", src="src")
    #     self.copy("*.lib", dst="lib", keep_path=False)
    #     self.copy("*.dll", dst="bin", keep_path=False)
    #     self.copy("*.dylib*", dst="lib", keep_path=False)
    #     self.copy("*.so", dst="lib", keep_path=False)
    #     self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ffmpeg"]
