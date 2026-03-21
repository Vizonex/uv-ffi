import cffi
import sys

is_64bit = sys.maxsize > 2**32
BIT_TYPES = f"""
typedef {'unsigned long long' if is_64bit else 'unsigned int'} size_t;
typedef {'long long' if is_64bit else 'int' } ssize_t;
"""


if sys.platform != "win32":
    PLATFORM_TYPES = """
#define SIGCHLD ...

typedef int uv_file;
typedef int uv_os_sock_t;
typedef int uv_os_fd_t;
typedef int uv_pid_t; /* literally same as pid_t... */  

/* Note: May be cast to struct iovec. See writev(2). */
typedef struct {
  char* base;
  size_t len;
} uv_buf_t;

"""

else:
    PLATFORM_TYPES = f"""



typedef void* HANDLE;
typedef {'unsigned long long' if is_64bit else 'unsigned int'} UINT_PTR;

typedef UINT_PTR SOCKET;
typedef int uv_file;
typedef SOCKET uv_os_sock_t;
typedef HANDLE uv_os_fd_t;
typedef int uv_pid_t;
""" + """
typedef struct {
  char* base;
  unsigned long len;
} uv_buf_t;
"""

INCLUDES = """
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
# include <WinSock2.h>
#else
# include <sys/types.h>
# include <sys/socket.h>
# include <netdb.h> /* struct hostent */
# include <netinet/in.h> /* struct sockaddr_in/sockaddr_in6 */
#endif
#include <uv.h>
"""

