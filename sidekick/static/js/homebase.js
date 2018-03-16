
$(document).ready(function () {
    console.log("Homebase loaded");
    //TODO: Program the things!
    $(".e-form").hide();

    $(".create-e").click(function(){
      $(".a-form").hide();
      $(".e-form").show();
    });

    $(".create-a").click(function(){
      $(".e-form").hide();
      $(".a-form").show();
    });
});
