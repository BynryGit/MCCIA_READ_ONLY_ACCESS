$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_servicetax_list_datatable();
 		});

function get_servicetax_list_datatable(){

var table = $('#servicetax_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-servicetax-list/?sort_var='+sort_var,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false,"className": "text-center"},
                {"targets": 1, "orderable": false,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
                {"targets": 5, "orderable": false,"className": "text-center"},
                {"targets": 6, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4]} },
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4]}},
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4]}},
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4]} },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2, 3, 4]} },
//                { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

            // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: false,

            //"ordering": false, disable column ordering
            //"paging": false, disable pagination

            "order": [
                [0, 'asc']
            ],

            "lengthMenu": [
                // change per page values here
                [10, 25, 50, 100],
                [10, 25, 50, 100]
            ],
            // set the initial value
            "pageLength": 10,


        });
        $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

        // handle datatable custom tools
        $('#servicetax_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_servicetax_list_datatable();
}


function editSlabDetailsModal(servicetax_id){
        $("#cgst_div").hide()
        $("#sgst_div").hide()
        $("#igst_div").hide()
        $('#servicetax_name_error').css("display", "none");
        $("#edit_servicetax_detail_modal").modal('show');
        $('#servicetax_id').val(servicetax_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-servicetax-detail/',
                data : {
                'servicetax_id':servicetax_id
                },
              success: function (response) {
              if (response.success == "true") {
                if (response.tax_type=='0'){
                    $('#cgst_tax').val(response.cgst);
                    $('#sgst_tax').val(response.sgst);
                    $("#cgst_div").show()
                    $("#sgst_div").show()
                }else{
                    $('#igst_tax').val(response.igst);
                    $("#igst_div").show()
                }

                $('#select_state_id').val(response.tax_type)
                $('#select_state').val(response.tax_type).trigger("change")

              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}
$("#edit-servicetax").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("servicetax_id",$('#servicetax_id').val());
		formData.append("cgst_tax",$('#cgst_tax').val());
		formData.append("sgst_tax",$('#sgst_tax').val());
		formData.append("igst_tax",$('#igst_tax').val());
        $.ajax({
            type	: "POST",
            url : '/backofficeapp/save-edit-servicetax-details/',
            data : formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response.success == "true"){
                    $("#edit_servicetax_detail_modal").modal('hide');
                    $("#success_modal").modal('show');
                    get_servicetax_list_datatable();
                }
                if (response.success == "false") {
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

function validateData(){
    select_state_id = $("#select_state_id").val()
    if (select_state_id == '0'){
        if(checktax("#cgst_tax") && checktax("#sgst_tax") && checktotal())
        {
            return true;
        }
        return false;
    }else{
        if(checktax("#igst"))
        {
            return true;
        }
        return false;
    }

}

//function checktax(taxvalue){
//checkvalue=$(taxvalue).val()
//if(checkvalue != '' && parseFloat(checkvalue) > 100 ){
//    $(taxvalue +'_error').css("display", "block");
//    $(taxvalue +'_error').text("Please enter Value");
//    return false;
//}else{
//    $(taxvalue +'_error').css("display", "block");
//    $(taxvalue +'_error').text("Please enter Value");
//    return false;
//}
//$(taxvalue +'_error').css("display", "none");
//return true
//}

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


function update_servicetax_status(status, servicetax_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this servicetax  Active ?');
        $("#servicetax_status").val(status);
        $("#status_servicetax_id").val(servicetax_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this servicetax Inactive ?');
        $("#servicetax_status").val(status);
        $("#status_servicetax_id").val(servicetax_id);
    }
}

function change_servicetax_status(){
    var status_servicetax_id = $("#status_servicetax_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-servicetax-status/',
        data: {'status_servicetax_id': status_servicetax_id},
        success: function(response){
            get_servicetax_list_datatable();
        }
    });
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