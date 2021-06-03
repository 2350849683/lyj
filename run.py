from  flask import Flask
import click
import zerorpc
import requests
from web import web
from gevent.pywsgi import WSGIServer
from node import RemoteNode,LocalNode
class Runer():
    def __init__(self,host,port,as_rpc):
        self.host=host
        self.port =port
        self.as_rpc=as_rpc
        self.nodes={}
    def register_agent(slef,node):   #作为rpc server 启动时，向http server 注册

        slef.nodes[node] = RemoteNode(slef.host, slef.port) #远端数据


    def create_app(slef):  #创建flask app 对象
        app = Flask(__name__)
        app.psdash=slef
        app.register_blueprint(web)
        slef.app = app

    def run_as_web(slef):  #作为http server启动
        slef.create_app()
        slef.nodes[(f"localnode:{slef.port}")]=LocalNode()  #本地数据
        slef.server = WSGIServer((slef.host,slef.port),application=slef.app,)
        slef.server.serve_forever()

    def run_as_rpc(slef):  #作为rpc server 启动

        requests.get(slef.as_rpc + f"/register?port={slef.port}")  #请求 注册
        r = LocalNode().get_service()  #本地数据

        s = zerorpc.Server(r)   #把本数据注册到服务
        s.bind(f"tcp://{slef.host}:{slef.port}")           #启动
        s.run()


@click.command()
@click.option("-h",'--host', default='0.0.0.0', help='输入ip')
@click.option('-p',"--port",type=int,default=5000 ,help='输入端口号')
@click.option("-a",'--as_rpc',default=None, help='psdash节点来注册这个代理启动。如http://127.0.0.1:5000')
def main(host,port,as_rpc):
    run=Runer(host,port,as_rpc)
    if as_rpc:
        run.run_as_rpc()    #启动rpc
    else:
        run.run_as_web()    #启动web

if __name__ == '__main__':
    main()