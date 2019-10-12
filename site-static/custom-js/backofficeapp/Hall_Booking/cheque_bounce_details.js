
$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(document).ready(function(){
       hall_booking_id = $("#hidden_booking_id").val();
 	   load_cheque_details_datatable(hall_booking_id);
});


function load_cheque_details_datatable(hall_booking_id) {

var table = $('#chequebounceTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-cheque-details-datatable/?hall_booking_id="+hall_booking_id,
        "searching": false,
        "paging": true,
        "columnDefs": [
			{"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": false, "className": "text-center"},
            {"targets": 2, "orderable": false, "className": "text-center"},
            {"targets": 3, "orderable": false, "className": "text-center"},
            {"targets": 4, "orderable": false, "className": "text-center"},
            {"targets": 5, "orderable": false, "className": "text-center"},
            {"targets": 6, "orderable": false, "className": "text-center"},
        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
        ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,
        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 20, 50,100,-1],
            [10, 20, 50,100,'All']
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#regSearch").keyup(function() {
        oTable.fnFilter($("#regSearch").val());
    });
    $('#hallregtable_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}

function get_cheque_data(pay_cheque_id){
    $.ajax({
            type : "GET",
            url : '/backofficeapp/get-bounce-cheque-details/',
            data : {'pay_cheque_id':pay_cheque_id},
            success: function (response) {
                if(response.success =='true'){
                        $("#modal_cheque_no").text(response.cheque_no)
                        $("#modal_cheque_date").text(response.cheque_date)
                        $("#modal_bank_name").text(response.bank_name)
                        $("#modal_cheque_amount").text(response.paid_amount)
                        $("#modal_tds_amt").text(response.tds_amount)
                        $("#hidden_pay_cheque_id").val(pay_cheque_id)
                }
            },
            error : function(response){
                alert("_Error");
            }
        });

    $("#cheque_detail_modal").modal('show');
}



$("#cancel_bounce_cheque").click(function(event){
	event.preventDefault();
	if(1){
	     var formData= new FormData();
        formData.append("modal_remark",$('#modal_remark').text());
        formData.append("modal_extra_amt",$('#modal_extra_amt').val());
		  formData.append("pay_cheque_id", $('#hidden_pay_cheque_id').val());

        $.ajax({
            type: "POST",
            url: '/backofficeapp/update-cheque-details/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success=='true'){
                	  $("#cheque_detail_modal").modal('hide');
                    bootbox.alert('Changes applied successfully');                  
                }
                else{
                    bootbox.alert('Sorry for inconvenience. An error occurred');
                    $("#cheque_detail_modal").modal('hide');
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
                $("#cheque_detail_modal").modal('hide');
            }
       });
  }
});





// Validate Payment Modal Input Data
function validateChequeSubmit(){

//To DO
    paymentType=$('input[name=paymentType_Submit]:checked').val()
    if (paymentType == "ByCash"){
        if(checkReceiptNo("#cash_receipt_Submit")&checkTDS("#TDS_Submit")&checkCashAmount_Submit("#cash_amount_Submit")){
            return true;
        }
        return false;
    }
    else{
        if (paymentType == "ByCheque"){
            if(checkChequeAmount_Submit("#Cheque_amount_Submit")&checkTDS("#TDS_Submit")&checkChequeNo_Submit("#Cheque_No_Submit")&checkChequeDate_Submit("#Cheque_Date_Submit")&checkBankName_Submit("#Bank_Name_Submit")){
                return true;
            }
            return false;
        }
        else if (paymentType == "ByDeposit"){
            if(checkDepositAmount_Submit("#deposit_amount_Submit")&checkTDS("#TDS_Submit")){
                return true;
            }
            return false;
        }
        else{
            if(checkNEFTAmount_Submit("#NEFT_amount_Submit")&checkTDS("#TDS_Submit")&checkNEFTID_Submit("#NEFT_Transfer_Submit")){
                return true;
            }
            return false;
        }
    }
}

function checkReceiptNo(cash_receipt_Submit){
    cash_receipt_Submit = $(cash_receipt_Submit).val()

    if(cash_receipt_Submit!=''){
        $('#cash_receipt_Submit_error').css("display", "none");
        return true;
    }else{
        $('#cash_receipt_Submit_error').css("display", "block");
        $('#cash_receipt_Submit_error').text("Please enter valid Receipt No");
        return false;
    }
}

