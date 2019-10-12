    $("#hall_booking_anchor").addClass("tab-active");
    $("#hall_booking_nav").addClass("active");
    $("#hall_booking_icon").addClass("icon-active");
    $("#hall_booking_active").css("display", "block");

$(document).ready(function () {
	get_blacklisting_datatable();
});

function change_data(){
	get_blacklisting_datatable();
}

// Function for validate remark&date while changing user status

function validateDate(){
    if($('#blacklisting_date').val() == '' || $('#blacklisting_date').val() == null){
       bootbox.alert("<span class='center-block text-center'>Please Select Date</span>");
       return false;
    } else{
        return true;
    }
}

function validateRemark(){
    if($('#remark').val() == '' || $('#remark').val() == null){
       bootbox.alert("<span class='center-block text-center'>Please Enter Remark</span>");
       return false;
    } else{
        return true;
    }
}

function validateDetails(){
    if(validateDate() & validateRemark()){
        return true;
    }
    return false;
}

function get_blacklisting_datatable(){
        var table = $('#blacklisting_table');
	     sort_var = $('#sortby :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/load-blacklisting-table/?sort_var='+sort_var,
            "searching": true,
            "filtering": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false,"className": "text-center"},
                {"targets": 1, "orderable": false,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
            ],
            responsive: false,
            "order": [
                [0, 'asc']
            ],
            "lengthMenu": [
                // change per page values here
                [10, 25, 50, 100],
                [10, 25, 50, 100]
            ],
            "pageLength": 10,
        });
        $("#txtSearch").keyup(function() {
          oTable.fnFilter($("#txtSearch").val());
    });
}

function update_user_status(status, user_id){
    if (status == "False"){
        $('#blacklisting_div').removeClass('hidden');
        $('#title_blacklist').addClass('hidden');
        $('#title_reactive').removeClass('hidden');
        $("#active_deactive_user_text").html('').text('Do you want to make this User Active ?');
        $("#user_status").val(status);
        $("#user_id").val(user_id);
    }
    else{
        $('#blacklisting_div').removeClass('hidden');
        $('#title_blacklist').removeClass('hidden');
        $('#title_reactive').addClass('hidden');
        $("#active_deactive_user_text").html('').text('Do you want to Blacklist this user ?');
        $("#user_status").val(status);
        $("#user_id").val(user_id);
    }
}

 toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-center",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

function change_user_status(){
    if(validateDetails()){
        var user_id = $("#user_id").val();
        var blacklist_date = $("#blacklisting_date").val();
        var reactivated_date = $("#blacklisting_date").val();
        var blacklist_remark = $("#remark").val();
        var reactivated_remark = $("#remark").val();
        $.ajax({
            type: "GET",
            url: '/backofficeapp/update-user-track-status/',
            data: {'user_id': user_id,
                   'blacklist_date': blacklist_date,
                   'blacklist_remark': blacklist_remark,
                   'reactivated_date': reactivated_date,
                   'reactivated_remark': reactivated_remark,
                   },
            success: function(response){
                   toastr.success("User Updated Successfully");
                get_blacklisting_datatable();
            }
        });
    }
}

function return_deposit_open(user_id, deposit_available, refund_status){
	     $('#remark_error').css("display", "none");
	     $("#user_track_id").val(user_id);
	     get_deposit_status(user_id);  
  }

function get_deposit_status(user_id) {
	$.ajax({
        type: "GET",
        url: '/backofficeapp/get-deposit-status/',
        data: {'user_id': user_id},
        success: function(response){
        	   $("#deposit_modal_text").text(response.deposit_available);
        	   $("#deposit_remark").text(response.deposit_remark);
        		$("#deposit_returning").val(response.deposit_available);     
        		
				if (response.refund_status == 1) {				
			     	$("#submit_deposit").css('display','none');	
			     	$("#submit_cheque_finalDiv").css('display','block');	
			     	$("#initiatedDiv").css('display','block');	
			     }
			  else if (response.refund_status == 2) {
					$("#submit_deposit").css('display','none');
					$("#submit_cheque_finalDiv").css('display','none');
					$("#initiatedDiv").css('display','block');
			     }
			  else {
					$("#submit_deposit").css('display','block');
					$("#submit_cheque_finalDiv").css('display','block');
					$("#initiatedDiv").css('display','none');
			   }	
			   
			   $("#depositCheque_No_Submit").val(response.cheque_no);
			   $("#depositCheque_Date_Submit").val(response.cheque_date);
			   $("#depositBank_Name_Submit").val(response.bank_name);
			   $("#depositCheque_amount_Submit").val(response.amount);
			     	             		   
        		$("#return_deposit_modal").modal('show');
        }
    });
}
$("#deposit_remark").keyup(function () {
	$('#remark_error').css("display", "none");
});
	  
