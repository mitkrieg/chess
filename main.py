from flask import Flask, render_template,request, jsonify
# import json
from board import Board
from pieces import *
import sys

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
        promo = body.get('promotion')
        origin = body.get('origin')
        player = piece.split('-')[0]
        origin_list = [int(x) for x in origin.split('-')]
        dest = body.get('destination')
        dest_list = [int(x) for x in dest.split('-')]
        print('Piece: ',piece)
        print('Origin: ',origin)
        print('Requested Destination: ',dest)
        if piece.split('-')[1] == 'pawn':
            if promo:
                print('promo if')
                match promo.split('-')[1] :
                    case 'rook':
                        promo_class = Rook
                        if player == 'white':
                            unicode = '&#9814;'
                        else:
                            unicode = '&#9820;'
                    case 'knight':
                        promo_class = Knight
                        if player == 'white':
                            unicode = '&#9816;'
                        else:
                            unicode = '&#9822;'
                    case 'queen':
                        promo_class = Queen
                        if player == 'white':
                            unicode = '&#9813;'
                        else:
                            unicode = '&#9819;'
                    case 'bishop':
                        promo_class = Bishop
                        if player == 'white':
                            unicode = '&#9815;'
                        else:
                            unicode = '&#9821;'
                    case _:
                        promo_class=None
            else:
                promo_class = None
            capture, promotion = game.grid[origin_list[0]][origin_list[1]].move((dest_list[0],dest_list[1]), game, promotion=promo_class)
        else:
            print('other if')
            capture = game.grid[origin_list[0]][origin_list[1]].move((dest_list[0],dest_list[1]),game)
            promotion = None
        print('Captured: ', capture)
        if issubclass(type(capture),Piece):
            if promotion is None:
                return jsonify({
                    "success":True, 
                    'capture':True,
                    'castle':False,
                    'promoted':False,
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
                    'capture':True,
                    'castle':False,
                    'promoted':True,
                    'promotion':{
                        'piece':promo,
                        'player':player,
                        'unicode':unicode
                    },
                    'piece':piece,
                    'captured_slug':capture.slug,
                    'movement':{
                        'origin':origin,
                        'destination':dest
                    }
                })
        elif capture == 'castle':
            return jsonify({
                "success":True, 
                'capture':False,
                'castle':True,
                'piece':piece,
                'promoted':False,
                'movement':{
                    'origin':origin,
                    'destination':dest,
                }
            })
        else:
            if promotion is None:
                return jsonify({
                    "success":True, 
                    'capture':False,
                    'castle':False,
                    'piece':piece,
                    'promoted':False,
                    'movement':{
                        'origin':origin,
                        'destination':dest
                    }
                })
            else:
               return jsonify({
                    "success":True, 
                    'capture':False,
                    'castle':False,
                    'piece':piece,
                    'movement':{
                        'origin':origin,
                        'destination':dest
                    },
                    'promoted':True,
                    'promotion':{
                        'piece':promo,
                        'player':player,
                        'unicode':unicode
                    },
                }) 
    except Exception as e:
        print(e)
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        print(f'Occured at {lineno}')
        return jsonify({
            "success":False,
            "error":str(e),
            'piece':piece,
            'movement':{'origin':origin}
        })