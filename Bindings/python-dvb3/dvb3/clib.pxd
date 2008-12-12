cdef extern from *:
    enum:
        O_RDONLY
        O_RDWR
        O_NONBLOCK
    enum:
        F_SETFL

    int errno

    cdef char *strerror(int errnum)
    cdef int ioctl(int d, int request, ...)
    cdef int fcntl(int fd, int cmd, long arg)
    cdef int open(char *pathname, int flags)
    cdef int close(int fd)
    cdef void *memset(void *s, int c, int n)
