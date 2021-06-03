from flask import Blueprint,current_app,request



web = Blueprint('psdash', __name__)



@web.route("/register")
def register():
    nodes=request.remote_addr + ":" + request.args["port"]
    if nodes not in current_app.psdash.nodes:
        current_app.psdash.register_agent(nodes)
    return ""

@web.route("/nodes")
def nodes():
    return str(current_app.psdash.nodes)