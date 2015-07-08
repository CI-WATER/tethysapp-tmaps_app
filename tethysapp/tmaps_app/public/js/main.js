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
