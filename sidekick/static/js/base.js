$(window).load(function() {
    $("#modCarousel").carousel('cycle');

    //Run once/30 sec
    var shiftInfo;
    var techType = $(".shMeta .tech-type").text();
    if ($(".shMeta") && techType != "stt" && techType != "stm") {
        shiftInfo = setInterval(updateShiftInfo, 60000);
        updateShiftInfo();
    } else {
        shiftInfo = null;
    }

    function updateShiftInfo() {
        console.log("Updating Shift Info");
        var end = new Date($(".shMeta > .sh-end").text());
        var now = new Date();
        $("#shEndsIn").text(parseInt((end-now)/60000));


        var next_report = new Date();

        switch ($(".shMeta .tech-type").text()) {
        case "lbt":
            var interval = 0;
            if (now.getMinutes() >= 15) {
                interval = 60 * 60 * 1000;
                if (now.getMinutes() == 15) {
                    alert("Hi there! Just a friendly reminder that your rounds report is due :)");
                }
            }
            next_report = new Date(now.getTime() + interval);
            next_report.setMinutes(15);
            break;

        case "spt":
            next_report = new Date(end.getTime() - 10 * 60 * 1000);

            if (now.getHours() == next_report.getHours() && now.getMinutes() == next_report.getMinutes()) {
                alert("Your shift ends in 10 minutes! Don't forget to document :)");
            } else if (now > next_report) {
                next_report = now;
            }
            break;

        case "mgr":
            next_report.setHours(16);
            next_report.setMinutes(0);

            if (now.getHours() == next_report.getHours() && now.getMinutes() == next_report.getMinutes()) {
                alert("Hey you, time for the MoD Report! Keep being awesome!");
            } else if (now > next_report) {
                next_report = now;
            }
            break;
        }

        $("#shRoundsIn").text(parseInt((next_report - now) / 60000));
    }

});