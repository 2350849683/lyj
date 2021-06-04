import zerorpc

class Node(object):
    def __init__(self):
        self.service = None


    def get_service(self):
        if not self.service:
            self.service = self.create_service()
        return self.service


class RemoteNode(Node):
    def __init__(self,host,port):
        self.host = host
        self.port = int(port)

    def create_service(self):
        client = zerorpc.Client()
        client.connect('tcp://%s:%s' % (self.host, self.port))
        return client


class LocalNode(Node):
    def create_service(self):
        return  LocalService()



class LocalService(object):
    pass
