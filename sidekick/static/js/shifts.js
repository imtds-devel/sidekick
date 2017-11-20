/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// Variables for the page
weekDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] // Week days in order

$(document).ready(function() {
    // On page load we want to load the correct shifts and update the display
    ajaxWithDate('curr');

    function ajaxWithDate(option){
        console.log("Sent")
        // Retreive the date that the user selected
        var date = $('#your-shift-date').val();
        console.log(date);
            // Make an AJAX call with the date selected
        $.ajax({
            url: 'ajax/filter_shifts/',
            data: {
                'date': date,
                'option' : option
            },
            dataType: 'json',
            // With the retreived date, we will populate the panels
            success: function (data) {
                if (data.date.slice(0,10) != date) {
                    $('#your-shift-date').val(data.date.slice(0,10));
                }
                console.log(data)
                console.log("Received")
                $('#your-week').text(data.week[0].slice(5,10) + ' to ' + data.week[6].slice(5,10));                                        
                generateShiftPanels(data.week, data.shifts);
            }
        });
    }

    // This triggers when the user clicks the post button, fiddling right now
    $('#post-cover-btn').click(function(){
        $('#post-det').hide();        
        $('#posting-progress').addClass('loader');
        setTimeout(function(){
            $('#posting-progress').removeClass('loader');            
            $('#post-conf').modal('toggle');
        }, 2000);
    });
    // This triggers when the user selects a new date in the date selector
    $('#your-shift-date').change(function(){
        var option = 'curr';
        ajaxWithDate(option);
    });
    // When the user clicks the previous shift button
    $('#your-week-previous').click(function(){
        var option = 'prev';
        ajaxWithDate(option);
    });
    // When the user clicks the next shift button
    $('#your-week-next').click(function(){
        var option = 'next';
        ajaxWithDate(option);
    });
    function generateShiftPanels(week, shifts){
        $('#your-shifts-panel-group').empty();
        $('#shift-modals').empty();
        // Loop through the days in the given week
        for (day = 0; day < week.length; day++){
            // Evaluate if we should be displaying this day
            // Hint: We should only display a day if there are shifts on that day
            if (isShiftOnDay(week[day], shifts)) {
                $('#your-shifts-panel-group').append(            
                    "<div class = 'panel panel-primary shift-panel' id= '" + weekDays[day] + "-shifts' >" +
                        "<div class = 'panel-heading'>" + weekDays[day] + " " +  week[day].slice(5,10) + "</div>" + // Here we are displaying the week day and the date of that day
                        "<div class = 'panel-body'><div>" + // This is where the individual shifts will go
                    "</div>");
                // Generate a new group of shifts that only contains the one on this day
                shiftsDay = shiftsOnDay(week[day], shifts);
                // Loop through those shifts
                for (shift = 0; shift < shiftsDay.length; shift++)
                {
                    // Generate a shift "button" for each shift
                    $('#' + weekDays[day] + '-shifts .panel-body').append(
                        "<button type = 'button' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#" + shiftsDay[shift].id + "' >" + shiftsDay[shift].title + "</button>"                    
                    )
                    $('#shift-modals').append(
                        "<div id = '" + shiftsDay[shift].id + "' class = 'modal fade'>"
                        + "<div class='modal-dialog modal-lg'>"
                        +    "<div class='modal-content'>"
                        +        "<div class='modal-header'>"
                        +            shiftsDay[shift].title
                        +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                        +            "<h4 class='modal-title'></h4>"
                        +        "</div>"
                        +        "<div class='modal-body hero-bio'>"
                        +            "<div class='hero-bio'>"
                        +                "<button type = 'button' class = 'btn btn-default' data-dismiss = 'modal' data-toggle= 'modal' data-target = '#post-conf-" + String(shiftsDay[shift].id) + "'>Post Cover</button>"
                        +            "</div>"
                        +        "</div>"
                        +        "<div class='modal-footer'>"
                        +            "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
                        +        "</div>"
                        +    "</div>"
                        +"</div>"
                    +"</div>"
                    )
                    $('#shift-modals').append(
                        "<div id = 'post-conf-" + String(shiftsDay[shift].id) + "' class = 'modal fade'>"
                        +"<div class='modal-dialog modal-sm'>"
                        +   "<div class='modal-content'>"
                        +       "<div class='modal-header'>"
                        +       shiftsDay[shift].title
                        +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + shiftsDay[shift].id + "'>&times;</button>"
                        +       "<h4 class='modal-title'></h4>"
                        +   "</div>"
                        +   "<div class='modal-body'>"
                        +       "<div id='posting-progress'></div>"
                        +       "<div id='post-det'>"
                        +           "<p>Post Cover for " + shiftsDay[shift].owner + " at Marshburn: 10AM - 2PM?</p>"
                        +              "<button id= 'post-cover-btn' type= 'button' class= 'btn btn-primary'>Post</button>"
                        +              "<button type='button' class='btn btn-default' data-toggle = 'modal' data-target = '#" + shiftsDay[shift].id + "' data-dismiss='modal'>Cancel</button>"
                        +          "</div>"
                        +      "</div>"
                        +      "</div>"
                        +   "</div>"
                        +"</div>"
                    )                        
                }
            }
        }
        console.log("Panels")
    }
    // This function evaulates if there is atleast 1 shift on the given date
    // Give it a day and some formatted shifts.
    function isShiftOnDay(day, shifts) {
        // Loop through the shifts given
        for (shift = 0; shift < shifts.length; shift++) {
            if (shifts[shift].shift_date == day.slice(0,10))
                return true; // If we found a shift on that date 
        }
        // If we looked through the shifts but found nothing 
        return false
    }
    // This function evaulates a group of shifts and returns those shifts that are on the given day
    // Don't call this function if there aren't shifts on the day (if you do it returns an empty set)
    function shiftsOnDay(day, shifts) {
        // create an empty set of shifts
        shiftsDay = []
        // Loop through the shifts
        for (shift = 0; shift < shifts.length; shift++) {
            if (shifts[shift].shift_date == day.slice(0,10)) // If there is a shift on that date
                shiftsDay.push(shifts[shift]) // pushes that shift to the new set we made
        }
        return shiftsDay; // Return the shifts found on that day 
    }
});    