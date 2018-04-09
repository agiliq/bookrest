Bookrest - The easiest way to add rest API to an arbitrary DB
------------------------------------------------------------------------------

![bookrest image](bookrest.jpg)

Bookrest allows you to add an API (and browsable htmls) to arbitrary databases -- well almost arbitrary, the tables must have PKs.
The databases do no need to be managed by Django.


Installation and usage
++++++++++++++++++++++++

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


![bookrest image](bookrest.gif)
