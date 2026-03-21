import os
import shutil
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_ext import build_ext


use_system_lib = bool(int(os.environ.get("UVFFI_USE_SYSTEM_LIB", 0)))

# inspired by pycares and modified via seperating into different functions.


class uv_build_ext(build_ext):
    def add_include_dir(self, dir, force=False):
        if use_system_lib and not force:
            return
        dirs = self.compiler.include_dirs
        if dir not in dirs:
            dirs.insert(0, dir)
        self.compiler.set_include_dirs(dirs)

    def abspath(self, path: str) -> str:
        return os.path.abspath(os.path.join(self.build_temp, path))

    def find_installed_library(self, install_dir: str) -> str:
        if sys.platform == "win32":
            possible_paths = [
                os.path.join(install_dir, "lib", "libuv.lib"),
                os.path.join(install_dir, "lib", "libuv_static.lib"),
                os.path.join(install_dir, "lib", "libuv.a"),
            ]
        else:
            possible_paths = [
                os.path.join(install_dir, "lib", "uv.a"),
                os.path.join(install_dir, "lib64", "uv.a"),
                os.path.join(install_dir, "lib", "libuv.a"),
                os.path.join(install_dir, "lib64", "libuv.a"),
            ]
        lib_path = None
        for path in possible_paths:
            if os.path.exists(path):
                lib_path = path
                break

        if not lib_path:
            raise RuntimeError(
                f"Could not find installed libuv library in {install_dir}.\n"
                f"Checked: {', '.join(possible_paths)}"
            )
        print(f"Found libuv library at: {lib_path}")
        return lib_path

    def build_in_cmake(self):
        cmake_cmd = shutil.which("cmake")
        if not cmake_cmd:
            raise RuntimeError(
                "CMake >= 3.5 is required to build uv-ffi.\n"
                "Please install CMake from https://cmake.org/ or through your system package manager:\n"
                "  Ubuntu/Debian: apt-get install cmake\n"
                "  RHEL/CentOS/Fedora: dnf install cmake\n"
                "  macOS: brew install cmake\n"
                "  Windows: Download from https://cmake.org/download/\n"
                "  FreeBSD: pkg install cmake"
            )

        if not os.path.exists("build"):
            os.mkdir("build")

        uv_dir = "vendor"
        build_temp = self.abspath("uv-build")
        install_dir = self.abspath("uv-install")
        print(install_dir)
        os.makedirs(build_temp, exist_ok=True)
        os.makedirs(install_dir, exist_ok=True)

        cmake_args = [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_CONFIGURATION_TYPES=Release",
            "-DLIBUV_BUILD_SHARED=off",
            f"-DCMAKE_INSTALL_PREFIX={install_dir}",
        ]

        if sys.platform == "darwin":
            # Set minimum macOS deployment target
            cmake_args.append("-DCMAKE_OSX_DEPLOYMENT_TARGET=10.12")
        elif sys.platform == "win32":
            # Windows-specific handling
            if "mingw" in self.compiler.compiler_type:
                cmake_args.extend(["-G", "MinGW Makefiles"])

       
        subprocess.check_call(
            [cmake_cmd, os.path.abspath(uv_dir)] + cmake_args, cwd=build_temp
        )

        print("Building libuv...")
        build_args = ["--build", ".", "--config", "Release"]

        subprocess.check_call([cmake_cmd] + build_args, cwd=build_temp)

        print(f"Installing libuv to {install_dir}")
        install_args = ["--install", ".", "--config", "Release"]
        subprocess.check_call([cmake_cmd] + install_args, cwd=build_temp)

        lib_path = self.find_installed_library(install_dir)

        self.add_include_dir(os.path.join(install_dir, "include"), force=True)
        self.add_include_dir(os.path.join(uv_dir, ""), force=True)

        self.extensions[0].extra_objects = [lib_path]
        if sys.platform == "win32":
            self.compiler.add_library("Shell32")
            self.compiler.add_library("Ws2_32")
            self.compiler.add_library("Advapi32")
            self.compiler.add_library("iphlpapi")
            self.compiler.add_library("Userenv")
            self.compiler.add_library("User32")
            self.compiler.add_library("Dbghelp")
            self.compiler.add_library("Ole32")
        else:
            raise NotImplementedError("TODO")

    def build_extensions(self):
        # Use system libuv library if requested
        if use_system_lib:
            self.compiler.add_library("libuv")
            build_ext.build_extensions(self)
            return
        self.build_in_cmake()
        build_ext.build_extensions(self)


setup(
    cmdclass={"build_ext": uv_build_ext},
    cffi_modules=["src/build_uv.py:ffi"],
    ext_package="uv_ffi",
)
