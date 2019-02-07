from flask import Flask, request, jsonify
import cypher_app.cyphers as cyphers
from cypher_server.cypher_datto import CypherDatto
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


@app.route("/")
def primary_get_routes():
    return jsonify({
        "data":
        [e.serialize() for e in available_cyphers],
        "successful": True
    })


@app.route("/<cypher_name>/encrypt/<message>/<key>")
def encrypt_route(cypher_name, message, key):
    status_code, response = generateMessageData(
        cypher_name, "encrypt", message, key)
    json = jsonify(response)
    json.status_code = status_code
    return json


@app.route("/<cypher_name>/decrypt/<message>/<key>")
def decrypt_route(cypher_name, message, key):
    status_code, response = generateMessageData(
        cypher_name, "decrypt", message, key)
    json = jsonify(response)
    json.status_code = status_code
    return json


def generateMessageData(cypher_name, method, message, key):
    cypher = getCypherFromName(cypher_name)
    response = {"data": None, "successful": False}
    status_code = 404
    if(cypher is not None):
        try:

            message = getattr(cypher, method)(message, key)
            response["data"] = message.serialize()
            response["successful"] = True
            status_code = 200
        except AssertionError as e:
            status_code = 500
    return (status_code, response)


@app.route("/<cypher_name>/encrypt/", methods=["POST"])
def encrypt_post_route(cypher_name):
    pass


@app.route("/<cypher_name>/decrypt", methods=["POST"])
def decrypt_post_route(cypher_name):
    pass


@app.route("/<cypher_name>/encrypt")
def getCypherEncryptInfo(cypher_name):
    cypher = getCypherFromName(cypher_name)
    response = None
    if(cypher is None):
        response = {"successful": True, "data": None}
    else:
        response = {"successful": True, "data": {
            "encryptUrl": "%s/encrypt/<message>/<key>" % (cypher.url),
            "messageTemplate": "<message>",
            "keyTemplate": "<key>"
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
            "messageTemplate": "<message>",
            "keyTemplate": "<key>"
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
    cypher_list = list(filter(lambda e: e.name.upper() ==
                              name.upper(), available_cyphers))
    return cypher_list[0] if len(cypher_list) > 0 else None


if __name__ == "__main__":
    app.run(port=PORT, host=HOST)
