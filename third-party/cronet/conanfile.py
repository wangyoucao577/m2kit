from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class CronetConan(ConanFile):
    name = "cronet"
    version = "97.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Cronet is the networking stack of Chromium put into a library for use on mobile."
    url = "https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/cronet"
    license = "None"
    author = "None"
    topics = ("cronet", "http", "quic")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    def package(self):
        src_path = "."
        if self.settings.os == "Linux":
            src_path = "prebuilt/linux"
        else:
            print("os {} is not supported yet".format(self.settings.os))
            exit(-1)

        self.copy("*", src=src_path)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
