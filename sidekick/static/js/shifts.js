/////////////////////////////////////////
// JavaScript/Jquery for the shifts module
// Written by Josh Wood in Fall 2017
/////////////////////////////////////////


$(document).ready(function() {
    // This triggers when the user clicks the post button, mostly dev fiddling right now
    $('#post-cover-btn').click(function(){
        $('#post-det').hide();        
        $('#posting-progress').addClass('loader');
        setTimeout(function(){
            $('#posting-progress').removeClass('loader');            
            $('#post-conf').modal('toggle');
        }, 2000);
    });
});    