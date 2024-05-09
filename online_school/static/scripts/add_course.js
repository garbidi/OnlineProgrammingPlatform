document.getElementById('startCourseBtn').addEventListener('click', function() {
    const topicId = this.dataset.topicId;
    const topicName = topicId; // Используем topicId в качестве названия темы

    console.log('Отправляемое название темы:', topicName);

    // Отправка AJAX-запроса на сервер Flask
    fetch('/add_topic_to_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic_name: topicName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Тема успешно добавлена в "Моё обучение"');
            alert('Тема успешно добавлена в ваш раздел "Моё обучение".');
        } else {
            console.error('Ошибка при добавлении темы в "Моё обучение":', data.error);
            alert('Ошибка: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка при выполнении AJAX-запроса:', error);
        alert('Произошла ошибка при добавлении темы в "Моё обучение". Пожалуйста, попробуйте еще раз.');
    });
});
