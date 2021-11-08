# Rest-In-Peace (Database API)

## What is?
Is a database abstraction to use as a REST API with zero config.

## How to use
```
$ pip install rest-in-peace
$ rest-in-peace database.db 8000
```

## Routes
Static server. Return 'public/index.html'
```
GET /
```

Return schema
```
GET /schema.json
```

Return all items from collection
```
GET /{collection}
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

## Next steps
- Auth

# License
MIT