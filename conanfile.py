# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class MsgpackConan(ConanFile):
    name = "msgpack"
    version = "3.2.0"
    description = "The official C++ library for MessagePack"
    url = "https://github.com/bincrafters/conan-msgpack"
    homepage = "https://github.com/msgpack/msgpack-c"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "msgpack", "message-pack", "serialization")
    license = "BSL-1.0"
    exports = ["LICENSE.md"]
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "build_type", "compiler"
    options = {"fPIC": [True, False], "shared": [True, False], "header_only": [True, False], "with_boost": [True, False]}
    default_options = {"fPIC": True, "shared": False, "header_only": False, "with_boost": False}

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        if self.options.header_only:
            self.settings.clear()
            del self.options.shared
            del self.options.fPIC
            del self.options.with_boost

    def requirements(self):
        if not self.options.header_only and self.options.with_boost:
            self.requires.add("boost/1.69.0@conan/stable")

    def source(self):
        sha256 = "fbaa28c363a316fd7523f31d1745cf03eab0d1e1ea5a1c60aa0dffd4ce551afe"
        archive_name = self.name + "-" + self.version
        tools.get("{0}/releases/download/cpp-{1}/{2}.tar.gz".format(self.homepage,  self.version, archive_name), sha256=sha256)
        os.rename(archive_name, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["MSGPACK_BOOST"] = self.options.with_boost
        cmake.definitions["MSGPACK_32BIT"] = self.settings.arch == "x86"
        cmake.definitions["MSGPACK_BUILD_EXAMPLE"] = False
        cmake.definitions["MSGPACK_BUILD_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        if not self.options.header_only:
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        self.copy("LICENSE_1_0.txt", dst="licenses", src=self._source_subfolder)
        if self.options.header_only:
            self.copy("*.h", dst="include", src=os.path.join(self._source_subfolder, "include"))
            self.copy("*.hpp", dst="include", src=os.path.join(self._source_subfolder, "include"))
        else:
            cmake = self._configure_cmake()
            cmake.install()
            tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        if self.options.header_only:
            self.info.header_only()
        else:
            self.cpp_info.libs = tools.collect_libs(self)
