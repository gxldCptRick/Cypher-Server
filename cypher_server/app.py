from flask import Flask
from flask import jsonify
import cypher_app.cyphers as cyphers
from cypher_datto import CypherDatto
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.env = "Development"
app.debug = True
HOST = "localhost"
PORT = 5000
URL_TEMPLATE = "http://%s:%s/%s"

available_cyphers = [CypherDatto(e, URL_TEMPLATE % (
    HOST, PORT, e.name)) for e in cyphers.cyphers]


@app.route("/<cypher_name>/encrypt/<message>/<key>")
def encrypt_route(cypher_name, message, key):
    pass


@app.route("/<cypher_name>/decrypt/<message>/<key>")
def decrypt_route(cypher_name, message, key):
    pass


@app.route("/")
def primary_get_routes():
    return jsonify({
        "data":
        [e.serialize() for e in available_cyphers],
        "successful": True
    })


@app.route("/<cypher_name>/encrypt")
def getCypherEncryptInfo(cypher_name):
    cypher = getCypherFromName(cypher_name)
    response = None
    if(cypher is None):
        response = {"successful": True, "data": None}
    else:
        response = {"successful": True, "data": {
            "encryptUrl": "%s/encrypt/<message>/<key>" % (cypher.url),
            "encryptDescription": "You must pass in the message and the message append to this route in order to get the response"
        }}
    return jsonify(response)


@app.route("/<cypher_name>/decrypt")
def getCypherDecryptInfo(cypher_name):
    cypher = getCypherFromName(cypher_name)
    response = None
    if(cypher is None):
        response = {"successful": True, "data": None}
    else:
        response = {"successful": True, "data": {
            "decryptUrl": "%s/encrypt/<message>/<key>" % (cypher.url),
            "decryptDescription": "You must pass in the message and the message append to this route in order to get the response"
        }}
    return jsonify(response)


@app.route("/<cypher_name>")
def get_cypher(cypher_name):
    cypher = getCypherFromName(cypher_name)
    result = None
    if(cypher is not None):
        result = {
            "data": {
                "decryptUrl": "%s/decrypt" % cypher.url,
                "encryptUrl": "%s/encrypt" % cypher.url,
            },
            "successful": True
        }
    else:
        result = {
            "data": None,
            "successful": False
        }
    return jsonify(result)


def getCypherFromName(name):
    cypher_list = list(filter(lambda e: e.name == name, available_cyphers))
    return cypher_list[0] if len(cypher_list) > 0 else None


if __name__ == "__main__":
    app.run(port=PORT, host=HOST)
