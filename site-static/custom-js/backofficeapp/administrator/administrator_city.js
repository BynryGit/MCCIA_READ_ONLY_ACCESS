$("#administration_anchor").addClass("tab-active");
$("#administration_nav").addClass("active");
$("#administration_icon").addClass("icon-active");
$("#administration_active").css("display","block")

 $(document).ready(function(){
    $(".sel2").select2({
            width: '100%'
        })
	    get_city_list_datatable();
 		});

function get_city_list_datatable(){

var table = $('#city_table');
	    sort_var = $('#slab_filter :selected').val();
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-city-list/?sort_var='+sort_var,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false},
                {"targets": 1, "orderable": false},
                {"targets": 2, "orderable": false},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
            ],
           buttons: [
                { extend: 'print', className: 'btn dark btn-outline',exportOptions: {columns: [0, 1, 2, 3]} },
                { extend: 'copy', className: 'btn red btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'pdf', className: 'btn green btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'excel', className: 'btn yellow btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
                { extend: 'csv', className: 'btn purple btn-outline',exportOptions: {columns: [0, 1, 2, 3]}  },
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
        $('#city_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });

}




function change_data(){
 get_city_list_datatable();
}


function editSlabDetailsModal(city_id){
        $('#city_name_error').css("display", "none");
        $("#edit_city_detail_modal").modal('show');
        $('#city_id').val(city_id);
        $.ajax({
                type: "GET",
                url : '/backofficeapp/show-city-detail/',
                data : {
                'city_id':city_id
                },
              success: function (response) {
              if (response.success == "true") {
                $('#city_name').val(response.abc);
                $('#select_state').val(response.state_id).trigger("change")
              }
              },
               error : function(response){
                    alert("_Error");
                }
           });
}



$("#edit-city").click(function(event)  {
	event.preventDefault();
	if(validateData()){
	   var formData= new FormData();
		formData.append("city_id",$('#city_id').val());
		formData.append("city_name",$('#city_name').val());
		formData.append("state_id",$('#select_state').val());

  			$.ajax({

				  type	: "POST",
				   url : '/backofficeapp/save-edit-city-details/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {

	              if(response.success == "true"){
	                    $("#edit_city_detail_modal").modal('hide');
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

	if(checkcity_name("#city_name"))
	{
		return true;
	}
	return false;
}

function checkcity_name(city_name){
	city_name = $(city_name).val()
  	var namePattern = /[A-Za-z]$/;
   if(city_name!='' & namePattern.test(city_name)){
 	$('#city_name_error').css("display", "none");
   return true;
   }else{
    $('#city_name_error').css("display", "block");
    $('#city_name_error').text("Please valid enter city");
   return false;
   }
}

function update_city_status(status, city_id){
    if (status == "False"){
        $("#active_deactive_text").html('').text('Do you want to make this city  Active ?');
        $("#city_status").val(status);
        $("#status_city_id").val(city_id);
    }
    else{
        $("#active_deactive_text").html('').text('Do you want to make this city Inactive ?');
        $("#city_status").val(status);
        $("#status_city_id").val(city_id);
    }
}

function change_city_status(){
    var status_city_id = $("#status_city_id").val();
    $.ajax({
        type: "GET",
        url: '/backofficeapp/update-city-status/',
        data: {'status_city_id': status_city_id},
        success: function(response){
            get_city_list_datatable();
        }
    });
}