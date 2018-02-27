/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////

$(document).ready(function() {


// Load image
$(document).ready(function(){
  $('.img').load(function() {
     $('.img').show()
     });
});

// Upon panel click with panelemp class, function of Modal population initiates
$('.panelemp').click(function showModal(){
    console.log("hi");

    // Grab all info from HTML load for each employee
    netid_1 = $(this).find(".emp-meta").attr('id');
    fullname = $(this).find(".m-fullname").text();
    codename = $(this).find(".m-code").text();
    fname = $(this).find(".m-fname").text();
    lname = $(this).find(".m-lname").text();
    apuid = $(this).find(".m-apuid").text();
    pos = $(this).find(".m-pos").text();
    position = $(this).find(".m-position").text();
    standing = $(this).find(".m-stand").text();
    phone = $(this).find(".m-nicephone").text();
    notnicephone = $(this).find(".m-phone").text();
    birthday = $(this).find(".m-birth").text();
    pic = $(this).find(".m-pic").text();
    color = $(this).find(".m-poscol").text();
    dev = $(this).find(".m-dev").text();
    skills = $(this).find(".m-profs").text();

    // These are used more for security reasons to check access
    active_user = $(this).find("#m-activeuser").text();
    manager = $(this).find("#m-mgr").text();
    leadlab = $(this).find("#m-lead").text();
    developer = $(this).find(".m-developer").text();


    // Parse all proficiencies from list
    var netid_1 = netid_1.toString()
    netid_1 = netid_1.slice(2)
    var basic = skills.slice(0,1);
    var adv = skills.slice(3,4);
    var field = skills.slice(6,7);
    var print = skills.slice(9,10);
    var net = skills.slice(12,13);
    var mobile = skills.slice(15,16);
    var ref = skills.slice(18,19);
    var soft = skills.slice(21,22);

    // If all proficiencies are null/0, set all to 0 for functionality
    if (basic == 0 && adv == 0 && field == 0 && print == 0 && net == 0 && mobile == 0 && ref == 0 && soft == 0){
        basic = 0
        adv = 0
        field = 0
        print = 0
        net = 0
        mobile = 0
        ref = 0
        soft = 0
    }
    // Conditional for if the employee is a developer
    if (developer == "True"){
        developer = true
    } else{
        developer = false
    }
    // Conditional if someone has not input their phone number or birthday to not let DB break
    if (birthday == 'None' || notnicephone == 'None'){
        birthday = null
        notnicephone == null
    }

    // Replace the modal-fade id, title name, bio info, color, and pic according to specific modal clicked
    $('#netid-standin').attr('id', netid_1);
    $('#content-standin').attr('class', "modal-content "+ color + " dev_"+ dev);
    $('#pic-standin').attr('src', pic);
    $('#title-name').append(
        "<b>" + fullname + "</b>"
    );
    $('#bio-div').append(
      "<div id='cur-bio'>"
    + "<h4><b>" + netid_1 + "</b></h4>"
    + "<h5>" + codename + "</h5>"
    + "<h5>" + position + "</h5>"
    + "<h5>" + phone + "</h5>"
    + "<h5>" + birthday + "</h5>"
    + "</div>"
    + "<div id='edit-bio'></div>"
    );

    // Function for a switch that replaces the number value with proficiency phrase
    function getProf(input) {
        var proficient = "";
        switch(parseInt(input)) {
        case 0:
            proficient = "Untrained";
            break;
        case 1:
            proficient = "Training";
            break;
        case 2:
            proficient = "Beginner";
            break;
        case 3:
            proficient = "Proficient";
            break;
        case 4:
            proficient = "Experienced";
            break;
        case 5:
            proficient = "Master";
            break;
        }
        return proficient;
    }

    // Conditional to append info for employee skills if Active User is a manager, and the modal is for a non-Lab Tech and non-Lead Lab Tech (who don't have skills)
    if((active_user == netid_1 || manager == "True") && (position != "Lab Technician" && position != "Lead Lab Tech")) {
        $("#li-skills").append("<a data-toggle='tab' href='#emp-skills'>Skills</a>")
        $("#emp-skills").append("<div id='skills-div'></div>")
    }

    // Skills and Radar Chart are appended to modal
    $('#skills-div').append(
       "<div class='container magic-container'"
     + "<div class ='row'>"
     + "<div class='chart col-xs-6 col-sm-6 col-md-7' data-width='90%' data-height='90%' data-red='100' data-green='100' data-blue='400' style='margin-top:5px;'>"
     + "<div class='chartCanvasWrap' style='left:5px;'></div>"
     + "</div>"
     + "<div class='col-xs-7 col-sm-7 col-md-5' id='cur-profs' style='text-align:right;  margin-top: 30px; margin-left: 15px;'>"
     + "<p><b>Basic Hardware: </b>" + getProf(basic) + "</p>"
     + "<p><b>Adv. Hardware: </b>" + getProf(adv) + "</p>"
     + "<p><b>Field Support: </b>" + getProf(field) + "</p>"
     + "<p><b>Printers: </b>" + getProf(print) + "</p>"
     + "<p><b>Networking: </b>" + getProf(net) + "</p>"
     + "<p><b>Mobile: </b>" + getProf(mobile) + "</p>"
     + "<p><b>Refreshes: </b>" + getProf(ref) + "</p>"
     + "<p><b>Software: </b>" + getProf(soft) + "</p>"
     + "</div>"
     + "<div id='prof-update' class='col-xs-7 col-sm-7 col-md-5' style:'text-align:right'></div>"
     + "</div>"
     + "</div>"
    );

    // Forms are added to allotted areas, all forms are then hidden until called upon
    $('#starform').appendTo("#comarea");
    $("#comform").appendTo("#comarea");
    $("#disform").appendTo("#comarea");
    $("#profform").appendTo('#prof-update');
    $("#bioform").appendTo('#edit-bio');
    $("#comform").hide();
    $("#starform").hide();
    $("#disform").hide();
    // Forms are defaulted to specific netid
    $("input[name='recipient']").val(netid_1);
    $("input[name='about']").val(netid_1);
    $("input[name='bio-netid']").val(netid_1);
    $("input[name='prof-netid']").val(netid_1);
    $("input[name='status']:checked").val(developer);

    // Proficiency Form is given existent default values
    $('#basic-input').attr('value', basic);
    $('#adv-input').attr('value', adv);
    $('#field-input').attr('value', field);
    $('#print-input').attr('value', print);
    $('#net-input').attr('value', net);
    $('#mobile-input').attr('value', mobile);
    $('#ref-input').attr('value', ref);
    $('#soft-input').attr('value', soft);

    // Bio Form is given existent default values
        // Format Birthday so that it's user friendly
        var bday = new Date(birthday)
        bday = bday.toLocaleDateString("en-US")
        var month = bday.split("/")[0]
        var day = bday.split("/")[1]
        var year = bday.split("/")[2]
        bday = year + "-" + month + "-" + day;
    $('#fname-input').attr('value', fname);
    $('#lname-input').attr('value', lname);
    $('#phone-input').attr('value', notnicephone);
    $('#apu-input').attr('value', apuid);
    $('#code-input').attr('value', codename);
    $('#bday-input').attr('value', bday);
    $('#pos_desc-input').attr('value', position);
    $('#opt-'+ pos).prop('selected', true);
    $('#opt-' + standing).prop('selected', true);
    $('#status-' + developer).prop('checked',true);


    // Ajax call to generate trophies according to specific modals
    $.ajax({
        method: "GET",
        dataType: "json",
        url: 'ajax/awardsget/',
        dataType: 'json',
        data: {
            'netid': netid_1,
        },
        success: function(data){
            console.log("LET THE STARS SHINE!")
            console.log(data)

            for (i = 0; i < data.trophlist.length; i++) {
                    var output = "<a href='#' class='trophy' data-toggle='popover' data-placement='auto top' data-trigger='hover' title='" + data.trophlist[i].name;
                    output += "' data-content='" + data.trophlist[i].reason + " -- " + data.trophlist[i].giver + "'>";
                    output += "<img class='trophy-img' src='/static/" + data.trophlist[i].url + "'></a>";
                    $(output).appendTo("#trophy-m");
            }
            // Allows for hover effect over each trophy
            $('[data-toggle="popover"]').popover();
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong with your STARS!")
        }
    });

    // Ajax call to get comments according to each specific modal
    $.ajax({
        method: "GET",
        dataType: "json",
        url: 'ajax/commentsget/',
        dataType: 'json',
        data: {
           'netid': netid_1,
        },
        success: function(data){

            if((active_user != netid_1 && leadlab == "True" && position == "Lab Technician") || manager == "True"){
                $("#li-comment").append("<a data-toggle='tab' href='#emp-comment'>Comments</a>")

                $("#comment-div").html(" ");
                for (i = 0; i < data.comlist.length; i++) {
                    var output = "<div class='panel comment-panel' id='comment-list-" + data.comlist[i].pk + "'><div class='panel-body'>";
                    output += "<div class='row'><div class='col-xs-10 col-sm-10 col-md-10'><h4><b>Subject: </b></h4><h4>" + data.comlist[i].subject + "</h4></div>";
                    output += "<div class='col-xs-2 col-sm-2 col-md-2'><button type='button' style='display:none' onclick=DeleteComment('list-"+ data.comlist[i].pk + "','"+ netid_1 +"') class='btn delete-btn btn-default btn-sm' id='list-"+i+"'><span class='oi oi-trash'></span> </button></div>"
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
            }
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong with your comments!")
        }
    });

    // ALL THE STUFF HAS BEEN ADDED/CHANGED, NOW IT SHOWS!
    $('#'+ netid_1).modal('show');

    // If Star button is clicked, show star form and hide others
    $('#starpanel').click(function(){
        $("#starform")[0].reset();
        $("#comform").hide();
        $("#disform").hide();
        $('#starform').fadeIn(200);
    });

    // If Comment button is clicked, show comment form and hide others
    $('#companel').click(function(){
        $("#comform")[0].reset();
        $("#starform").hide();
        $("#disform").hide();
        $('#comform').fadeIn(200);
    });

    // If Discipline button is clicked, show discipline form and hide others
    $('#dispanel').click(function(){
        $("#disform")[0].reset();
        $("#starform").hide();
        $("#comform").hide();
        $('#disform').fadeIn(200);
    });

    // Editing function when "Edit" button is clicked
    $('#edit-btn').click(function() {
        console.log("Edit Clicked!")
        $("#cur-bio").hide();
        $("#cur-profs").hide();
        $("#bioform").fadeIn(300);
        $("#profform").fadeIn(300);
        $("#delete-emp").fadeIn(300);
        $(".delete-btn").fadeIn(200);
    });


    //Delete the modal info when modal is hidden
    $("#" + netid_1).on("hidden.bs.modal", function(){

        // Set all attributes of tab-panes, and classes to original status
        $("#li-home").attr('class', 'active')
        $("#li-skills").attr('class', '')
        $("#li-comment").attr('class', '')
        $("#emp-home").attr('class', 'modal-body hero-bio tab-pane fade in active')
        $("#emp-skills").attr('class', 'tab-pane row fade')
        $("#emp-comment").attr('class', 'modal-body hero-bio tab-pane fade')
        $("#profform").appendTo('#prof-form');
        $("#bioform").appendTo('#bio-form');

        // Clear the skills and comments divs
        $("#li-skills").empty();
        $("#li-comment").empty();
        $("#emp-skills").empty();

        //Return all forms to original form divs, and hide them
        $("#comform").appendTo("#comment-form");
        $("#starform").appendTo("#star-form");
        $("#disform").appendTo("#dis-form");
        $("#profform").hide();
        $("#bioform").hide();
        $("#comment-form").hide();
        $("#star-form").hide();
        $("#disform").hide();
        $("#delete-emp").hide();

        // Fully clear the modal-fade info and set it to standard
        $("#trophy-m").empty();
        $('#bio-div').empty();
        $('#skills-div').empty();
        $('#title-name').empty();
        $('#' + netid_1).attr('id', 'netid-standin')
        $("input[name='netid']").val('');
    });


    // Radar chart function, found on https://www.jqueryscript.net/chart-graph/Simple-Radar-Chart-Plugin-with-jQuery-Canvas-Radar-Plus.html
    $(function(){
      $('.chart').radarChart({
        size: [325, 325],
        step: 1,
        values: {
          "Basic": basic,
          "Advanced": adv,
          "Field": field,
          "Printer": print,
          "Network": net,
          "Mobile": mobile,
          "Refresh": ref,
          "Software": soft,
        },
        showAxisLabels: true
      });
    });

    });
    (function($) {

      var Radar = (function() {

        function Radar(ele, settings) {
          this.ele = ele;
          this.settings = $.extend({
            showAxisLabels: $(ele).data("showAxisLabels"),
            title: $(ele).data("text"),
            step: $(ele).data("step"),
            values: $(ele).data("values"),
            color: [$(ele).data("red"),$(ele).data("green"),$(ele).data("blue")],
            insertFirst : $(ele).data("insert-first"),
            fixedMaxValue:$(ele).data("fixed-max-value"),
            size : [$(ele).data("width"),$(ele).data("height")],
            additionalLineDistance: $(ele).data("additional-line-distance"),
            annimationDelay: $(ele).data("annimation-delay")
          },settings);
          this.width = this.settings.size[0];
          this.height = this.settings.size[1];
          $(ele).css({
            'position': 'relative',
          });
          this.canvas = {};
          this.draw();
        }

        Radar.prototype.newCanvas = function() {

        var div = $(this.ele).find(".chartCanvasWrap").first();

        $(div).css({
            'position': 'relative'
        });

          var canvas = document.createElement('canvas');
          canvas.width = this.width;
          canvas.height = this.height;
          canvas.style.position = "relative";

          $(div).append(canvas);

          this.canvas = canvas;

            var annimationDelay = 100;
            if(this.settings.annimationDelay){
                annimationDelay=this.settings.annimationDelay;
            }
          this.cxt = canvas.getContext('2d');

            $(canvas).css('opacity',0).delay(annimationDelay).animate({opacity: 1}, annimationDelay);

        }

        Radar.prototype.draw = function() {
          this.newCanvas();
          var min = 0;
          var max = 5;

          $.each(this.settings.values, function(i,val){
            if (val < min)
              min = val;
            if (val > max)
              max = val;
          });
          if(this.settings.fixedMaxValue){
            max=this.settings.fixedMaxValue;
          }
          min = Math.floor(min);
          max = Math.ceil(max);

          var spacing = Math.ceil(this.width/20);

          for(var i = min; i <= max; i += this.settings.step) {
            this.cxt.beginPath();
            this.cxt.arc(this.width/2,
                         this.height/2,
                         this.settings.step * spacing * i,
                         0, 2 * Math.PI, false);
            this.cxt.strokeStyle = "#666";
            this.cxt.fillStyle = "#444";
            this.cxt.stroke();
            if (this.settings.showAxisLabels)
              this.cxt.fillText(i,this.width/2 + this.settings.step * spacing * i+4, this.height/2-2);
          }

          var size = 0;
          for(var key in this.settings.values)
            size += 1;

          for(var i = 0; i < size; i += 1) {
            this.cxt.beginPath();
            this.cxt.moveTo(this.width / 2, this.height /2);
            var x = this.width / 2 + Math.cos((Math.PI * 2) * (i / size)) * spacing * max;
            var y = this.height /2 + Math.sin((Math.PI * 2) * (i / size)) * spacing * max;
            this.cxt.lineTo(x, y);
            this.cxt.stroke();
          }

          this.cxt.beginPath();
          var first = true;
          var i = 0;
          var that = this;
          var end = {x: null, y: null};
          $.each(this.settings.values, function(key,val){
            var x = that.width / 2 + Math.cos((Math.PI * 2) * (i / size)) * spacing * val;
            var y = that.height / 2 + Math.sin((Math.PI * 2) * (i / size)) * spacing * val;
            if (first) {
              that.cxt.moveTo(x, y);
              end.x = x;
              end.y = y;
              first = false;
            }
            that.cxt.lineTo(x, y);
            i += 1;
          });

          this.cxt.lineTo(end.x, end.y);
          var grad = this.cxt.createLinearGradient(0, 0, 0, this.height);
          grad.addColorStop(0,"rgba("+this.settings.color[0]+","+this.settings.color[1]+","+this.settings.color[2]+",0)");
          grad.addColorStop(1,"rgba("+this.settings.color[0]+","+this.settings.color[1]+","+this.settings.color[2]+",1)");
          this.cxt.fillStyle = grad;
          this.cxt.shadowBlur = 2;
          this.cxt.shadowColor = "rgba(0, 0, 0, .2)";
          this.cxt.stroke();
          this.cxt.fill();

          var additionalLineDistance =  this.settings.additionalLineDistance;
          i = 0;
          $.each(this.settings.values, function(key,val){
            that.cxt.fillStyle = "rgba(0,0,0,.8)";
            that.cxt.strokeStyle = "rgba(0,0,0,.5)";
            that.cxt.font = "bold 14px Helvetica";
            var dist = Math.min(spacing * val, size * spacing);
            var x = that.width / 2 + Math.cos((Math.PI * 2) * (i / size)) * spacing * val;
            var y = that.height / 2 + Math.sin((Math.PI * 2) * (i / size)) * spacing * val;

            var textX = that.width / 2 + Math.cos((Math.PI * 2) * (i / size)) * spacing * max;
            var textY = that.height / 2 + Math.sin((Math.PI * 2) * (i / size)) * spacing * max * 1.5;

            if (textX < that.width/2) {
              textX -= (max *3) ;

            if(additionalLineDistance){
                textX -= additionalLineDistance;
             }

              that.cxt.textAlign="end";
              that.cxt.beginPath();
              var width = that.cxt.measureText(key).width;
              that.cxt.moveTo(textX - width - 15, textY + 4);
              that.cxt.lineTo(textX , textY + 4);
              that.cxt.lineTo(x - 2, y);
              that.cxt.lineWidth = 2;
              that.cxt.stroke();
            } else {
              textX += (max *3);

            if(additionalLineDistance){
                textX += additionalLineDistance;
            }
              that.cxt.textAlign="start";
              that.cxt.beginPath();
              var width = that.cxt.measureText(key).width;
              that.cxt.moveTo(x + 2,y);
              that.cxt.lineTo(textX , textY + 4);
              that.cxt.lineTo(textX + width + 15, textY + 4);
              that.cxt.lineWidth = 2;
              that.cxt.stroke();
            }
            that.cxt.fillText(key, textX, textY);
            //For arrows that aren't done.
            i += 1;
          });

          if(this.settings.title){
          this.cxt.font = "bold 20px Helvetica";
          this.cxt.fillText(this.settings.title, 10, 25);
          }
        }

        return Radar;

      })();

      $.fn.radarChart = function(settings){
        this.each(function(i,ele){
          var radar = new Radar(ele, settings);
        });
      }

    })(jQuery);

// Search bar function for employees
$("#searchbar").keyup(function () {
    //set all values entered in to lower case to generalize
    var value = $("#searchbar").val().toLowerCase();

    // As each value is entered in, the panels are faded out accordingly
    if (value.length >= 1) {
        $(".panelemp[id*=" + value + "]").fadeIn(150);
        $(".panelemp:not([id*=" + value + "])").fadeOut(100);
    } else {
        $(".panelemp").fadeIn(100);
    }
});

// AJAX call for when someone submits and update to someone's bio
$("#bioform").on("submit", function(event) {
    event.preventDefault();
    // Variable collection according the values input to form
    var fname = $("#fname-input").val();
    var lname = $("#lname-input").val();
    var phone = $("#phone-input").val();
    var apuid = $("#apu-input").val();
    var code = $("#code-input").val();
    var bday = $("#bday-input").val();
    var position = $("#position-input").val();
    var pos_desc = $("#pos_desc-input").val();
    var standing = $("#standing-input").val();
    var about = $("#bio-about").val();
    var developer = $("input[name='status']:checked").val();
    // Convert developer input back to a string
    if (developer == "True"){
        developer = "True"
    } else{
        developer = "False"
    }

    $.ajax({
        url: 'ajax/employeeupdate/',
        type: 'POST',
        data: {
            'fname': fname,
            'lname': lname,
            'apuid': apuid,
            'code': code,
            'phone': phone,
            'bday': bday,
            'about': about,
            'pos_desc': pos_desc,
            'position': position,
            'standing': standing,
            'developer': developer,
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Bio has been updated!")
            $('.modal').modal('hide');
            location.reload();
        },
        error: function(data){
            console.log("Failure to update bio!")
            alert("Failed! Please check format of all fields (especially the birthday)!")
            console.log(data)
        }
    })
});
// AJAX call for when proficiencies are updated for employee
$("#profform").on("submit", function(event) {
    event.preventDefault();
    // Variables are collected from form according to input values
    var basic = $("#basic-input").val();
    var adv = $("#adv-input").val();
    var field = $("#field-input").val();
    var print = $("#print-input").val();
    var net = $("#net-input").val();
    var mobile = $("#mobile-input").val();
    var ref = $("#ref-input").val();
    var soft = $("#soft-input").val();
    var about = $("#prof-about").val();


    $.ajax({
        url: 'ajax/proficienciesupdate/',
        type: 'POST',
        data: {
            'basic': basic,
            'adv': adv,
            'field': field,
            'print': print,
            'net': net,
            'mobile': mobile,
            'ref': ref,
            'soft': soft,
            'about': about,
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Proficiencies have been updated!")
            $('.modal').modal('hide');
            location.reload();
        },
        error: function(data){
            console.log("Failure to update proficiencies!")
            alert("Failed! Please check all fields (must be values 0-5)!")
            console.log(data)
        }
    })
});

// When the star form is submitted, the ajax is called to POST
$("#starform").on("submit", function(event) {
    event.preventDefault();

    var short = $("#award-subject").val();
    var type = $("#award-type").val();
    var reason = $("#award-reason").val();
    var recip = $("#recipient").val();

    $.ajax({
        url: 'ajax/awardpost/',
        type: 'POST',
        data: {
            'name': short,
            'type': type,
            'reason': reason,
            'recipient': recip
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Star has been posted!")
            $("#starform")[0].reset();
            $('.modal').modal('hide');
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
        }
    })
});

// When the comment form is submitted, the ajax is called to POST
$("#comform").on("submit", function(event) {
    event.preventDefault();

    var subject = $("#comm-subject").val();
    var body = $("#comm-body").val();
    var about = $("#comm-about").val();

    $.ajax({
        url: 'ajax/commentpost/',
        type: 'POST',
        data: {
            'subject': subject,
            'body': body,
            'about': about,
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Comment has been posted!")
            $("#comform")[0].reset();
            $('.modal').modal('hide');
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong!")
        }
    })

});

// When the discipline form is submitted, the ajax is called to POST
$("#disform").on("submit", function(event) {
    event.preventDefault();

    var subject = $("#disc-subject").val();
    var body = $("#disc-body").val();
    var extent = $("input[name='extent']:checked").val();
    var about = $("#disc-about").val();

    console.log(extent)

    $.ajax({
        url: 'ajax/disciplinepost/',
        type: 'POST',
        data: {
            'subject': subject,
            'body': body,
            'extent': extent,
            'about': about,
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Discipline has been posted!")
            $("#disform")[0].reset();
            $('.modal').modal('hide');
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong!")
        }
    })

});
// Function to confirm the deletion of a comment
function DeleteComment(comment,netid) {
    // Conditional for if confirmed, AJAX call is initiated AFTER comment fades out
    if (confirm("Are you sure you want to delete this comment for " + netid + "?") == true) {
        // Receives the comment primary key from DB and deletes accordingly
        $("#comment-"+comment).fadeOut(1600)
        setTimeout(DeleteCommentAJAX(comment,netid), 2000);
    }
}
// AJAX call for when comment is deleted
function DeleteCommentAJAX(comment,netid){

        var del_comment = comment.slice(5)
        var about = netid

        $.ajax({
            url: 'ajax/commentdelete/',
            type: 'POST',
            data: {
                'about': about,
                'del_comment': del_comment
            },
            dataType: 'json',
            success: function(data){
                console.log(data)
                alert("Comment has been deleted!")
            },
            error: function(data){
                console.log("Failure to delete comment!")
                console.log(data)
            }
        })
}

// AJAX call for when Employee deletion is instantiated
$("#delete-emp").click(function(event) {
    event.preventDefault();
    // This does not delete the row from the DB, but changes the employee column "Delete" to true
    var about = $("#prof-about").val();

    $.ajax({
        url: 'ajax/employeedelete/',
        type: 'POST',
        data: {
            'about': about,
        },
        dataType: 'json',
        success: function(data){
            console.log(data)
            alert("Employee has been deleted!")
            $('.modal').modal('hide');
            location.reload();
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