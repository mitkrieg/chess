// import {Droppable} from '@shopify/draggable';
// import * as http from http;
const d = require('@shopify/draggable')

const url = 'http://127.0.0.1:5000/move'

const draggable = new d.Droppable(document.querySelectorAll('.space'), {
    draggable: '.piece',
    dropzone: '.space'
});

// draggable.on('droppable:dropped', () => console.log('droppable:dropped'))
let promotion = null

function promotionClick() {
    return new Promise((resolve) => {
        document.querySelectorAll('.promotion').forEach(item => {
            item.addEventListener('click', event => {
                console.log(event.target.id);
                promotion = event.target.id;
                if (promotion !== null) {
                    console.log('resolved')
                    resolve();
                }
                
            })
        });
    })
}

async function waitForPromotion(modal,body) {
    console.log(modal)
    let clicked = await promotionClick();
    modal.style.display = 'none'
    body['promotion'] = promotion
    move(body);
}



draggable.on('drag:stop', (evt) => {
    let piece = evt.data.source.id
    let origin = evt.data.sourceContainer.id
    let destination = evt.data.source.parentNode.id
    let body = {
        "origin":origin,
        "destination":destination,
        "piece":piece,
        "promotion":promotion
    };

    document.getElementById(evt.data.source.parentNode.id).classList.remove('draggable-dropzone--occupied');

    
    if (piece.split('-')[1] == 'pawn') {
        if (destination.split('-')[0] == '7' && piece.split('-')[0] == 'black') {
            console.log('in promotionblock')
            let modal = document.getElementById("black-promotion-modal");
            modal.style.display = 'block';
            waitForPromotion(modal,body);
        } else if (destination.split('-')[0] == '0' && piece.split('-')[0] == 'white') {
            console.log('in promotionblock')
            let modal = document.getElementById("white-promotion-modal")
            modal.style.display = 'block'
            waitForPromotion(modal,body);
        } else {
            move(body);
        }
    } else {
        let body = {
            "origin":origin,
            "destination":destination,
            "piece":piece,
            "promotion":promotion
        };
        move(body);
    }
    
    //log
    console.log('Piece: ', piece);
    console.log('Origin: ', origin);
    console.log('Distination: ', destination);
    console.log('Promotion: ', promotion);

    

    

});
// draggable.on('droppable:dropped', (evt) => console.log(evt))

function move(body) {
        //check if movable and move on backend
        fetch(url, {
            "method":'POST',
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify(body)
        }).then(
            response => {
                return response.json();
            }
        ).then(
            body => {
                console.log(body)
                if (body.success == true) {
                    console.log(body.piece + ' moved from '+ body.movement.origin + ' to ' + body.movement.destination)
                    if (body.castle == true) {
                        console.log('castle process');
                        let rook;
                        let rook_dest;
                        if (body.movement.destination == '7-6') {
                            rook = document.getElementById('white-rook-k');
                            console.log(rook);
                            rook_dest = '7-5';
                        } else if (body.movement.destination == '7-2') {
                            rook = document.getElementById('white-rook-q')
                            rook_dest = '7-3';
                        } else if (body.movement.destination == '0-6') {
                            rook = document.getElementById('black-rook-k')
                            rook_dest = '0-5';
                        } else if (body.movement.destination == '0-2') {
                            rook = document.getElementById('black-rook-q')
                            rook_dest = '0-3';
                        } 
    
                        document.getElementById(rook_dest).appendChild(rook)
    
                        console.log(rook + ' moved to ' + rook_dest)
                    }
                    if (body.capture == true) {
                        console.log('CAPTURE: ', body.captured_slug)
                        document.getElementById(body.captured_slug).remove();
                        console.log(body.captured_slug + ' was captured')
                    }
                    if (body.promoted == true) {
                        console.log('PROMOTION: ', body.promotion.piece)
                        let pawn = document.getElementById(body.piece)
                        let new_id = body.promotion.player + '-' + body.promoted.piece + '-' + 'promo'
                        console.log(pawn)
                        pawn.innerHTML = body.promotion.unicode
                        
                    }
                } else {
                    console.log(body.error);
                    console.log(document.getElementById(body.movement.origin))
                    console.log(document.getElementById(body.piece))
                    document.getElementById(body.movement.origin).appendChild(
                        document.getElementById(body.piece)
                    )
                }
            }
        ).catch(
            (e) => {console.log(e)}
        )
}

// Get the modal
var modal = document.getElementById("black-promotion-modal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}