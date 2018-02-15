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
                        var output = "<div class='panel panel-print-log'>";
                        output += "<div class='row'><div class='col-xs-10 col-sm-10 col-md-10'><h4><b>Status: </b>" + data.replist[i].print_stat + "</h4></div>";
                        output += "<div class='row'><div class='col-xs-12 col-sm-12 col-md-12'><h5><b>Description: </b></h5><p>" + data.replist[i].desc + "</p>";
                        if(data.replist[i].netid == null){
                        output += "<h5><b>When: </b>" + data.replist[i].date + "   Poster: None </h5>";
                        } else{
                            output += "<h5><b>When: </b>" + data.replist[i].date + "   Poster: " + data.replist[i].netid + "</h5>";
                        }
                        output += "</div></div></div>";

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
});