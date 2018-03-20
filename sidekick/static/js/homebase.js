
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