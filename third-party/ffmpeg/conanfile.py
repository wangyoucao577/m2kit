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
        configureArgs=["--cc="+str(self.settings.compiler), "--cxx="+str(self.settings.compiler)]
        if self.settings.build_type == "Debug":
            configureArgs.append("--enable-debug")

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
            autotools.configure(args=configureArgs)
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
