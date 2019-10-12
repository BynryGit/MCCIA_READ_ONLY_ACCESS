$("#forget-password").click(function(e){
    $("#forgot_pass_div").show();
    $("#login_div").hide();
    $("#username").val('');
    $("#user_password").val('');
});

$("#back-btn").click(function(e){
    $("#forgot_pass_div").hide();
    $("#login_div").show();
    $("#uname").val('');

});

$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13' || keycode == 13){
        if($("#login_div").is(":visible")){
            $("#login_button").trigger('click');
        }
        if($("#forgot_pass_div").is(":visible")){
            $("#forgot_pass_submit_btn").trigger('click');
        }
    }
});

$('#login_button').click(function(event){
    event.preventDefault();
    $.ajax({
        type : 'POST',
        url : '/authenticate/sign_in/',
        data : $("#login_form").serialize(),
        success: function(response) {
            if(response.success=='true'){
                location.href = response.redirect_url
            }
            else if(response.success=='false'){
                $("#login_modal").modal('show');
            }
            else if(response.success=='Invalid Username'){
                $("#login_modal").modal('show');
            }
            else if(response.success=='Invalid Password'){
                $("#password").modal('show');
            }
            else if(response.success=='false1'){
                $("#inactive").modal('show');
            }
        },
        beforeSend: function () {
            $("#processing").show();
        },
        complete: function () {
            $("#processing").hide();
        },
        error: function(response){
            alert(response.abc);
            console.log('error',response);
        }
    });
});

function forgot_backoffice_password(){
    event.preventDefault();
    $.ajax({
        type : 'POST',
        url : '/authenticate/backoffice-forgot-password/',
        data : $("#forgot_password").serialize(),
        success: function(response) {
            if(response.success=='true'){
                $("#affiliate-modal4").modal('show');
            }
            if(response.success=='false'){
                $("#login_modal").modal('show');
            }
        },
        beforeSend: function () {
             $("#processing").show();
        },
        complete: function () {
             $("#processing").hide();
        },
        error: function(response){
             console.log('FPE = ', response);
        }
    });
}