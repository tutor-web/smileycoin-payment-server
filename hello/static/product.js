// =======
// GLOBALS
// =======
var csrfToken = null;
var price = 50000;
// so we can update the value
$(function() {

	csrfToken = (document.cookie).split("=")[1];
	console.log("This is the cookie we got "+csrfToken);
	console.log("You should call update now");
	updateAmounts();
	console.log("Done updating");

	$("#amount").change(function() {
		updateAmounts();
	});

	$("#noItems").change(function() {
		updateAmounts();
	});
});

// Grabs the data from the form fields, updates the UI accordingly
// and sets the price of the Dalpay form as the number from the number field.
function updateAmounts() {
	console.log("Calling Update() new");
	$("#prodPrice").html(parseAmountString(price.toString(), "SMLY")["stringVal"]);
	var totalPrice = parseAmountString(($("#noItemsInput").val()*price).toString(), "SMLY");
	$("#totPrice").html(totalPrice["stringVal"]);
	//$("#totPriceInput").html(totalPrice["amountVal"]);
	$("input[name=totPrice]").val(totalPrice["amountVal"]);
	//var current = getCurrentData();
	//updateUI(current);
	//updateDalpayBtn(current);
}

// Submits a request to the server to purchase the
// items detailed in the form. The server will respond
// with a confirmation that the items exist on the server,
// reserve them and give the SMLY address for the user to pay to.
function submitPurchaseRequest() {
	console.log("We need to make sure were actually sending data");
	console.log("Here is the cartForm data");
	console.log($('#cartForm'));
	$.ajax({
		url:"checkout.html",
		async:true,
		type:"POST",
		data:$('#cartForm').serialize(),
		crossDomain: true,
		headers: {
        	"X-CSRFToken":csrfToken
    	},
		beforeSend: function(xhr) {
		    xhr.setRequestHeader("Cookie", "csrftoken="+csrfToken);
		},
		success: function(result){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			console.log(result);
			handleResponse(result, enablePayment, reportError);
			//handleVerifyResponse(result, successCallback, errorCallback);
		},
		error: function(xhr,ajaxOptions, thrownError){
			console.log(xhr);
			console.log(thrownError);
		}
	});
}


function handleResponse(result, successCallback, errorCallback) {
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

function enablePayment() {
	freezePurchase();
	configAndShowPayment();
}

function freezePurchase() {
	return;
}

function configAndShowPayment() {
	$(".paymentInterface").fadeIn("fast");
}

function reportError() {
	return;
}


var extractFromJson = function(result, key) {
	return ($.parseJSON(result))[key];
}


// Generates a new url/uri for the given address with sessionInfo.amount smly:
var makeNewUrl = function(address) {
     return  "smileycoin:"+address+"?amount="+sessionInfo.amount+"&label=airfare";
}


// updates the payment button of the site with the new url
var updatePaymentButton = function(url) {
	/*$('#payWithSMLY').click(function() {
		try {
			window.location.href = url;
		} catch(err) {
			window.location.href = "https://play.google.com/store/apps/details?id=hashengineering.smileycoin.wallet&hl=en";
		}
	});*/
	$('#payWithSMLY').attr("onclick", "location.href='"+url+"';");
}

// updates the QR code of the site with the new url
var updateQRCode = function(url) {
	$('#qrcode')[0].innerHTML="";
	new QRCode($('#qrcode')[0], url);
}


// old 
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







// =============================
// AMOUNT STRING-INT CONVERSIONS
// =============================

// Parses input of the form 
// 10000
// 10.000,-
// 10.000
// 10000 ISK
// 10.000 ISK
// ... etc
function parseInput(amountField, ticker) {
	return parseAmountString($(amountField).val(), ticker);
}

// Grab input as above and create an object like
// {"amountVal": 1000, "stringVal": "1.000 ISK"}
function parseAmountString(amountStr, ticker) {
	var input = amountStr;
	var amount = (input.split(",")[0]).replaceAll(".", "").replaceAll(" ", "").replaceAll("-").replaceAll("ISK", "");
	amount = parseInt(amount);
	// Return var:
	var current = {"stringVal": null, "amountVal": null}
	if(!isNaN(amount)) {
		// Update current and update the input field
		current["amountVal"] = amount;
		current["stringVal"] = addCommas(current["amountVal"])+" "+ticker;
	} else {
		current["amountVal"] = 0;
		current["stringVal"] = "0 "+ticker;
	}

	return current;
}


// A function to replace all occurrences of str1 with str2
String.prototype.replaceAll = function(str1, str2, ignore) {
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
} 

// Function to add commas so we can make a nice string with the amount
function addCommas(nStr) {
	nStr += '';
	x = nStr.split('.');
	x1 = x[0];
	x2 = x.length > 1 ? '.' + x[1] : '';
	var rgx = /(\d+)(\d{3})/;
	while (rgx.test(x1)) {
		x1 = x1.replace(rgx, '$1' + '.' + '$2');
	}
	return x1 + x2;
}

