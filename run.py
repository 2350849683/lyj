from  flask import Flask
import click
import zerorpc
import requests
from web import web
import random
from gevent.pywsgi import WSGIServer
from node import RemoteNode,LocalNode
class Runer():
    def __init__(self,**psdash):
        self.host=psdash['host']
        self.port =psdash['port']
        self.hostname=psdash['as_name']
        self.as_rpc=psdash['as_rpc']
        self.nodes={}
        self.local=LocalNode()

    def register_agent(slef,node,name):   #作为rpc server 启动时，向http server 注册
        print(f"已注册 {node}")
        host,port= node.split(":")
        slef.nodes[f'{name}:{node}']=RemoteNode(host,port)   #远端数据存储


    def create_app(slef):  #创建flask app 对象
        app = Flask(__name__)
        app.psdash=slef
        app.register_blueprint(web)
        slef.app = app

    def run_as_web(slef):  #作为http server启动
        slef.create_app()
        slef.nodes[f"{slef.hostname}:localnode:{slef.port}"]= slef.local #本地数据存储
        print(f"已启动  localnode:{slef.port}  http  server")
        slef.server = WSGIServer((slef.host,slef.port),application=slef.app,)
        slef.server.serve_forever()

    def run_as_rpc(slef):  #作为rpc server 启动

        requests.get(slef.as_rpc + f"/register?port={slef.port}&name={slef.hostname}")  #请求 注册
        locals = slef.local.get_service()  #本地数据
        print(f"已启动 {slef.host}:{slef.port} rpc server")
        s = zerorpc.Server(locals)   #把本数据注册到服务
        s.bind(f"tcp://{slef.host}:{slef.port}")           #启动
        s.run()


@click.command()
@click.option("-h",'--host', default='0.0.0.0', help='输入ip')
@click.option('-p',"--port",type=int,default=5000 ,help='输入端口号')
@click.option("-a",'--as_rpc',default=None, help='psdash节点来注册这个代理启动。如http://127.0.0.1:5000')
@click.option("-n",'--as_name',default="psdash", help='psdash节点名字')
def main(host,port,as_rpc,as_name):
    run=Runer(**locals())
    if as_rpc:
        run.run_as_rpc()    #启动rpc
    else:
        run.run_as_web()    #启动web

if __name__ == '__main__':
    main()
