# Da-Da-Da (Database API)

## What is?
Is a database abstraction to use as a REST API with zero config.

## How to install and use
(Not published yet)
```
pip install dadada
```

## Routes
Return all collections
```
GET /
```

Return all items from collection
```
GET /<collection>
```

Get a specific item
```
GET /<collection>/<id>
```

Create an item
```
POST /<collection>/<id>
DATA 'Data'
```

Update an item
```
PUT /<collection>/<id>
DATA 'Data'
```

Delete an item
```
DELETE /<collection>/<id>
```

## Next steps
- Search

# License
MIT