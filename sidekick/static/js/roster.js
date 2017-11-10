/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////

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
        +"<div class='modal-dialog modal-lg'>"
        +"<div class='modal-content "+ color +" dev_"+ dev +"'>"
        +"<div class='modal-header'>"
        +"<h4 style='text-align: center' class='modal-title'>" + fullname + "</h4></div>"
        +"<div class='modal-body hero-bio'>"
        +"<div class='row'>"
        +"<img src='" + pic + "' class='img-circle img-herobio'>"
        +"<div class='hero-bio'>"
        +"<p>" + fullname +"</p>"
        +"<p>" + netid_1 + "</p>"
        +"<p>" + codename + "</p>"
        +"<p>" + position + "</p>"
        +"<p>" + phone + "</p>"
        +"<p>" + birthday + "</p>"
        +"</div>"
        +"</div>"
        +"</div>"
        +"<div class='modal-footer'>"
        +"<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>"
        +"</div>"
        +"</div>"
        +"</div>"
        +"</div>");

$('#'+ netid_1).modal('show');

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
