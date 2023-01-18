// import {Droppable} from '@shopify/draggable';
// import * as http from http;
const d = require('@shopify/draggable')

const url = 'http://127.0.0.1:5000/move'

const draggable = new d.Droppable(document.querySelectorAll('.space'), {
    draggable: '.piece',
    dropzone: '.space'
});

// draggable.on('droppable:dropped', () => console.log('droppable:dropped'))
// draggable.on('droppable:stop', () => console.log('droppable:returned'))
// draggable.on('droppable:start', () => console.log('droppable:start'))

// draggable.on('drag:start', (evt) => console.log(evt))
// draggable.on('drag:move', (evt) => console.log(evt))
// let movedPiece 
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
            console.log(body.capture)
            if (body.capture == true) {
                console.log(body.slug)
                document.getElementById(body.slug).remove()
            }

        }
    )
});
// draggable.on('droppable:dropped', (evt) => console.log(evt))


