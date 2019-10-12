$(document).ready(function () {
  sampada_input = $("#sampada_year").val(new Date().getFullYear())
  filter_year()
});

function validate_data(){
    var flag=true;
    if ($('#sampada_year').val() == ''){
    $("#input_year").css("display","block");
    flag=false;
    }
    else{
     $("#input_year").css("display","none");
     x= $('#sampada_year').val();
         filter =/^[0-9]{4}$/;
         if (!filter.test(x)) {
             flag=false;
             $("#correct_year").css("display","block");}
         else{
             $("#correct_year").css("display","none");
}
    }
    if(flag){
    filter_year();
    }
}



function filter_year() {
	sampada_input = $("#sampada_year").val()
	$('#sampada_detail').dataTable({
		"serverSide": true,
		"destroy": true,
		"ajax": "/publicationapp/get-publication/?sampada_input=" + sampada_input,
		"searching": false,
		"6": true,
		"paging": false,

		"columnDefs": [{
				"targets": 0,
				"orderable": false,
				"className": "text-left"
			},
			{
				"targets": 1,
				"orderable": false,
				"className": "text-left"
			},
		],

		// setup responsive extension: http://datatables.net/extensions/responsive/
		responsive: true,

		//"ordering": false, disable column ordering
		//"paging": false, disable pagination

		"order": [
			[1, 'asc']
		],

		"lengthMenu": [
			// change per page values here
			[6, 11],
			[6, 11],
		],
		// set the initial value
		"pageLength": 11,
	});
}
function clear_sampada(){
    $('#sampada_year').val('');
}

//<-------------------------Anual Report--------------------->//
//$(document).ready(function () {
//  select_year = $("#year").val(new Date().getFullYear())
//  filter_year()
//});


function filter_anual_report(){
    flag = true;
    if ($('#annual_year').val() == '' ){
	    flag = false;
	    $('#year').css("border-color","red");
	}
	else{
	    $('#year').css("border-color","initial");
	    x = $('#annual_year').val()
	    pattern = /^[0-9]{4}$/;
	    if(!pattern.test(x)){
	    flag = false;
	    $('#firstname').css("border-color","red");
	    $('#year_error').css("display","block");
	    }
	    else{
	    $('#year').css("border-color","initial");
	    $('#year_error').css("display","none");
	    }
	}
	if(flag){
        filter_year_annual();
	}
	else{
        return false;
	}
}


function filter_year_annual() {
    var select_year = $("#annual_year").val();
	$('#annual_report_table').dataTable({
		"serverSide": true,
		"destroy": true,
		"ajax": "/publicationapp/get-publication-details/?select_year=" + select_year,
		"searching": false,
		"6": true,
		"paging": false,

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
		],

		// setup responsive extension: http://datatables.net/extensions/responsive/
		responsive: false,

		//"ordering": false, disable column ordering
		//"paging": false, disable pagination

//		"order": [
//			[1, 'asc']
//		],
//
//		"lengthMenu": [
//			// change per page values here
//			[5, 10, 20],
//			[5, 10, 20],
//		],
//		// set the initial value
//		"pageLength": 5,
	});
// handle datatable custom tools
}


function clear_report(){
    $('#annual_year').val('');
}

