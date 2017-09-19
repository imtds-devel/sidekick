/////////////////////////////////////////
// JavaScript/Ajax for the quotes module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// The variables for the page
var subTotal = 0; // Will contain the current subtotal (before tax and shipping)
var total = 0; // Will contain the current quote total
var partsCost = 0; // Contains the current subtotal of parts in the quote
var shippingTotal = 0; // Contains the current total of all shipping in the quote
var taxRate = .0925 // !! Contains the sales tax rate, update this when sales tax changes !! - 9.25% as of Fall 2017
var taxPartsCost = 0; // Contains the calculated tax on the part
var addService; // For use with clicking a service

$(document).ready(function() {

    // When the "Reset Quote" button is pressed, 
    $('#reset-button').click(function(){
        $('#quote-items').empty();
        $('#text-quote').empty();
        $('input').val("");
        $('#quote-totals').addClass('hidden-quote');
        subTotal = 0;
        total = 0;
        partsCost = 0;
        shippingTotal = 0;
        taxPartsCost = 0;
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
        
    // When a part is filled in and added
    $('#add-part').click(function(){
        var partName = $('input[name=part-name]').val();

        // First we must ensure the user didn't leave the name blank
        if (partName.length == 0) {
            // If it was blank we make it clear to the user that the field is required
            $('#part-name').addClass('required-field');
        }
        else{
            // We clear the required field class so it looks normal again, hopefully our user has learned
            $('#part-name').removeClass('required-field');
            // Here we make a partID variable that looks like a normal id
            var partID = partName.replace(/\s+/g, '-').toLowerCase() + "-part";

            // Here we check there isn't already a part of the same name
            if (document.querySelector('#' + partID) == null)
                {
                    // Here we get the part and shipping cost from the input fields
                    var partCost = $('input[name=part-price]').val()
                    var shippingCost = parseFloat($('input[name=shipping-price]').val())
        
                    // Here we generate the part visual
                    $('#quote-items').append("<li id='" + partID + "' class='list-group-item quoted-service'>"
                    +"<div class ='media'>"
                        +"<div class ='media-left'>"
                        + "Name: " + "<input type='text' name='" + partID + "-name' value='" + partName + "'><br>"
                        + "Price: " + "<input type='number' name='" + partID + "-price' value='" + partCost + "'><br>"   
                        + "Shipping: " + "<input type='number' name='" + partID + "-shipping' value='" + shippingCost + "'><br>"                                
                        +"<div id = 'service-price' class ='media-body'>"
                        +"</div>"
                        +"</div>"
                        +"<div class ='media-right'>"
                        +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>X</button></div>"            
                    +"</div></li>");
        
                    // Here we recalculate our numbers with the part and shipping cost we grabbed
                    subTotal += parseFloat(partCost); 
                    partsCost += parseFloat(partCost);
                    taxPartsCost = parseFloat(partsCost * taxRate);
                    shippingTotal += parseFloat(shippingCost);
                    total = parseFloat(subTotal + shippingTotal + taxPartsCost);
        
                    // Now we update all feilds of the quote
                    $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                    $('input[name=total]').val("$ " + total.toFixed(2));   
                    $('input[name=shipping]').val("$ " + shippingTotal.toFixed(2));   
                    $('input[name=tax]').val("$ " + taxPartsCost.toFixed(2));   
                    
                    // These make the totals box and the text quote update
                    checkTotalsDisplay();
                    updateTextQuote();
                }
        }
    });
    

    // When a service (non part) is clicked
    addService = function(serviceName, servicePrice, serviceCategory){
        // We use this service id to label the element that we create
        var serviceID = serviceCategory.replace(" ", "-").toLowerCase();

        // If it returns null then the service hasn't been added already 
        if (document.querySelector('#' + serviceID) == null){
            $('#quote-items').append("<li id='" + serviceID + "' class='list-group-item quoted-service'>"
            +"<div class ='media'>"
                +"<div class ='media-left'>"
                + serviceName
                +"<div id = 'service-price' class ='media-body'>"
                + "$" + servicePrice
                +"</div>"
                +"</div>"
                +"<div class ='media-right'>"
                +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>X</button></div>"            
            +"</div></li>");
    
            subTotal += parseFloat(servicePrice);
            total = parseFloat(subTotal + shippingTotal + taxPartsCost);
            $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
            $('input[name=total]').val("$ " + total.toFixed(2));        
    
            checkTotalsDisplay();
            updateTextQuote();
        }
        else
            {
                alert("Sorry, you have already added this service to the quote.")
            }

    };

    // Each service added to the quote has a remove button which triggers this function
    $('#quote-items').on("click", "#remove-button", function(){
        // We pull the id by with the parents of the remove button, !WARNING! messing with the HTML will break this :(
        var id = "#" + $(this).parent().parent().parent().attr('id');

        // We need to handle parts differently
        if (id.includes('-part')){
            var idNoHash = id.slice(1);
            // We grab the part price and shipping cost
            var partPrice = parseFloat($('input[name=' + idNoHash + '-price]').val());
            var shippingCost = parseFloat($('input[name=' + idNoHash + '-shipping]').val());

            // Now we subtract everything 
            subTotal -= partPrice;
            partsCost -= partPrice;
            taxPartsCost = partsCost * taxRate;
            shippingTotal -= shippingCost;            
            total = subTotal + shippingTotal + taxPartsCost;

            // If the subtotal is now 0, we want to clear the fields
            if (subTotal == 0){
                $('#quote-items').empty();
                $('#text-quote').empty();
                $('input').val("");
                }
            // Else, we just update the value 
            else {
                $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                $('input[name=total]').val("$ " + total.toFixed(2));
                $('input[name=shipping]').val("$ " + shippingTotal.toFixed(2));
                $('input[name=tax]').val("$ " + taxPartsCost.toFixed(2));                
                $(id).remove();                
                }            
            }
        // If it is just a service, not a part
        else{
            // A lot happens here, but it allows us to pull the price as a float to a variable :)
            var servicePrice = parseFloat($(id).find('#service-price').text().slice(1));
            // Now we subtract the removed item from our total and refresh the totals display
            subTotal -= servicePrice;
            total = subTotal + shippingTotal + taxPartsCost;

            // If the subtotal is now 0, we want to clear the fields
            if (subTotal == 0){
                $('#quote-items').empty();
                $('#text-quote').empty();
                $('input').val("");
                }
            // Else, we just update the value 
            else {
                $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                $('input[name=total]').val("$ " + total.toFixed(2));   
                $(id).remove();
                }
        }
    })

    // This function will check if quote totals should be visible, and makes it visible
    function checkTotalsDisplay(){
        // Checks if quote totals card doesn't exist, if it doesn't we make it
        if ($('#quote-totals').hasClass('hidden-quote'))
            {
                $('#quote-totals').removeClass('hidden-quote');
            }
    }

    // This function will make a formatted text quote everytime there is a change 
    // It does this with a 
    function updateTextQuote(){
        var quoteText = "";
        if (true){

        }
    }
});