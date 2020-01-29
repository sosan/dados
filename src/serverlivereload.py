"""
LIVE RELOAD

"""

import logging
from os import getcwd, path
# from formic import FileSet
from livereload import Server, shell
from flask import Flask

STATIC_FOLDER = "."


##### routes
# app = Flask(__name__,
#             static_folder=STATIC_FOLDER,
#             static_url_path="")


app = Flask(__name__, instance_relative_config=True)


# @app.route("/")
# def root():
#     return app.send_static_file("index.html")


@app.route('/')
def index():
    return render_template("index.html")

#####################


#### servidor #################



if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