$("#submit_deposit").click(function(event){
	   //alert($("#deposit_returning").val())
	   remark = $('#deposit_remark').val()
	   if(remark==''){
	   	$('#remark_error').css("display", "block");
		   $('#remark_error').text("Please enter remark ");
	   	return false   	
	   }
		var formData = new FormData();
		formData.append("user_track_id",$('#user_track_id').val());
		formData.append("deposit_remark",$('#deposit_remark').val());
	 
       $.ajax({
                type: "POST",
                url : '/backofficeapp/return-user-deposit/',
                data : formData,
	            cache: false,
	            processData: false,
	            contentType: false,                
              success: function (response) {
                    if (response.success == "true") {
                    	   $("#return_deposit_modal").modal('hide');
			               bootbox.alert('Changes applied successfully');
			               get_blacklisting_datatable()
                     }
               },
               error : function(response){
                    alert("_Error");
                }
           });
});

function validateChequeSubmit() {
	if(checkChequeNo_Submit("#depositCheque_No_Submit")&checkChequeDate_Submit("#depositCheque_Date_Submit")&checkBankName_Submit("#depositBank_Name_Submit")&checkChequeAmount_Submit("#depositCheque_amount_Submit")){
      return true;
   }
   return false;
}
function checkChequeNo_Submit(ChequeNo){
    ChequeNo = $(ChequeNo).val()
    namePattern= /[0-9]{6,}$/

    if($(ChequeNo).val()!='' && namePattern.test(ChequeNo)){
         $("#depositCheque_No_Submit_error").css("display", "none");
         return true;
    }else{
   	   $("#depositCheque_No_Submit_error").css("display", "block");
         $('#depositCheque_No_Submit_error').text("Please enter Cheque No");
         return false;
    }
}

function checkChequeAmount_Submit(Cheque_amount_Submit){
    Cheque_amount = $(Cheque_amount_Submit).val()
    
    if(Cheque_amount!='') {
        $('#depositCheque_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#depositCheque_amount_Submit_error').css("display", "block");
        $('#depositCheque_amount_Submit_error').text("Please enter proper Cheque amount ");
        return false;
    }
}


function checkChequeDate_Submit(Cheque_Date){
    if($(Cheque_Date).val()!='' && $(Cheque_Date).val()!=null){
        $("#depositCheque_Date_Submit_error").css("display", "none");
        return true;
    }else{
        $("#depositCheque_Date_Submit_error").css("display", "block");
        $("#depositCheque_Date_Submit_error").text("Please enter Cheque Date");
        return false;
    }
}

function checkBankName_Submit(BankName){
	BankName = $(BankName).val()
  	var namePattern = /[a-zA-Z0-9_@&.,#&+-\/]$/;

    if(BankName!='' & namePattern.test(BankName)){
 	    $('#depositBank_Name_Submit_error').css("display", "none");
        return true;
    }else{
        $('#depositBank_Name_Submit_error').css("display", "block");
        $('#depositBank_Name_Submit_error').text("Please enter valid Bank Name");
        return false;
    }
}

$("#submit_cheque_final").click(function(event){
	event.preventDefault();
	if(validateChequeSubmit()){
	     var formData= new FormData();
        formData.append("depositCheque_No",$('#depositCheque_No_Submit').val());
        formData.append("depositCheque_Date",$('#depositCheque_Date_Submit').val());
        formData.append("depositBank_Name",$('#depositBank_Name_Submit').val());
        formData.append("depositCheque_amount",$('#depositCheque_amount_Submit').val());       
		  formData.append("user_track_id", $('#user_track_id').val());

        $.ajax({
            type: "POST",
            url: '/backofficeapp/deposit-cheque-details-return/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){                    
                    $("#return_deposit_modal").modal('hide');
                    bootbox.alert('Changes applied successfully');
                }
                else{                    
                    $("#return_deposit_modal").modal('hide');
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
           error : function(response){
                console.log("ErroSP = ",response);
                bootbox.alert('Sorry for inconvenience. An error occurred');
                $("#edit_deposit_modal").modal('hide');
            }
       });
  }
});


// Todo modal value reset
$('#active_deactive_user').on('hidden.bs.modal', function() {
    $("#blacklist_modal").trigger("reset");
});