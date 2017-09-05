$(document).ready(function() {
    // When the "Reset Quotes" button is pressed, 
    $('#reset-button').click(function(){
        $('#quote-items').empty();
        $('#text-quote').empty();
    })

    // When the "Copy Quote to Clipboard" button is pressed 
    // #TODO - FIX 
    $('#clipboard-button').click(function(){
        // Select the text in the quote        
        document.querySelector('#text-quote').querySelectorAll('p').select();
        document.execCommand('copy');
        
        // The copy is in a try because some browsers do not support the feature to copy this way
        try {
            document.execCommand('copy');
        } catch (err) {
            alert("Sorry, your browser does not support this feature!")
        }
    });
    // When a service is clicked
    $('#service').click(function(){

        // Adds the selected quote as a button
        $('#quote-items').append("<button id='service' type='button' class='btn btn-block service-btn'>"
        +"<div class ='media'>"
           +"<div class ='media-left'>"
            +"{{service.service}}"
            +"</div>"
            +"<div class ='media-body'>"
            +"{{service.description}}"
            +"</div>"
            +"<div class ='media-right'>"
            +"${{service.price}}"
            +"</div>"
        +"</div>"
    +"</button>");
        
        // Adds the selected quote as text
        $('#text-quote').append($("<p></p>").text("Quote Item $100"));
    });
});