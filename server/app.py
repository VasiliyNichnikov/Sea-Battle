from flask import Flask
from api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route('/')
def test():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5002)