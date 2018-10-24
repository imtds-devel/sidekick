
$(document).ready(function () {
    console.log("Homebase loaded");

    //Power the announcement/event menu nav buttons
    $(".announce-menu").click(function() {
        var opt = $(this).attr('id');
        $(".announce-menu").removeClass("active");
        $(".announce-menu-body").hide(200);
        $("#"+opt+"-container").show(200);

        $(this).addClass("active");
    });

    $("#announce-submit").click(function() {
        //start by verifying submitted data
        var subj = $("#announce-subject").val();
        var body = $("#announce-body").val();

        //send data to server
        $.ajax({
            method:"POST",
            dataType:"json",
            url:"ajax/newannounce",
            data: {
                'subject': subj,
                'body': body
            },
            success: function(data) {
                if (data.result=="success") {
                    alert("Announcement submitted successfully!");
                    location.reload();
                } else
                    alert("Announcement posting failed! Please contact Nico");
            },
            error: function(err) {
                alert("Announcement posting failed! Please contact Nico and give him the error details:\n"+err);
                console.log(err);
            }
        });
    });

    $("#event-submit").click(function() {
        //start by verifying submitted data
        var title = $("#event-title").val();
        var loc = $("#event-loc").val();
        var date = $("#event-date").val();
        var desc = $("#event-desc").val();

        //send data to server
        $.ajax({
            method:"POST",
            dataType:"json",
            url:"ajax/newevent",
            data: {
                'title': title,
                'location': loc,
                'date': date,
                'description': desc
            },
            success: function(data) {
                if (data.result=="success") {
                    alert("Event submitted successfully!");
                    location.reload();
                } else
                    alert("Event posting failed! Please contact Nico");
            },
            error: function(err) {
                alert("Event posting failed! Please contact Nico");
                console.log(err);
            }
        });


    });

// Function that clears cookies from forms to cleanly submit forms
$(function() {
    // When the check in form is submitted, the ajax is called to POST
    $("#checkform").submit(function(event) {
        event.preventDefault();

        // builds a list of shift event_ids (only if they are checked in)
        var shift_ids = [];
        $('#checkform input:checked').each(function() {
            shift_ids.push($(this).val());
        });
        console.log(shift_ids);

        // builds a list of check in times (only if they are populated)
        var check_times = [];
        $('.check_time').each(function(){
            if( $(this).val() )
                check_times.push($(this).val());
        });
        console.log("timez: " + check_times);


        $.ajax({
            url: 'ajax/checkinpost/',
            type: 'POST',
            data: {
                'shift_ids': shift_ids,
                'check_times': check_times
            },
            dataType: 'json',
            success: function(data){
                console.log("success(?)")
                console.log(data)
                alert("Check in was successful!")
                $("#checkform")[0].reset();
                $('.modal').modal('hide');
                document.location.reload();
            },
            error: function(data){
                console.log("Failure!")
                console.log(data)
                alert("Oh no! Something went wrong!")
            }
        })

    });
});

});
