"""
LIVE RELOAD

"""

import logging
from os import getcwd, path
from formic import FileSet
from livereload import Server, shell
from flask import Flask

STATIC_FOLDER = "."


##### routes
app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            static_url_path="")


@app.route("/")
def root():
    return app.send_static_file("index.html")

#####################


#### servidor #################

def make_livereload_server(wsgi_app):
    server = Server(wsgi_app)

    watch_patterns = (
        "/src/**",
        "/static/**"
    )

    build_cmd = "make"

    print ("Files being monitored:")

    cwd = getcwd()

    for pattern in watch_patterns:
        print ("Pattern: {0}".format(pattern))
        for filepath in FileSet(include=pattern):
            print ("=>".format(path.relpath(filepath, cwd)))
            server.watch(filepath, build_cmd)
        print

    return server


def main():
    flask_wsgi_app = app.wsgi_app
    server = make_livereload_server(flask_wsgi_app)
    server.serve()


if __name__ == "__main__":
    main()
