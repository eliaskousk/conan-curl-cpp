from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class CurlCppConan(ConanFile):
    name = "curl-cpp"
    version = "latest"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    requires = "libcurl/7.52.1@eliaskousk/stable"
    url="http://github.com/eliaskousk/conan-curl-cpp"
    license="https://opensource.org/licenses/MIT"
    exports= "CMakeLists.txt", "change_dylib_names.sh"
    folder_name = "curl-cpp-%s" % version

    def source(self):

        self.run("git clone https://github.com/JosephP91/curlcpp.git %s" % self.folder_name)
        self.run("cd %s && git checkout master" % self.folder_name)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        self.run("%s && cmake -DBUILD_SHARED_LIBS=ON .. %s" % (cd_build, cmake.command_line))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):

        if self.settings.os == "Macos":
            self.run("bash ./change_dylib_names.sh")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="./%s/include" % self.folder_name, keep_path=False)


        libdir = "./_build/%s/src" % self.folder_name
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['curlcpp curl']
