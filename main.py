from flask import Flask, render_template,request, jsonify
# import json
from board import Board
from pieces import Piece
#import pieces

app = Flask(__name__)

game = Board()

@app.route("/")
def main(name=None):
    print('it worked')
    return render_template('page_layout.html',name=name)

@app.route('/move', methods=["POST"])
def make_move():
    # print('It worked!')
    body = request.get_json()
    
    piece = body.get('piece')
    origin = [int(x) for x in body.get('origin').split('-')]
    dest = [int(x) for x in body.get('destination').split('-')]
    print('Piece: ',piece)
    print('Origin: ',origin)
    print('Requested Destination: ',dest)
    capture = game.grid[origin[0]][origin[1]].move((dest[0],dest[1]),game)
    print('Captured: ', capture)
    if issubclass(type(capture),Piece):
        return jsonify({
            "success":True, 
            'capture':True,
            'piece':capture.name,
            'slug':capture.slug
        })
    else:
        return jsonify({"success":'true','capture':'false'})