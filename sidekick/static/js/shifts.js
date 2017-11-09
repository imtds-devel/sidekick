/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////

$(document).ready(function() {
    // This triggers when the user clicks the post button, mostly dev fiddling right now
    $('#post-cover-btn').click(function(){
        $('#post-det').hide();        
        $('#posting-progress').addClass('loader');
        setTimeout(function(){
            $('#posting-progress').removeClass('loader');            
            $('#post-conf').modal('toggle');
        }, 2000);
    });
    // This triggers when the user selects a new date in the date selector
    $('#date').change(function(){
        console.log("Sent")
        // Retreive the date that the user selected
        var date = $(this).val();
            // Make an AJAX call with the date selected
            $.ajax({
                url: 'ajax/filter_shifts/',
                data: {
                  'date': date
                },
                dataType: 'json',
                // With the retreived date, we will populate the panels
                success: function (data) {
                    console.log(data);
                    console.log("Received")
                    generateShiftPanels(data.shifts);
                    //console.log(data.shifts);
                }
            });
    });
    function generateShiftPanels(shifts){
        $('#your-shifts-panel-group').empty();
        for (i = 0; i < shifts.length; i++) {
            $('#your-shifts-panel-group').append(            
            "<div class = 'panel panel-primary shift-panel'>" +
                "<div class = 'panel-heading'>" + shifts[i].title + "</div>" +
                "<div class = 'panel-body'>" +
                        "<button type = 'button' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#shift-id' >Marshburn: 10AM - 2PM</button>" +
                        "<button type = 'button' class = 'btn btn-block shift-btn'>Marshburn: 9PM - 1AM</button>" + 
                "</div>" +
            "</div>");
        }
        console.log("Panels")
    }
});    