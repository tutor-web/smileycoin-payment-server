// =========
// Update UI
// =========

hideCardShowSmly = function() {
	$(".cardInformation").hide("fast");
	$(".asterisk").hide();
	$(".smlyInformation").fadeIn("fast");
}

showCardHideSmly = function() {
	$(".smlyInformation").hide();
	$(".cardInformation").fadeIn("fast");
	$(".asterisk").fadeIn("fast");
}

showMessage = function() {
	$("#message").fadeIn("fast");
}

hideMessage = function() {
	$("#message").hide();
}

setMessage = function(message) {
	$("#message").html(message);
}

changeVerifyBox = function(verified) {
	if(!verified) {
		$("#verifyBox").css("background-color", "#f2511d");
		document.getElementById("verifyText").innerHTML = "Greiðsla óstaðfest";
		verified = false;
	} else {
		$("#verifyBox").css("background-color", "#47BD4E");
		document.getElementById("verifyText").innerHTML = "Greiðsla staðfest";
		verified = true;
	}
}
	
