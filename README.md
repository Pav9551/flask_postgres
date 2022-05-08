## Тестовое задание для демонстрации работы Flask (веб-фреймворк) и PostgreSQL
#### Веб-сервис реализован на Python3, установлен через docker-compose и выполняет следующие функции:
```
```
- В сервисе реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer} ;
- После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов;
- Далее, полученные ответы сохраняются в базе данных, причем сохранена должна быть следующая информация: 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
- Ответом на Post запрос должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
```
```
## Оглавление

1. [Требования к операционной системе](#Требования-к-операционной-системе)
2. [Описание файла docker-compose.yaml](#Описание-файла-docker-compose.yaml)
3. [Установка веб-сервиса](#Установка-веб-сервиса)
4. [Пример использования](#Пример-использования)

## Требования к операционной системе
Тестирование сервиса проводилось на операционной системе ubuntu 20.04 установленной на виртуальном выделенном сервере. Перед началом работы необходимо установить на операционную систему docker и docker-compose<sup>[1](#myfootnote1)</sup>




## Описание файла docker-compose.yaml

```yaml
version: '3'

services:
  #имя сервиса
  postgres_jser:
    #имя контейнера
    container_name: postg_jser
    #образ, извлеченный из реестра Docker Hub
    image: postgres:13.6-alpine
    #Всегда перезапускать контейнер, если он останавливается.
    #Если он остановлен вручную, он перезапускается только при перезапуске демона Docker
    #или при ручном перезапуске самого контейнера.
    restart: always
    #Создание переменных окружения в контейнере
    #(параметры базы данных)
    environment:
      POSTGRES_DB: main
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 1234
    # Прописываем путь для хранения файлов.
    volumes:
      - ./postgres_jser/data/:/var/lib/postgresql/data
      - ./postgres_jser/prepare/init.sql:/docker-entrypoint-initdb.d/init.sql
    # Открываем порт в контейнер
    # Порт, который будет смотреть наружу : порт который используется внутри контейнера
    ports:
      - 5352:5432
  #имя сервиса
  web:
    # Путь до Dockerfile с настройками
    build: ./server
    #имя контейнера
    container_name: server-msg-broker
    #ссылка коммуникации сервисов
    links:
      - "postgres_jser"
    # Создание переменных окружения в контейнере
    environment:
      # для отладки (при запуске в релиз убрать!)
      - FLASK_ENV=development
      # Позволяет отслеживать процесс работы приложения в командной строке
      - PYTHONUNBUFFERED=True
    # ждет пока не будет запущен сервис с базой данных
    depends_on:
      - postgres_jser
    restart: always
    # Прописываем путь для хранения файлов.
    volumes:
      - ./server:/server
    # Открываем порт в контейнер
    # Порт, который будет смотреть наружу : порт который используется внутри контейнера
    ports:
      - "4999:4999"
    #команда для запуска исполняемого файла веб-сервиса через интерпретотор
    command: python app.py --host=0.0.0.0


```
## Установка веб-сервиса
 - Для установки веб-сервиса необходимо скопировать содержимое репозитория на диск выделенного сервера:
```curl   
git clone https://github.com/Pav9551/flask_postgres
```
 - перейти в папку с файлом restart.sh;
```curl   
cd flask_postgres
```
 - сделать файл restart.sh исполняемым:
```curl 
 sudo chmod +x restart.sh
 ```
 - запустить файл:
```curl 
 ./restart.sh
```
 - дождаться конца установки;
 - проверить состояние контейнеров командой:
```curl 
 docker-compose ps
```

 - убедиться, что подняты сервисы согласно документу docker-compose.yaml.

## Пример использования
Чтобы протестировать веб-сервис необходимо отправить Post запрос. Для этого необходимо знать IP адрес хоста, порт и шаблон запроса:
```curl
curl http://127.0.0.1:4999/questions -X POST -H "Content-Type: application/json" -d '{"questions_num": 5}'
```
```Python
#Python
import requests
endpoint = f'http://127.0.0.1:4999/questions'
headers = {
    "Content-Type": "application/json"
}
data = {"questions_num": 5}
r = requests.post(endpoint, json = data, headers = headers)#
print(r.status_code)
print(r.text)

```
Для подключения к базе данных PostgreSQL с помощью программы Navicat 15 for PostgreSQL извне используйте следующие данные:
```
```
 - Хост: {внешний IP хоста}
 - Порт: 5352
 - DB: main
 - USER: root
 - PASSWORD: 1234
```
```
<a name="myfootnote1">1</a> Информация по установке сервисов docker и docker-compose взята с сайта https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru и https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04 (step1):

