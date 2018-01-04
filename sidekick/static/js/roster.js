/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////
$(document).ready(function(){
  $('.img').load(function() {
     $('.img').show()
     });
});

$('.btn').click(function showModal(){

//grab all info from HTML load for each employee
netid_1 = $(this).find(".emp-meta").attr('id')
fullname = $(this).find(".m-fullname").text()
codename = $(this).find(".m-code").text()
position = $(this).find(".m-position").text()
phone = $(this).find(".m-phone").text()
birthday = $(this).find(".m-birth").text()
pic = $(this).find(".m-pic").text()
color = $(this).find(".m-poscol").text()
dev = $(this).find(".m-dev").text()
skills = $(this).find(".m-profs").text();


//grab all proficiencies from list
var netid_1 = netid_1.slice(2,);
var basic = skills.slice(0,1);
var adv = skills.slice(3,4);
var field = skills.slice(6,7);
var print = skills.slice(9,10);
var net = skills.slice(12,13);
var mobile = skills.slice(15,16);
var ref = skills.slice(18,19);
var soft = skills.slice(21,22);
//Append the mother-modal div upon click

    if (basic == 0, adv == 0, field == 0, print == 0, net == 0, mobile == 0, ref == 0, soft == 0){
        basic = 0
        adv = 0
        field = 0
        print = 0
        net = 0
        mobile = 0
        ref = 0
        soft = 0
    }

    $('#netid-standin').attr('id', netid_1);
    $('#content-standin').attr('class', "modal-content "+ color + " dev_"+ dev);
    $('#pic-standin').attr('src', pic);

    $('#title-name').append(
        "<b>" + fullname + "</b>"
    );

    $('#bio-div').append(
      "<h4><b>" + netid_1 + "</b></h4>"
    + "<h5>" + codename + "</h5>"
    + "<h5>" + position + "</h5>"
    + "<h5>" + phone + "</h5>"
    + "<h5>" + birthday + "</h5>"
    );

    $('#skills-div').append(
     "<div class='chart col-sm-' data-width='200' data-height='300' data-red='100' data-green='100' data-blue='400' style='margin-top:5px;'>"
     + "<div class='chartCanvasWrap col-md-7' style='left:5px'></div>"
     + "<div class='col-sm-4' style='text-align:right'>"
     + "<p><b>Basic Hardware: </b>" + basic + "</p>"
     + "<p><b>Advanced Hardware: </b>" + adv + "</p>"
     + "<p><b>Field Support: </b>" + field + "</p>"
     + "<p><b>Printers: </b>" + print + "</p>"
     + "<p><b>Networking: </b>" + net + "</p>"
     + "<p><b>Mobile: </b>" + mobile + "</p>"
     + "<p><b>Refreshes: </b>" + ref + "</p>"
     + "<p><b>Software: </b>" + soft + "</p>"
     + "</div>"
     + "</div>"
    );

    //Once modal div is added, it is shown
    $('#'+ netid_1).modal('show');

    $('#starform').appendTo("#comarea");
    $("#comform").appendTo("#comarea");
    $("#disform").appendTo("#comarea");
    $("#comform").hide();
    $("#starform").hide();
    $("#disform").hide();
    $("input[name='recipient']").val(netid_1);
    $("input[name='about']").val(netid_1);

    var subject
    var time
    var description
    var extent

    $.ajax({
        method: "GET",
        dataType: "json",
        url: 'ajax/getcomments/',
        dataType: 'json',
        data: {
           'netid': netid_1,
           'subject': subject,
           'extent': extent,
           'time': time,
           'descrip': description
        },
        success: function(data){
            console.log(data)

            console.log(data.comlist)

            $("#comment-div").html(" ");
	        for (i = 0; i < data.comlist.length; i++) {
		        var output = "<panel>";
		        output += "<h4><b>Subject: </b>"+ data.comlist[i].subject +"</h4>";
		        output += "<h5><b>Value: </b>"+ data.comlist[i].val +"</h5>";
		        output += "<h5><b>Why: </b>"+ data.comlist[i].description +"</h5>";
		        output += "<h5><b>When: </b>"+ data.comlist[i].time +"</h5>";
		        output += "</panel>";
		        $(output).appendTo("#comment-div");
		        }
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong with your comments!")
        }
    });

//Delete the modal info when modal is hidden
$("#" + netid_1).on("hidden.bs.modal", function(){
    $("#comform").appendTo("#comment-form");
    $("#starform").appendTo("#star-form");
    $("#disform").appendTo("#dis-form");
    $("#comment-form").hide();
    $("#star-form").hide();
    $("#disform").hide();
    $('#bio-div').empty();
    $('#skills-div').empty();
    $('#title-name').empty();
    $('#' + netid_1).attr('id', 'netid-standin')
});

$('#starpanel').click(function(){
    $("#starform")[0].reset();
    $("#comform").hide();
    $("#disform").hide();
    $('#starform').fadeIn(200);
});

$('#companel').click(function(){
    $("#comform")[0].reset();
    $("#starform").hide();
    $("#disform").hide();
    $('#comform').fadeIn(200);
});

$('#dispanel').click(function(){
    $("#disform")[0].reset();
    $("#starform").hide();
    $("#comform").hide();
    $('#disform').fadeIn(200);
});

//radar chart function
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

$("#searchbar").keyup(function () {
    var value = $("#searchbar").val().toLowerCase();

    console.log(value)

    if (value.length >= 1) {
        $(".panelemp[id*=" + value + "]").fadeIn(150);
        $(".panelemp:not([id*=" + value + "])").fadeOut(100);
    } else {
        $(".panelemp").fadeIn(100);
    }
});

$("#starform").on("submit", function(event) {
    event.preventDefault();

    var short = $("#award-subject").val();
    var type = $("#award-type").val();
    var reason = $("#award-reason").val();
    var recip = $("#recipient").val();

    $.ajax({
        url: 'ajax/postaward/',
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
            $("#starform")[0].reset();
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
        }
    })
});


$("#comform").on("submit", function(event) {
    event.preventDefault();

    var subject = $("#comm-subject").val();
    var body = $("#comm-body").val();
    var about = $("#comm-about").val();

    $.ajax({
        url: 'ajax/postcomment/',
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
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong!")
        }
    })

});

$("#disform").on("submit", function(event) {
    event.preventDefault();

    var subject = $("#disc-subject").val();
    var body = $("#disc-body").val();
    var extent = $("input[name='extent']:checked").val();
    var about = $("#disc-about").val();

    console.log(extent)

    $.ajax({
        url: 'ajax/postdiscipline/',
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
        },
        error: function(data){
            console.log("Failure!")
            console.log(data)
            alert("Oh no! Something went wrong!")
        }
    })

});

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