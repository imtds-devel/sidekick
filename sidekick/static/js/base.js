$(document).ready(function(){
    $('[data-toggle="popover"]').popover();

    $("#task-submit").click(function() {
        //start by verifying submitted data
        var task = $("#task-text").val();

        //send data to server
        $.ajax({
            method:"POST",
            dataType:"json",
            url:"ajax/newtask",
            data: {
                'task': task,
            },
            success: function(data) {
                if (data.result=="success") {
                    alert("Task submitted successfully!");
                    location.reload();
                } else
                    alert("Task posting failed! Please contact Mattaniah");
            },
            error: function(err) {
                alert("Task posting failed! Please contact Mattaniah and give her the error details:\n"+err);
                console.log(err);
            }
        });
    });
    //This function enables the complete button when a checkbox is selected.
    //Disables if no checkboxes are selected.
    var checkBoxes = $('fieldset .task-checkbox');
    checkBoxes.change(function () {
        $('#task-complete').prop('disabled', checkBoxes.filter(':checked').length < 1);
    });
    checkBoxes.change(); // or add disabled="true" in the HTML

    //This function completes tasks in the database
    $('#task-complete').click(function() {
        //Filters out all the unchecked checkboxes
        checkBoxes = checkBoxes.filter(':checked');
        //cycle through an array of checked checkboxes
        var succeed = true
        for(var i=0; i<checkBoxes.length; i++)
        {
            //Pull the task text from the checkbox label(nextElementSibling
            var task = checkBoxes[i].nextElementSibling.textContent;

            $.ajax({
                url: 'ajax/completetask',
                type: 'POST',
                data: {
                    'task': task,
                },
                dataType: 'json',
                success: function(data) {
                    console.log("task completed")
                },
                error: function(data) {
                    i=checkBoxes.length;
                    succeed=false
                    alert("Something went wrong. Please contact Mattaniah.")
                }
            })
            if(succeed=true){
                alert("Tasks have been completed")
                location.reload();
            }
        }
    });

    $('#note-update').click(function() {
        var note = $('#modnote').val()

        $.ajax({
            url: 'ajax/updatenote',
            type: 'POST',
            data:{
                'note': note,
            },
            dataType: 'json',
            success: function(data) {
                alert("Mod note has been updated")
            },
             error: function(err) {
                alert("Note update failed! Please contact Mattaniah and give her the error details:\n"+err);
                console.log(err);
            }
        })
    })

    $('#note-clear').click(function()   {
        $.ajax({
            url: 'ajax/clearnote',
            type: 'POST',
            data:{},
            dataType: 'json',
            success: function(data) {
                alert("Mod note has been cleared")
                LoadNote();
            },
             error: function(err) {
                alert("Note clear failed! Please contact Mattaniah and give her the error details:\n"+err);
                console.log(err);
            }
        })
    })

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
$(window).load(function() {
    $("#modCarousel").carousel('cycle');

    //Run once/min
    var shiftInfo;
    var techType = $(".shMeta .tech-type").text();
    if ($(".shMeta") && techType != "stt" && techType != "stm") {
        shiftInfo = setInterval(updateShiftInfo, 60000);
        updateShiftInfo();
    } else {
        shiftInfo = null;
    }

    function updateShiftInfo() {
        console.log("Updating Shift Sidebar Info");
        var end = new Date($(".shMeta > .sh-end").text());
        var now = new Date();
        $("#shEndsIn").text(parseInt((end-now)/60000));


        var next_report = new Date();

        switch ($(".shMeta .tech-type").text()) {
        case "lbt":
            var interval = 0;
            if (now.getMinutes() >= 15) {
                interval = 60 * 60 * 1000;
                if (now.getMinutes() == 15) {
                    alert("Hi there! Just a friendly reminder that your rounds report is due :)");
                }
            }
            next_report = new Date(now.getTime() + interval);
            next_report.setMinutes(15);
            break;

        case "spt":
            next_report = new Date(end.getTime() - 10 * 60 * 1000);

            if (now.getHours() == next_report.getHours() && now.getMinutes() == next_report.getMinutes()) {
                alert("Your shift ends in 10 minutes! Don't forget to document :)");
            } else if (now > next_report) {
                next_report = now;
            }
            break;

        case "mgr":
            next_report.setHours(16);
            next_report.setMinutes(0);

            if (now.getHours() == next_report.getHours() && now.getMinutes() == next_report.getMinutes()) {
                alert("Hey you, time for the MoD Report! Keep being awesome!");
            } else if (now > next_report) {
                next_report = now;
            }
            break;
        }
        UncheckAll();
        LoadNote();
        $("#shRoundsIn").text(parseInt((next_report - now) / 60000));
    }

});

function UncheckAll(){
      var w = document.getElementsByTagName('input');
      for(var i = 0; i < w.length; i++){
        if(w[i].type=='checkbox'){
          w[i].checked = false;
        }
      }
  }
function LoadNote() {
    var id = 1;
    $.ajax({
         url: 'ajax/loadnote',
            type: 'Get',
            data:{
                'id': id,
            },
            dataType: 'json',
            success: function(data) {
                $('#modnote').val(data.note)
            },
             error: function(err) {
                alert("Something went wrong with the mod note! Please contact Mattaniah and give her the error details:\n"+err);
                console.log(err);
            }
    })
}