// JavaScript Document
//$( document ).ready(function() {


jQuery.validator.addMethod("dollarsscents", function(value, element) {
        return this.optional(element) || /^\d{0,9}(\.\d{0,2})?$/i.test(value);
    }, "You must include two decimal places");

$.validator.addMethod("panNumber", function(value, element) {
	return this.optional(element) || /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/.test(value);
}, "Invalid Pan Number");

$.validator.addMethod("udyogAadhar", function(value, element) {
  return this.optional(element) || /(([A-Z]{2})([0-9]{2})([A-Z]{1})([0-9]{7}))|([0-9]{12})$/.test(value);
}, "Invalid Aadhar");

$.validator.addMethod("gstNumber", function(value, element) {
  return this.optional(element) || /^([a-zA-Z0-9]){15}?$/.test(value);
}, "Invalid GST Number");


$.validator.addMethod("ifscCode", function(value, element) {
	return this.optional(element) || /^([a-zA-Z]){4}([0-9]){7}?$/.test(value);
}, "Invalid IFSC");

jQuery.validator.addMethod("propertyLogoFormat", function(value, element){
    if (/^(.*\.(?!(png|jpg)$))?[^.]*$/i.test(value)) {
        return false;  // FAIL validation when REGEX matches
    } else {
        return true;   // PASS validation otherwise
    };
}, "Please upload .jpg or .png file format");

jQuery.validator.addMethod("policiesLicensesFileFormat", function(value, element){
    if (/^(.*\.(?!(pdf)$))?[^.]*$/i.test(value)) {
        return false;  // FAIL validation when REGEX matches
    } else {
        return true;   // PASS validation otherwise
    };
}, "Please upload .pdf file format");

//minStrict
$.validator.addMethod('minStrict', function (value, el, param) {
  return value > param;
}, "Enter value greater than zero");

$.validator.addMethod('minStrict1', function (value, el, param) {
  return value > param;
}, "Enter value greater than one");

//Duration validation
$.validator.addMethod('endYearGreaterThanOrEqualTO',
function (value, element, params) {
  if (!/Invalid|NaN/.value) {
    if ($(params[1]).val() != 0) {
      if (value == 9999) {
        return false;
      } else {
        return value >= $(params[0]).val();
      }
    } else {
      if (value == 9999) {
        return true;
      } else {
        return false;
      }
    }
  }
  return isNaN(value) && isNaN($(params[2]).val());
  //|| (Number(value) >= Number($(params[2]).val())); 
}, 'Must be greater than start year.');

$.validator.addMethod('endMonthGreaterThanOrEqualTO',
function (value, element, params) {
  if (!/Invalid|NaN/.value) {
    if ($(params[0]).val() == $(params[1]).val()) {
      return value > $(params[2]).val();
    } else {
      return value;
    }
  }
  return isNaN(value) && isNaN($(params[2]).val());
  //|| (Number(value) >= Number($(params[2]).val())); 
}, 'Must be greater than start Month.');

//file size validation
$.validator.addMethod('filesize', function (value, element, param) {
  return this.optional(element) || (element.files[0].size <= param)
});

//password validation (This will match 1 or more uppercase characters, 1 or more lowercase characters and 1 or more digit/special character) and at least 8 char
$.validator.addMethod("passwordcheck", function (value) {
  return /[A-Z]+/.test(value) && /[a-z]+/.test(value) &&
  /[\d\W]+/.test(value) && /\S{8,}/.test(value);
}, 'Must contain minimum 8 characters including 1 Upper, 1 Lower and 1 or more digit/special char');

// select value not null check
$.validator.addMethod("valueNotEquals", function (value, element, arg) {
  return arg != value;
}, "Value must not equal arg.");

