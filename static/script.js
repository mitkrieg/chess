// import {Droppable} from '@shopify/draggable';
// import * as http from http;
const d = require('@shopify/draggable')

const url = 'http://127.0.0.1:5000/move'

const draggable = new d.Droppable(document.querySelectorAll('.space'), {
    draggable: '.piece',
    dropzone: '.space'
});

// draggable.on('droppable:dropped', () => console.log('droppable:dropped'))

draggable.on('drag:stop', (evt) => {
    console.log('Piece: ',evt.data.source.id);
    console.log('Origin: ', evt.data.sourceContainer.id);
    console.log('Distination: ', evt.data.source.parentNode.id);
    document.getElementById(evt.data.source.parentNode.id).classList.remove('draggable-dropzone--occupied')
    fetch(url, {
        "method":'POST',
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify({
            "origin":evt.data.sourceContainer.id,
            "destination":evt.data.source.parentNode.id,
            "piece":evt.data.source.id
        })
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
                    document.getElementById(body.captured_slug).remove();
                    console.log(body.captured_slug + ' was captured')
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
});
// draggable.on('droppable:dropped', (evt) => console.log(evt))


// Get the modal
var modal = document.getElementById("myModal");

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