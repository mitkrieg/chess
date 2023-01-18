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
    
    try:
        piece = body.get('piece')
        origin = body.get('origin')
        origin_list = [int(x) for x in origin.split('-')]
        dest = body.get('destination')
        dest_list = [int(x) for x in dest.split('-')]
        print('Piece: ',piece)
        print('Origin: ',origin)
        print('Requested Destination: ',dest)
        capture = game.grid[origin_list[0]][origin_list[1]].move((dest_list[0],dest_list[1]),game)
        print('Captured: ', capture)
        if issubclass(type(capture),Piece):
            return jsonify({
                "success":True, 
                'capture':True,
                'piece':piece,
                'captured_slug':capture.slug,
                'movement':{
                    'origin':origin,
                    'destination':dest
                }
            })
        else:
            return jsonify({
                "success":True, 
                'capture':False,
                'piece':piece,
                'movement':{
                    'origin':origin,
                    'destination':dest
                }
            })
    except Exception as e:
        print(e)
        return jsonify({
            "success":False,
            "error":str(e),
            'piece':piece,
            'movement':{'origin':origin}
        })