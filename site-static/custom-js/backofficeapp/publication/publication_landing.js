$("#publication_anchor").addClass("tab-active");
$("#publication_nav").addClass("active");
$("#publication_icon").addClass("icon-active");
$("#publication_active").css("display", "block");

$(document).ready(function () {
	load_publication_data(select_status)
});

function change_publication() {
	select_status = $("#select_status").val()
	load_publication_data(select_status);

}

function load_publication_data(select_status) {
	$('#PublicationListTable').dataTable({
		"serverSide": true,
		"destroy": true,
		"ajax": "/publicationapp/get-publication-datatable/?select_status=" + select_status,
		"searching": false,
		"6": true,
		"paging": true,

		"columnDefs": [{
				"targets": 0,
				"orderable": false,
				"className": "text-center"
			},
			{
				"targets": 1,
				"orderable": false,
				"className": "text-center"
			},
			{
				"targets": 2,
				"orderable": false,
				"className": "text-center"
			},
			{
				"targets": 3,
				"orderable": false,
				"className": "text-center"
			},
			{
				"targets": 4,
				"orderable": false,
				"className": "text-center"
			},
		],

		// setup responsive extension: http://datatables.net/extensions/responsive/
		responsive: false,

		//"ordering": false, disable column ordering
		//"paging": false, disable pagination

		"order": [
			[1, 'asc']
		],

		"lengthMenu": [
			// change per page values here
			[50, 100, 500],
			[50, 100, 500],
		],
		// set the initial value
		"pageLength": 50,
	});
// handle datatable custom tools
}

function update_publication(status,publication_id){
    if (status == "Inactive"){
        $("#active_deactive_publication_text").html('').text('Do you want to make this Publication  Active ?');
        $("#publication_id").val(publication_id);
    }
    else{
        $("#active_deactive_publication_text").html('').text('Do you want to make this Publication  Inactive ?');
        $("#publication_id").val(publication_id);
    }
}


function change_publication_status(){
    var publication_id = $("#publication_id").val();
    $.ajax({
        type: "GET",
        url: '/publicationapp/update-publication-status/',
        data: {'publication_id': publication_id},
        success: function(response){
            change_publication();
        }
    });
}