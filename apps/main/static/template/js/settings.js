$(document).ready(function(){
	$('#change-password-btn').on('click', function(){
		$.ajax({
			url: CHANGE_USER_SETTINGS,
			method: 'POST',
			data: {'field': 'password', 'password_new': $('#password-new').val(), 'password_old': $('#password-old').val()},
			dataType: 'json',
			success: function(data){
				console.log(data);
				if (data['status'] == 'success'){
					$('#password-old').val('');
					$('#password-new').val('');
					$('#password-notify').removeClass();
					$('#password-notify').addClass('alert alert-success');
					
				}
				else{
					$('#password-notify').removeClass();
					$('#password-notify').addClass('alert alert-danger');
					
				}
				$('#password-notify').html(data['message']);
			},
			error: function(data){ 
					console.log('error');
					console.log(data); 
					
			}
		});
		return false;
	});
	
    $('#changeemail').click(function(event) {
     	$.ajax({
			url: CHANGE_USER_SETTINGS,
			method: 'POST',
			data: {'field': 'email', 'email': $('#email').val()},
			dataType: 'json',
			success: function(data){
				console.log(data);
				if (data['status'] == 'success'){
					$('#email').val(data['email']);
					$('#email-notify').removeClass();
					$('#email-notify').addClass('alert alert-success');
					
				}
				else{
					$('#email-notify').removeClass();
					$('#email-notify').addClass('alert alert-danger');
					
				}
				$('#email-notify').html(data['message']);
			},
			error: function(data){ 
					console.log('error');
					console.log(data); 
					
			}
		});
		return false;
    });
});