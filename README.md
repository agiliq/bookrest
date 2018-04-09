### Bookrest - The easiest way to add rest API to an arbitrary DB


![bookrest image](assets/bookrest.jpg)

Bookrest allows you to add an API (and browsable htmls) to arbitrary databases -- well almost arbitrary, the tables must have PKs.
The databases do not need to be managed by Django.


#### Installation and usage


```bash
pip install bookrest
```

Then in your `settings.py`,


```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "bookrest",
]
```

Add a key to your `settings.DATABASES` named `bookrest`, and point it to the DB you want to expose as an API. Keep your `default` db as is, you can use it for user management and other Django apps.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    },
    "bookrest": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "data/sample.sqlite3"),
    },
}
```

Connect your urls to `bookrest.urls`

```python
urlpatterns = [
    # ...
    path("api/", include("bookrest.urls"))
]
```

🚀 Boom! You are in business. All your tables will have a full read/write API

![bookrest image](assets/bookrest.gif)

### Todo

- [X] Test with Sqlite
- [ ] Publish on Pypi
- [ ] Test with Postgres
- [ ] Test with Mysql
- [ ] Add setting to enable a read only API
- [ ] Enable circleci
- [ ] Silently drop tables with no PKs rather than failing (bad idea??)
