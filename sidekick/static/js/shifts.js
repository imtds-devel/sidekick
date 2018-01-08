/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// Variables for the page
var weekDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]; // Week days in order
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
};

$(document).ready(function() {
    // On page load we want to load the correct shifts to update the display
    ajaxUserShifts('curr');
    ajaxOpenShifts('curr');
    // This function sends an ajax request to django which responds with data
    function ajaxUserShifts(option){
        console.log("Sent");
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
                console.log(data);
                console.log("Received");
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
        });
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
                generateRelativeShifts(shiftID, data);
            }
        });
    }

    function ajaxPostCover(data) {
        $.ajax({
            type:"POST",
            url: 'ajax/post_cover/',
            data: data,
            dataType: 'json',
            success : function (data) {
                console.log("POSTED YES IT POSTED YES");
		console.log(data);
                alert("Your cover has been posted! Don't forget: you are still responsible for it until it's taken.");
                $('.modal').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                ajaxUserShifts('curr');
                ajaxOpenShifts('curr');
            }
        });
    }

    function ajaxTakeCover(data) {
        $.ajax({
            type:"POST",
            url: 'ajax/take_cover/',
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log("TAKEN YES IT TOOK YES");
		console.log(data);
                alert("You've taken the cover successfully!");
                $('.modal').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                ajaxUserShifts('curr');
                ajaxOpenShifts('curr');
            }
        });
    }

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
    // When the user clicks the previous shift button for open shift
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

    // When the user selects "yes" for full cover
    $(document).on('change', '.full-cover', function() {
        // Fetch the id of the post-conf modal
        modalID = $(this).closest('.modal').attr('id');
        // Hide the partial selectors and enable the post button
        $('#' + modalID).find('.partial-selectors').hide('fast');
        $('#' + modalID).find('#post-cover-btn').prop('disabled', false);
        $("#" + modalID).find(".modal-footer > p").remove();
    });

    // When the user selects "no" for full cover
    $(document).on('change', '.partial-cover', function() {
        // Fetch the id of the post-conf modal
        modalID = $(this).closest('.modal').attr('id');
        // Hide the partial selectors and enable the post button
        $('#' + modalID).find('.partial-selectors').show('fast');
        $('#' + modalID).find('#post-cover-btn').prop('disabled', true); // Temporarily disabled until I code this
        $("#" + modalID).find(".modal-footer").append("<p style='text-align:center'>(psst, partial covers aren't supported yet, sorry!)</p>");
    });

    // When the user selects "yes" for full take
    $(document).on('change', '.full-take', function() {
        // Fetch the id of the post-conf modal
        modalID = $(this).closest('.modal').attr('id');
        // Hide the partial selectors and enable the post button
        $('#' + modalID).find('.partial-selectors').hide('fast');
        $('#' + modalID).find('#take-cover-btn').prop('disabled', false);
    });

    // When the user selects "no" for full cover
    $(document).on('change', '.partial-take', function() {
        // Fetch the id of the post-conf modal
        modalID = $(this).closest('.modal').attr('id');
        // Hide the partial selectors and enable the post button
        $('#' + modalID).find('.partial-selectors').show('fast');
        $('#' + modalID).find('#take-cover-btn').prop('disabled', true); // Temporarily disabled until I code this
    });

    // When the user clicks "post"
    $(document).on('click', '#post-cover-btn', function() {
        console.log("Post cover triggered");
        modalID = $(this).closest('.modal').attr('id');
        $('#' + modalID).find('#post-cover-btn').prop('disabled', true);
        $("#" + modalID).find(".modal-footer").append("<p style='text-align:center'>Posting Cover now</p>");
        var modalID = $(this).closest('.modal').attr('id');
        var eventID = modalID.slice(10); // Cuts the 'post-conf' off
        var isPerm = $('#' + modalID).find('.perm-cover').prop('checked');
        var permID;
        if (isPerm) {
            permID = eventID.slice(0, eventID.indexOf("_")); // Cuts the _ off the end
        }
        else {
            permID = eventID;
        }

        var isPartial = $('#' + modalID).find('.partial-cover').prop('checked');
        var part_start, part_end;
        if (isPartial) {
            part_start = $('#' + modalID).find('.partial-start').val();
            part_end = $('#' + modalID).find('.partial-end').val();
        }
        else {
            part_start = 'None';
            part_end = 'None';
        }

        var sobStory = $('#' + modalID).find('#sob-story').val();
        var data = {
            'event_id' : eventID,
            'permanent' : isPerm,
            'permanent_id' : permID,
            'partial' : isPartial,
            'part_start' : part_start,
            'part_end' : part_end,
            'sob_story' : sobStory
        };
        ajaxPostCover(data);
    });
    // When the user clicks "take"
    $(document).on('click', '#take-cover-btn', function(evt) {
        console.log("take shift");
        modalID = $(this).closest('.modal').attr('id');
        $('#' + modalID).find('#take-cover-btn').prop('disabled', true);
        $("#" + modalID).find(".modal-footer").append("<p style='text-align:center'>Taking cover now</p>");
        modalID = $(this).closest('.modal').attr('id');
        eventID = modalID.slice(10); // Cuts the 'post-conf' off
        isPerm = $('#' + modalID).find('.perm-cover').prop('checked');
        var permID;
        if (isPerm) {
            permID = eventID.slice(0, eventID.indexOf("_")); // Cuts the _ off the end
        }
        else {
            permID = eventID;
        }

        var isPartial = $('#' + modalID).find('.partial-cover').prop('checked');
        var part_start, part_end;
        if (isPartial) {
            part_start = $('#' + modalID).find('.partial-start').val();
            part_end = $('#' + modalID).find('.partial-end').val();
        }
        else {
            part_start = 'None';
            part_end = 'None';
        }

        var sobStory = $('#' + modalID).find('#sob-story').text();
        console.log($('#' + modalID).find('.perm-cover').prop('checked'));
        var data = {
            'event_id' : eventID,
            'permanent' : isPerm,
            'permanent_id' : permID,
            'partial' : isPartial,
            'part_start' : part_start,
            'part_end' : part_end,
            'sob_story' : sobStory
        };
        ajaxTakeCover(data);
    });

    //TODO: This function
    function generateRelativeShifts(shiftID, shiftData){
        // We fill in the modal
        $('#' + String(shiftID) + '-modal').find('#shift-details').text(locations[shiftData.thisShift.location] + ": " + formatTimeRange(shiftData.thisShift.shift_start, shiftData.thisShift.shift_end));
        if (shiftData.thisShift.is_open) {
            $('#' + String(shiftID) + '-modal').find('#cover-details-1').text("Shift cover posted by " + String(shiftData.shiftCover.poster));
            $('#' + String(shiftID) + '-modal').find('#cover-details-2').text("Sob story: " + shiftData.shiftCover.sobstory);
        }
    }
    // This function is called by the AJAX function, it fills in the shifts on the page
    function generateUserShiftPanels(week, shifts){
        // First we remove the current shifts
        $('#your-shifts-panel-group').empty();
        $('#user-shift-modals').empty();
        // Loop through the days in the given week
        for (var day = 0; day < week.length; day++){
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
                    if (shiftsDay[shift].is_open) { // If this shift is currently open, we want that to be apparent to the user
                        $('#' + weekDays[day] + '-shifts .panel-body').append( // Select the body of the current day we are looping through
                            "<button type = 'button' id = '" + shiftsDay[shift].event_id  + "' class = 'btn btn-block btn-warning shift-btn' data-toggle= 'modal' data-target= '#"
                            + String(shiftsDay[shift].event_id) + "-modal' >" + locations[shiftsDay[shift].location] // This line labels the modal we will make and the location of the shift
                            + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end) // This line lays out the time range of the shift using a handy method
                            +"</button>"
                        )
                        // Generate a modal for each shift, this displays some information for the shift
                        $('#user-shift-modals').append(
                            "<div id = '" + String(shiftsDay[shift].event_id) + "-modal' class = 'modal fade'>"
                            + "<div class='modal-dialog modal-lg'>"
                            +    "<div class='modal-content'>"
                            +        "<div class='modal-header'>"
                            +            shiftsDay[shift].title
                            +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                            +            "<h4 class='modal-title'></h4>"
                            +        "</div>"
                            +        "<div class='modal-body'>"
                            +            "<div class='shift-body'>"
                            +                "<p id = shift-details></p>" // Once again we will fill this when the shift is clicked
                            +                "<p id = cover-details-1></p>" // Open shifts have extra cover details that are filled on click
                            +                "<p id = cover-details-2></p>"
                            +            "</div>"
                            +        "</div>"
                            +        "<div class='modal-footer'>"
                            +            "<button type='button' class='align-left btn btn-default' data-dismiss='modal' data-toggle='modal' data-target = '#post-conf-" + String(shiftsDay[shift].event_id) + "'>Take Shift</button>"
                            +            "<button type='button' class='align-right btn btn-default' data-dismiss='modal'>Close</button>"
                            +        "</div>"
                            +    "</div>"
                            +"</div>"
                        +"</div>"
                        );
                        // These secondary modals are for confirming the shift posting
                        $('#user-shift-modals').append(
                            "<div id = 'post-conf-" + String(shiftsDay[shift].event_id) + "' class = 'modal fade'>"
                            +"<div class='modal-dialog modal-md'>"
                            +   "<div class='modal-content'>"
                            +       "<div class='modal-header'>"
                            +       shiftsDay[shift].title
                            +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal'>&times;</button>"
                            +       "<h4 class='modal-title'></h4>"
                            +   "</div>"
                            +   "<div class='modal-body'>"
                            +       "<div id='post-det'>"
                            +           "<p id='full-prompt'>Would you like to take the full shift?"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='full-take' type='radio' name='full-take'>Yes</label>"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='partial-take' type='radio' name='full-take'>No</label></p>"
                            +           "<div style='display:none;' class='partial-selectors'>"
                            +               fillPartialTimes('std', shiftsDay[shift].shift_start, shiftsDay[shift].shift_end)
                            +           "</div>"
                            +           "<p class='hidden' id='perm-prompt'>Do you want to take this shift permanently?"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='perm-cover' type='radio' name='perm-take'>Yes</label>"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='temp-cover' type='radio' name='perm-take' checked='checked'>No</label></p>"
                            +       "</div>"
                            +   "</div>"
                            +   "<div class='modal-footer'>"
                            +       "<button disabled id='take-cover-btn' type='button' class='align-left btn btn-primary'>Take Shift Cover</button>"
                            +       "<button type='button' class='align-right btn btn-default' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal' data-dismiss='modal'>Cancel</button>"
                            +   "</div>"
                            +      "</div>"
                            +   "</div>"
                            +"</div>"
                        );
                    }
                    else { // If the shift isn't open, we display normally
                        $('#' + weekDays[day] + '-shifts .panel-body').append( // Select the body of the current day we are looping through
                            "<button type = 'button' id = '" + shiftsDay[shift].event_id  + "' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#"
                            + String(shiftsDay[shift].event_id) + "-modal' >" + locations[shiftsDay[shift].location] // This line labels the modal we will make and the location of the shift
                            + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end) // This line lays out the time range of the shift using a handy method
                            +"</button>"
                        )
                        // Generate a modal for each shift
                        $('#user-shift-modals').append(
                            "<div id = '" + String(shiftsDay[shift].event_id) + "-modal' class = 'modal fade'>"
                            + "<div class='modal-dialog modal-lg'>"
                            +    "<div class='modal-content'>"
                            +        "<div class='modal-header'>"
                            +            shiftsDay[shift].title // The title of the shift becomes the title of the modal
                            +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                            +            "<h4 class='modal-title'></h4>"
                            +        "</div>"
                            +        "<div class='modal-body'>"
                            +            "<div class='shift-body'>"
                            +                "<p id = shift-details></p>" // We will fill this when we actually click a modal
                            +            "</div>"
                            +        "</div>"
                            +        "<div class='modal-footer'>"
                            +            "<button type='button' class='align-left btn btn-default' data-dismiss='modal' data-toggle= 'modal' data-target = '#post-conf-" + String(shiftsDay[shift].event_id) + "'>Post Cover</button>"
                            +            "<button type='button' class='align-right btn btn-default' data-dismiss='modal'>Close</button>"
                            +        "</div>"
                            +    "</div>"
                            +"</div>"
                        +"</div>"
                        )
                        // These modals are the modals that actually handle posting details
                        $('#user-shift-modals').append(
                            "<div id = 'post-conf-" + String(shiftsDay[shift].event_id) + "' class = 'modal fade'>"
                            +"<div class='modal-dialog modal-md'>"
                            +   "<div class='modal-content'>"
                            +       "<div class='modal-header'>"
                            +       shiftsDay[shift].title // Once again the title is the title of the shift
                            +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal'>&times;</button>"
                            +       "<h4 class='modal-title'></h4>"
                            +   "</div>"
                            +   "<div class='modal-body'>"
                            +       "<div id='post-det'>"
                            +           "<p id='full-prompt'>Would you like to post the full shift?"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='full-cover' type='radio' name='full-post'>Yes</label>"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='partial-cover' type='radio' name='full-post'>No</label></p>"
                            +           "<div style='display:none;' class='partial-selectors'>"
                            +               fillPartialTimes('std', shiftsDay[shift].shift_start, shiftsDay[shift].shift_end)
                            +           "</div>"
                            +           "<p class='hidden' id='perm-prompt'>Do you want to post this shift permanently?"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='perm-cover' type='radio' name='perm-post'>Yes</label>"
                            +           "<label class='spaced-radio-btn radio-inline'><input class='temp-cover' type='radio' name='perm-post' checked='checked'>No</label></p>"
                            +           "<div class='form-group'>"
                            +               "<label for='sob-story'>Sob Story:</label>"
                            +               "<textarea class='form-control' rows='2' id='sob-story'></textarea>"
                            +           "</div>"
                            +       "</div>"
                            +   "</div>"
                            +   "<div class='modal-footer'>"
                            +       "<button disabled id='post-cover-btn' type='button' class='align-left btn btn-primary'>Post Shift Cover</button>"
                            +       "<button type='button' class='align-right btn btn-default' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal' data-dismiss='modal'>Cancel</button>"
                            +   "</div>"
                            +   "</div>"
                            +"</div>"
                        )
                    }
                    if (isPermanentShift(shiftsDay[shift])) {
                        console.log("Permanent");
                        $('#post-conf-' + String(shiftsDay[shift].event_id)).find('#perm-prompt').removeClass('hidden')
                    }
                }
            }
        }
        console.log("Panels")
    }

    //Function to generate a list of time options for partial shift covers
    function fillPartialTimes(order, start, end) {
        var out = "Start:<select class='partial-start' name='post-partial-start'>"+listPartialTimes('std', start, end)+"</select>";
        out += "End:<select class='partial-end' name='post-partial-end'>"+listPartialTimes('invert', start, end)+"</select>";
        return out;
    }

    function listPartialTimes(order, begin, end) {
        var interval, start, stop;
        var ord = order == "std";
        if (ord) {
            interval = 15;
            start = begin;
            stop = end;
        } else {
            interval = -15;
            start = end;
            stop = begin;
        }
        interval *= 60000; // We have to give it to JS in milliseconds

        start = new Date(start);
        stop = new Date(stop);
        stop = stop.setTime(stop.getTime() - interval); //so that users can't create a 15-min long shift!
        var printDate = start;
        var out = "";

        // Here is where we generate the option html
        while (true) {
            if (ord && printDate >= stop)
                break;
            if (!ord && printDate <= stop)
                break;

            var hourMer = checkHour(printDate.getHours());
            var hour = hourMer[0];
            var min = checkTime(printDate.getMinutes());
            var mer = hourMer[1]; //Meridiem (am or pm)
            out += "<option value='"+printDate.toISOString()+"'>"+hour+":"+min+mer+"</option>";

            printDate.setTime(printDate.getTime() + interval);
        }
        return out;
    }

    function checkHour(hour) {
        if (hour == 12)
            return [hour, "pm"]
        else if (hour == 0)
            return [1, "am"]
        else if (hour > 12)
            return [hour%12, "pm"]
        else
            return [hour, "am"]
    }

    function checkTime(time) {
        if (time < 10)
            time = "0"+time;
        return time;
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
                    "<div class = 'panel panel-primary shift-panel' id= '" + weekDays[day] + "-open-shifts' >" +
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
                        "<button type = 'button' id = '" + shiftsDay[shift].event_id  + "' class = 'btn btn-block btn-warning shift-btn' data-toggle= 'modal' data-target= '#"
                        + String(shiftsDay[shift].event_id) + "-modal' >" + locations[shiftsDay[shift].location]
                        + ": " + formatTimeRange(shiftsDay[shift].shift_start, shiftsDay[shift].shift_end)
                        +"</button>"
                    )
                    // Generate a modal for each shift, this displays some information for the shift
                    $('#open-shift-modals').append(
                        "<div id = '" + String(shiftsDay[shift].event_id) + "-modal' class = 'modal fade'>"
                        + "<div class='modal-dialog modal-lg'>"
                        +    "<div class='modal-content'>"
                        +        "<div class='modal-header'>"
                        +            shiftsDay[shift].title
                        +            "<button type='button' class='close' data-dismiss='modal'>&times;</button>"
                        +            "<h4 class='modal-title'></h4>"
                        +        "</div>"
                        +        "<div class='modal-body'>"
                        +            "<div class='shift-body'>"
                        +                "<p id = shift-details></p>" // Once again we will fill this when the shift is clicked
                        +                "<p id = cover-details-1></p>" // Open shifts have extra cover details that are filled on click
                        +                "<p id = cover-details-2></p>"
                        +            "</div>"
                        +        "</div>"
                        +        "<div class='modal-footer'>"
                        +            "<button type = 'button' class='align-left btn btn-default' data-dismiss = 'modal' data-toggle= 'modal' data-target = '#post-conf-" + String(shiftsDay[shift].event_id) + "'>Take Shift</button>"
                        +            "<button type='button' class='align-right btn btn-default' data-dismiss='modal'>Close</button>"
                        +        "</div>"
                        +    "</div>"
                        +"</div>"
                    +"</div>"
                    )
                    // These secondary modals are for confirming the shift posting
                    $('#open-shift-modals').append(
                        "<div id = 'post-conf-" + String(shiftsDay[shift].event_id) + "' class = 'modal fade'>"
                        +"<div class='modal-dialog modal-md'>"
                        +   "<div class='modal-content'>"
                        +       "<div class='modal-header'>"
                        +       shiftsDay[shift].title
                        +       "<button type='button' class='close' data-dismiss='modal' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal'>&times;</button>"
                        +       "<h4 class='modal-title'></h4>"
                        +   "</div>"
                        +   "<div class='modal-body'>"
                        +       "<div id='post-det'>"
                        +           "<p id='full-prompt'>Would you like to take the full shift?"
                        +           "<label class='spaced-radio-btn radio-inline'><input class='full-take' type='radio' name='full-take'>Yes</label>"
                        +           "<label class='spaced-radio-btn radio-inline'><input class='partial-take' type='radio' name='full-take'>No</label></p>"
                        +           "<div style='display:none;' class='partial-selectors'>"
                        +               fillPartialTimes('std', shiftsDay[shift].shift_start, shiftsDay[shift].shift_end)
                        +           "</div>"
                        +           "<p class='hidden' id='perm-prompt'>Do you want to take this shift permanently?"
                        +           "<label class='spaced-radio-btn radio-inline'><input class='perm-cover' type='radio' name='perm-take'>Yes</label>"
                        +           "<label class='spaced-radio-btn radio-inline'><input class='temp-cover' type='radio' name='perm-take' checked='checked'>No</label></p>"
                        +       "</div>"
                        +   "</div>"
                        +   "<div class='modal-footer'>"
                        +       "<button disabled id='take-cover-btn' type='button' class='align-left btn btn-primary'>Take Shift Cover</button>"
                        +       "<button type='button' class='align-right btn btn-default' data-toggle = 'modal' data-target = '#" + String(shiftsDay[shift].event_id) + "-modal' data-dismiss='modal'>Cancel</button>"
                        +   "</div>"
                        +      "</div>"
                        +   "</div>"
                        +"</div>"
                    )
                    if (isPermanentShift(shiftsDay[shift])) {
                        console.log('#post-conf-' + String(shiftsDay[shift].event_id));
                        $('#post-conf-' + String(shiftsDay[shift].event_id)).find('#perm-prompt').removeClass('hidden')
                    }
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
    // This function checks if a given shift is a part of recurring instance
    // We refer to this as a permanent shift
    function isPermanentShift(shift) {
        // A permanent shift contains a formatted time date after the id seperated by a _
        return String(shift.event_id).includes('_')
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
                startTime += "PM";
            // Else calculate the time and then add PM
            else
            {
                sTimeNum -= 12;
                startTime = startTime.slice(2,5);
                startTime = String(sTimeNum) + startTime + "PM";
            }
        }
        // If it is before noon then just add AM
        else if (sTimeNum == 0)
        {
            sTimeNum = 12;
            startTime = startTime.slice(2,5);
            startTime = String(sTimeNum) + startTime + "AM";
        }
        else
        {
            startTime += "AM";
        }

        // Now do the same thing for the ending time
        if (eTimeNum > 11)
        {
            if (eTimeNum == 12)
                endTime += "PM";
            else
            {
                eTimeNum -= 12;
                endTime = endTime.slice(2,5);
                endTime = String(eTimeNum) + endTime + "PM";
            }
        }
        else if (eTimeNum == 0)
        {
            eTimeNum = 12;
            endTime = endTime.slice(2,5);
            endTime = String(eTimeNum) + endTime + "AM";
        }
        else
        {
            endTime += "AM";
        }

        // Format the time range and return it
        time = startTime + ' - ' + endTime;
        return time
    }

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
