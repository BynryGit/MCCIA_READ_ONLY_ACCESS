
$(document).ready(function(){
    $(".sel2").select2({
        width: '100%'
    });
    var membership_detail_status = 'show_all';
    get_membership_details_table(membership_detail_status);
});


function save_membership_category_code(){

    $.ajax({
        type: "POST",
        url: "/backofficeapp/save-membership-details/",
        data:$('#membership_category_code').serialize(),
        success: function(response) {

        if (response.success == 'true'){
                bootbox.alert("New Membership Details Added Successfully");
                $('#membership_category_code').trigger("reset");
                location.href="/backofficeapp/membership-details/";
            }
        },
        error: function(response) {
            console.log('Error = ',response);
        },

        beforeSend: function() {
            $("#processing").show();
        },

        complete: function() {
            $("#processing").hide();
        }
    });
}




function get_membership_details_table(membership_detail_status){

    var table = $('#membership_details');
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-membership-details-datatable/?membership_detail_status='+membership_detail_status,
            "searching": true,
            "Filter": true,
            "ordering": false,
            "serverSide": true,
            "paging": true,
            "columnDefs": [
                {"className": "text-center", "targets": 0, "orderable": false},
                {"className": "text-center", "targets": 1, "orderable": false},
                {"className": "text-center", "targets": 2, "orderable": false},
                {"className": "text-center", "targets": 3, "orderable": false},
		        {"className": "text-center", "targets": 4, "orderable": false},
            ],
            buttons: [
                { extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'excel', className: 'btn yellow btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'csv', className: 'btn purple btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

            responsive: false,

            "order": [[0, 'asc']],

            "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],

            "pageLength": 10,
        });

        $(".dataTables_filter").hide();

        $('#membership_details_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#membership_details').DataTable().button(action).trigger();
        });

        $("#search_membership_detail_text").keyup(function() {
            oTable.fnFilter($("#search_membership_detail_text").val());
        });
}


function filter_membership_detail_table(){
    membership_detail_status = $("#select_membership_detail_status").val();
    get_membership_details_table(membership_detail_status);
}


function validateDataEditCategory(){
	if(checkCategory_code("#edit_category_code")&checkCategory_descriptions("#edit_category_descriptions")){
        return true;
	}
	return false;
}


function checkCategory_code(category_code){
	category_code = $(edit_category_code).val();
  	var namePattern = /^\d{1,3}$/;

    if(category_code!='' & namePattern.test(category_code)){
 	    $('#edit_category_code_error').css("display", "none");
        return true;
    }
    else{
        $('#edit_category_code_error').css("display", "block");
        $('#edit_category_code_error').text("Please enter valid Code");
        return false;
   }
}

function checkCategory_descriptions(edit_category_descriptions){
	category_descriptions = $(edit_category_descriptions).val()
	var len = category_descriptions.length;
  	var namePattern = /^[A-Za-z0-9_@&.,#&+-\/]+( [A-Za-z0-9_@$.,#&+-\/]+)*$/;
    if(category_descriptions != '' & namePattern.test(category_descriptions) & len >= 1 & len <=20){
 	    $('#edit_category_descriptions_error').css("display", "none");
        return true;
    }
    else{
        $('#edit_category_descriptions_error').css("display", "block");
        $('#edit_category_descriptions_error').text("Please enter valid Membership Description");
        return false;
   }
}

function editMembershipCategoryModal(category_code_id){
    $("#edit_membership_category_code_modal").modal('show');

    $.ajax({
        type: "GET",
        url : '/backofficeapp/show-membership-details/',
        data : {
        'category_code_id':category_code_id
        },

        success: function (response) {
            if (response.success == "true") {
                $('#category_code_id').val(response.membserhipDetails.category_code_id);
                $('#edit_category_code').val(response.membserhipDetails.membership_code);
                $('#edit_category_descriptions').val(response.membserhipDetails.membership_category);
            }
        },
        error : function(response){
            console.log('Error = ',response);
        }
   });
}

$("#edit-countinue").click(function(event)  {
    if(validateDataEditCategory()){
        var formData= new FormData();
		formData.append("category_code_id",$('#category_code_id').val());
		formData.append("edit_category_code",$('#edit_category_code').val());
		formData.append("edit_category_descriptions",$('#edit_category_descriptions').val());

        $.ajax({
            type: "POST",
            url: '/backofficeapp/edit-membership-details/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,

            success: function (response) {
                if(response.success== 'true'){
                    $("#success_modal").modal('show');
                    filter_membership_detail_table();
                }
                if (response.success == "false") {
                    $("#error-modal").modal('show');
                    filter_membership_detail_table();
                }
            },
            beforeSend: function () {
                $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
            error : function(response){
                console.log('Error = ',response);
            }
        });
    }
});


// Update Membership Detail Status
function activeInactiveDetail(status,membership_detail_id){
    if (status == "False"){
        $("#active_deactive_mem_detail_text").html('').text('Do you want to Activate Membership Detail ?');
        $("#membership_detail_status").val(status);
        $("#membership_detail_id").val(membership_detail_id);
    }
    else{
        $("#active_deactive_mem_detail_text").html('').text('Do you want to Deactivate Membership Detail ?');
        $("#membership_detail_status").val(status);
        $("#membership_detail_id").val(membership_detail_id);
    }
}

function update_mem_detail_status(){
    var mem_detail_id = $("#membership_detail_id").val();

    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-membership-status/',
        data: {'mem_detail_id': mem_detail_id },

        success: function(response){
            if (response.success == 'true'){
                filter_membership_detail_table();
            }
            else{
                filter_membership_detail_table();
            }
        },
    });
}