TYPES = """


/* stdint */

typedef signed char        int8_t;
typedef short              int16_t;
typedef int                int32_t;
typedef long long          int64_t;
typedef unsigned char      uint8_t;
typedef unsigned short     uint16_t;
typedef unsigned int       uint32_t;
typedef unsigned long long uint64_t;

/* uv.h */

typedef unsigned char uv_gid_t;
typedef unsigned char uv_uid_t;

typedef enum {
  UV_E2BIG = ...,
  UV_EACCES = ...,
  UV_EADDRINUSE = ..., 
  UV_EADDRNOTAVAIL = ..., 
  UV_EAFNOSUPPORT = ..., 
  UV_EAGAIN = ...,
  UV_EAI_ADDRFAMILY = ..., 
  UV_EAI_AGAIN = ..., 
  UV_EAI_BADFLAGS = ..., 
  UV_EAI_BADHINTS = ...,
  UV_EAI_CANCELED = ...,
  UV_EAI_FAIL = ..., 
  UV_EAI_FAMILY = ..., 
  UV_EAI_MEMORY = ..., 
  UV_EAI_NODATA = ...,
  UV_EAI_NONAME = ...,
  UV_EAI_OVERFLOW = ..., 
  UV_EAI_PROTOCOL = ..., 
  UV_EAI_SERVICE = ..., 
  UV_EAI_SOCKTYPE = ..., 
  UV_EALREADY = ..., 
  UV_EBADF = ..., 
  UV_EBUSY = ...,
  UV_ECANCELED = ...,
  UV_ECHARSET = ...,
  UV_ECONNABORTED = ..., 
  UV_ECONNREFUSED = ..., 
  UV_ECONNRESET = ..., 
  UV_EDESTADDRREQ = ..., 
  UV_EEXIST = ..., 
  UV_EFAULT = ..., 
  UV_EFBIG = ..., 
  UV_EHOSTUNREACH = ...,
  UV_EINTR = ..., 
  UV_EINVAL = ..., 
  UV_EIO = ...,
  UV_EISCONN = ...,
  UV_EISDIR = ..., 
  UV_ELOOP = ..., 
  UV_EMFILE = ..., 
  UV_EMSGSIZE = ...,
  UV_ENAMETOOLONG = ...,
  UV_ENETDOWN = ...,
  UV_ENETUNREACH = ...,
  UV_ENFILE = ..., 
  UV_ENOBUFS = ...,
  UV_ENODEV = ...,
  UV_ENOENT = ...,
  UV_ENOMEM = ..., 
  UV_ENONET = ..., 
  UV_ENOPROTOOPT = ...,
  UV_ENOSPC = ...,
  UV_ENOSYS = ..., 
  UV_ENOTCONN = ..., 
  UV_ENOTDIR = ..., 
  UV_ENOTEMPTY = ..., 
  UV_ENOTSOCK = ..., 
  UV_ENOTSUP = ...,
  UV_EOVERFLOW = ..., 
  UV_EPERM = ...,
  UV_EPIPE = ..., 
  UV_EPROTO = ..., 
  UV_EPROTONOSUPPORT = ..., 
  UV_EPROTOTYPE = ..., 
  UV_ERANGE = ..., 
  UV_EROFS = ..., 
  UV_ESHUTDOWN = ..., 
  UV_ESPIPE = ..., 
  UV_ESRCH = ..., 
  UV_ETIMEDOUT = ..., 
  UV_ETXTBSY = ..., 
  UV_EXDEV = ..., 
  UV_UNKNOWN = ...,
  UV_EOF = ..., 
  UV_ENXIO = ...,
  UV_EMLINK = ..., 
  UV_EHOSTDOWN = ..., 
  UV_EREMOTEIO = ..., 
  UV_ENOTTY = ..., 
  UV_EFTYPE = ..., 
  UV_EILSEQ = ..., 
  UV_ESOCKTNOSUPPORT = ..., 
  UV_ENODATA = ..., 
  UV_EUNATCH = ..., 
  UV_ENOEXEC = ...,
} uv_errno_t;

typedef enum  {
    UV_UNKNOWN_REQ = ...,
    UV_REQ = ...,
    UV_CONNECT = ...,
    UV_WRITE = ...,
    UV_SHUTDOWN = ...,
    UV_UDP_SEND = ...,
    UV_FS = ...,
    UV_WORK = ...,
    UV_GETADDRINFO = ...,
    UV_GETNAMEINFO = ...,

} uv_req_type;

typedef enum {
    UV_RUN_DEFAULT = ...,
    UV_RUN_ONCE = ...,
    UV_RUN_NOWAIT = ...
} uv_run_mode;

enum uv_poll_event {
    UV_READABLE = ...,
    UV_WRITABLE = ...,
    UV_DISCONNECT = ...
};

enum uv_udp_flags{
    UV_UDP_IPV6ONLY = ...,
    UV_UDP_PARTIAL = ...
};

typedef enum {
    UV_LEAVE_GROUP = ...,
    UV_JOIN_GROUP = ...
} uv_membership;

enum uv_fs_event {
    UV_RENAME = ...,
    UV_CHANGE = ...
};

#define SO_BROADCAST ...
#define SIGINT ...
#define SIGHUP ...

#define SIGKILL ...
#define SIGTERM ...


typedef struct uv_loop_s {
    void* data;
} uv_loop_t;

typedef struct uv_handle_s {
    void* data;
    uv_loop_t* loop;
    unsigned int flags;
} uv_handle_t;

typedef struct uv_idle_s {
    void* data;
    uv_loop_t* loop;
} uv_idle_t;

typedef struct uv_check_s {
    void* data;
    uv_loop_t* loop;
} uv_check_t;

typedef struct uv_signal_s {
    void* data;
    uv_loop_t* loop;
} uv_signal_t;

typedef struct uv_async_s {
    void* data;
    uv_loop_t* loop;
} uv_async_t;

typedef struct uv_timer_s {
    void* data;
    uv_loop_t* loop;
} uv_timer_t;

typedef struct uv_stream_s {
    void* data;
    size_t write_queue_size;
    uv_loop_t* loop;
} uv_stream_t;

typedef struct uv_tcp_s {
    void* data;
    uv_loop_t* loop;
} uv_tcp_t;

typedef struct uv_pipe_s {
    void* data;
    uv_loop_t* loop;
} uv_pipe_t;

typedef struct uv_udp_s {
    void* data;
    uv_loop_t* loop;
    size_t send_queue_size;
    size_t send_queue_count;
} uv_udp_t;

typedef struct uv_udp_send_s {
    void* data;
    uv_udp_t* handle;
} uv_udp_send_t;

typedef struct uv_poll_s {
    void* data;
    uv_loop_t* loop;
} uv_poll_t;

typedef struct uv_req_s {
    void* data;
    uv_req_type type;
} uv_req_t;

typedef struct uv_connect_s {
    void* data;
} uv_connect_t;

typedef struct uv_getaddrinfo_s {
    void* data;
} uv_getaddrinfo_t;

typedef struct uv_getnameinfo_s {
    void* data;
} uv_getnameinfo_t;

typedef struct uv_write_s {
    void* data;
} uv_write_t;


typedef struct uv_shutdown_s {
    void* data;
} uv_shutdown_t;


typedef struct uv_process_s {
    void* data;
    int pid;
} uv_process_t;

typedef struct uv_fs_event_s {
    void* data;
} uv_fs_event_t;

struct sockaddr {
    unsigned short sa_family;
    char           sa_data[14];
};

struct addrinfo {
    int            ai_flags;
    int            ai_family;
    int            ai_socktype;
    int            ai_protocol;
    size_t         ai_addrlen;
    struct sockaddr* ai_addr;
    char*          ai_canonname;
    struct addrinfo* ai_next;
};

struct sockaddr_in {
    unsigned short sin_family;
    unsigned short sin_port;
};

struct sockaddr_in6 {
    unsigned short sin6_family;
    unsigned short sin6_port;
    unsigned long  sin6_flowinfo;
    unsigned long  sin6_scope_id;
};

struct sockaddr_storage {
    unsigned short ss_family;
};

enum uv_process_flags {
    UV_PROCESS_SETUID = 1,
    UV_PROCESS_SETGID = 2,
    UV_PROCESS_WINDOWS_VERBATIM_ARGUMENTS = 4,
    UV_PROCESS_DETACHED = 8,
    UV_PROCESS_WINDOWS_HIDE = 16
};

typedef enum  {
    UV_IGNORE = 0x00,
    UV_CREATE_PIPE = 0x01,
    UV_INHERIT_FD = 0x02,
    UV_INHERIT_STREAM = 0x04,
    UV_READABLE_PIPE = 0x10,
    UV_WRITABLE_PIPE = 0x20,
    UV_NONBLOCK_PIPE = 0x40
} uv_stdio_flags;

// typedef union {
//     uv_stream_t* stream;
//     int fd;
// } uv_stdio_container_data_u;
// 
// typedef struct {
//     uv_stdio_flags flags;
//     uv_stdio_container_data_u data;
// } uv_stdio_container_t;
"""

