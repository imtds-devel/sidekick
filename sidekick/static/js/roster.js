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

unformatted_info = $(this).find("ul")
formatted_info = $(this).find("li")

netid_1 = $(this).find(".emp-meta").attr('id')
fullname = $(this).find(".m-fullname").text()
codename = $(this).find(".m-code").text()
position = $(this).find(".m-position").text()
phone = $(this).find(".m-phone").text()
birthday = $(this).find(".m-birth").text()
pic = $(this).find(".m-pic").text()
color = $(this).find(".m-poscol").text()
dev = $(this).find(".m-dev").text()

netid_1 = netid_1.slice(2)
console.log(fullname, netid_1, codename, position, phone, birthday, pic)

    $('#drop-down').append("<div id=" + netid_1 + " class='modal fade'>"
        +"<div class='modal-dialog modal-md'>"
        +"<div class='modal-content "+ color +" dev_"+ dev +"'>"
        +"<div class='modal-header'>"
        +"<h4 style='text-align: center' class='modal-title'>" + fullname + "</h4></div>"
        +"<div class='tab-content'>"
        +"<div id='h-" + netid_1 +"' class='modal-body hero-bio fade in active'>"
        +"<div class='row'>"
        +"<img src='" + pic + "' class='img-circle img-herobio'>"
        +"<div class='hero-bio'>"
        +"<p><b>" + netid_1 + "</b></p>"
        +"<p>" + codename + "</p>"
        +"<p>" + position + "</p>"
        +"<p>" + phone + "</p>"
        +"<p>" + birthday + "</p>"
        +"</div>"
        +"</div>"
        +"</div>"
        +"<div id='s-" + netid_1 +"' class='modal-body hero-bio fade'>"
        +"<div class='skillsPieChart'"
        +"data-values='{'jQuery': 4.5,'CSS/CSS3': 3.0,'Html5':3.0,'Python':4.0,'Node.js':4.0}"
        +"data-width='300'"
        +"data-height='300'"
        +"data-red='0'"
        +"data-green='128'"
        +"data-blue='255'>"
        +"<div class='chartCanvasWrap'></div>"
        +"</div>"
        +"</div>"
        +"<div id='d-" + netid_1 +"' class='modal-body hero-bio fade'>"
        +"</div>"
        +"</div>"
        +"<div class='modal-footer'>"
        +"<ul class='nav nav-tabs'>"
        +"<li class='active'><a data-toggle='tab' href='#h-" + netid_1 +"'>Info</a></li>"
        +"<li><a data-toggle='tab' href='#s-" + netid_1 +"'>Skills</a></li>"
        +"<li><a data-toggle='tab' href='#d-" + netid_1 +"'>Disciplines</a></li>"
        +"<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
        +"</div>"
        +"</div>"
        +"</div>"
        +"</div>");

$('#'+ netid_1).modal('show');

$('.skillsPieChart').radarChart({
size: [380, 300],
step: 1,
fixedMaxValue:5,
showAxisLabels: true
});

data = unformatted_info

console.log(data)


});
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
