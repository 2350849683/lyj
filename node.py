import zerorpc
import psutil

class Node(object):
    def __init__(self):
        self.service = None

    def get_service(self):
        if not self.service:
            self.service = self.create_service()
        return self.service


class RemoteNode(Node):
    def __init__(self,host,port):
        super(RemoteNode, self).__init__()  # 对继承自父类Node的属性进行初始化
        self.host = host
        self.port = int(port)

    def create_service(self):
        client = zerorpc.Client()
        print(f'已连接{self.host}:{self.port}')
        client.connect('tcp://%s:%s' % (self.host, self.port))
        return client


class LocalNode(Node):
    def __init__(self,name):
        super(LocalNode, self).__init__()
        self.name = name
    def create_service(self):
        return  LocalService(self)



class LocalService(object):
    def __init__(self,node):
        self.node=node
    def memory(self):#获取内存
        info = psutil.virtual_memory()
        cs={
        "hostname":self.node.name,
        "memory":f"{info.total/1073741824:.2f}GB",
        "used":f"{info.used/1073741824:.2f}GB",
        "surplus":f"{info.free/1073741824:2f}GB"
        }
        return cs

    def get_disks(self):  #获取磁盘信息
        disks = []
        for dp in psutil.disk_partitions():
            usage = psutil.disk_usage(dp.mountpoint)
            disk = {
                'device': dp.device,
                'mountpoint': dp.mountpoint,
                'type': dp.fstype,
                'options': dp.opts,
                'space_total': usage.total,
                'space_used': usage.used,
                'space_used_percent': usage.percent,
                'space_free': usage.free
            }
            disks.append(disk)

        return disks

    def get_cpu(self):
        cpu={
        "hyperthreading":psutil.cpu_count(),
        "Not hyper-threading":psutil.cpu_count(logical=False)
        }
        return cpu

    def get_pid(self):
        pid = []
        p = psutil.pids()
        for i in p:
            pids = {
                "name": psutil.Process(i).name(),
                "pid": i,
            }
            pid.append(pids)
        return pid
    def get_pid_int(self,pid):
        p=psutil.Process(pid)
        pi={
            "name":p.name(),
            "path":p.exe()
        }
        return pi