var verified;
$(function() {
	verified = false;
	$("#verifyBox").click(changeVerifyBox);
});

changeVerifyBox = function() {
	if(verified) {
		$("#verifyBox").css("background-color", "#f2511d");
		document.getElementById("verifyText").innerHTML = "UNVERIFIED";
		verified = false;
	} else {
		$("#verifyBox").css("background-color", "#47BD4E");
		document.getElementById("verifyText").innerHTML = "VERIFIED";
		verified = true;
	}
}
	

