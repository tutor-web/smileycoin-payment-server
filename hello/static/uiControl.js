// =========
// Update UI
// =========

hideCardShowSmly = function() {
	$(".cardInformation").hide("fast");
	$(".asterisk").hide();
	$(".smlyInformation").fadeIn("fast");
	$("#paragraph").hide();
}

showCardHideSmly = function() {
	$(".smlyInformation").hide();
	$("#paragraph").fadeIn("fast");
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
		$("#verifyBox").css("border", "2px solid #ec8c47");
		document.getElementById("verifyText").innerHTML = "Greiðsla óstaðfest";
		verified = false;
	} else {
		$("#verifyBox").css("background-color", "#47BD4E");
		$("#verifyBox").css("border", "2px solid #91ec47");
		document.getElementById("verifyText").innerHTML = "Greiðsla staðfest";
		verified = true;
	}
}
	
