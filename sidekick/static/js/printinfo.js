/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Spring 2018
/////////////////////////////////////////
$(window).load(function() {
// Upon panel click with panelemp class, function of Modal population initiates
    $('.panelprint').click(showPrintModal);
    function showPrintModal() {
        console.log("Hi!");

        // Grab all info from HTML load for each employee
        var printpk = $(this).find(".m-printpk").text();
        var type = $(this).find(".m-printtype").text();
        var location = $(this).find(".m-locname").text();
        var statpic = $(this).find(".m-statpic").text();

        console.log(printpk)

        // Replace the modal-fade id, title name, bio info, color, and pic according to specific modal clicked
        $('#standin').attr('id', printpk);
        $('#print_id').attr('value', printpk);
        $('#standin-pic').attr('src', "/static/" + statpic);
        $('#printer-title').append("<b>"+ location +" "+ type +"</b>")

        // Ajax call to get comments according to each specific modal
        $.ajax({
            method: "GET",
            dataType: "json",
            url: 'ajax/printreportsget/',
            dataType: 'json',
            data: {
            'printpk': printpk,
            },
            success: function(data){
                console.log(data.replist.length)
                    $("#report-div").html(" ");
                    for (i = data.replist.length-1; i >= data.replist.length-5; i--) {
                        var output = "<div class='card panel-print-log'>";
                        output += "Status: </b>" + data.replist[i].print_stat + "</h4>";
                        output += "<h5><b>Description: </b></h5><p>" + data.replist[i].desc + "</p>";
                        if(data.replist[i].netid == null){
                        output += "<h5><b>When: </b>" + data.replist[i].date + "   Poster: None </h5>";
                        } else{
                            output += "<h5><b>When: </b>" + data.replist[i].date + "   <b>Poster: </b>" + data.replist[i].netid + "</h5>";
                        }
                        output += "</div>";

                        $(output).appendTo("#report-div");
                    }
            },
            error: function(data){
                console.log("Failure!")
                console.log(data)
                alert("Oh no! Something went wrong with your comments!")
            }
        });

        // ALL THE STUFF HAS BEEN ADDED/CHANGED, NOW IT SHOWS!
        $('#'+ printpk).modal('show');

        //Delete the modal info when modal is hidden
        $("#" + printpk).on("hidden.bs.modal", function(){

            // Set all attributes of tab-panes, and classes to original status
            $('#' + printpk).attr('id', 'standin')
            $('#printer-title').empty()
            $('#report-div').empty()
            $('#pic-standin').attr('src', '')
        });
    }

    $("#report-btn").click(function(event) {
        // Variables are collected from form according to input values
        var printstatus = $("#printer-stat").val();
        var printdesc = $("#printer-desc").val();
        var printid = $("#print_id").val();
        var date = new Date();

        Date.prototype.yyyymmdd = function() {
            var mm = this.getMonth() + 1; // getMonth() is zero-based
            var dd = this.getDate();

            return [this.getFullYear(),
                    (mm>9 ? '' : '0') + mm,
                    (dd>9 ? '' : '0') + dd
                   ].join('-');
          };

        date =  date.yyyymmdd();


        $.ajax({
            url: 'ajax/printreportupdate/',
            type: 'POST',
            data: {
                'printstat': printstatus,
                'printdesc': printdesc,
                'printid': printid,
                'date': date,
            },
            dataType: 'json',
            success: function(data){
                console.log(data)
                alert("Printer Report has been updated!")
                $("#repform")[0].reset();
                $('.modal').modal('hide');
                location.reload();
            },
            error: function(data){
                console.log("Failure to update printer reports!")
                alert("Failed!!")
                console.log(data)
            }
        })
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
