document.addEventListener('DOMContentLoaded', () => {
  const registerBtn = document.getElementById('registerBtn');
  const loginForm = document.getElementById('loginForm');
  const loginButton = document.getElementById('loginButton');

  registerBtn.addEventListener('click', () => {
    const fullName = document.getElementById('fullName').value;
    const registerEmail = document.getElementById('registerEmail').value;
    const registerPassword = document.getElementById('registerPassword').value;

    // Проверка заполнения полей
    if (!fullName || !registerEmail || !registerPassword) {
      alert('Пожалуйста, заполните все поля!');
      return;
    }

    // Отправляем данные на сервер
    fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: fullName,
        email: registerEmail,
        password: registerPassword
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert(data.message);
        // Обновляем страницу после успешной регистрации
        window.location.reload();
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при регистрации');
    });
  });

  loginButton.addEventListener('click', () => {
    const loginEmail = document.getElementById('loginEmail').value;
    const loginPassword = document.getElementById('loginPassword').value;

    // Проверка заполнения полей
    if (!loginEmail || !loginPassword) {
      alert('Пожалуйста, заполните поля email и пароля!');
      return;
    }

    // Отправляем данные на сервер для входа
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: loginEmail,
        password: loginPassword
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert(data.message);
        // Обновляем страницу после успешного входа
        window.location.reload();
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при входе');
    });
  });
});

function updateAuthContainer(email = null) {
    const authContainer = document.getElementById('authContainer');
    if (email) {
        authContainer.innerHTML = `
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#userModal">
                Welcome, ${email}
            </button>
        `;
    } else {
        authContainer.innerHTML = `
            <button type="button" class="btn btn-primary custom-login-btn" data-toggle="modal" data-target="#loginModal">
                Войти
            </button>
        `;
    }
}

function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateAuthContainer();
            $('#userModal').modal('hide');
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error(error));
}

window.onload = function() {
    fetch('/check_auth', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_authenticated) {
            updateAuthContainer(data.email);
        }
    })
    .catch(error => console.error(error));
}