$(function() {
	$('#Booking_Payment_PaymentMethod').on('change', function(){
			if (this.value=="Smileycoin"){
				// Hide the card related stuff and then get address.
				// Get address function takes two callbacks to handle
				// successfully getting the address and any errors that might come up.
				hideCardRelated()
				getAddress(onGetAddressSuccess, onGetAddressFailure);			
			}
			else {
				hideSmileyRelated();
				showCardRelated();

			}
	}).trigger('change');
});

onGetAddressSuccess = function() {
	hideMessage();
	showSmileyRelated();
}

onGetAddressFailure = function() {
	showMessage();
	hideSmileyRelated();
}

hideCardRelated = function() {
	$("#korthafi").hide();
	$("#Booking_Payment_CardHolder").hide();
	$("#kortanumer").hide();
	$("#Booking_Payment_CardNumber").hide();
	$("#gildistimi").hide();
	$("#Booking_Payment_ExpirationDateMonth").hide();
	$("#Booking_Payment_ExpirationDateYear").hide();
	$("#cvcnumer").hide();
	$("#Booking_Payment_CVCode").hide();
	$(".asterisk").hide();
}

showCardRelated = function() {
	$("#korthafi").fadeIn("fast");
	$("#Booking_Payment_CardHolder").fadeIn("fast");
	$("#kortanumer").fadeIn("fast");
	$("#Booking_Payment_CardNumber").fadeIn("fast");
	$("#gildistimi").fadeIn("fast");
	$("#Booking_Payment_ExpirationDateMonth").fadeIn("fast");
	$("#Booking_Payment_ExpirationDateYear").fadeIn("fast");
	$("#cvcnumer").fadeIn("fast");
	$("#Booking_Payment_CVCode").fadeIn("fast");
	$(".asterisk").fadeIn("fast");
}

hideSmileyRelated = function() {
	$("#smileyamount").hide();
	$("#payWithSMLY").hide();
	$("#qrcode").hide();
}

showSmileyRelated = function() {
	$("#smileyamount").fadeIn("fast");
	$("#payWithSMLY").fadeIn("fast");
	$("#qrcode").fadeIn("fast");
}

showMessage = function() {
	$("#message").fadeIn("fast");
}

hideMessage = function() {
	$("#message").hide();
}