CALLBACKS = """

typedef void (*uv_walk_cb)(uv_handle_t* handle, void* arg);

typedef void (*uv_close_cb)(uv_handle_t* handle);
typedef void (*uv_idle_cb)(uv_idle_t* handle);
typedef void (*uv_check_cb)(uv_check_t* handle);
typedef void (*uv_signal_cb)(uv_signal_t* handle, int signum);
typedef void (*uv_async_cb)(uv_async_t* handle);
typedef void (*uv_timer_cb)(uv_timer_t* handle);
typedef void (*uv_connection_cb)(uv_stream_t* server, int status);
typedef void (*uv_alloc_cb)(uv_handle_t* handle, size_t suggested_size, uv_buf_t* buf);

typedef void (*uv_read_cb)(uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf);
typedef void (*uv_write_cb)(uv_write_t* req, int status);
typedef void (*uv_getaddrinfo_cb)(uv_getaddrinfo_t* req, int status, struct addrinfo* res);
typedef void (*uv_getnameinfo_cb)(uv_getnameinfo_t* req, int status, const char* hostname, const char* service);
typedef void (*uv_shutdown_cb)(uv_shutdown_t* req, int status);
typedef void (*uv_poll_cb)(uv_poll_t* handle, int status, int events);
typedef void (*uv_connect_cb)(uv_connect_t* req, int status);

typedef void (*uv_udp_send_cb)(uv_udp_send_t* req, int status);
typedef void (*uv_udp_recv_cb)(
    uv_udp_t* handle, ssize_t nread,
    const uv_buf_t* buf,
    const struct sockaddr* addr,
    unsigned int flags
);
typedef void (*uv_fs_event_cb)(uv_fs_event_t* handle,
    const char *filename,
    int events,
    int status
); 

typedef void (*uv_exit_cb)(uv_process_t*, int64_t exit_status, int term_signal);

typedef struct {
    uv_exit_cb exit_cb;
    char* file;
    char** args;
    char** env;
    char* cwd;
    unsigned int flags;
    int stdio_count;
    // uv_stdio_container_t* stdio;
    uv_uid_t uid;
    uv_gid_t gid;
} uv_process_options_t;

"""

