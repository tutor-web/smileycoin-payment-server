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

/*	$( window ).resize(function() {
		if($(".rowFlexContainer").width() > 512) {
			$(".largeFlexItem").css("max-width", "256px");
		} else {
			$(".largeFlexItem").css("max-width", "1000px");
		}
	});*/
});

// ========================
// Success/Failure handlers
// ========================

onGetAddressSuccess = function() {
	hideMessage();
	hideCardShowSmly()
}

onGetAddressFailure = function() {
	setMessage("Ekki tókst að sækja smileycoin reikning á þessari stundu. Vinsamlegast reynið aftur síðar	.");
	showMessage();
	//hideSmileyRelated();
}

onGetVerifySuccess = function(paidAmount, expectedAmount) {
	console.log("Success callback ");
	console.log("Paid amount is "+paidAmount);
	console.log("Expected amount is "+expectedAmount);
	msg = "Þú hefur greitt upphæð "+paidAmount+" SMLY.";		
	if(paidAmount >= expectedAmount) {
		msg += " Greiðsla tókst!."
		changeVerifyBox(true);
	} else msg += " Eftirstöður: -"+(expectedAmount-paidAmount)+" SMLY.";
	setMessage(msg);
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
	$("#message").html(message);
}

changeVerifyBox = function(verified) {
	if(verified) {
		$("#verifyBox").css("background-color", "#f2511d");
		document.getElementById("verifyText").innerHTML = "Greiðsla óstaðfest";
		verified = false;
	} else {
		$("#verifyBox").css("background-color", "#47BD4E");
		document.getElementById("verifyText").innerHTML = "Greiðsla staðfest";
		verified = true;
	}
}
	
