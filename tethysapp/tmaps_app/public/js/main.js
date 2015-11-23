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

    var tm_passed_list = $('#tmapsIframe').attr('data-tm_info');
    tm_passed_list = JSON.parse(tm_passed_list);


    var tm_num = $(this).val();
    tm_num = tm_num-1;



    var theIframe = document.getElementById('tmapsIframe');
    var theUrl;


    theUrl = tm_passed_list[tm_num][2];
    theIframe.src = theUrl;

});

