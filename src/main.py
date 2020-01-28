"""
APP DONDE SIMULAMOS TIRADA DE DADOS
DADOS DE 4 6 8 10 CARAS 

"""

import random
import os
import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from flask import session
from ModuloMongodb.ManagerMongodb import managermongo


app = Flask(__name__)
app.secret_key = "gkajsajkaskd"


@app.route("/", methods=["get"])
def home():
    return render_template("index.html")


@app.route("/", methods=["post"])
def recibir_login():
    if "usuario" and "password" in request.form:
        ok = managermongo.comprobarlogin(request.form["usuario"], request.form["password"])
        if ok == True:
            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]

            return redirect(url_for("profile"))

    return redirect(url_for("home"))


@app.route("/profile", methods=["get"])
def profile():
    if "usuario" and "password" in session:
        ok = managermongo.comprobarlogin(session["usuario"], session["password"])

        if ok == False:
            return redirect(url_for("home"))

        return render_template("profile.html")

    return redirect(url_for("home"))


@app.route("/profile", methods=["post"])
def recibir_datos_dados():
    if "dados" in request.form:

        try:
            caras = int(request.form["dados"])
            tiradas = int(request.form["cantidad_tiradas"])
            if tiradas <= 0:
                return redirect(url_for("profile"))

        except ValueError:
            raise Exception("no posible conversion")

        listado = []
        suma = 0
        for i in range(0, tiradas):
            rnd = random.randint(1, caras)
            suma += rnd            
            listado.append(rnd)
            
        elemento = {
            "usuario": session["usuario"],
            "tirada": listado,
            "fecha": datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
            "puntuacion_total": suma
        }
        
        ok, maximo = managermongo.insertarelemento(elemento)

        return render_template("profile.html", datos=elemento, len=len(listado), maximo=maximo)


if __name__ == "__main__":
    # app.run("127.0.0.1", 5000, debug=True)
    env_port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=env_port, debug=True)
