from flask import Flask
from flask import jsonify
import cypher_app.cyphers as cyphers
from cypher_datto import CypherDatto
app = Flask(__name__)
app.env = "Development"
app.debug = True
HOST = "localhost"
PORT = 5000
URL_TEMPLATE = "https://%s:%s/%s"

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
    return jsonify(available_cyphers)


@app.route("/<cypher_name>")
def get_cypher(cypher_name):
    pass


if __name__ == "__main__":
    app.run(port=PORT, host=HOST)
