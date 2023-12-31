# KubernetesService-TestTask
Задание: разработать сервис, предназначенный для работы в облачной среде (Kubernetes).

## Описание сервиса
Сервис представляет собой хранилище JSON-объектов с HTTP-интерфейсом. Сохраненные
объекты размещаются в оперативной памяти, имеется возможность задать время жизни объекта.

## Функции сервиса
## 2.1 Запись объектов в хранилище PUT /objects/{Key}
    {Key} - идентификатор объекта в хранилище json объектов.
    Метод поддерживает опциональный заголовок Expires, который определяет время
    автоматического удаления объекта из хранилища.
    
## 2.2 Чтение объектов из хранилища GET /objects/{Key}
    {Key} - идентификатор объекта в хранилище json объектов

## 2.3 Проверка работоспособности и готовности
    Сервис должен поддерживать стандартные HTTP-методы проверки liveness и readiness для интеграции с k8s, саму интеграцию проводить не обязательно:

    • GET /probes/liveness
    • GET /probes/readiness

## 2.4 Получение метрик
    Сервис должен поддерживать метод для получения метрик в формате prometheus (можно использовать одноимённый пакет): 
    
    GET /metrics
    
    Достаточно стандартных системных метрик приложения, экспортируемых пакетом
    prometheus, но добавление прикладных метрик приветствуется.

## 2.5 Хранение данных на диске
    Необходимо обеспечить запись содержимого хранилища в файл на диске и восстановление состояния хранилища из файла при запуске приложения.

## Примечания:
    • время на выполнение задания - 1 неделя;
    • развитие функциональности за рамки задания не является обязательным, но приветствуется;
    • результаты работы имеет смысл отдать даже при частично выполненном задании.

## Запуск через Docker
```
$ docker-compose up
```

## Полезные ссылки
API документация к сервису
```
http://localhost:8000/docs
```
Prometheus для сбора метрик
```
http://localhost:9090/targets
```
Grafana для визуализации метрик (логин и пароль: admin/admin)
```
http://localhost:3000
```

## Визуализация метрик
Доступные дэшборды:
<img src="https://github.com/DanilaLabydin/KubernetesService-TestTask/blob/main/images/dashboards.png"/>
Кастомный дэшборд:
<img src="https://github.com/DanilaLabydin/KubernetesService-TestTask/blob/main/images/custom_dashboard.jpg"/>
