$(function() {
    $("#Icon1").draggable({
        grid: [80, 80]
    });
});
$(function() {
    $("#Icon2").draggable({
        grid: [80, 80]
    });
});

$("#Icon1").dblclick(function() {
    $('#ComWin').removeClass('hidden');
});

$("#ClsBtn").click(function() {
    $('#ComWin').addClass('hidden');
});

$("#Icon2").dblclick(function() {
    $('#NoteWin').removeClass('hidden');
});

$("#ClsBtn1").click(function() {
    $('#NoteWin').addClass('hidden');
});

$("#Icon3").dblclick(function() {
    $('#ProgressWin').removeClass('hidden');
});

$("#ClsBtn2").click(function() {
    $('#ProgressWin').addClass('hidden');
});

$(function() {
    $("#ComWin").draggable({
        handle: "#ctrlbar"
    });
});

$(function() {
    $("#NoteWin").draggable({
        handle: "#ctrlbar2"
    });
});

Materialize.toast('Double click sur l\'icone pour ouvrir', 2000)

$(document).ready(function() {
    $('input#input_text, textarea#textarea1').characterCounter();
});
$(document).ready(function() {
    $('input#input_text, textarea#textarea2').characterCounter();
});

$(document).ready(function() {
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();
});

function FNA() {
    Materialize.toast('Function not available', 2000)
}