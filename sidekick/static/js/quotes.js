var addService;
$(document).ready(function() {
    // When the "Reset Quotes" button is pressed, 
    $('#reset-button').click(function(){
        $('#quote-items').empty();
        $('#text-quote').empty();
    })

    // When the "Copy Quote to Clipboard" button is pressed 
    $('#clipboard-button').click(function(){
        // Select the text in the quote        
        document.querySelector('#text-quote').select();        
        // The copy is in a try because some browsers do not support the feature to copy this way
        try {
            document.execCommand('copy');
        } catch (err) {
            alert("Sorry, your browser does not support this feature!")
        }
    });
        
    // When a service is clicked
    addService = function(serviceName, servicePrice){

        // Adds the selected quote as a button
        $('#quote-items').append("<button type='button' class='btn btn-block service-btn'>"
        +"<div class ='media'>"
           +"<div class ='media-left'>"
            +serviceName
            +"</div>"
            +"<div class ='media-center'>"
            +"$" + servicePrice
            +"</div>"
            +"<div class ='media-right'>"
            +"<button id ='remove-service' type='button' class='btn btn-danger'>X</button></div>"
        +"</div>"
    +"</button>");
        
        // Adds the selected quote as text
        $('#text-quote').append(serviceName);
    };
});