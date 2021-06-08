from flask import Blueprint,current_app,request,jsonify



web = Blueprint('psdash', __name__)



@web.route("/<string:hostname>/<string:kind>")
def memory(hostname,kind):

    current_service=current_app.psdash.node[hostname].get_service()

    if kind=="memory":
        return jsonify(current_service.memory())
    elif kind=="disks":
        s=""
        for i in current_service.get_disks():
            s+=str(i)+"<br />"
        return  s
    elif kind == "cpu":
        return str(current_service.get_cpu())
    elif kind == "pids":
        s=""
        for i in current_service.get_pid():
            s+=str(i)+"<br />"
        return  s


@web.route("/register")
def register():
    nodes=request.remote_addr + ":" + request.args["port"]
    if nodes not in current_app.psdash.nodes:
        current_app.psdash.register_agent(nodes,request.args["name"])
    return ""

@web.route("/nodes")
def nodes():
    a=[]
    for node in  current_app.psdash.nodes:
        node=node.split(":")
        a.append({"hostname":node[0],"host":node[1],"port":int(node[2])})
    return str(a)
