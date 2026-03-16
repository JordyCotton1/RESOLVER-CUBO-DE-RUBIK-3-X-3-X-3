from flask import Flask, render_template, request, jsonify
import kociemba

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():

    cube = request.json["cube"]

    try:
        solution = kociemba.solve(cube)
    except:
        return jsonify({"error":"Cubo inválido"})

    return jsonify({"solution":solution})

if __name__ == "__main__":
    app.run()