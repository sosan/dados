"""
APP DONDE SIMULAMOS TIRADA DE DADOS
DADOS DE 4 6 8 10 CARAS 

"""

import random
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

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
        for i in range(0, tiradas):
            rnd = random.randint(1, caras)
            listado.append(rnd)

        return render_template("profile.html", datos=listado, len=len(listado))


        # if request.form["dados"] == "4":
            
        #     pass
        # elif request.form["dados"] == "6":
        #     pass
        
        # elif request.form["dados"] == "8":
        #     pass
        # if request.form["dados"] == "10":
        #     pass
        
        
    
    


        

if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=env_port)   
