/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Spring 2018
/////////////////////////////////////////
$(window).load(function() {
    function showPrintModal() {
        console.log("Hi!");

        // Grab all info from HTML load for each employee
        var printpk = $(this).find(".m-printpk").text();
        var type = $(this).find(".m-printtype").text();
        var location = $(this).find(".m-locname").text();
        var statpic = $(this).find(".m-statpic").text();

        console.log(location)

        // Replace the modal-fade id, title name, bio info, color, and pic according to specific modal clicked
        $('#standin').attr('id', printpk);
        $('#pic-standin').attr('src', "static/" + statpic);
        $('#printer-title').append("<b>"+ location +" "+ type +"</b>")

        // Forms are added to allotted areas, all forms are then hidden until called upon
        //$('#starform').appendTo("#comarea");

        // Forms are defaulted to specific netid
        //$("input[name='recipient']").val(netid_1);

        // Ajax call to get comments according to each specific modal
     /*    $.ajax({
            method: "GET",
            dataType: "json",
            url: 'ajax/printcommentsget/',
            dataType: 'json',
            data: {
               'printpk': printpk,
            },
            success: function(data){

                    $("#comment-div").html(" ");
                    for (i = 0; i < data.comlist.length; i++) {
                        var output = "<div class='panel comment-panel' id='comment-list-" + data.comlist[i].pk + "'><div class='panel-body'>";
                        output += "<div class='row'><div class='col-xs-10 col-sm-10 col-md-10'><h4><b>Subject: </b></h4><h4>" + data.comlist[i].subject + "</h4></div>";
                        output += "<div class='col-xs-2 col-sm-2 col-md-2'><button type='button' style='display:none' onclick=DeleteComment('list-"+ data.comlist[i].pk + "','"+ netid_1 +"') class='btn delete-btn btn-default btn-sm' id='list-"+i+"'><span class='glyphicon glyphicon-trash'></span> </button></div>"
                        if (data.comlist[i].val != 0 && data.comlist[i].val != null){
                            if(data.comlist[i].val == 1){
                                output += "<h5><b>Extent: </b> <u>Full Discipline</u> </h5>";
                            }else{
                                output += "<h5><b>Extent: </b> <u>Half Discipline</u> </h5>";
                            }
                        }
                        output += "<div class='row'><div class='col-xs-12 col-sm-12 col-md-12'><h5><b>Why: </b></h5><p>" + data.comlist[i].description + "</p>";
                        output += "<h5><b>When: </b>" + data.comlist[i].time + "</h5>";
                        output += "</div</div></div></div>";

                        $(output).appendTo("#comment-div");

                            if(data.comlist[i].val == 1){
                                $('#comment-list-' + i).attr('style', 'background-color: #ffad99;');
                            }
                            if(data.comlist[i].val == .5){
                                $('#comment-list-' + i).attr('style', 'background-color: #ffffb3;');
                            }
                    }
            },
            error: function(data){
                console.log("Failure!")
                console.log(data)
                alert("Oh no! Something went wrong with your comments!")
            }
        }); */

        // ALL THE STUFF HAS BEEN ADDED/CHANGED, NOW IT SHOWS!
        $('#'+ printpk).modal('show');

        //Delete the modal info when modal is hidden
        $("#" + printpk).on("hidden.bs.modal", function(){

            // Set all attributes of tab-panes, and classes to original status
            $('#' + printpk).attr('id', 'netid-standin')
            $('#printer-title').empty()
            $('#pic-standin').attr('src', '')
        });
    }

    // Upon panel click with panelemp class, function of Modal population initiates
    $('.panelprint').click(showPrintModal);
});