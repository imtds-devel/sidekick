/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// The variables for the page
var subTotal = 0; // Will contain the current subtotal (before tax and shipping)
var total = 0; // Will contain the current quote total
var partsCost = 0; // Contains the current subtotal of parts in the quote
var shippingTotal = 0; // Contains the current total of all shipping in the quote
var taxRate = 0.095; // !! Contains the sales tax rate, update this when sales tax changes !! - 9.5% as of Fall 2017
var taxPartsCost = 0; // Contains the calculated tax on the part
var addService; // For use with clicking a service
var addDiscount; // For use with clicking a discount

$(document).ready(function () {

    // When the "Reset Quote" button is pressed, 
    $('#reset-button').click(function () {
        $('#quote-items').empty();
        $('#text-quote').empty();
        $('input').val("");
        $('#quote-totals').addClass('hidden-quote');
        subTotal = 0;
        total = 0;
        partsCost = 0;
        shippingTotal = 0;
        taxPartsCost = 0;
    });

    // When the "Copy Quote to Clipboard" button is pressed 
    $('#clipboard-button').click(function () {
        // Select the text in the quote        
        document.querySelector('#text-quote').select();        
        // The copy is in a try because some browsers do not support the feature to copy this way
        // There are potentially other reasons why it wouldn't work, but usually it will be a browser issue
        try {
            document.execCommand('copy');
        } catch (err) {
            alert("Sorry, your browser does not support this feature! " + err);
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
            var partID = (partName.replace(/\s+/g, '-').toLowerCase() + "-part");

            // Here we check there isn't already a part of the same name
            if (document.querySelector('#' + partID) == null)
                {
                    // Here we get the part and shipping cost from the input fields
                    // If the fields are left empty or the user didn't enter a number we
                    // make them 0
                    var partCost = parseFloat($('input[name=part-price]').val());
                    if (isNaN(partCost)){
                        partCost = 0;
                    }
                    var shippingCost = parseFloat($('input[name=shipping-price]').val());
                    if (isNaN(shippingCost)){
                        shippingCost = 0;
                    }
        
                    // Here we generate the part visual
                    $('#quote-items').append("<li id='" + partID + "' class='list-group-item quoted-part'>"
                    +"<div class ='media'>"
                        +"<div class ='media-body'>"
                        +"<div class = 'input-group'>"
                        +"<span class='input-group-prepend'><i class='glyphicon glyphicon-wrench'></i></span>"
                        +"<input id='part-name' type='text' readonly class='form-control input-sm'"
                        +"placeholder='Part Name' value=" + partName +  " name='" + partID + "-name'></div>"
                        +"<div class = 'input-group'>"
                        +"<span class='input-group-prepend'><i class='glyphicon glyphicon-usd'></i></span>"
                        +"<input id='part-price' type='number' readonly class='form-control input-sm'"
                        +"placeholder='Part Price' value=" + partCost + " name='" + partID +"-price'></div>"   
                        +"<div class = 'input-group'>"
                        +"<span class='input-group-prepend'><i class='glyphicon glyphicon-envelope'></i></span>"
                        +"<input id='shipping-price' type='number' readonly class='form-control input-sm'" 
                        +"placeholder='Shipping Cost' value=" + shippingCost + " name='" + partID + "-shipping'></div>"                            
                        +"</div>"
                        +"<div class ='media-right'>"
                        +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>"
                        +"<i class='glyphicon glyphicon-trash'></i></button></div>"            
                    +"</div></li>");
        
                    // Here we recalculate our numbers with the part and shipping cost we grabbed
                    subTotal += parseFloat(partCost); 
                    partsCost += parseFloat(partCost);
                    taxPartsCost = parseFloat(partsCost * taxRate);
                    shippingTotal += parseFloat(shippingCost);
                    total = parseFloat(subTotal + shippingTotal + taxPartsCost);
        
                    // Now we update all totals fields of the visual quote
                    $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                    $('input[name=total]').val("$ " + total.toFixed(2));   
                    $('input[name=shipping]').val("$ " + shippingTotal.toFixed(2));   
                    $('input[name=tax]').val("$ " + taxPartsCost.toFixed(2));   
                    
                    // Finally, we make the totals visible and display the text
                    checkTotalsDisplay();
                    updateTextQuote();
                }
        }
    });
    
    // When a service (non part) is clicked
    addService = function(serviceName, servicePrice, serviceCategory){
        // We use this service id to label the element that we create
        var serviceID = serviceName.replace(/ /g, "-").toLowerCase();

        // We handle adding backup and labor a litte differently because we want to replace
        // differing sized services (ex. Small to Medium)
        if (serviceID.includes('backup') && document.querySelector("[id*=backup]") != null){
            // We get the id of the service that we want to remove (that matches the type of thing we are adding)
            var removedServiceID = $("[id*=backup]").attr('id');
            // A lot happens here, but it allows us to pull the price as a float to a variable :)
            var removedServicePrice = parseFloat($('#' + removedServiceID).find('#service-price').text().slice(1));
            // Now we subtract the removed item from our total and refresh the totals display
            subTotal -= removedServicePrice;
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
                $('#' + removedServiceID).remove();
                }
        }
        if (serviceID.includes('labor') && document.querySelector('[id*=labor]') != null){
            // We get the id of the service that we want to remove (that matches the type of thing we are adding)
            var removedServiceID = $("[id*=labor]").attr('id');         
            // A lot happens here, but it allows us to pull the price as a float to a variable :)
            var removedServicePrice = parseFloat($('#' + removedServiceID).find('#service-price').text().slice(1));
            // Now we subtract the removed item from our total and refresh the totals display
            subTotal -= removedServicePrice;
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
                $('#' + removedServiceID).remove();
                }
        }

        // If this returns null then the service hasn't been added already 
        if (document.querySelector('#' + serviceID) == null){
            $('#quote-items').append("<li id='" + serviceID + "' class='list-group-item quoted-service'>"
            +"<div class ='media'>"
                +"<div id= 'service-name' class ='media-body'>"
                +serviceName
                +"</div>"
                +"<div class ='media-right'>"
                +"<div id ='service-price'>"
                +"$" + servicePrice
                +"</div>"
                +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>"
                +"<i class='glyphicon glyphicon-trash'></i></button></div>"
                +"</div></li>");
    
            subTotal += parseFloat(servicePrice);
            total = parseFloat(subTotal + shippingTotal + taxPartsCost);
            $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
            $('input[name=total]').val("$ " + total.toFixed(2));
            }

            // Check these functions out at the bottom of this js :)
            checkTotalsDisplay();
            updateTextQuote();
    };

    // When a service (non part) is clicked
    addDiscount = function(discountName, discountAmount){
        // We use this discount id to label the element that we create
        var serviceID = discountName.replace(/ /g, "-").toLowerCase() + "-discount";

        // If this returns null then the service hasn't been added already 
        if (document.querySelector('#' + serviceID) == null){
            $('#quote-items').append("<li id='" + serviceID + "' class='list-group-item quoted-discount'>"
            +"<div class ='media'>"
                +"<div id= 'discount-name' class ='media-body'>"
                +discountName
                +"</div>"
                +"<div class ='media-right'>"
                +"<div id ='discount-amount'>"
                +"-$" + discountAmount
                +"</div>"
                +"<button id ='remove-button' type='button' class='btn btn-danger remove-button'>"
                +"<i class='glyphicon glyphicon-trash'></i></button></div>"
                +"</div></li>");
    
            subTotal -= parseFloat(discountAmount);
            total = parseFloat(subTotal + shippingTotal + taxPartsCost);
            $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
            $('input[name=total]').val("$ " + total.toFixed(2));
            }

            // Check these functions out at the bottom of this js :)
            checkTotalsDisplay();
            updateTextQuote();
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
            if (isNaN(partPrice)){
                partPrice = 0;
            }
            var shippingCost = parseFloat($('input[name=' + idNoHash + '-shipping]').val());
            if (isNaN(partPrice)){
                partPrice = 0;
            }

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
                $('#quote-totals').addClass('hidden-quote');                
                }
            // Else, we just update the value 
            else {
                $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                $('input[name=total]').val("$ " + total.toFixed(2));
                $('input[name=shipping]').val("$ " + shippingTotal.toFixed(2));
                $('input[name=tax]').val("$ " + taxPartsCost.toFixed(2));                
                $(id).remove();
                updateTextQuote();                
                }            
            }

        // If it is a discount we also need to handle it differently
        else if (id.includes('-discount')){
            // A lot happens here, but it allows us to pull the discount as a float to a variable :)
            var discountAmount = parseFloat($(id).find('#discount-amount').text().slice(2));

            subTotal += discountAmount;
            total = subTotal + shippingTotal + taxPartsCost;

            // If the subtotal is now 0, we want to clear the fields
            if (subTotal == 0){
                $('#quote-items').empty();
                $('#text-quote').empty();
                $('input').val("");
                $('#quote-totals').addClass('hidden-quote');                
                }
            // Else, we just update the value 
            else {
                $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                $('input[name=total]').val("$ " + total.toFixed(2));   
                $(id).remove();
                updateTextQuote();                
                }
            
        }
                

        // If it is just a service, not a part or discount
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
                $('#quote-totals').addClass('hidden-quote');                
                }
            // Else, we just update the value 
            else {
                $('input[name=subtotal]').val("$ " + subTotal.toFixed(2));
                $('input[name=total]').val("$ " + total.toFixed(2));   
                $(id).remove();
                updateTextQuote();                
                }
        }
    })

    // This function will check if quote totals should be visible, and makes it visible
    function checkTotalsDisplay(){
        // Checks if quote totals card doesn't exist, if it doesn't we make it appear
        if ($('#quote-totals').hasClass('hidden-quote'))
            {
                $('#quote-totals').removeClass('hidden-quote');
            }
    }

    // This function will make a formatted text quote everytime there is a change (must call the method)
    function updateTextQuote(){
        var quoteText = "";
        // The power of jquery allows us to loop through each quoted-service and pass the id into a 
        // method that generates text from it
        $('.quoted-service').each(function() {
            quoteText += pullServiceText($(this).attr('id'));
        });
        // Same for discounts
        $('.quoted-discount').each(function() {
            quoteText += pullDiscountText($(this).attr('id'));
        });
        // Same goes for parts, jquery magic
        $('.quoted-part').each(function() {
            quoteText += pullPartText($(this).attr('id'));
        });
        // Now we pull the text we want with labeled elements of the service items
        function pullServiceText(serviceID){
            var text = "";
            text += $('#' + serviceID).find('#service-name').text() + ": ";
            text += $('#' + serviceID).find('#service-price').text() + "\n";
            return text;
        }
        // For discounts, we print it differently
        function pullDiscountText(serviceID){
            var text = "";
            text += $('#' + serviceID).find('#discount-name').text() + " Discount: ";
            text += $('#' + serviceID).find('#discount-amount').text() + "\n";
            return text;
        }
        // For parts, we pull the values of corresponding input fields
        function pullPartText(partID){
            var text = "";
            text += $('input[name=' + partID + '-name]').val() + ": " ;
            text += "$" + $('input[name=' + partID + '-price]').val() + "\n";
            return text;
        }

        // Here we check if there is any shipping or tax in the quote, then add that to the text quote
        if (shippingTotal != 0)
        {
            quoteText += "Shipping: $" +  shippingTotal.toFixed(2) + "\n";
        }
        if (taxPartsCost != 0)
        {
            quoteText += "Tax: $" + taxPartsCost.toFixed(2) + "\n";
        }

        quoteText += "**Total: $" + total.toFixed(2) + "**";
        $('#text-quote').text(quoteText);
        
    }
});