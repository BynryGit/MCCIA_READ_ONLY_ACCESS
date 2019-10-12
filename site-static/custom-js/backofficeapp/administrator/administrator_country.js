$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_country_list_datatable();
 		});

function get_country_list_datatable(){

var table = $('#country_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-country-list/?sort_var='+sort_var,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2]}},
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2]}},
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2]} },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2]} },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2]} },
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
        $('#country_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_country_list_datatable();
}


function editSlabDetailsModal(country_id){
        $('#country_name_error').css("display", "none");
        $("#edit_country_detail_modal").modal('show');
        $('#country_id').val(country_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-country-detail/',
                data : {
                'country_id':country_id
                },
              success: function (response) {
              if (response.success == "true") {
                $('#country_name').val(response.abc);
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-country").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("country_id",$('#country_id').val());
		formData.append("country_name",$('#country_name').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-country-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_country_detail_modal").modal('hide');
	           	  		$("#success_modal").modal('show');
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

	if(checkcountry_name("#country_name"))
	{
		return true;
	}
	return false;
}

function checkcountry_name(country_name){
	country_name = $(country_name).val()
  	var namePattern = /[A-Za-z]$/;
   if(country_name!='' & namePattern.test(country_name)){
 	$('#country_name_error').css("display", "none");
   return true;
   }else{
    $('#country_name_error').css("display", "block");
    $('#country_name_error').text("Please valid enter Country");
   return false;
   }
}

function update_country_status(status, country_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this Country  Active ?');
        $("#country_status").val(status);
        $("#status_country_id").val(country_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this Country Inactive ?');
        $("#country_status").val(status);
        $("#status_country_id").val(country_id);
    }
}

function change_country_status(){
    var status_country_id = $("#status_country_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-country-status/',
        data: {'status_country_id': status_country_id},
        success: function(response){
            get_country_list_datatable();
        }
    });
}