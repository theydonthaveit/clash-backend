"""
Quart Server for backend to server template changes
to the Neo4j docker instance
"""
import json

from quart import Quart, request, send_from_directory
from quart_cors import cors

from database import access_correct_function_to_engage_with_db

app = Quart(
    __name__,
    static_folder='static')
app = cors(app)


@app.route('/riot', methods=['GET'])
async def riot(path):
    """
    Specific end point for riot
    """
    return send_from_directory(
        app.static_folder,
        'riot.txt')


@app.route('/', methods=['POST'])
async def hello():
    """
    An async call serving POST requests from the frontend
    Each request handled is sent to Neo4j for possible modifications
    rtype -> None
    """
    if request.method == 'POST':
        data = await request.get_data()
        res = json.loads(data)


if __name__ == '__main__':
    app.run(debug=True,
            port=4000,
            host='0.0.0.0')
