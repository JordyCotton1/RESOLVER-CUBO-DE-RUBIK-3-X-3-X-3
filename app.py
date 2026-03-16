from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import kociemba

app = Flask(__name__)

def detectar_color(h,s,v):

    if s < 50 and v > 180:
        return "W"

    if (h <= 7 or h >= 170) and s > 90:
        return "R"

    if 8 <= h <= 35 and s > 80:
        return "O"

    if 23 <= h <= 40 and s > 90:
        return "Y"

    if 41 <= h <= 85:
        return "G"

    if 90 <= h <= 130:
        return "B"

    return "?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():

    data = request.json
    cube = data["cube"]

    try:
        solution = kociemba.solve(cube)
    except:
        return jsonify({"error":"cubo invalido"})

    return jsonify({
        "solution":solution
    })

if __name__ == "__main__":
    app.run()