/////////////////////////////////////////
// JavaScript/Ajax for the quotes module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// The variables for the page
var subTotal = 0; // Will contain the current subtotal (before tax and shipping)
var total = 0; // Will contain the current quote total
var partsCost = 0; // Contains the current subtotal of parts in the quote
var shippingCost = 0; // Contains the current total of all shipping in the quote
var taxRate = .0925 // !! Contains the sales tax rate, update this when sales tax changes !! - 9.25% as of Fall 2017
var taxPartCost = 0; // Contains the calculated tax on the part
var addService; // For use with clicking a service
$(document).ready(function() {
    // When the "Reset Quotes" button is pressed, 
    $('#reset-button').click(function(){
        $('#quote-items').empty();
        $('#text-quote').empty();
        $('input').val("");
        subTotal = 0;
        total = 0;
        partsCost = 0;
        shippingCost = 0;
        taxPartCost = 0;
    })

    // When the "Copy Quote to Clipboard" button is pressed 
    $('#clipboard-button').click(function(){
        // Select the text in the quote        
        document.querySelector('#text-quote').select();        
        // The copy is in a try because some browsers do not support the feature to copy this way
        // There are potentially other reasons why it wouldn't work, but usually it will be a browser issue
        try {
            document.execCommand('copy');
        } catch (err) {
            alert("Sorry, your browser does not support this feature!")
        }
    });
        
    // When a service (non part) is clicked
    addService = function(serviceName, servicePrice, serviceCategory){
        // We use this service id to label the element that we create
        var serviceID = serviceName.replace(" ", "-").toLowerCase();

        // If it returns null
        if (document.querySelector('#' + serviceID) == null){
            $('#quote-items').append("<li id='" + serviceID + "' class='list-group-item quoted-service'>"
            +"<div class ='media'>"
                +"<div class ='media-body'>"
                +serviceName + " $" + servicePrice
                +"</div>"
                +"<div class ='media-right'>"
                +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>X</button></div>"            
            +"</div></li>");
            
            // Adds the selected quote as text
            $('#text-quote').append(serviceName);
    
            subTotal += parseFloat(servicePrice);
            total = subTotal + shippingCost + taxPartCost;
    
            $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
            $('input[name=total]').val("$ " + total.toFixed(2));        
    
            checkTotalsDisplay();
        }
        else
            {
                alert("Sorry, you have already added this service to the quote.")
            }

    };

    // Each service added to the quote has a remove button which triggers this function
    $('#quote-items').on("click", "#remove-button", function(){
        var id = $(this).parent().parent().parent().attr('id');
        $('#' + id).remove();
    })

    // This function will generate the card for displaying totals if it doesn't exist
    checkTotalsDisplay = function(){
        // Checks if quote totals card doesn't exist, if it doesn't we make it
        if (document.querySelector('#quote-totals') == null)
            {
            }
    }
});