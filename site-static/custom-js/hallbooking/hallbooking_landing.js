
locationID = $("#LocationID").val();
is_member=false
booking_id=''
bokking_detail_ids=[]
hall_id=''

function show_hall_booking_form(hall_id,hall_name){	
    $.ajax({
          type  : "GET",
          url   : '/hallbookingapp/get-server-time/',
          success: function (response) {
            console.log(response.server_time)
            var start_time = Date.parse('10:00 AM');
            var end_time = Date.parse('04:00 PM');
            var server_date = response.server_time;
            var today_date = Date.parse(server_date);
            if ($("#user_type").val() == 'backoffice'){
                $("#backoffice_hide_div").hide();
                $("#user_type_div").hide();
                $("#hall_id").val(hall_id);
                $("#hall_name").val(hall_name);
                $("#booking_hall_name").text(hall_name)
                $("#hall_booking_landing_div").hide();
                $("#location_div").hide();
                $("#hall_booking_form_div").show();
                $('html, body').animate({
                        scrollTop: $("#booking_hall_name").first().offset().top - 150
                }, 1000);
            }
            else if (start_time <= today_date && end_time >= today_date){
                $("#hall_id").val(hall_id);
                $("#hall_name").val(hall_name);
                $("#booking_hall_name").text(hall_name)
                $("#hall_booking_landing_div").hide();
                $("#location_div").hide();
                $("#hall_booking_form_div").show();

                $('html, body').animate({
                        scrollTop: $("#booking_hall_name").first().offset().top - 150
                }, 1000);
            }
            else{
                toastr.error("Booking is closed for today. Booking time is between 10:00 AM to 4:00 PM");
                setTimeout(function(){
                                window.location.href = "/hallbookingapp/open-hallbooking-page/"}, 1000);
                return false;
            }
        }

              });
    }

$(document).load(function(e){
	$("#processing").css('display','block');
	
});

//var inFormOrLink = true;
//$('a').live('click', function() { inFormOrLink = true; });
//$('form').bind('submit', function() { inFormOrLink = true; });

$(document).ready(function(e){
	$("#processing").css('display','none');
    $("#hall_booking_landing_div").show();
    $("#location_div").show();
    $("#hall_booking_form_div").hide();

//    if ($("#user_type").val() == 'backoffice'){
//        $("#user_type_div").hide();
//    }
//    else{
//        $("#user_type_div").show();
//    }

    var pathname = window.location.pathname; // Returns path only
    location_url_ID= pathname.split('/')[3]

    if (location_url_ID == ''){
        $("#locationlistID_"+'1').addClass('active').removeClass('""')
    }
    else{
        $("#locationlistID_"+location_url_ID).addClass('active')
    }   
    
    $('#check_hall_availbility_status').on('shown.bs.modal', function () {
   		$("#hall_event_calendar").fullCalendar('render');
   });
   
});

function load_hallevent_calender() {
	    halldeatil_id = $("#selectHallName").val()
	    if (halldeatil_id) {
		    $.ajax({
	          type  : "GET",
	          url   : '/hallbookingapp/get-hallevent-calender-data/',
	          data : {'halldeatil_id':halldeatil_id},
		       success: function (response) {
			 		  	 if (response.success == 'true') {	
			 		  	       console.log(response.final_list)
			 		  	 		if (response.final_list.length > 0){
									$('#hall_event_calendar').fullCalendar('destroy');
								
								   $('#hall_event_calendar').fullCalendar({
	  								
									        header: { center: 'month,agendaWeek' },
									        defaultView: 'month',
									        navLinks: true, // can click day/week names to navigate views
	      								  editable: true,
									        eventLimit: true, // allow "more" link when too many events 
											  eventSources: [							
													    {
													        events : response.final_list,												        	      
													    }												
											 ],
											 
											 
											eventMouseover: function (data, event, view) {											 	
            						 		tooltip = '<div class="tooltiptopicevent" style="width:auto;height:auto;background:#c1dec2;position:absolute;z-index:10001;padding:10px 10px 10px 10px ;  line-height: 200%;">' + data.title + '</br>' + 'Date : ' + data.new_date + '</br>' + '</div>';	
	
	            							$("body").append(tooltip);
	            							$(this).mouseover(function (e) {
	                							$(this).css('z-index', 10000);
	                							$('.tooltiptopicevent').fadeIn('500');
	                							$('.tooltiptopicevent').fadeTo('10', 1.9);
	            							}).mousemove(function (e) {
	                							$('.tooltiptopicevent').css('top', e.pageY + 10);
	                							$('.tooltiptopicevent').css('left', e.pageX + 20);
	            							});
	
	
	        								},
	        								eventMouseout: function (data, event, view) {
	            							$(this).css('z-index', 8);
	            							$('.tooltiptopicevent').remove();
	        								},    											
								  });	
									     		  	 		
			 		  	 		}			 		  	 			
			 		  	 		else {
			 		  	 			$('#hall_event_calendar').fullCalendar('destroy');
			 		  	 			$('#hall_event_calendar').fullCalendar({
			 		  	 			        header: { center: 'month,agendaWeek' },
									        defaultView: 'month'
									});
			 		  	 		}	 		  	 		
		 		  		 }	 		  		 	 		  		
		        },
	          error : function(response){
	                alert("_Error");                
	        },
	
	      });   
     }
     else {
 		$('#hall_event_calendar').fullCalendar('destroy');
 		$('#hall_event_calendar').fullCalendar({
 		  	     header: { center: 'month,agendaWeek' },
		        defaultView: 'month'
		});						  
    }	   
}

function check_hall_availbility_status(){	 
    load_hallevent_calender();
    $("#check_hall_availbility_status").modal("show");
    
}

// Show Bigger Hall Image on hover
$(".zoom_hall_image").hover(function(e){	
	$("body").append("<p id='preview'><img src='"+ $(this).attr('src') +"' alt='Image preview' /></p>");
	$("#preview")
            .css("top",(e.pageY - 150) + "px")
            .css("left",(e.pageX + 150) + "px")
            .css("display", "block")
            
}, function() {
	$("#preview").remove();
});

$("#preview").mousemove(function(e){
    $("#preview")
        .css("top",(e.pageY - 150) + "px")
        .css("left",(e.pageX + 150) + "px");
});






