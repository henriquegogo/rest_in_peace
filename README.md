# Da-Da-Da (Database API)

## What is?
Is a database abstraction to use as a REST API with zero config.

## How to use
```
python main.py
```

## Routes
Return schema
```
GET /
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
- Router improvements

# License
MIT