// regx for companyName - alphanumaric , - , _ , space, [], ()
$.validator.addMethod("AddressFieldRegEx", function (value, element) {
  return this.optional(element) || /^[a-z\d\-_.\[\]\(\)\/\,\#\@\s]+$/i.test(value);
}, "Must contain only letters, numbers, dot, comma, [], (), dashes or underscore.");

// regx for cityNameRegex - alphanumaric , - , _ , space
$.validator.addMethod("cityNameRegex", function (value, element) {
  return this.optional(element) || /^[a-z\d\s]+$/i.test(value);
}, "It allows alphanumeric characters only.");

// regx for countryCode - alphanumaric , - , _ , space
$.validator.addMethod("countryCodeRegex", function (value, element) {
  //return this.optional(element) || /^\+?\d+$/i.test(value);
  return this.optional(element) || /^[+]\d+$/i.test(value);
  
}, "Country code is not valid.");


$.validator.addMethod("laxEmail", function(value, element) {
  // allow any non-whitespace characters as the host part
  return this.optional( element ) || /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test( value );
}, 'Please enter a valid email address.');





// regx for alphabet and space
$.validator.addMethod("alpha", function (value, element) {
  return this.optional(element) || /^[a-zA-Z\d\s]+$/i.test(value);
}, "Must contain alphabet characters only.");

// regx for alphanumaric , - , _ , space
$.validator.addMethod("alphanumaricRegex", function (value, element) {
  return this.optional(element) || /^[A-Za-z0-9_$&+,:;=?@#|<>.-^*()%!\s]*$/i.test(value);
//  return this.optional(element) || /^[^a-zA-Z\d\s]+$/i.test(value);
}, "It allows alphanumeric characters only.");

$.validator.addMethod("designationRegex", function (value, element) {
  return this.optional(element) || /^[a-z\d\-_.\s]+$/i.test(value);
}, "Must contain only letters, numbers, dot, dashes or underscore.");
// regx for MM/DD/YYYY
$.validator.addMethod("dateRegex", function (value, element) {
    //return this.optional(element) || /^((0[1-9]|1[0-2])\/((0|1)[0-9]|2[0-9]|3[0-1])\/((19|20)\d\d))$/i.test(value);
	return this.optional(element) || /^[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{4}$/i.test(value);
}, "Enter Date in MM/DD/YYYY format.");

$.validator.addMethod("timeRegex", function(value, element) {  
    return this.optional(element) || /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/i.test(value);  
}, "Please enter a valid time.");

$.validator.addMethod("roles", function(value, elem, param) {
    if($(".roles:checkbox:checked").length > 0){
       return true;
   }else {
       return false;
   }
},"You must select at least one!");

 $.validator.addMethod('selectcheck', function (value) {
        return (value != 'default');
    }, "country required");

// regx for countryCode - alphanumaric , - , _ , space
$.validator.addMethod("countryCodeRegex", function (value, element) {
  return this.optional(element) || /^[+]\d+$/i.test(value);
}, "Country code is not valid.");

// regx for landlineRegex - alphanumaric , - , _ , space
$.validator.addMethod("landlineRegex", function (value, element) {
  return this.optional(element) || /^([0-9]{3,4}[\-]{1}[0-9]{8,10})$/i.test(value);
}, "Landline is not valid.");




// regx for STDNumber - alphanumaric , - , _ , space
$.validator.addMethod("STDNumber", function (value, element) {
  return this.optional(element) || /^([0-9]{2,6})$/i.test(value);
}, "Number required");

// regx for landlineRegex - alphanumaric , - , _ , space
$.validator.addMethod("landlineContactRegex", function (value, element) {
  return this.optional(element) || /^([0-9]{8,10})$/i.test(value);
}, "Number is required");


$("form").validate({
  ignore: [],  
  onsubmit: false,
  //ignore: ':hidden:not(.validateField input)',
  onkeyup: function (element) { $(element).valid() },
  errorClass: 'help-block',
  errorElement: 'span',
  errorPlacement: function (error, e) {
    e.closest('.validateField').append(error);
    return false;
  },
  highlight: function (e, errorClass, validClass) {
    
    $(e).closest('.validateField').removeClass('has-success has-error').addClass('has-error');
    $(e).closest('.help-block').remove();
    return false;
  },
  success: function (e) {
    
    // You can remove the .addClass('has-success') part if you don't want the inputs to get green after success!
    e.closest('.validateField').removeClass('has-success has-error').addClass('has-success');
    e.closest('.help-block').remove();
    return false;
  },
  rules: {
            country: {
                selectcheck: true
            }
        },
  
});

$.validator.addClassRules({

  /*about Company*/
  validateRequired: {
    required: true
  },
  validateAlphaonly: {
    alpha: true
  },
  validateAlphanumaric: {
    alphanumaricRegex: true
  },
  validateNumber: {
    digits: true
  },
  validateDecimalNumber: {
    dollarsscents: true
  },
  validateEmail: {
    laxEmail: true
  },
  validateURL: {
	url: true
  },
  validatePassword: {
    passwordcheck: true
  },
  validateConfirmPassword: {
    equalTo: '.validatePassword'
  },
  
  validateMobileNoLimit: {
    minlength: 10,
    maxlength: 10,
    digits: true
  },
  validatePincodeLimit: {
    minlength: 6,
    maxlength: 6,
    digits: true
  },
  validateTelephoneNoLimit: {
    minlength: 13,
    maxlength: 15,
    landlineRegex: true
  },
  
  validatetxtDesignation: {
	 designationRegex: true
  },
  
  validateDate: {
      dateRegex: true
  },
  
  validateTime: {
      timeRegex: true
  },
  
  validateMinStrict: {
    minStrict: 0
  },

  validateSubvenueCount: {
    minStrict1: 1
  },
  validateAddressField: {
    AddressFieldRegEx:true
  },
  validatePropertyLogo: {
	required: false,
    propertyLogoFormat: true
  },
  validatePoliciesLicensesFileFormat: {
	 policiesLicensesFileFormat: true
  },
  validatePanNumber: {
	  panNumber: true
  },
  validateUdyogAadhar: {
    udyogAadhar: true
  },
  validateGSTNumber: {
    gstNumber: true
  },
  validateIFSC: {
	  ifscCode: true
  },
  validateAtleastOne: {
    require_from_group: [1, ".validateAtleastOneHidden"]
  },
  validateAtleastOneAdvanceSearch: {
    require_from_group: [1, ".advanceSearchHiddenField"]
  },
  validateCountryCode: {
    countryCodeRegex: true 
  },
  validateSTDNumber: {
    STDNumber: true
  },
  validatelandlineContactNumber: {
    landlineContactRegex: true
  },

});

jQuery.extend(jQuery.validator.messages, {
    /*required: "This field is required.",
    remote: "Please fix this field.",
    email: "Please enter a valid email address.",
    url: "Please enter a valid URL.",
    date: "Please enter a valid date.",
    dateISO: "Please enter a valid date (ISO).",
    number: "Please enter a valid number.",
    digits: "Please enter only digits.",
    creditcard: "Please enter a valid credit card number.",
    equalTo: "Please enter the same value again.",
    accept: "Please enter a value with a valid extension.",*/
    maxlength: jQuery.validator.format("Please enter no more than {0} digits."),
    minlength: jQuery.validator.format("Please enter at least {0} digits.")
/*    rangelength: jQuery.validator.format("Please enter a value between {0} and {1} characters long."),
    range: jQuery.validator.format("Please enter a value between {0} and {1}."),
    max: jQuery.validator.format("Please enter a value less than or equal to {0}."),
    min: jQuery.validator.format("Please enter a value greater than or equal to {0}.")*/
});

$('.validateContainer .checkValidationBtn').click(ValidateAndSubmit);

function ValidateAndSubmit(evt) {
  var $group = $(evt.currentTarget).parents('.validateContainer');
  var isValid = true;
  //$group.find(':input').each(function (i, item) {
  $group.find('.validateField .form-control').each(function (i, item) {
    if (!$(item).valid())
      isValid = false;
  });
  if (!isValid)
    evt.preventDefault();
	
	
    //var errorDiv = $('.has-error').first();
	//var scrollPos = errorDiv.offset().top - 150;
	//$(window).scrollTop(scrollPos);
}

//});

/*function pageLoad() {
	$('.validateContainer .checkValidationBtn').click(ValidateAndSubmit);
}*/

/*$("#ctl00_ContentPlaceHolder1_FULogo").change(function() {

    var val = $(this).val();

    switch(val.substring(val.lastIndexOf('.') + 1).toLowerCase()){
        case 'jpg': case 'png':
            alert("an image");
            break;
        default:
            $(this).val('');
            // error message here
            alert("not an image");
            break;
    }
});*/
