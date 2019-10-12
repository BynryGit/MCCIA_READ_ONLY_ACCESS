$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");


$("#save_new_hall_equipment").click(function(event) {
	$("#equipment_nameDiv").addClass("has-success").removeClass("has-error");
   if ($("#equipment_name").val() != ''){
    $.ajax({
        type: "POST",
        url: '/backofficeapp/save-new-hall-equipment/',
        data: $("#add_new_hall_equipment").serialize(),
        success: function(response) {
            if (response.success == 'true') {
                $("#success_modal").modal('show');
            }
            if (response.success == "false") {
                $("#error-modal").modal('show');
            }
        },
        beforeSend: function() {
            $("#processing").css('display', 'block');
        },
        complete: function() {
            $("#processing").css('display', 'none');
        },
        error: function(response) {
            alert("_Error");
        }
    });
  }
  else {
  		$("#equipment_nameDiv").addClass("has-error").removeClass("has-success");
  }
});