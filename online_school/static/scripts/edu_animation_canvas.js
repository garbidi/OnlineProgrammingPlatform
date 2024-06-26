window.onload = function() {
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let prevMouseX = null;
        let prevMouseY = null;
        let mouseSpeed = 0;

        let mouse = {
            x: null,
            y: null,
            radius: 50 // Радиус взаимодействия с частицами
        };

        window.addEventListener('scroll', function() {
            updateMousePosition();
        });

        canvas.addEventListener('mousemove', function(event) {
            updateMousePosition(event);
            if (prevMouseX !== null && prevMouseY !== null) {
                const dx = event.x - prevMouseX;
                const dy = event.y - prevMouseY;
                mouseSpeed = Math.sqrt(dx * dx + dy * dy);
            }
            prevMouseX = event.x;
            prevMouseY = event.y;
        });

        function updateMousePosition(event) {
            const canvasBounds = canvas.getBoundingClientRect();
            if (event) {
                mouse.x = event.x - canvasBounds.left;
                mouse.y = event.y - canvasBounds.top;
            } else {
                mouse.x = event.clientX - canvasBounds.left;
                mouse.y = event.clientY - canvasBounds.top;
            }

        // Проверяем, находится ли курсор внутри видимой области canvas
        if (
                mouse.x >= 0 &&
                mouse.x <= canvas.width &&
                mouse.y >= 0 &&
                mouse.y <= canvas.height
            ) {
                // Применяем эффекты частиц
            } else {
                // Курсор за пределами canvas, не применяем эффекты
            }
        }

        const textProperties = {
            text: 'EDULINE',
            size: 120,
            x: canvas.width / 2,
            y: canvas.height / 2

        };

        class Particle {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.size = 1;
                this.baseX = x; // Начальная позиция по X
                this.baseY = y; // Начальная позиция по Y
                this.density = (Math.random() * 30) + 1;
                this.speedX = 0; // Начальная скорость по X
                this.speedY = 0; // Начальная скорость по Y
                this.friction = 0.95; // Коэффициент торможения (0 < friction < 1)
            }

            draw() {
                ctx.fillStyle = 'black';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
            }

            update() {
                let dx = this.x - mouse.x;
                let dy = this.y - mouse.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                let maxDistance = mouse.radius;
                let force = 0;

                // Добавляем эффект дребезжания
                let jitterStrength = 0.37; // Сила дребезжания, можно настроить
                this.x += (Math.random() - 0.5) * jitterStrength;
                this.y += (Math.random() - 0.5) * jitterStrength;

                if (distance < maxDistance) {
                    force = (maxDistance - distance) / maxDistance;
                    force *= mouseSpeed;
                }

                let directionX = dx / distance;
                let directionY = dy / distance;

                let speed = 2;

                this.speedX = (this.speedX * this.friction) + (directionX * force * speed); // Применяем торможение к скорости по X
                this.speedY = (this.speedY * this.friction) + (directionY * force * speed); // Применяем торможение к скорости по Y

                this.x += this.speedX; // Используем скорость для перемещения частицы
                this.y += this.speedY; // Используем скорость для перемещения частицы

                // Возвращаем частицу к новым начальным координатам
                if (this.x !== this.baseX) {
                    let dx = this.x - this.baseX;

                    this.x -= dx / 20; // Уменьшаем скорость возвращения
                }
                if (this.y !== this.baseY) {
                    let dy = this.y - this.baseY;
                    this.y -= dy / 20; // Уменьшаем скорость возвращения
                }
            }
        }

        function createParticles() {
            ctx.fillStyle = 'black';
            ctx.font = `${textProperties.size}px Verdana`;
            ctx.fillText(textProperties.text, textProperties.x - ctx.measureText(textProperties.text).width / 2, textProperties.y);

            const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < canvas.width; i += 2) {
                for (let j = 0; j < canvas.height; j += 2) {
                    if (data[(i + j * canvas.width) * 4 + 3] > 128) {
                        particlesArray.push(new Particle(i, j));
                    }
                }
            }
        }

        let particlesArray = [];
        createParticles();

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particlesArray.length; i++) {
                particlesArray[i].draw();
                particlesArray[i].update();
            }
            requestAnimationFrame(animate);
        }

        animate();

        }