/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// Variables for the page
var weekDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] // Week days in order
var locations = {
    ma: "Marshburn",
    da: "Darling",
    st: "Stamps",
    sd: "Support Desk",
    sr: "Support Rep",
    rc: "Repair Center",
    md: "MoD Desk",
    ss: "SST",
    sf: "Staff"
}

$(document).ready(function() {
    // On page load we want to load the correct shifts to update the display
    ajaxUserShifts('curr');
    ajaxOpenShifts('curr');
    
    // This function sends an ajax request to django which responds with data
    function ajaxUserShifts(option){
        console.log("Sent")
        // Retreive the date that the user selected
        var date = $('#your-shift-date').val();
        console.log(date);
            // Make an AJAX call with the date selected
        $.ajax({
            url: 'ajax/filter_user_shifts/',
            data: {
                'date' : date,
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
                generateUserShiftPanels(data.week, data.shifts);
            }
        });
    }

    // This function sends an ajax request for open shifts for a given position
    function ajaxOpenShifts(option){
        var date = $('#open-shift-date').val();
        var location = $('#open-shift-location').val();
        $.ajax({
            url : 'ajax/filter_open_shifts/',
            data: {
                'date' : date,
                'location' : location,
                'option' : option
            },
            dataType: 'json',

            success: function (data) {
                if (data.date.slice(0,10) != date) {
                    $('#open-shift-date').val(data.date.slice(0,10));
                }
                $('#open-week').text(data.week[0].slice(5,10) + ' to ' + data.week[6].slice(5,10));                                        
                generateOpenShiftPanels(data.week, data.shifts);
            }
        })
    }

    function ajaxRelativeShifts(shiftID) {
        $.ajax({
            url: 'ajax/filter_near_shifts/',
            data: {
                'shiftID' : shiftID
            },
            dataType: 'json',
            success: function (data) {
                console.log("Relative Shifts:");
                console.log(data);
                generateRelativeShifts(shiftID, data)
            }
        })
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
        ajaxUserShifts(option);
    });
    // When the user clicks the previous shift button
    $('#your-week-previous').click(function(){
        var option = 'prev';
        ajaxUserShifts(option);
    });
    // When the user clicks the next shift button
    $('#your-week-next').click(function(){
        var option = 'next';
        ajaxUserShifts(option);
    });

    // This triggers when the user selects a new date in the date selector
    $('#open-shift-date').change(function(){
        var option = 'curr';
        ajaxOpenShifts(option);
    });
    // This triggers when the user selects a new date in the date selector
    $('#open-shift-location').change(function(){
        var option = 'curr';
        ajaxOpenShifts(option);
    });
    // When the user clicks the previous shift button for open shif
    $('#open-week-previous').click(function(){
        var option = 'prev';
        ajaxOpenShifts(option);
    });
    // When the user clicks the next shift button
    $('#open-week-next').click(function(){
        var option = 'next';
        ajaxOpenShifts(option);
    });

    // When an individual shift is selected
    $(document).on('click', '.shift-btn', function() {
        // Grab the id of that shift
        shiftID = $(this).attr('id');
        // Call the function to generate the relative shifts
        ajaxRelativeShifts(shiftID);
    });

    // This function #TODO this function 
    function generateRelativeShifts(shiftID, shiftData){
        // We fill in the modal
        $('#' + String(shiftID) + '-modal').find('#shift-details').text(locations[shiftData.thisShift.location] + ": " + formatTimeRange(shiftData.thisShift.shift_start, shiftData.thisShift.shift_end));
        if (shiftData.thisShift.is_open) {
            $('#' + String(shiftID) + '-modal').find('#cover-details-1').text("Shift cover posted by " + String(shiftData.shiftCover.poster) + " on " + String(shiftData.shiftCover.post_date))
            $('#' + String(shiftID) + '-modal').find('#cover-details-2').text("Sob story: " + shiftData.shiftCover.sobstory) 
        }
    }
    // This function is called by the AJAX function, it fills in the shifts on the page
    function generateUserShiftPanels(week, shifts){
        // First we remove the current shifts 
        $('#your-shifts-panel-group').empty();
        $('#user-shift-modals').empty();
        // Loop through the days in the given week
        for (day = 0; day < week.length; day++){
            // Evaluate if we should be displaying this day
            // Hint: We should only display a day if there are shifts on that day
            if (isShiftOnDay(week[day], shifts)) {
                // If there are shifts we start by adding the "days" in the week that have a shift on them
                $('#your-shifts-panel-group').append(            
                    "<div class = 'panel panel-primary shift-panel' id= '" + weekDays[day] + "-shifts' >" +
                        "<div class = 'panel-heading'>" + weekDays[day] + " " +  week[day].slice(5,10) + "</div>" + // Here we are displaying the week day and the date of that day
                        "<div class = 'panel-body'><div>" + // This is where the individual shifts will go
                    "</div>");
                // Generate a new group of shifts that only contains the one on this day
                shiftsDay = shiftsOnDay(week[day], shifts);
                // Loop through those shifts and add the individual shifts
                for (shift = 0; shift < shiftsDay.length; shift++)
                {
                    // Generate a shift "button" for each shift
                    $('#' + weekDays[day] + '-shifts .panel-body').append( // Select the body of the current day we are looping through
                        "<button type = 'button' id = '" + shiftsDay[shift].id  + "' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#"
                        + String(shiftsDay[shift].id) + "-modal' >" + locations[shiftsDay[shift].location] // This line labels the modal we will make and the location of the shift
                        + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end) // This line lays out the time range of the shift using a handy method
                        +"</button>"                    
                    )
                    // Generate a modal for each shift
                    $('#user-shift-modals').append(
                        "<div id = '" + String(shiftsDay[shift].id) + "-modal' class = 'modal fade'>"
                        + "<div class='modal-dialog modal-lg'>"
                        +    "<div class='modal-content'>"
                        +        "<div class='modal-header'>"
                        +            shiftsDay[shift].title // The title of the shift becomes the title of the modal
                        +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                        +            "<h4 class='modal-title'></h4>"
                        +        "</div>"
                        +        "<div class='modal-body'>"
                        +            "<div class='shift-body'>"
                        +                "<p>[Not Final Design]</p>" // #TODO final design
                        +                "<p id = shift-details></p>" // We will fill this when we actually click a modal
                        +                "<button disabled type = 'button' class = 'btn btn-default' data-dismiss = 'modal' data-toggle= 'modal' data-target = '#post-conf-" + String(shiftsDay[shift].id) + "'>Post Cover</button>"
                        +            "</div>"
                        +        "</div>"
                        +        "<div class='modal-footer'>"
                        +            "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
                        +        "</div>"
                        +    "</div>"
                        +"</div>"
                    +"</div>"
                    )
                    // These modals are the modals that actually handle posting and taking details 
                    // This is very much in progress 
                    $('#user-shift-modals').append(
                        "<div id = 'post-conf-" + String(shiftsDay[shift].id) + "' class = 'modal fade'>"
                        +"<div class='modal-dialog modal-sm'>"
                        +   "<div class='modal-content'>"
                        +       "<div class='modal-header'>"
                        +       shiftsDay[shift].title // Once again the title is the title of the shift 
                        +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].id) + "-modal'>&times;</button>"
                        +       "<h4 class='modal-title'></h4>"
                        +   "</div>"
                        +   "<div class='modal-body'>"
                        +       "<div id='relative-calender'></div>"
                        +       "<div id='post-det'>"
                        +           "<p>Post Cover for " + shiftsDay[shift].owner + " at " + locations[shiftsDay[shift].location] + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end) +"?</p>"
                        +              "<button id= 'post-cover-btn' type= 'button' class= 'btn btn-primary'>Post</button>"
                        +              "<button type='button' class='btn btn-default' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].id) + "-modal' data-dismiss='modal'>Cancel</button>"
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
    // Like the other method with some small differences for open shifts
    function generateOpenShiftPanels(week, shifts){
        // First we empty the old stuff
        $('#open-shifts-panel-group').empty();
        $('#open-shift-modals').empty();
        // Loop through the days in the given week
        for (day = 0; day < week.length; day++){
            // Evaluate if we should be displaying this day
            // Hint: We should only display a day if there are shifts on that day
            if (isShiftOnDay(week[day], shifts)) {
                $('#open-shifts-panel-group').append(            
                    "<div class = 'panel panel-warning shift-panel' id= '" + weekDays[day] + "-open-shifts' >" +
                        "<div class = 'panel-heading'>" + weekDays[day] + " " +  week[day].slice(5,10) + "</div>" + // Here we are displaying the week day and the date of that day
                        "<div class = 'panel-body'><div>" + // This is where the individual shifts will go
                    "</div>");
                // Generate a new group of shifts that only contains the one on this day
                shiftsDay = shiftsOnDay(week[day], shifts);
                // Loop through those shifts
                for (shift = 0; shift < shiftsDay.length; shift++)
                {
                    // Generate a shift "button" for each shift
                    $('#' + weekDays[day] + '-open-shifts .panel-body').append(
                        "<button type = 'button' id = '" + shiftsDay[shift].id  + "' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#"
                        + String(shiftsDay[shift].id) + "-modal' >" + locations[shiftsDay[shift].location] 
                        + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end)
                        +"</button>"                    
                    )
                    // Generate a modal for each shift, this displays some information for the shift
                    $('#open-shift-modals').append(
                        "<div id = '" + String(shiftsDay[shift].id) + "-modal' class = 'modal fade'>"
                        + "<div class='modal-dialog modal-lg'>"
                        +    "<div class='modal-content'>"
                        +        "<div class='modal-header'>"
                        +            shiftsDay[shift].title
                        +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                        +            "<h4 class='modal-title'></h4>"
                        +        "</div>"
                        +        "<div class='modal-body'>"
                        +            "<div class='shift-body'>"
                        +                "<p>[Not Final Design]</p>"                        
                        +                "<p id = shift-details></p>" // Once again we will fill this when the shift is clicked
                        +                "<p id = cover-details-1></p>" // Open shifts have extra cover details that are filled on click     
                        +                "<p id = cover-details-2></p>"                                    
                        +                "<button disabled type = 'button' class = 'btn btn-default' data-dismiss = 'modal' data-toggle= 'modal' data-target = '#post-conf-" + String(shiftsDay[shift].id) + "'>Take Shift</button>"
                        +            "</div>"
                        +        "</div>"
                        +        "<div class='modal-footer'>"
                        +            "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
                        +        "</div>"
                        +    "</div>"
                        +"</div>"
                    +"</div>"
                    )
                    // These secondary modals are for confirming the shift posting
                    $('#open-shift-modals').append(
                        "<div id = 'post-conf-" + String(shiftsDay[shift].id) + "' class = 'modal fade'>"
                        +"<div class='modal-dialog modal-sm'>"
                        +   "<div class='modal-content'>"
                        +       "<div class='modal-header'>"
                        +       shiftsDay[shift].title
                        +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].id) + "-modal'>&times;</button>"
                        +       "<h4 class='modal-title'></h4>"
                        +   "</div>"
                        +   "<div class='modal-body'>"
                        +       "<div id='post-det'>"
                        +           "<p>Take Cover for " + shiftsDay[shift].owner + " at " + locations[shiftsDay[shift].location] + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end) + "?</p>"
                        +              "<button id= 'post-cover-btn' type= 'button' class= 'btn btn-primary'>Post</button>"
                        +              "<button type='button' class='btn btn-default' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].id) + "-modal' data-dismiss='modal'>Cancel</button>"
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
    // This function returns a formatted string with the start and end times
    function formatTimeRange(shiftStart, shiftEnd) {
        // Slice out just the time
        var startTime = shiftStart.slice(11, 16);
        var endTime = shiftEnd.slice(11, 16);
        
        // Parse out the "hours"
        var sTimeNum = parseInt(startTime.slice(0,2));
        var eTimeNum = parseInt(endTime.slice(0,2));

        // If noon or later
        if (sTimeNum > 11)
        {
            // If just noon then add PM
            if (sTimeNum == 12)
                startTime += "PM"
            // Else calculate the time and then add PM
            else
            {
                sTimeNum -= 12
                startTime = startTime.slice(2,5)
                startTime = String(sTimeNum) + startTime + "PM"
            }
        }
        // If it is before noon then just add AM
        else if (sTimeNum == 0)
        {
            sTimeNum = 12
            startTime = startTime.slice(2,5)
            startTime = String(sTimeNum) + startTime + "AM"
        }
        else
        {
            startTime += "AM"
        }

        // Now do the same thing for the ending time 
        if (eTimeNum > 11)
        {
            if (eTimeNum == 12)
                endTime += "PM"
            else
            {
                eTimeNum -= 12
                endTime = endTime.slice(2,5)
                endTime = String(eTimeNum) + endTime + "PM"
            }
        }
        else if (eTimeNum == 0)
        {
            eTimeNum = 12
            endTime = endTime.slice(2,5)
            endTime = String(eTimeNum) + endTime + "AM"
        }
        else
        {
            endTime += "AM"
        }

        // Format the time range and return it
        time = startTime + ' - ' + endTime
        return time
    }
});    