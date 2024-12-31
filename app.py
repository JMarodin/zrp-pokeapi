from flask import Flask, render_template
from flask.globals import request
import requests
import json
from model.pokemon import Pokemon

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", foto="https://www.formulatv.com/images/series/posters/1100/1106/dest_1.jpg")

@app.route("/buscar", methods=['GET',"POST"])
def buscar():
    pokemon = Pokemon(request.form['nome'].lower(),"","","")
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.nome}").text)
        habilidades = [ability["ability"]["name"].upper() for ability in res["abilities"]]
        habilidades.sort()
        pokemon.habilidades=habilidades
        tipos = [ability["type"]["name"].upper() for ability in res["types"]]
        pokemon.tipos=tipos
        result = res['sprites']
        result = result['front_default']
        pokemon.foto = res['sprites']['front_default']
    except:
        return "Nome incorreto"
    return render_template("index.html", foto=pokemon.foto, nome=pokemon.nome.upper(), tipos=pokemon.tipos, habilidades=pokemon.habilidades)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
