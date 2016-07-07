// =======
// Globals
// =======

// SessionInfo = {csrftoken: , customerAddress: , amount: }
var sessionInfo = {"csrftoken": null, "customerAddress": null, "amount": null};
sessionInfo.amount = 200; //200 SMLY, this needs to be updated to some realistic value.


// =====================
// Get Address Functions
// =====================
var getAddress = function(successCallback, errorCallback) {
	$.ajax({
		url:"/generateAddress",
		async:true,
		type:"GET",
		xhrFields: {
        	withCredentials: true
    	},
		success: function(result, xhr){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			sessionInfo.csrftoken = getCookie('csrftoken');
			console.log("Managed to get the token? "+ sessionInfo.csrftoken);
			handleAddressResponse(result, successCallback, errorCallback);
		},
		error: function(xhr,ajaxOptions, thrownError){
			console.log(xhr);
			console.log(thrownError);
		}
	});
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
    }
    return "";
} 

var handleAddressResponse = function(result, successCallback, errorCallback) {
	if(jsonSuccess(result)) {
		newAddress = extractFromJson(result, 'address');
		console.log("this is the new address " + newAddress);
		console.log("SETTING CUSTOMER ADDRESS");
		sessionInfo.customerAddress = newAddress;
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
//var extractAddress = function(result) {
//	console.log($.parseJSON(result)['address']);
//	return ($.parseJSON(result)).address;
//}

var extractFromJson = function(result, key) {
	return ($.parseJSON(result))[key];
}


// Generates a new url/uri for the given address with amount 500000 smly:
var makeNewUrl = function(address) {
     return  "smileycoin:"+address+"?amount=1.0&label=airfare";
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


// ========================
// Verify Payment Functions
// ========================
var verifyPayment = function(successCallback, errorCallback) {
	console.log("CALLING VERIFY PAYMENT! THIS IS THE ADDRESS WE HAVE "+sessionInfo.customerAddress);
	$.ajax({
		url:"/verifyPayment",
		async:true,
		type:"POST",
		data:sessionInfo.customerAddress,
		crossDomain: true,
		headers: {
        	"X-CSRFToken":sessionInfo.csrftoken
    	},
		beforeSend: function(xhr) {
		    xhr.setRequestHeader("Cookie", "csrftoken="+sessionInfo.csrftoken);
		},
		success: function(result){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			console.log(result);
			handleVerifyResponse(result, successCallback, errorCallback);
		},
		error: function(xhr,ajaxOptions, thrownError){
			console.log(xhr);
			console.log(thrownError);
		}
	});
}

var handleVerifyResponse = function(result, successCallback, errorCallback) {
	//if(jsonSuccess(result)) {
		console.log("Verifying....");
		var amount = extractFromJson(result, 'amount');
		console.log("This is the amount we got "+amount);
		successCallback(amount, sessionInfo.amount);
	//} else {
	//	errorCallback("We couldn't verify the transaction at this time.");
	//}
}

