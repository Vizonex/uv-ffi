from .. import _uv as uv
from typing import Any, ClassVar
import errno
import asyncio
import socket
import sys

ffi = uv.ffi
lib = uv.lib

def convert_python_error(uverr: int):
    err = getattr(errno, ffi.string(lib.uv_err_name(uverr)).decode(), uverr)
    return OSError(err, ffi.string(lib.uv_strerror(uverr)).decode())

def convert_error(uverr: int):
    sock_err = 0
    match uverr:
        case lib.UV_ECANCELED:
            return asyncio.CancelledError()
        case lib.UV_EAI_AGAIN:
            sock_err = socket.EAI_AGAIN
        case lib.UV_EAI_BADFLAGS:
            sock_err = socket.EAI_BADFLAGS
        case lib.UV_EAI_BADHINTS:
            sock_err = socket.EAI_BADHINTS
        case lib.UV_EAI_CANCELED:
            sock_err = socket.EAI_CANCELED
        case lib.UV_EAI_FAIL:
            sock_err = socket.EAI_FAIL
        case lib.UV_EAI_FAMILY:
            sock_err = socket.EAI_FAMILY
        case lib.UV_EAI_MEMORY:
            sock_err = socket.EAI_MEMORY
        case lib.UV_EAI_NODATA:
            sock_err = socket.EAI_NODATA
        case lib.UV_EAI_OVERFLOW:
            sock_err = socket.EAI_OVERFLOW
        case lib.UV_EAI_PROTOCOL:
            sock_err = socket.EAI_PROTOCOL
        case lib.UV_EAI_SERVICE:
            sock_err = socket.EAI_SERVICE
        case lib.UV_EAI_SOCKTYPE:
            sock_err = socket.EAI_SOCKTYPE
    if sock_err:
        msg = ""
        if sys.platform == "win32":
            if sock_err in (socket.EAI_FAMILY, socket.EAI_NONAME):
                msg = "getaddrinfo failed"
        return socket.gaierror(sock_err, msg)
    else:
        return convert_python_error(uverr)


class UVHandle:
    HANDLE: ClassVar[str] = "uv_handle_t *"
    
    def __new_handle__(self):
        return ffi.cast("uv_handle_t *", ffi.new(self.HANDLE))
    
    @property
    def ptr(self) -> Any:
        """casts to the real handle's name ex: uv_timer_t"""
        return ffi.cast(self.HANDLE, self._handle)
        
    def __init__(self, loop):
        self._handle = self.__new_handle__()
        self._loop = loop

    def is_active(self) -> bool:
        return lib.uv_is_active(self._handle) == 1
    
    def is_closing(self) -> bool:
        return lib.uv_is_closing(self._handle) == 1
    
    def fileno(self) -> Any:
        fd = ffi.new("uv_os_fd_t [1]")
        err = lib.uv_fileno(self._handle, fd)
        if err < 0:
            raise convert_error(err)
        return fd[0]




        



