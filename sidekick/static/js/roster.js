/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////

$('.btn').click(function showModal(){

unformatted_info = $(this).find("ul")

netid_1 = $(this).find(".emp-meta").attr('id')

netid_1 = netid_1.slice(2)
console.log(netid_1)

$('#'+ netid_1).modal('show');

data = unformatted_info

console.log(data)


});
$("#searchbar").keyup(function () {
    var value = $("#searchbar").val().toLowerCase();

    console.log(value)

    if (value.length >= 1) {
        $(".panel[id*=" + value + "]").fadeIn(200);
        $(".panel:not([id*=" + value + "])").fadeOut(200);
    } else {
        $(".panel").fadeIn(200);
    }
});