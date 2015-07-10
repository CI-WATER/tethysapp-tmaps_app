$("#select1").on('change',function() {
    if ($(this).val() == "1")
        $("#enter-name").show("slow");
    if ($(this).val() == "1")
	$("#upload-file").show("slow");
    if ($(this).val() == "1")
	$("#progress-bar").show("slow");
    if ($(this).val() == "2")
        alert("Unfortunately, TMAPS tools are still being developed for GSSHA. Stay tuned!");
    if ($(this).val() == "3")
        alert("Unfortunately, TMAPS tools are still being developed for RAPID. Stay tuned!");
});

$("#select5").on('change',function() {
    if ($(this).val() == "1")
        alert("Unfortunately, TMAPS tools are still being developed for GSSHA. Stay tuned!");
    if ($(this).val() == "2")
	alert("Unfortunately, TMAPS tools are still");
});

$("#select_input5").on('change',function() {
    var theIframe = document.getElementById('tmapsIframe');
    var theUrl;

    if ($(this).val() == "1")
        theUrl = "http://gme.byu.edu/tmaps_app_timemachines/greenriversnoweq.timemachine/view.html";
        theIframe.src = theUrl;
    if ($(this).val() == "2")
        theUrl = "http://gme.byu.edu/tmaps_app_timemachines/greenriver_surfacewaterdepthwomap.timemachine/view.html";
        theIframe.src = theUrl;
    if ($(this).val() == "3")
        theUrl = "http://gme.byu.edu//tmaps_app_timemachines/surfacewaterdepthwbasemap.timemachine/view.html";
        theIframe.src = theUrl;
});

