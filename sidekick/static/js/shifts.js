/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////
// Variables for the page
weekDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] // Week days in order

$(document).ready(function() {
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
                    generateShiftPanels(data.week, data.shifts);
                    //console.log(data.shifts);
                }
            });
    });
    function generateShiftPanels(week, shifts){
        $('#your-shifts-panel-group').empty();
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
                        "<button type = 'button' class = 'btn btn-block shift-btn' data-toggle= 'modal' data-target= '#shift-id' >" + shiftsDay[shift].title + "</button>"                    
                    )
                    //TODO: Generate modals for those shifts
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
    // Don't call this function if there aren't shifts on the day
    function shiftsOnDay(day, shifts) {
        // Loops through the given shifts
        for (shift = 0; shift < shifts.length; shift++) {
            if (shifts[shift].shift_date != day.slice(0,10)) // If there is a shift not on that date
                shifts.splice(shift, 1) // Splices (removes) that shift
        }
        return shifts; // Return the newly spliced shifts
    }
});    