
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
            url:"ajax/submitannounce",
            data: {
                'subject': subj,
                'body': body
            },
            success: function(data) {
                if (data.result=="success")
                    alert("Announcement submitted successfully!");
                else
                    alert("Announcement posting failed! Please contact Nico");
            }
            error: function(err) {
                alert("Announcement posting failed! Please contact Nico and give him the error details:\n"+err);
            }
        });

        //TODO: Reload page
    });

    $("#event-submit").click(function() {
        //start by verifying submitted data
    });
});
