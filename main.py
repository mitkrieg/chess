from flask import Flask, render_template,request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def main(name=None):
    return render_template('page_layout.html',name=name)

@app.route('/move', methods=["POST"])
def make_move():
    print('It worked!')
    body = request.get_json()
    # print(body)
    print('Piece: ',body.get('piece'))
    print('Origin: ',body.get('origin'))
    print('Destination: ',body.get('destination'))
    return jsonify({"success":'true'})