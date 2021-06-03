import socket


def socket_constants(prefix):
    return dict((getattr(socket, n), n) for n in dir(socket) if n.startswith(prefix))


socket_families = socket_constants('AF_')
socket_types = socket_constants('SOCK_')
def con(c):
    return {
                'fd': c.fd,
                'family': socket_families[c.family],
                'type': socket_types[c.type],
                'local_addr_host': c.laddr[0] if c.laddr else None,
                'local_addr_port': c.laddr[1] if c.laddr else None,
                'remote_addr_host': c.raddr[0] if c.raddr else None,
                'remote_addr_port': c.raddr[1] if c.raddr else None,
                'state': c.status
            }