
$(document).ready(function () {
    console.log("Homebase loaded");

    // When the check in form is submitted, the ajax is called to POST
    $("#checkform").submit(function(event) {
        event.preventDefault();


        var shift_id = $("#shift_id").val();
        //var shift_id = document.getElementById("shift_id").value;
        var check_time = document.getElementById("check_time").value;

        if( $("#shift_id").val() == null)
            console.log("im NOT in boys");

        console.log(shift_id);
        console.log("time: " + check_time);

        $.ajax({
            url: 'ajax/checkinpost/',
            type: 'POST',
            data: {
                'shift_id': shift_id,
                'check_time': check_time
            },
            dataType: 'json',
            success: function(data){
                console.log("success(?)")
                console.log(data)
                alert("Check in was successful!")
                $("#checkform")[0].reset();
                $('.modal').modal('hide');
            },
            error: function(data){
                console.log("Failure!")
                console.log(data)
                alert("Oh no! Something went wrong!")
            }
        })

    });

// Function that clears cookies from forms to cleanly submit forms
$(function() {

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

});