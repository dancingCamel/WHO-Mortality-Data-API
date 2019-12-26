const navLogout = $('#navLogout');
const navRegister = $('#navRegister');
const navLogin = $('#navLogin');

// navbar link redirects
navLogin.click(() => (window.location.href = '/login'));
navLogout.click(() => (window.location.href = '/logout'));
navRegister.click(() => (window.location.href = '/register'));

// form validation functions
function validCountry(country_code) {
	// country code is 4 digit number
	if (/^[0-9]{4}$/g.test(country_code) || country_code == '') {
		return true;
	}
	return false;
}

function validAdmin(admin_code) {
	// admin code is 3 digit number
	if (/^[0-9]{3}$/g.test(admin_code) || admin_code == '') {
		return true;
	}
	return false;
}

function validSubdiv(subdiv_code) {
	// subdiv code is a letter followed by two numbers
	if (/^[a-zA-z]{1}([\d]{2}$)/g.test(subdiv_code) || subdiv_code == '') {
		return true;
	}
	return false;
}

function validYear(year) {
	// year between 1950 (just before data begins) and current year
	var start_year = 1950;
	var this_year = new Date().getFullYear();
	if (start_year < Number(year) && Number(year) < this_year) {
		return true;
	}
	else if (year == '') {
		return true;
	}
	return false;
}

function validCause(cause_code) {
	// cause is either 4 numbers, 3 letters (AAA), 2 letters and 2 numbers, 1 letter and 2 numbers or 1 letter and 3 numbers
	if (/^([a-zA-Z]?)\d{2,3}$/g.test(cause_code)) {
		// check letter followed by two or three numbers
		return true;
	}
	else if (/^([a-zA-Z]{2})\d{2}$/g.test(cause_code)) {
		// check if two letters followed by two numbers
		return true;
	}
	else if (/^[0-9]{4}$/g.test(cause_code)) {
		//check all 4 numbers
		return true;
	}
	else if (/^AAA$/gi.test(cause_code)) {
		// check if AAA - all causes
		return true;
	}
	else if (cause_code == '') {
		return true;
	}
	return false;
}

// function to resize element
function auto_grow(element) {
	$(element).css('height', element[0].scrollHeight + 'px');
}
// function to capitalise the first letter
function capFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function getRandomColor() {
	var letters = '0123456789ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

// autocomplete function for text inputs
function addAutocomplete(element) {
	element = $(element);
	element.autocomplete({
		minLength : 3,
		source    : function(request, response) {
			var table = element[0].getAttribute('data-table');
			$.ajax({
				url      : '/api/' + table + '-search/' + request.term,
				dataType : 'json',
				headers  : { api_key: api_key },
				success  : function(data) {
					// .slice(0, 10) after results to shorten possibilities
					response(
						$.map(data['results'], function(item) {
							autocomplete_output = item.description + ' (' + item.code + ')';
							return {
								label : autocomplete_output,
								value : item.code
							};
						})
					);
				}
			});
		}
	});
}
