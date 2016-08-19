// =======
// GLOBALS
// =======
var csrfToken = null;
var sessionInfo = {"csrfToken": "", "address" : "", "amount" : 0};
var price = 10;
// so we can update the value
$(function() {
	
	sessionInfo.csrfToken = (document.cookie).split("=")[1];
	console.log("This is the cookie we got "+csrfToken);
	console.log("You should call update now");
	updateAmounts();
	console.log("Done updating");

	$("#verifyPayment").prop("disabled", false);
	$("#fundBtn").prop("disabled", false);
	$("#verifyPayment").removeClass("disabled");
	$("#fundBtn").removeClass("disabled");

	$("#amount").change(function() {
		updateAmounts();
	});

	$("#noItemsInput").change(function() {
		updateAmounts();
	});

	// Click event listener to verify payment button
	$("#verifyPayment").on('click', function() {
		$(this).prop("disabled", true);
		$(this).addClass("disabled");
		verifyPayment(onGetVerifySuccess, onGetVerifyFailure);
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
	$("#noItemsBox").html($("#noItemsInput").val());
}

// Submits a request to the server to purchase the
// items detailed in the form. The server will respond
// with a confirmation that the items exist on the server,
// reserve them and give the SMLY address for the user to pay to.
function submitPurchaseRequest() {
	console.log("We need to make sure were actually sending data");
	console.log("Here is the cartForm data");
	console.log($('#cartForm'));

	$("#fundBtn").prop("disabled", true);
	$("#fundBtn").addClass("disabled");
	
	$.ajax({
		url:"checkout.html",
		async:true,
		type:"POST",
		data:$('#cartForm').serialize(),
		crossDomain: true,
		headers: {
        	"X-CSRFToken":sessionInfo.csrfToken
    	},
		beforeSend: function(xhr) {
		    xhr.setRequestHeader("Cookie", "csrftoken="+sessionInfo.csrfToken);
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
		newAmount = extractFromJson(result, 'amount');
		sessionInfo.amount = newAmount;
		sessionInfo.address = newAddress;


		var URL = makeNewUrl();
		updatePaymentButton(URL);
		updateQRCode(URL);
		successCallback();
	} else {
		errorCallback(result);
	}
}

var jsonSuccess = function(result) {
	return (($.parseJSON(result)).message === "Success")
}

function enablePayment() {
	freezePurchase();
	configAndShowPayment();
	fixFooter();
}

function fixFooter() {
       
	var footerHeight = 0,
           footerTop = 0,
           $footer = $("#footer");
           
       positionFooter();
       
       function positionFooter() {
       
                footerHeight = $footer.height();
                footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px";
                heightDifference = $("body").height() - $('.container').height()-$("header").height()-$("footer").height();
       
               if ( ($(document.body).height()+footerHeight) < $(window).height()) {
                   console.log("IS THIS HAPPENING?");
                   $footer.css({
                        position: "absolute"
                   }).animate({
                        top: footerTop
                   })
               } else {
                   console.log("OR THIS? Height difference "+heightDifference);
                   $footer.css({
                        position: "relative",
                        top: heightDifference
                   })
               }
               
       }

       $(window)
               .scroll(positionFooter)
               .resize(positionFooter)
               
}

function freezePurchase() {
	$("#cartForm").removeClass("activePayment").addClass("fixedPayment");
	return;
}

function configAndShowPayment() {
	$(".paymentInterface").fadeIn("fast");
}

function reportError(request) {
	console.log("CALLING ERROR")
	var errorMsg = extractFromJson(request, "message");
	setMessage(errorMsg);
	showMessage();
	return;
}


var extractFromJson = function(result, key) {
	return ($.parseJSON(result))[key];
}


// Generates a new url/uri for the given address with sessionInfo.amount smly:
var makeNewUrl = function() {
     return  "smileycoin:"+sessionInfo.address+"?amount="+sessionInfo.amount+"&label=airfare";
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
		sessionInfo.address = newAddress;
		var URL = makeNewUrl(newAddress);
		updatePaymentButton(URL);
		updateQRCode(URL);
		successCallback();
	} else {
		errorCallback();
	}
}



// ========================
// Verify Payment Functions
// ========================
var verifyPayment = function(successCallback, errorCallback) {
	console.log("CALLING VERIFY PAYMENT! THIS IS THE ADDRESS WE HAVE "+sessionInfo.address);
	$.ajax({
		url:"/verifyPayment",
		async:true,
		type:"POST",
		data:sessionInfo.address,
		crossDomain: true,
		headers: {
        	"X-CSRFToken":sessionInfo.csrfToken
    	},
		beforeSend: function(xhr) {
		    xhr.setRequestHeader("Cookie", "csrftoken="+sessionInfo.csrfToken);
		},
		success: function(result){
			// Handle a successful response based on whether the server
			// actually managed to get an address or not. 
			successCallback(result);
		},
		error: function(xhr,ajaxOptions, thrownError){
			errorCallback(result);
			console.log(xhr);
			console.log(thrownError);
		}
	});
}


onGetVerifySuccess = function(result) {
	var paymentStatus = extractFromJson(result, "status");
	var paidAmount = extractFromJson(result, 'amount');
	if(paymentStatus === "PAID") {
		console.log("PAID IS HAPPENING");
		changeVerifyBox(true);
		deliverProduct(result);
	} 
	else {
		console.log("UNPAID IS HAPPENING");
		setMessage("Þú hefur greitt upphæð "+paidAmount+" SMLY. Eftirstöðvar: -"+(sessionInfo.amount-paidAmount)+" SMLY.");
		showMessage();
		$("#verifyPayment").prop("disabled", false);
		$("#verifyPayment").removeClass("disabled");
	}
}

onGetVerifyFailure = function(result) {
	setMessage(message);
	showMessage();
	$("#verifyPayment").prop("disabled", false);
	$("#verifyPayment").removeClass("disabled");
}

deliverProduct = function(result) {
	var injectedHTML = 'Greiðsla samþykkt. <ul class="product">';

	couponJSON = extractFromJson(result, "coupon");
	for(var key in couponJSON) {
		couponName = couponJSON[key].product;
		couponCode = couponJSON[key].code;
		injectedHTML += '<li>'+couponName+': <h2>'+couponCode+'</h2></li>';
	}

	injectedHTML += '</ul>'

	setMessage(injectedHTML);
	showMessage();
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


showMessage = function() {
	$("#message").fadeIn("fast");
}

hideMessage = function() {
	$("#message").hide();
}

setMessage = function(message) {
	$("#message").html(message);
}