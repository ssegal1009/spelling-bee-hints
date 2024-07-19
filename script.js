/**
 * Author: Sofia Segal
 * Version: 7.18.24
 */


/**
 * The getHint1 function performs the following steps:

Retrieves the value from an input field with the ID bee.
Sends this value to the server using an AJAX POST request to the /get_hint endpoint.
If the request is successful, it updates the text content of an HTML element with the ID hint to display the hint returned by the server.
 */

function getHint1() {
    const bee = $('#bee').val(); //selects HTML element w the ID bee and gets its current value (the text input)
    $.ajax({ //initiates AJAX (Asynchronous JavaScript and XML), which allows you to send/receive data from a server async w/out refreshing the web page
        url: '/get_hint', //specifies the URL to which the AJAX req will be sent. an endpoint on my app.py server
        method: 'POST', //HTTP method, post the hint
        contentType: 'application/json', //means that the data being sent to the server is in JSON format
        data: JSON.stringify({ bee: bee }), //specifying what data to send -- stringify convers JSON to a JSON string. uses the 'bee' key w the value that was retrieved from the input (text input) field earlier. this JSON STRING is sent in the body of the post
        success: function(response) {//defines a callback function to be executed if the AJAX req succeeds. 'response' parameter represents the data returned from the server, aka the hint.
            $('#hint').text(response.hint);//$('#hint'): Uses jQuery to select the HTML element with the ID hint.
            //.text(response.hint) sets the text content of the selected element, the hint, to the value of response.hint. this assumes that the server (app.py)'s response is a JSON object that contains a hint key. this actually updates the HTML to display the hint.
        }
    });
}
function getHint2() {
    const bee = $('#bee').val();
    $.ajax({
        url: '/get_compound',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ bee: bee }),
        success: function(response) {
            $('#hint').text(response.hint);
        }
    });
}
function getHint3() {
    const bee = $('#bee').val();
    $.ajax({
        url: '/get_letterCount',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ bee: bee }),
        success: function(response) {
            $('#hint').text(response.hint);
        }
    });
}
