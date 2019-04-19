from flask import Flask, request, jsonify, json
import cypher_app.cyphers as cyphers
from cypher_server.cypher_datto import CypherDatto
from flask_cors import CORS
import socket
map = {
   "%20":" ",
   "%24":"$",
   "%26":"&",
   "%60":"`",
   "%3A":":",
   "%3C":"<",
   "%3E":">",
   "%5B":"[",
   "%5D":"]",
   "%7B":"{",
   "%7D":"}",
   "%22":'"',
   "%2B":"+",
   "%23":"#",
   "%25":"%",
   "%40":"@",
   "%2F":"/",
   "%3B":";",
   "%3D":"=",
   "%3F":"?",
   "%5C" :"\\",
   "%5E" :"^",
   "%7C" :"|",
   "%7E":"~",
   "%27":"'",
   "%2C":","
}

def unEncryptMessage(message=""):
    print(''.join(message))
    deEscaped = message
    for key in map.keys():
        deEscaped = map[key].join(deEscaped.split(key))
    return deEscaped


app = Flask(__name__)
CORS(app)

app.env = "Development"
app.debug = True
# HOST = "cryptickryptonite.tk"
HOST = "69.27.22.220"
PORT = 5000
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
        cypher_name, "encrypt", unEncryptMessage(message), key)
    jsonResponse = jsonify(response)
    jsonResponse.status_code = status_code
    return jsonResponse


@app.route("/<cypher_name>/decrypt/<message>/<key>")
def decrypt_route(cypher_name, message, key):
    status_code, response = generate_message_data(
        cypher_name, "decrypt", unEncryptMessage(message), key)
    jsonResponse = jsonify(response)
    jsonResponse.status_code = status_code
    return jsonResponse


def generate_message_data(cypher_name, method, message, key):
    cypher = get_cypher_from_name(cypher_name)
    response = {"data": {"message": "Cypher Not Found"}, "successful": False}
    status_code = 404
    if(cypher is not None):
        try:
            message = getattr(cypher, method)(unEncryptMessage(message), key)
            response["data"] = message.serialize()
            response["successful"] = True
            status_code = 200
        except AssertionError as e:
            status_code = 500
            response["data"] = {"message": str(e)}
    return (status_code, response)


@app.route("/<cypher_name>/encrypt/", methods=["POST"])
def encrypt_post_route(cypher_name):
    obj = request.json
    (status_code, response) = generate_message_data(
        cypher_name, "encrypt", unEncryptMessage(obj["message"]), obj["key"])
    flask_response = jsonify(response)
    flask_response.status_code = status_code
    return flask_response


@app.route("/<cypher_name>/decrypt/", methods=["POST"])
def decrypt_post_route(cypher_name):
    obj = request.json
    (status_code, response) = generate_message_data(
        cypher_name, "decrypt", unEncryptMessage(obj["message"]), obj["key"])
    flask_response = jsonify(response)
    flask_response.status_code = status_code
    return flask_response


@app.route("/<cypher_name>/encrypt/", methods=["GET"])
def get_cypher_encrypt_info(cypher_name):
    cypher = get_cypher_from_name(cypher_name)
    response = None
    if(cypher is None):
        response = {
            "successful": False,
            "data": {
                "message": "Cypher Not Found"
            }
        }
    else:
        response = {
            "successful": True,
            "data": {
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
        response = {
            "successful": False,
            "data": {
                "message": "Cypher Not Found"
            }
        }
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
            "successful": False,
            "data": {
                "message": "Cypher Not Found"
            }
        }
    return jsonify(result)


def get_cypher_from_name(name):
    cypher_list = list(filter(lambda e: e.name.upper() ==
                              name.upper(), available_cyphers))
    return cypher_list[0] if len(cypher_list) > 0 else None


if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0")
