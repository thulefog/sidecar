 
""" 
REST Endpoint - rudimentary sidecar seed.
"""

import os
import io

from flask import Flask, request, abort, jsonify, send_from_directory, send_file

UPLOAD_DIRECTORY = "./STORAGE_AREA"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

@app.route("/inventory")
def inventory_files():
    """This is an endpoint to generate a list of files as an inventory of what is on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/query")
def query_data_source():
    key = request.args.get('key') #if key doesn't exist, returns None

    data_source = key+".json"
    """This function enables the client to retrieve a file, storing it as a binary stream (octet-stream)."""
    path = os.path.join(UPLOAD_DIRECTORY, data_source)
    print(path)
    with open(path, 'rb') as bytes:
        return send_file(
            io.BytesIO(bytes.read()),
            attachment_filename=key,
            mimetype='application/octet-stream' )


@app.route("/retrieve/<filename>")
def retrieve_file(filename):

    """This function enables the client to retrieve a file, storing it as a binary stream (octet-stream)."""
    path = os.path.join(UPLOAD_DIRECTORY, filename)
    print(path)
    with open(path, 'rb') as bytes:
        return send_file(
            io.BytesIO(bytes.read()),
            attachment_filename=filename,
            mimetype='application/octet-stream' )

@app.route("/store/<filename>", methods=["POST"])
def store_file(filename):
    """Upload a file and store in the upload directory storage location."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)
    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    #app.run(debug=True, port=9000)
    app.run(host='127.0.0.1', port=8080, debug=True)