from flask import Flask, request, jsonify, json
import cypher_app.cyphers as cyphers
from cypher_server.cypher_datto import CypherDatto
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.env = "Development"
app.debug = True
HOST = "cryptickryptonite.tk"
PORT = 80
URL_TEMPLATE = "http://%s:%s/%s/"

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
    status_code, response = generate_message_data(
        cypher_name, "encrypt", message, key)
    jsonResponse = jsonify(response)
    jsonResponse.status_code = status_code
    return jsonResponse


@app.route("/<cypher_name>/decrypt/<message>/<key>")
def decrypt_route(cypher_name, message, key):
    status_code, response = generate_message_data(
        cypher_name, "decrypt", message, key)
    jsonResponse = jsonify(response)
    jsonResponse.status_code = status_code
    return jsonResponse


def generate_message_data(cypher_name, method, message, key):
    cypher = get_cypher_from_name(cypher_name)
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
    obj = request.json
    (status_code, response) = generate_message_data(
        cypher_name, "encrypt", obj["message"], obj["key"])
    flask_response = jsonify(response)
    flask_response.status_code = status_code
    return flask_response


@app.route("/<cypher_name>/decrypt/", methods=["POST"])
def decrypt_post_route(cypher_name):
    obj = request.json
    (status_code, response) = generate_message_data(
        cypher_name, "decrypt", obj["message"], obj["key"])
    flask_response = jsonify(response)
    flask_response.status_code = status_code
    return flask_response


@app.route("/<cypher_name>/encrypt/", methods=["GET"])
def get_cypher_encrypt_info(cypher_name):
    cypher = get_cypher_from_name(cypher_name)
    response = None
    if(cypher is None):
        response = {"successful": True, "data": None}
    else:
        response = {"successful": True, "data": {
            "encryptUrl": "%sencrypt/<message>/<key>" % (cypher.url),
            "messageTemplate": "<message>",
            "keyTemplate": "<key>"
        }}
    return jsonify(response)


@app.route("/<cypher_name>/decrypt/", methods=["GET"])
def get_cypher_decrypt_info(cypher_name):
    cypher = get_cypher_from_name(cypher_name)
    response = None
    if(cypher is None):
        response = {"successful": True, "data": None}
    else:
        response = {"successful": True, "data": {
            "decryptUrl": "%sdecrypt/<message>/<key>" % (cypher.url),
            "messageTemplate": "<message>",
            "keyTemplate": "<key>"
        }}
    return jsonify(response)


@app.route("/<cypher_name>/")
def get_cypher(cypher_name):
    cypher = get_cypher_from_name(cypher_name)
    result = None
    if(cypher is not None):
        result = {
            "data": {
                "decryptUrl": "%sdecrypt/" % cypher.url,
                "encryptUrl": "%sencrypt/" % cypher.url,
            },
            "successful": True
        }
    else:
        result = {
            "data": None,
            "successful": False
        }
    return jsonify(result)


def get_cypher_from_name(name):
    cypher_list = list(filter(lambda e: e.name.upper() ==
                              name.upper(), available_cyphers))
    return cypher_list[0] if len(cypher_list) > 0 else None


if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0")
