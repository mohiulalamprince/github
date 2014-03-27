import _socket
from _socket import *
from functools import partial
from types import MethodType

try:
    import _ssl
except ImportError:
    # no SSL support
    pass
else:
    def ssl(sock, keyfile=None, certfile=None):
        # we do an internal import here because the ssl
        # module imports the socket module
        import ssl as _realssl
        warnings.warn("socket.ssl() is deprecated.  Use ssl.wrap_socket() instead.",
                      DeprecationWarning, stacklevel=2)
        return _realssl.sslwrap_simple(sock, keyfile, certfile)

    # we need to import the same constants we used to...
    from _ssl import SSLError as sslerror
    from _ssl import \
         RAND_add, \
         RAND_egd, \
         RAND_status, \
         SSL_ERROR_ZERO_RETURN, \
         SSL_ERROR_WANT_READ, \
         SSL_ERROR_WANT_WRITE, \
         SSL_ERROR_WANT_X509_LOOKUP, \
         SSL_ERROR_SYSCALL, \
         SSL_ERROR_SSL, \
         SSL_ERROR_WANT_CONNECT, \
         SSL_ERROR_EOF, \
         SSL_ERROR_INVALID_ERROR_CODE

import os, sys, warnings

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import errno
except ImportError:
    errno = None
EBADF = getattr(errno, 'EBADF', 9)
EINTR = getattr(errno, 'EINTR', 4)

__all__ = ["getfqdn", "create_connection"]
__all__.extend(os._get_exports_list(_socket))


_realsocket = socket

# WSA error codes
if sys.platform.lower().startswith("win"):
    errorTab = {}
    errorTab[10004] = "The operation was interrupted."
    errorTab[10009] = "A bad file handle was passed."
    errorTab[10013] = "Permission denied."
    errorTab[10014] = "A fault occurred on the network??" # WSAEFAULT
    errorTab[10022] = "An invalid operation was attempted."
    errorTab[10035] = "The socket operation would block"
    errorTab[10036] = "A blocking operation is already in progress."
    errorTab[10048] = "The network address is in use."
    errorTab[10054] = "The connection has been reset."
    errorTab[10058] = "The network has been shut down."
    errorTab[10060] = "The operation timed out."
    errorTab[10061] = "Connection refused."
    errorTab[10063] = "The name is too long."
    errorTab[10064] = "The host is down."
    errorTab[10065] = "The host is unreachable."
    __all__.append("errorTab")



def getfqdn(name=''):
    """Get fully qualified domain name from name.

    An empty argument is interpreted as meaning the local host.

    First the hostname returned by gethostbyaddr() is checked, then
    possibly existing aliases. In case no FQDN is available, hostname
    from gethostname() is returned.
    """
    name = name.strip()
    if not name or name == '0.0.0.0':
        name = gethostname()
    try:
        hostname, aliases, ipaddrs = gethostbyaddr(name)
    except error:
        pass
    else:
        aliases.insert(0, hostname)
        for name in aliases:
            if '.' in name:
                break
        else:
            name = hostname
    return name


_socketmethods = (
    'bind', 'connect', 'connect_ex', 'fileno', 'listen',
    'getpeername', 'getsockname', 'getsockopt', 'setsockopt',
    'sendall', 'setblocking',
    'settimeout', 'gettimeout', 'shutdown')

if os.name == "nt":
    _socketmethods = _socketmethods + ('ioctl',)

if sys.platform == "riscos":
    _socketmethods = _socketmethods + ('sleeptaskw',)

# All the method names that must be delegated to either the real socket
# object or the _closedsocket object.
_delegate_methods = ("recv", "recvfrom", "recv_into", "recvfrom_into",
                     "send", "sendto")

class _closedsocket(object):
    __slots__ = []
    def _dummy(*args):
        raise error(EBADF, 'Bad file descriptor')
    # All _delegate_methods must also be initialized here.
    send = recv = recv_into = sendto = recvfrom = recvfrom_into = _dummy
    __getattr__ = _dummy

# Wrapper around platform socket objects. This implements
# a platform-independent dup() functionality. The
# implementation currently relies on reference counting
# to close the underlying socket object.
class _socketobject(object):

    __doc__ = _realsocket.__doc__

    __slots__ = ["_sock", "__weakref__"] + list(_delegate_methods)

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, _sock=None):
        if _sock is None:
            _sock = _realsocket(family, type, proto)
        self._sock = _sock
        for method in _delegate_methods:
            setattr(self, method, getattr(_sock, method))

    def close(self):
        self._sock = _closedsocket()
        dummy = self._sock._dummy
        for method in _delegate_methods:
            setattr(self, method, dummy)
    close.__doc__ = _realsocket.close.__doc__

    def accept(self):
        sock, addr = self._sock.accept()
        return _socketobject(_sock=sock), addr
    accept.__doc__ = _realsocket.accept.__doc__

    def dup(self):
        """dup() -> socket object

        Return a new socket object connected to the same system resource."""
        return _socketobject(_sock=self._sock)

    def makefile(self, mode='r', bufsize=-1):
        """makefile([mode[, bufsize]]) -> file object

        Return a regular file object corresponding to the socket.  The mode
        and bufsize arguments are as for the built-in open() function."""
        return _fileobject(self._sock, mode, bufsize)

    family = property(lambda self: self._sock.family, doc="the socket family")
    type = property(lambda self: self._sock.type, doc="the socket type")
    proto = property(lambda self: self._sock.proto, doc="the socket protocol")

def meth(name,self,*args):
    return getattr(self._sock,name)(*args)

for _m in _socketmethods:
    p = partial(meth,_m)
    p.__name__ = _m
    p.__doc__ = getattr(_realsocket,_m).__doc__
    m = MethodType(p,None,_socketobject)
    setattr(_socketobject,_m,m)

socket = SocketType = _socketobject

class _fileobject(object):
    """Faux file object attached to a socket object."""

    default_bufsize = 8192
    name = "<socket>"

    __slots__ = ["mode", "bufsize", "softspace",
                 # "closed" is a property, see below
                 "_sock", "_rbufsize", "_wbufsize", "_rbuf", "_wbuf", "_wbuf_len",
                 "_close"]

    def __init__(self, sock, mode='rb', bufsize=-1, close=False):
        self._sock = sock
        self.mode = mode # Not actually used in this version
        if bufsize < 0:
            bufsize = self.default_bufsize
        self.bufsize = bufsize
        self.softspace = False
        # _rbufsize is the suggested recv buffer size.  It is *strictly*
        # obeyed within readline() for recv calls.  If it is larger than
        # default_bufsize it will be used for recv calls within read().
        if bufsize == 0:
            self._rbufsize = 1
        elif bufsize == 1:
            self._rbufsize = self.default_bufsize
        else:
            self._rbufsize = bufsize
        self._wbufsize = bufsize
        # We use StringIO for the read buffer to avoid holding a list
        # of variously sized string objects which have been known to
        # fragment the heap due to how they are malloc()ed and often
        # realloc()ed down much smaller than their original allocation.
        self._rbuf = StringIO()
        self._wbuf = [] # A list of strings
        self._wbuf_len = 0
        self._close = close

    def _getclosed(self):
        return self._sock is None
    closed = property(_getclosed, doc="True if the file is closed")

    def close(self):
        try:
            if self._sock:
                self.flush()
        finally:
            if self._close:
                self._sock.close()
            self._sock = None

    def __del__(self):
        try:
            self.close()
        except:
            # close() may fail if __init__ didn't complete
            pass

    def flush(self):
        if self