FUNCTIONS = """
int uv_cancel(uv_req_t* req);

int uv_is_active(const uv_handle_t* handle);
void uv_close(uv_handle_t* handle, uv_close_cb close_cb);
int uv_is_closing(const uv_handle_t* handle);
int uv_fileno(const uv_handle_t* handle, uv_os_fd_t* fd);
void uv_walk(uv_loop_t* loop, uv_walk_cb walk_cb, void* arg);

int uv_loop_init(uv_loop_t* loop);
int uv_loop_close(uv_loop_t* loop);
int uv_loop_alive(uv_loop_t* loop);
int uv_loop_fork(uv_loop_t* loop);
uv_os_fd_t uv_backend_fd(uv_loop_t* loop);

void uv_update_time(uv_loop_t* loop);
uint64_t uv_now(const uv_loop_t*);
int uv_run(uv_loop_t*, uv_run_mode mode);
void uv_stop(uv_loop_t*);

int uv_idle_init(uv_loop_t*, uv_idle_t* idle);
int uv_idle_start(uv_idle_t* idle, uv_idle_cb cb);
int uv_idle_stop(uv_idle_t* idle);

int uv_check_init(uv_loop_t*, uv_check_t* idle);
int uv_check_start(uv_check_t* check, uv_check_cb cb);
int uv_check_stop(uv_check_t* check);

int uv_signal_init(uv_loop_t* loop, uv_signal_t* handle);
int uv_signal_start(uv_signal_t* handle,
                    uv_signal_cb signal_cb,
                    int signum);
int uv_signal_stop(uv_signal_t* handle);


int uv_async_init(uv_loop_t*, uv_async_t* async_, uv_async_cb async_cb);
int uv_async_send(uv_async_t* async_);

int uv_timer_init(uv_loop_t*, uv_timer_t* handle);
int uv_timer_start(uv_timer_t* handle,
                   uv_timer_cb cb,
                   uint64_t timeout,
                   uint64_t repeat);
int uv_timer_stop(uv_timer_t* handle);

int uv_getaddrinfo(
    uv_loop_t* loop,
    uv_getaddrinfo_t* req,
    uv_getaddrinfo_cb getaddrinfo_cb,
    const char* node,
    const char* service,
    const struct addrinfo* hints
);

void uv_freeaddrinfo(struct addrinfo* ai);

int uv_getnameinfo(
    uv_loop_t* loop,
    uv_getnameinfo_t* req,
    uv_getnameinfo_cb getnameinfo_cb,
    const struct sockaddr* addr,
    int flags
);

int uv_ip4_name(const struct sockaddr_in* src, char* dst, size_t size);
int uv_ip6_name(const struct sockaddr_in6* src, char* dst, size_t size);

int uv_listen(uv_stream_t* stream, int backlog, uv_connection_cb cb);
int uv_accept(uv_stream_t* server, uv_stream_t* client);
int uv_read_start(uv_stream_t* stream,
                  uv_alloc_cb alloc_cb,
                  uv_read_cb read_cb);
int uv_read_stop(uv_stream_t*);
int uv_write(uv_write_t* req, uv_stream_t* handle,
             uv_buf_t bufs[], unsigned int nbufs, uv_write_cb cb);

int uv_try_write(uv_stream_t* handle, uv_buf_t bufs[], unsigned int nbufs);

int uv_shutdown(uv_shutdown_t* req, uv_stream_t* handle, uv_shutdown_cb cb);

int uv_is_readable(const uv_stream_t* handle);
int uv_is_writable(const uv_stream_t* handle);

int uv_tcp_init_ex(uv_loop_t*, uv_tcp_t* handle, unsigned int flags);
int uv_tcp_nodelay(uv_tcp_t* handle, int enable);
int uv_tcp_keepalive(uv_tcp_t* handle, int enable, unsigned int delay);
int uv_tcp_open(uv_tcp_t* handle, uv_os_sock_t sock);
int uv_tcp_bind(uv_tcp_t* handle, struct sockaddr* addr, unsigned int flags);

int uv_tcp_getsockname(const uv_tcp_t* handle, struct sockaddr* name, int* namelen);

int uv_tcp_getpeername(const uv_tcp_t* handle, struct sockaddr* name, int* namelen);

int uv_tcp_connect(uv_connect_t* req, uv_tcp_t* handle, const struct sockaddr* addr, uv_connect_cb cb);


int uv_udp_init_ex(uv_loop_t* loop, uv_udp_t* handle, unsigned int flags);
int uv_udp_connect(uv_udp_t* handle, const struct sockaddr* addr);
int uv_udp_open(uv_udp_t* handle, uv_os_sock_t sock);
int uv_udp_bind(uv_udp_t* handle, const struct sockaddr* addr,
                unsigned int flags);
int uv_udp_send(uv_udp_send_t* req, uv_udp_t* handle,
                const uv_buf_t bufs[], unsigned int nbufs,
                const struct sockaddr* addr, uv_udp_send_cb send_cb);
int uv_udp_try_send(uv_udp_t* handle,
                    const uv_buf_t bufs[], unsigned int nbufs,
                    const struct sockaddr* addr);
int uv_udp_recv_start(uv_udp_t* handle, uv_alloc_cb alloc_cb,
                      uv_udp_recv_cb recv_cb);
int uv_udp_recv_stop(uv_udp_t* handle);
int uv_udp_set_broadcast(uv_udp_t* handle, int on);

int uv_poll_init(uv_loop_t* loop, uv_poll_t* handle, int fd);
int uv_poll_init_socket(uv_loop_t* loop, uv_poll_t* handle,
                        uv_os_sock_t socket);
int uv_poll_start(uv_poll_t* handle, int events, uv_poll_cb cb);
int uv_poll_stop(uv_poll_t* poll);

int uv_fs_event_init(uv_loop_t *loop, uv_fs_event_t *handle);
int uv_fs_event_start(uv_fs_event_t *handle, uv_fs_event_cb cb,
                      const char *path, unsigned int flags);
int uv_fs_event_stop(uv_fs_event_t *handle);

typedef struct {
    long tv_sec;
    long tv_usec;
} uv_timeval_t;

typedef struct {
    uv_timeval_t ru_utime;  // user CPU time used
    uv_timeval_t ru_stime;  // system CPU time used
    uint64_t ru_maxrss;     // maximum resident set size
    uint64_t ru_ixrss;      // integral shared memory size
    uint64_t ru_idrss;      // integral unshared data size
    uint64_t ru_isrss;      // integral unshared stack size
    uint64_t ru_minflt;     // page reclaims (soft page faults)
    uint64_t ru_majflt;     // page faults (hard page faults)
    uint64_t ru_nswap;      // swaps
    uint64_t ru_inblock;    // block input operations
    uint64_t ru_oublock;    // block output operations
    uint64_t ru_msgsnd;     // IPC messages sent
    uint64_t ru_msgrcv;     // IPC messages received
    uint64_t ru_nsignals;   // signals received
    uint64_t ru_nvcsw;      // voluntary context switches
    uint64_t ru_nivcsw;     // involuntary context switches
} uv_rusage_t;



int uv_getrusage(uv_rusage_t* rusage);

int uv_ip4_addr(const char* ip, int port, struct sockaddr_in* addr);
int uv_ip6_addr(const char* ip, int port, struct sockaddr_in6* addr);

/* TODO: Memory */

int uv_spawn(uv_loop_t* loop, uv_process_t* handle, const uv_process_options_t* options);
int uv_process_kill(uv_process_t* handle, int signum);
unsigned int uv_version();
int uv_pipe(uv_file fds[2], int read_flags, int write_flags);
"""


ffi = cffi.FFI()
ffi.cdef(BIT_TYPES + PLATFORM_TYPES + TYPES + CALLBACKS + FUNCTIONS)
ffi.set_source("_uv", INCLUDES)

