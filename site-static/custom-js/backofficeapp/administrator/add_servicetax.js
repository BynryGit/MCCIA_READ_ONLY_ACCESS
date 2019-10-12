$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")


$(document).ready(function(){
$(".sel2").select2({
            width: '100%'
        })
  });


function check_state(){
select_state=$("#select_state").val()
if (select_state == '1'){
//    $("#gst_div").hide()
    $("#cgst_div").hide()
    $("#sgst_div").hide()
    $("#igst_div").show()
}else{
//    $("#gst_div").show()
    $("#cgst_div").show()
    $("#sgst_div").show()
    $("#igst_div").hide()
}
}


function validateData(){
    select_state = $("#select_state").val()
    if (select_state == '0'){
        if(checktax("#cgst_tax") && checktax("#sgst_tax") && checktotal())
        {
            return true;
        }
        return false;
    }else{
        if(checktax("#igst_tax"))
        {
            return true;
        }
        return false;
    }

}

$("#save-continue").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
//		formData.append("gst",($('#gst').val()).trim());
		formData.append("cgst_tax",$('#cgst_tax').val());
		formData.append("sgst_tax",$('#sgst_tax').val());
		formData.append("igst_tax",$('#igst_tax').val());
		formData.append("select_state",$('#select_state').val());
  			$.ajax({
				type	: "POST",
				url : '/backofficeapp/save-servicetax-details/',
 				data : formData,
				cache: false,
		        processData: false,
		        contentType: false,
                success: function (response) {
                    if(response.success=='true'){
                            location.href = '/backofficeapp/administrator-servicetax-landing'
                        }
                        if (response.success == "false") {
                                $("#error-modal").modal('show');
                        }
                        else if (response.success == 'exist'){
                            $("#error-modal").modal('show');
                        }
                },
               	beforeSend: function () {
                    $("#processing").css('display','block');
                },
                complete: function () {
                    $("#processing").css('display','none');
                },
                error : function(response){
                  	alert("_Error");
            	}
            });
    }
});
function checktax(taxvalue){
checkvalue=$(taxvalue).val()
if (checkvalue != ''){
    if (parseFloat(checkvalue) > 100.00){
        $(taxvalue +'_error').css("display", "block");
        $(taxvalue +'_error').text("Value should not greater than 100");
        return false;
    }

    $(taxvalue +'_error').css("display", "none");
    return true
}else{
    $(taxvalue +'_error').css("display", "block");
    $(taxvalue +'_error').text("Please enter Value");
    return false;
}
}

function checktotal(){
    cgst_tax= $('#cgst_tax').val()
    sgst_tax= $('#sgst_tax').val()
    total = parseFloat(cgst_tax) + parseFloat(sgst_tax)
    if (total > 100){
        $('#sgst_tax_error').css("display", "block");
        $('#sgst_tax_error').text("Addition of CGST and SGST should not greater than 100");
        return false;
    }
return true
}


function validateFloatKeyPresss(obj,evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    var value = obj.value;
    var dotcontains = value.indexOf(".") != -1;
    if (dotcontains)
        if (charCode == 46) return false;
    if (charCode == 46) return true;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}