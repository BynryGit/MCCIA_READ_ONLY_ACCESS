//<--------- sampada js Start--------->//

$(document).ready(function () {
  sampada_input = $("#sampada_year").val(new Date().getFullYear());
  filter_sampada_year();
  $("#collapse1").collapse();
});



function filter_sampada(){
    var flag=true;
    if ($('#sampada_year').val() == ''){
        flag=false;
        $('#sampada_year').css("border-color","red");
    }
    else{
         $('#sampada_year').css("border-color","initial");
         x= $('#sampada_year').val();
         pattern =/^[0-9]{4}$/;
         if (!pattern.test(x)) {
             flag=false;
             $('#sampada_year').css("border-color","red");
             $("#correct_year").css("display","block");}
         else{
             $('#year').css("border-color","initial");
             $("#correct_year").css("display","none");
             }
    }
    if(flag){
            filter_sampada_year();
    }
    else{
        return false;
    }
}



function filter_sampada_year() {
	sampada_input = $("#sampada_year").val()
	$('#sampada_detail').dataTable({
		"serverSide": true,
		"destroy": true,
		"ajax": "/publicationapp/get-sampada-details/?sampada_input=" + sampada_input,
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


function clear_sampada_report(){
    $('#sampada_year').val('');
}

//<--------- sampada js End--------->//


//<--------- World Of Business js Start--------->//

$(document).ready(function () {
  from_date = $("#from_date").val(new Date().getMonth()+1 + "/" + 1 + "/" + new Date().getFullYear())
  to_date = $("#to_date").val(new Date().getMonth()+1 + "/" + (new Date().getDate()) + "/" + new Date().getFullYear())
  filter_world_of_business();
  clear_world_of_business();
});


function DateCheck()
{
  var from_date= document.getElementById('from_date').value;
  var to_date= document.getElementById('to_date').value;
  var sDate = new Date(from_date);
  var eDate = new Date(to_date);
  if(from_date!= '' && to_date!= '' && sDate> eDate)
    {
    bootbox.alert("Please ensure that the End Date is greater than or equal to the Start Date.");
    $('#from_date').css("border-color","red");
    $('#to_date').css("border-color","red");
    return false;
    }
  else{
    filter_world_of_business()
    $('#from_date').css("border-color","initial");
    $('#to_date').css("border-color","initial");
  }
}


function filter_world_of_business(){
    var from_date=$('#from_date').val();
    var to_date=$('#to_date').val();
   $('#world_of_business_table').dataTable({
      "serverSide": true,
      "destroy": true,
      "ajax": "/publicationapp/get-world-of-business-details/?from_date=" + from_date + '&to_date=' + to_date,
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
      responsive: false,

      //"ordering": false, disable column ordering
      //"paging": false, disable pagination

      "order": [
         [1, 'asc']
      ],

      "lengthMenu": [
         // change per page values here
         [5, 10, 20],
         [5, 10, 20],
      ],
      // set the initial value
      "pageLength": 2,
   });
// handle datatable custom tools
}

function clear_world_of_business(){
    $('#from_date').val('');
    $('#to_date').val('');
}


//<--------- World Of Business js End--------->//


//<--------- Anual Report js Start--------->//

$(document).ready(function () {
  select_year = $("#year").val(new Date().getFullYear()-1)
  filter_year();
});


function filter_anual_report(){
    flag = true;
    if ($('#year').val() == '' ){
	    flag = false;
	    $('#year').css("border-color","red");
	}
	else{
	    $('#year').css("border-color","initial");
	    x = $('#year').val()
	    pattern = /^[0-9]{4}$/;
	    if(!pattern.test(x)){
	    flag = false;
	    $('#year').css("border-color","red");
	    $('#year_error').css("display","block");
	    }
	    else{
	    $('#year').css("border-color","initial");
	    $('#year_error').css("display","none");
	    }
	}
	if(flag){
        filter_year();
	}
	else{
        return false;
	}
}


function filter_year() {
    var select_year = $("#year").val();
	$('#annual_report_table').dataTable({
		"serverSide": true,
		"destroy": true,
		"ajax": "/publicationapp/get-anual-report-details/?select_year=" + select_year,
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
    $('#year').val('');
}

//<--------- Anual Report js End--------->//

//function filter_year(){
//       var select_year = $("#year").val();
//       $.ajax({
//            type: "GET",
//            url: '/publicationapp/get-publication-details/',
//            data: {'select_year': select_year},
//            success: function(response){
//                console.log(response);
//                alert(response.success);
//            },
//            error:function(response){
//            }
//    });
//}


//function DateCheck(){
//    var flag=true;
//    from_date= $('#from_date').val()
//    to_date= $('#to_date').val()
//    var sDate = new Date(from_date);
//    var eDate = new Date(to_date);
//    if(from_date = '' && to_date = ''){
//        flag=false;
//        $('#from_date').css("border-color","red");
//        $('#to_date').css("border-color","red");
//        alert("Please Fill the Date");
//    }
//    else{
//         if (from_date!= '' && to_date!= '' && sDate> eDate){
//             flag=false;
//             alert("Please ensure that the End Date is greater than or equal to the Start Date.");
//             }
//         else{
//             $('#from_date').css("border-color","red");
//             $('#to_date').css("border-color","red");
//             }
//         }
//    if(flag){
//            filter_world_of_business();
//    }
//    else{
//        return false;
//    }
//}