function checkTDS(TDS_Submit){
    TDS = $(TDS_Submit).val()

    if(TDS!=''){
        $('#TDS_Submit_error').css("display", "none");
        return true;
    }else{
        $('#TDS_Submit_error').css("display", "block");
        $('#TDS_Submit_error').text("TDS can't be blank");
        return false;
    }
}

function checkCashAmount_Submit(CashAmount){
    CashAmount = $(CashAmount).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(CashAmount) + parseFloat(TDS_amount)

    if(CashAmount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
        $('#cash_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#cash_amount_Submit_error').css("display", "block");
        $('#cash_amount_Submit_error').text("Please enter proper cash amount ");
        return false;
    }
}

function checkChequeAmount_Submit(Cheque_amount_Submit){
    Cheque_amount = $(Cheque_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(Cheque_amount) + parseFloat(TDS_amount)

    if(Cheque_amount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
        $('#Cheque_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#Cheque_amount_Submit_error').css("display", "block");
        $('#Cheque_amount_Submit_error').text("Please enter proper Cheque amount ");
        return false;
    }
}


function checkChequeNo_Submit(ChequeNo){
    ChequeNo = $(ChequeNo).val()
    namePattern= /[0-9]{6,}$/

    if($(ChequeNo).val()!='' && namePattern.test(ChequeNo)){
        $("#Cheque_No_Submit_error").css("display", "none");
        return true;
    }else{
   	    $("#Cheque_No_Submit_error").css("display", "block");
        $('#Cheque_No_Submit_error').text("Please enter Cheque No");
        return false;
    }
}

function checkChequeDate_Submit(Cheque_Date){
    if($(Cheque_Date).val()!='' && $(Cheque_Date).val()!=null){
        $("#Cheque_Date_Submit_error").css("display", "none");
        return true;
    }else{
        $("#Cheque_Date_Submit_error").css("display", "block");
        $("#Cheque_Date_Submit_error").text("Please enter Cheque Date");
        return false;
    }
}

function checkBankName_Submit(BankName){
	BankName = $(BankName).val()
  	var namePattern = /[a-zA-Z0-9_@&.,#&+-\/]$/;

    if(BankName!='' & namePattern.test(BankName)){
 	    $('#Bank_Name_Submit_error').css("display", "none");
        return true;
    }else{
        $('#Bank_Name_Submit_error').css("display", "block");
        $('#Bank_Name_Submit_error').text("Please enter valid Bank Name");
        return false;
    }
}


function checkNEFTAmount_Submit(NEFT_amount_Submit){
    NEFT_amount = $(NEFT_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(NEFT_amount) + parseFloat(TDS_amount)

    if(NEFT_amount!='' & parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())){
        $('#NEFT_amount_Submit_error').css("display", "none");
        return true;
    }else{
        $('#NEFT_amount_Submit_error').css("display", "block");
        $('#NEFT_amount_Submit_error').text("Please enter proper NEFT amount ");
        return false;
    }
}

function checkNEFTID_Submit(NEFTID){
    NEFTID = $(NEFTID).val()
    var namePattern = /[A-Za-z0-9_@./#&+-\s]{7,64}$/;

    if(NEFTID!='' & namePattern.test(NEFTID)){
        $('#NEFT_Transfer_Submit_error').css("display", "none");
        return true;
    }else{
        $('#NEFT_Transfer_Submit_error').css("display", "block");
        $('#NEFT_Transfer_Submit_error').text("Please enter valid Transfer ID");
        return false;
    }
}

function checkDepositAmount_Submit(deposit_amount_Submit){
    deposit_amount = $(deposit_amount_Submit).val()
    TDS_amount = $("#TDS_Submit").val()
    total_paying_amt = parseFloat(deposit_amount) + parseFloat(TDS_amount)

    if(deposit_amount!='' & parseFloat(deposit_amount) <= parseFloat($("#deposit_available_Submit").val())) {
    	  if(parseFloat(total_paying_amt) <= parseFloat($("#remain_amount").val())) {
	    	  	$('#deposit_amount_Submit_error').css("display", "none");
	        return true;
	     }else{
	        $('#deposit_amount_Submit_error').css("display", "block");
	        $('#deposit_amount_Submit_error').text("Please enter proper Deposit amount ");
	        return false;
	     }
    }else{
        $('#deposit_amount_Submit_error').css("display", "block");
        $('#deposit_amount_Submit_error').text("Don't have enough deposit to debit ");
        return false;
    }
}

