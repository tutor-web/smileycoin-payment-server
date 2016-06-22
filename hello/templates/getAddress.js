
var getAddress = function(successCallback, errorCallback) {
	$.ajax({
		url:"https://smileyservice.herokuapp.com/generateAddress",
		async:true,
		type:"GET",
		success: function(result){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			handleResponse(result, successCallback, errorCallback);
		},
		error: function(xhr,ajaxOptions, thrownError){
			console.log(xhr);
		}
	});
}

var handleResponse = function(result, successCallback, errorCallback) {
	if(jsonSuccess(result)) {
		var newAddress = extractAddress(result);
		console.log("this is the new address " + newAddress);
		var URL = makeNewUrl(newAddress);
		updatePaymentButton(URL);
		updateQRCode(URL);
		successCallback();
	} else {
		errorCallback();
	}
}

var jsonSuccess = function(result) {
	return (($.parseJSON(result)).message === "Success")
}

// Gets the address value from a JSON like {address: <somesmileycoinaddress>}
var extractAddress = function(result) {
	return ($.parseJSON(result)).address;
}


// Generates a new url/uri for the given address with amount 500000 smly:
var makeNewUrl = function(address) {
     return  "smileycoin:"+address+"?amount=500000.0&label=airfare";
}

// updates the payment button of the site with the new url
var updatePaymentButton = function(url) {
	$('#payWithSMLYURL').attr("href", url);
}

// updates the QR code of the site with the new url
var updateQRCode = function(url) {
	$('#qrcode')[0].innerHTML="";
	new QRCode($('#qrcode')[0], url);
}
