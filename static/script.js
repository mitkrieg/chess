// import {Draggable} from '@shopify/draggable'
const d = require('@shopify/draggable')

const draggable = new d.Droppable(document.querySelectorAll('.space'), {
    draggable: '.piece',
    dropzone: '.space'
});

