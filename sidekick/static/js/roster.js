/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////
$(document).ready(function(){
  $('.img').load(function() {
     $('.img').show()
     });
});

netid_1 = $(this).find(".emp-meta").attr('id')

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
netid_1 = netid_1.slice(2)
var basic = skills.slice(0,1);
var adv = skills.slice(3,4);
var field = skills.slice(6,7);
var print = skills.slice(9,10);
var net = skills.slice(12,13);
var mobile = skills.slice(15,16);
var ref = skills.slice(18,19);
var soft = skills.slice(21,22);
//Append the mother-modal div upon click

    $('#drop-down').append(
         "<div id=" + netid_1 + " class='modal fade'>"
        +   "<div class='modal-dialog modal-md'>"
        +       "<div class='modal-content "+ color +" dev_"+ dev +"'>"
        +           "<div class='modal-header'>"
        +               "<div class='flex-container'>"
        +               "<h4 style='text-align: left; margin-left:20px;' class='modal-title'><b>" + fullname + "</b></h4>"
        +                           "<ul class='nav nav-tabs' style='margin-left:60px'>"
        +                           "<li class='active'><a data-toggle='tab' href='#h-" + netid_1 +"'>Info</a></li>"
        +                           "<li><a data-toggle='tab' href='#s-" + netid_1 +"'>Skills</a></li>"
        +                           "<li><a data-toggle='tab' href='#c-" + netid_1 +"'>Comments</a></li>"
        +                 "</div>"
        +           "</div>"
        +                 "<div class='tab-content tab-card'>"
        +                   "<div id='h-" + netid_1 +"' class='modal-body hero-bio tab-pane fade in active'>"
        +                       "<img src='" + pic + "' class='img-circle img-herobio'>"
        +                           "<div class='hero-bio'>"
        +                               "<p><b>" + netid_1 + "</b></p>"
        +                               "<p>" + codename + "</p>"
        +                               "<p>" + position + "</p>"
        +                               "<p>" + phone + "</p>"
        +                               "<p>" + birthday + "</p>"
        +                           "</div>"
        +                           "<div class='inner-trophies'>"
        +                               "<h4><b>Trophies</b></h4>"
        +
        +                           "</div>"
        +                   "</div>"
        +                       "<div id='s-" + netid_1 +"' class='tab-pane row fade'>"
        +                           "<div class='chart col-md-' data-width='200' data-height='300' data-red='100' data-green='100' data-blue='400' style='margin-top:5px;'>"
		+                               "<div class='chartCanvasWrap col-md-7' style='left:5px'></div>"
		+                                   "<div class='col-sm-5 prof-al' align='right'>"
        +                                       "<p><b>Basic Hardware: </b>" + basic + "</p>"
        +                                       "<p><b>Advanced Hardware: </b>" + adv + "</p>"
        +                                       "<p><b>Field Support: </b>" + field + "</p>"
        +                                       "<p><b>Printers: </b>" + print + "</p>"
        +                                       "<p><b>Networking: </b>" + net + "</p>"
        +                                       "<p><b>Mobile: </b>" + mobile + "</p>"
        +                                       "<p><b>Refreshes: </b>" + ref + "</p>"
        +                                       "<p><b>Software: </b>" + soft + "</p>"
        +                                   "</div>"
		+                               "</div>"
		+                           "</div>"
        +                               "<div id='c-" + netid_1 +"' class='modal-body hero-bio tab-pane fade'>"
		+                                   "<div class='col-md-6' style='left:4px'>"
		+                                       "<h4 style='text-align: left; margin-left: 100px;' class='modal-title'><b>Comments</b></h4>"
		+                                       "<div style='height: 275px; overflow-y: auto; margin-top:5px'>"
		+                                       "<p>1</p><p>2</p><p>3</p><p>4</p><p>5</p><p>6</p><p>7</p><p>8</p><p>9</p><p>10</p><p>11</p><p>12</p><p>13</p>"
        +                                       "</div>"
		+                                   "</div>"
		+                                       "<div class='col-md-6' style='right:4px'>"
		+                                           "<button type='btn-md' style='margin:7px' id='starpanel'>Star</button>"
		+                                           "<button type='btn-md' style='margin:7px' id='dispanel'>Discipline</button>"
		+                                           "<div id='comarea' style='height: 250px; overflow-y: auto;'></div>"
		+                                       "</div>"
        +                               "</div>"
        +                        "</div>"
        +                    "<div class='modal-footer'>"
        +                       "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
        +                    "</div>"
        +              "</div>"
        +        "</div>"
        +"</div>");

//Once modal div is added, it is shown
$('#'+ netid_1).modal('show');

$("#comform").appendTo("#comarea")
$('#starform').appendTo("#comarea")
$("#comform").hide()
$("#stform").hide()
$('input[name=recipient]').val(netid_1);
$('input[name=about]').val(netid_1);

//Delete the modal info when modal is hidden
$("#" + netid_1).on("hidden.bs.modal", function(){
    $("#comform").appendTo("#comment-form")
    $("#starform").appendTo("#star-form")
    $("#comment-form").hide()
    $("#star-form").hide()
    $('#drop-down').empty();
});

$('#dispanel').click(function(){
$("#starform").hide()
$('#comform').fadeIn(200)
});

$('#starpanel').click(function(){
$("#comform").hide()
$('#starform').fadeIn(200)
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

		var annimationDelay = 1200;
		if(this.settings.annimationDelay){
			annimationDelay=this.settings.annimationDelay;
		}
	  this.cxt = canvas.getContext('2d');

        $(canvas).css('opacity',0).delay(annimationDelay).animate({opacity: 1}, annimationDelay);

    }

    Radar.prototype.draw = function() {
      this.newCanvas();
      var min = 0;
      var max = 0;

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
