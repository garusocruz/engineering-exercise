# Avaaz Engineering Exercise Flask Data Service

This is a Flask application that provides a simple API to manage a list of data items. It is built using Flask and SQLAlchemy.

---

### To build application

> docker compose build --no-cache

---

### Load data step 1/2 (ONLY IN YOUR FIRST RUN)

> cp input/data.json app/data.json

---

### To run application

> docker compose up

---

### Load data step 2/2 (ONLY IN YOUR FIRST RUN)

In a new terminal run

> docker exec -it engineering-exercise-app-1 bash

> python load_data.py

An output like bellow must appears.

```
root@bb6127d9414b:/usr/app# python load_data.py
Created: {'id': 1, 'title': 'A arte de atingir seus objetivos simplesmente', 'url': 'http://matthews-espinoza.com/', 'date_added': datetime.datetime(2014, 3, 8, 15, 0)}
Created: {'id': 2, 'title': "L'avantage d'innover à l'état purl", 'url': 'http://www.hood.net/about.html', 'date_added': datetime.datetime(1985, 3, 30, 0, 0)}
```

Can close terminal session and use app to fetch data.

### To run coverage/pytest

> ./scripts/coverage.sh

---

## How to fetch API

To consume the application can you execute a curl like the example bellow.

```
curl --location 'http://HOST:5000/data?between=2014-01-01%3A2015-12-31&title=g' \
--header 'Content-Type: application/json'
```

### Extra INFO

> GET /data

Optional query parameters:

- after: Filter data items by date added after this date. Format: YYYY-MM-DD
- before: Filter data items by date added before this date. Format: YYYY-MM-DD
- between: Filter data items by date added between two dates. Format: YYYY-MM-DD:YYYY-MM-DD
- title: Filter data items by title. Case-insensitive search.
- url: Filter data items by URL. Case-insensitive search.

> Example:
>
> GET /data?after=2022-01-01&title=python

---

### Get a data item by ID

> GET /data/:id

> Example:
>
> GET /data/1

---

## Additional Features

### Create a new data item

> POST /data

> Example:
>
> ```
> {
>   "url": "https://www.python.org",
>   "title": "Python",
>   "date_added": "2022-01-01"
> }
> ```
