# Rest-In-Peace (Database API)

## What is this?
It's a database abstraction to use as a REST API with zero config.

## How to use
```
$ pip install rest-in-peace
$ rest-in-peace database.db 8000
```

## Routes
Static server. Return 'public/index.html' (Tip: Download and use Swagger here)
```
GET /
```

Return API definitions
```
GET /openapi.json
```

Return all items from collection
```
GET /{collection}
```

Delete collection
```
DELETE /{collection}
```

Get a specific item
```
GET /{collection}/{id}
```

Create an item
```
POST /{collection}/{id}
DATA 'Data'
```

Update an item
```
PUT /{collection}/{id}
DATA 'Data'
```

Delete an item
```
DELETE /{collection}/{id}
```

## Tests
```
python tests
```

## Next steps
- Auth / Roles
- Dynamic / Static schema
- SQL Injection fix

# License
MIT