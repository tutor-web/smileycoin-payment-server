// ------------------------------------ listeneres...
var csrftoken;
var address;
$(function() {
	$("#verifyPayment").click(verifyPayment);
});

// ------------------------------------ getAddress functions
var getAddress = function(successCallback, errorCallback) {
	$.ajax({
		url:"http://localhost:5000/generateAddress",
		async:true,
		type:"GET",
		xhrFields: {
        	withCredentials: true
    	},
		success: function(result, xhr){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			csrftoken = getCookie('csrftoken');
			console.log("Managed to get the token? "+ csrftoken)
			handleResponse(result, successCallback, errorCallback);
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

var handleResponse = function(result, successCallback, errorCallback) {
	if(jsonSuccess(result)) {
		address = extractAddress(result);
		console.log("this is the new address " + address);
		var URL = makeNewUrl(address);
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


// -------------------------------- getTransaction funcions

var verifyPayment = function(successCallback, errorCallback) {
	$.ajax({
		url:"http://localhost:5000/verifyPayment",
		async:true,
		type:"POST",
		data:address,
		crossDomain: true,
		headers: {
        	"X-CSRFToken":csrftoken
    	},
		beforeSend: function(xhr) {
		    xhr.setRequestHeader("Cookie", "csrftoken="+csrftoken);
		},
		success: function(result){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			console.log(result);
			//handleResponse(result, successCallback, errorCallback);
		},
		error: function(xhr,ajaxOptions, thrownError){
			console.log(xhr);
			console.log(thrownError);
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