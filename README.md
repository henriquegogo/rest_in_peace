# sqlite-rest

## What is?
Is a SQLite abstraction to use as a REST API with zero config.
It will raise a simple static html server and create an /api route that represents sql tables.

## Could I use in production?
No. This isn't prepared for production, have a simple http server and doesn't prevent things like SQL injection.
Only use in development mode.

## How to install and use
(Not published yet)
```
pip install sqlite-rest
sqlite-rest STATIC_HTML_FOLDER DATABASE.db PORT
```

## Routes
Return all tables
```
GET /
```

Get all items from a table
```
GET /table
```

Get a specific item from table
```
GET /table/item_id
```

Get filtered from a table
```
GET /table?id=item_id
```

Insert an item in a table
```
POST /table
DATA name=New
```

## Next steps
- UPDATE data with PUT requests
- DELETE data with DELETE requests

# License
MIT