// =========
// Listeners
// =========
$(function() {
	// onChange listener to dropdown menu so we can get smileycoin address
	$('#Booking_Payment_PaymentMethod').on('change', function(){
			if (this.value=="Smileycoin"){
				// Hide the card related stuff and then get address.
				// Get address function takes two callbacks to handle
				// successfully getting the address and any errors that might come up.			
				getAddress(onGetAddressSuccess, onGetAddressFailure);			
			}
			else {
				showCardHideSmly();
			}
	}).trigger('change');

	// Click event listener to verify payment button
	$("#verifyPayment").on('click', function() {
		verifyPayment(onGetVerifySuccess, onGetVerifyFailure);
	});
});

// ========================
// Success/Failure handlers
// ========================

onGetAddressSuccess = function() {
	hideMessage();
	hideCardShowSmly()
}

onGetAddressFailure = function() {
	setMessage("We couldn't get a smileycoin address for you at this time. Please try again later.");
	showMessage();
	//hideSmileyRelated();
}

onGetVerifySuccess = function(message) {
	changeVerifyBox();
	setMessage(message);
	showMessage();
}

onGetVerifyFailure = function() {
	setMessage(message);
	showMessage();
}

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
	$("#message").innerHTML = message;
}

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
	
