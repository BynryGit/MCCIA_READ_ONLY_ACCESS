

$("#publication_anchor").addClass("tab-active");
$("#publication_nav").addClass("active");
$("#publication_icon").addClass("icon-active");
$("#publication_active").css("display", "block");

function check_magazine() {
	select_magazine = $("#select_magazine").val()
	if (select_magazine == '0') {
		$("#pub_img_div").show()
		$("#pub_file_div").show()
		$("#vol_div").hide()
		$("#issue_no").hide()
		$('#publication_image_error').hide()
		$('#publication_file_error').hide()

	} else if (select_magazine == '1') {
		$("#pub_img_div").show()
		$("#pub_file_div").show()
		$("#vol_div").hide()
		$("#issue_no").hide()
		$('#publication_image_error').hide('')
		$('#publication_file_error').hide('')
	} else {
		$("#pub_img_div").hide()
		$("#pub_file_div").show()
		$("#vol_div").show()
		$("#issue_no").show()
		$('#publication_file_error').hide('')


	}

}


$("#save-btn").click(function (event) {
	if (validateData()) {
		event.preventDefault();

		var formData = new FormData();

		var input = document.getElementById("publication_image");
		publication_image = input.files[0];
		formData.append("publication_image", publication_image);

		var input = document.getElementById('publication_file');
		publication_file = input.files[0];
		formData.append("publication_file", publication_file);

		formData.append("volume_number", $('#volume_number').val());
		formData.append("issue_number", $('#issue_number').val());
		formData.append("select_magazine", $('#select_magazine').val());
		formData.append("publish_date", $('#publish_date').val());

		$.ajax({
			type: "POST",
			url: "/publicationapp/save-new-publication/",
			data: formData,
			cache: false,
			processData: false,
			contentType: false,
			success: function (response) {
				console.log('response', response);
				if (response.success == "true") {
					bootbox.alert("<span class='center-block text-center'>Publication added successfully</span>", function () {
						location.href = '/publicationapp/publication-landing/'
					});
				} else("#errorMessage")
			},
			error: function (response) {
				bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
			},
			beforeSend: function () {
				$("#processing").show();
			},
			complete: function () {
				$("#processing").hide();
			}
		});
	}
});

function validateData() {
	if ($('#select_magazine').val() == "0" || $('#select_magazine').val() == "1"){
	    if (checkPublicationFile("#publication_file") & checkPublicationImage("#publication_image") & check_publishDate("#publish_date")){
		    return true;
		}
	}
	else{
	    if (checkPublicationFile("#publication_file") & checkVolumeNumber("#volume_number") & check_issueNumber("#issue_number") & check_publishDate("#publish_date")){
            return true;
	    }
    }
	return false;
}



	function checkPublicationFile(publication_file) {
		if ($('#publication_file').val() == '') {
			$(publication_file_error).css("display", "block");
			$(publication_file_error).text("Please Upload File");
			return false;
		} else {
			$(publication_file_error).css("display", "none");
			return true;
		}
	}


	function checkPublicationImage(publication_image) {
		if ($('#publication_image').val() == '') {
			$(publication_image_error).css("display", "block");
			$(publication_image_error).text("Please Upload Image");
			return false;
		} else {
			$(publication_image_error).css("display", "none");
			return true;
		}
	}


	function checkVolumeNumber(volume_number) {
		if ($('#volume_number').val() == '') {
			$(volume_number_error).css("display", "block");
			$(volume_number_error).text("Please Enter Volume Number");
			return false;
		} else {
			$(volume_number_error).css("display", "none");
			return true;
		}
	}

	function check_issueNumber(issue_number) {
		if ($('#issue_number').val() == '') {
			$(issue_number_error).css("display", "block");
			$(issue_number_error).text("Please Enter Issue Number");
			return false;
		} else {
			$(issue_number_error).css("display", "none");
			return true;
		}
	}

	function check_publishDate(publish_date) {
		if ($('#publish_date').val() == '') {
			$(publish_date_error).css("display", "block");
			$(publish_date_error).text("Please Enter Date");
			return false;
		} else {
			$(publish_date_error).css("display", "none");
			return true;
		}
	}

