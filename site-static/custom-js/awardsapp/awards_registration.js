

// Show Form according to Award
function show_form(){
    var award_id = parseInt($("#select_award").val());
    if (isNaN(award_id)){
        award_id = '';
    }
    window.location.href = '/awardsapp/awards-registration/'+award_id
}


// Save BG Deshmukh Form

function save_bg_deshmukh_form(){
    formsubmit = document.getElementById('bg_deshmukh_div_form_btn')
    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false;
    }
    else{
        $.ajax({
            type: 'POST',
            url: '/awardsapp/save-award-registration/',
            data:  $('#bg_deshmukh_div_form').serialize() + "&award_id="+$("#select_award").val() + "&form_type=bg_deshmukh_form",

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Award Registration is successfully saved.');
                    setTimeout(function(){location.reload('/');}, 500);
                }
                else{
                    bootbox.alert('Sorry for inconvenience, an error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").show();
            },
            complete: function () {
                $("#processing").hide();
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience, an error occurred');
                console.log('ARE = ',response);
            }
        });
    }
}


// Submit BG Deshmukh Award Form

$("#bg_deshmukh_div_form_btn").click(function(e){
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
    }
});


// Save Parkhe, Ramabai Joshi & Hari Malini Joshi Form

function save_three_award_form(){
    formsubmit = document.getElementById('submit_three_div_btn')
    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false;
    }
    else{
        $.ajax({
            type: 'POST',
            url: '/awardsapp/save-award-registration/',
            data:  $('#three_div_form').serialize() + "&award_id="+$("#select_award").val() + "&form_type=three_form",

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Award Registration is successfully saved.');
                    setTimeout(function(){location.reload('/');}, 500);
                }
                else{
                    bootbox.alert('Sorry for inconvenience, an error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").show();
            },
            complete: function () {
                $("#processing").hide();
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience, an error occurred');
                console.log('ARE = ',response);
            }
        });
    }
}


// Submit Parkhe, Ramabai Joshi & Hari Malini Joshi Form

$("#submit_three_div_btn").click(function(e){
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
    }
});


// Save Natu Award Form

function save_natu_award(){
    formsubmit = document.getElementById('natu_div_btn')
    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false;
    }
    else{
        $.ajax({
            type: 'POST',
            url: '/awardsapp/save-award-registration/',
            data:  $('#natu_div_form').serialize() + "&award_id="+$("#select_award").val() + "&form_type=natu_form",

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Award Registration is successfully saved.');
                    setTimeout(function(){location.reload('/');}, 500);
                }
                else{
                    bootbox.alert('Sorry for inconvenience, an error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").show();
            },
            complete: function () {
                $("#processing").hide();
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience, an error occurred');
                console.log('ARE = ',response);
            }
        });
    }
}


// Save Natu Award Form

$("#natu_div_btn").click(function(e){
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
    }
});


// Save Rathi Award Form

function save_rathi_award(){
    formsubmit = document.getElementById('rathi_div_btn')
    if (! formsubmit.classList.contains('checkValidationBtn')){
        return false;
    }
    else{
        $.ajax({
            type: 'POST',
            url: '/awardsapp/save-award-registration/',
            data:  $('#rathi_div_form').serialize() + "&award_id="+$("#select_award").val() + "&form_type=rathi_form",

            success: function(response){
                if (response.success == 'true'){
                    bootbox.alert('Award Registration is successfully saved.');
                    setTimeout(function(){location.reload('/');}, 500);
                }
                else{
                    bootbox.alert('Sorry for inconvenience, an error occurred');
                }
            },
            beforeSend: function () {
                $("#processing").show();
            },
            complete: function () {
                $("#processing").hide();
            },
            error: function(response){
                bootbox.alert('Sorry for inconvenience, an error occurred');
                console.log('ARE = ',response);
            }
        });
    }
}


// Save Rathi Award Form

$("#rathi_div_btn").click(function(e){
    if ($("form > div .has-error").length > 0){
        $('html, body').animate({
            scrollTop: $("form > div .has-error").first().offset().top - 150
        }, 1000);
    }
});