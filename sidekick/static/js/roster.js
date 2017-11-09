/////////////////////////////////////////
// JavaScript/Jquery for the quotes module
// Written by Brooks Duggan in Fall 2017
/////////////////////////////////////////

$('.btn').click(function showModal(){

unformatted_info = $(this).find("ul")
formatted_info = $(this).find("il")

netid_1 = $(this).find(".emp-meta").attr('id')
fname = $(netid_1).find(il).id(".emp-fname").text()

netid_1 = netid_1.slice(2)
console.log(fname)
console.log(netid_1)

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
