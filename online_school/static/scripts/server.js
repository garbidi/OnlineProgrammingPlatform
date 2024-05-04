$(document).ready(function() {
    $('#registerBtn').click(function(event) {
        event.preventDefault();

        var fullName = $('#fullName').val();
        var email = $('#registerEmail').val();
        var password = $('#registerPassword').val();

        var isValid = true;
        if (fullName.trim() === '') {
            $('#fullNameError').text('Пожалуйста, введите ФИО');
            isValid = false;
        } else {
            $('#fullNameError').text('');
        }

        if (email.trim() === '') {
            $('#registerEmailError').text('Пожалуйста, введите электронную почту');
            isValid = false;
        } else {
            $('#registerEmailError').text('');
        }

        if (password.trim() === '') {
            $('#registerPasswordError').text('Пожалуйста, введите пароль');
            isValid = false;
        } else {
            $('#registerPasswordError').text('');
        }

        if (isValid) {

            $.ajax({
                url: '/register',
                type: 'POST',
                data: JSON.stringify({ fullName: fullName, email: email, password: password }),
                contentType: 'application/json',
                success: function(response) {
                    console.log(response);
                    $('#registrationModal').modal('hide');
                    // Дополнительные действия после успешной регистрации
                },
                error: function(error) {
                    console.log(error);
                    // Отображение сообщения об ошибке
                }
            });
        }
    });
});
