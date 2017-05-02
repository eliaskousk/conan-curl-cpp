from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans.tools import replace_in_file
from conans.tools import cpu_count
from conans import CMake

class CurlCppConan(ConanFile):
    name = "curl-cpp"
    version = "1.0.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fpic": [True, False]}
    default_options = "shared=False", "fpic=True"
    url="http://github.com/eliaskousk/conan-curl-cpp"
    license="https://opensource.org/licenses/MIT"
    exports= "CMakeLists.txt", "cmake/detect.cpp11.cmake", "change_dylib_names.sh"
    folder_name = "curl-cpp-%s" % version

    def config_options(self):
        self.requires.add("libcurl/7.54.0@eliaskousk/stable", private=False)
        self.options['libcurl'].shared = self.options.shared

    def source(self):
        self.run("git clone https://github.com/JosephP91/curlcpp.git %s" % self.folder_name)
        self.run("cd %s && git checkout 1.0" % self.folder_name)

    def build(self):

        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        fpic = "-DCMAKE_POSITION_INDEPENDENT_CODE=TRUE" if self.options.fpic else ""

        # Detect c++11 instead of forcing it.
        # Will fail gracefully if unsupported.
        text_to_replace = '''if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
endif()
'''
        replaced_text = 'include("../../cmake/detect.cpp11.cmake")'
        replace_in_file(os.path.join(self.folder_name, "src", "CMakeLists.txt"), text_to_replace, replaced_text)

        self.run("%s && cmake .. %s %s %s" % (cd_build, cmake.command_line, shared, fpic))
        self.run("%s && cmake --build . %s -- -j%s" % (cd_build, cmake.build_config, cpu_count()))

    def package(self):
        if self.settings.os == "Macos":
            self.run("bash ./change_dylib_names.sh")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="./%s/include" % self.folder_name, keep_path=False)

        # Copying static libs
        libdir = "./_build/lib"
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)

        # Copying dynamic libs
        libdir = "./_build/%s/src" % self.folder_name
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['curlcpp curl']
