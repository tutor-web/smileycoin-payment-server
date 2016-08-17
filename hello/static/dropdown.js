var giftRatio = 2;

// On page rendering, add a click event and onChange event to the amount field
// so we can update the value
$(function() {

	// Update the page on pageload...
	update();

	$(".dropdown").hover(
		function(event) { triggerDropDown(event.target); }, // onHover function
		function(event) { triggerDropDown(event.target); }
    );

	$('.dropdown-content').each(function() {
		$parentWidth = $(this).parent().width();
		console.log("For this one "+$(this)+" the parent width is 0"+$parentWidth);
		$(this).width($parentWidth);
	});

	//$('.dropdown-content').width($(this).parent().width());
});

// Grabs the data from the form fields, updates the UI accordingly
// and sets the price of the Dalpay form as the number from the number field.
function update() {
	return;
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function triggerDropDown(target) {
	var dropdownContent = null;
	if($(target).hasClass('dropbtn')) {
		dropdownContent = $(target).parent().children('.dropdown-content')[0];
	} else if($(target).hasClass('dropdown-content')) {
		dropdownContent = $(target);
	} else if($(target).hasClass('dropdown')) {
		dropdownContent = $(target).children('.dropdown-content')[0];
	} else {
		dropdownContent = $(target).parent().parent().children('.dropdown-content')[0];
	} 

	dropdownContent.classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
