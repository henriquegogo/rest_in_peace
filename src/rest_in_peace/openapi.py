def openapi(schema, host, port):
    def convert_type(row_type):
        return 'string' if row_type == 'TEXT' else 'NUMBER' if row_type == 'REAL' else row_type.lower()

    definitions = {
        'openapi': '3.0.0',
        'servers': [{'url': f'http://{host}:{port}'}],
        'info': {'title': 'API', 'version': '1.0.0'},
        'paths': {
            '/': {'get': {'description': 'Static index.html contained in /public folder'}},
            '/openapi.json': {'get': {'description': 'Return API definitions'}},
            '/{collection}': {
                'post': {
                    'description': 'New item for {collection}',
                    'produces': ['application/json'],
                    'parameters': [
                        {'name': 'collection', 'in': 'path', 'required': True}
                    ],
                    'requestBody': {
                        'content': {
                            'application/json': {'schema': {'example': '{"key": "value"}'}},
                            'text/plain': {'schema': {'example': 'key=value&key2=value2'}}
                        }
                    },
                    'responses': {
                        '201': {'description': 'Created'}
                    }
                }
            },
        },
        'components': {'schemas': {}}
    }

    for table, columns in schema.items():
        definitions['paths'][f'/{table}'] = {
            'get': {
                'produces': ['application/json'],
                'description': f'Return all {table}',
                'parameters': [
                    {'name': 'orderby', 'in': 'query', 'required': False},
                    {'name': 'limit', 'in': 'query', 'required': False},
                    {'name': 'offset', 'in': 'query', 'required': False}
                ] + [{
                    'name': row_name, 'in': 'query', 'required': False,
                    'type': convert_type(row_type), 'description': f'Filter by {row_name}'
                } for row_name, row_type in columns.items() if row_name != 'id'],
                'responses': {
                    '200': {'description': 'OK'}
                }
            },
            'post': {
                'produces': ['application/json'],
                'consumes': ['application/json', 'multipart/form-data'],
                'description': f'New item for {table}',
                'requestBody': {
                    'content': {
                        'application/json': {'schema': {'$ref': f'#/components/schemas/{table}'}},
                        'text/plain': {'schema': {'example': 'key=value&key2=value2'}}
                    }
                },
                'responses': {
                    '201': {'description': 'Created'}
                }
            },
            'delete': {
                'description': f'Delete all {table}',
                'responses': {
                    '204': {'description': 'No Content'}
                }
            }
        }
        definitions['paths'][f'/{table}/{{id}}'] = {
            'get': {
                'produces': ['application/json'],
                'parameters': [
                    {'name': 'id', 'in': 'path', 'required': True}
                ],
                'responses': {
                    '200': {'description': 'OK'},
                    '404': {'description': 'Not Found'}
                }
            },
            'put': {
                'produces': ['application/json'],
                'consumes': ['application/json', 'multipart/form-data'],
                'parameters': [
                    {'name': 'id', 'in': 'path', 'required': True}
                ],
                'requestBody': {
                    'content': {
                        'application/json': {'schema': {'$ref': f'#/components/schemas/{table}'}},
                        'text/plain': {'schema': {'example': 'key=value&key2=value2'}}
                    }
                },
                'responses': {
                    '200': {'description': 'OK'},
                    '404': {'description': 'Not Found'}
                }
            },
            'delete': {
                'produces': ['application/json'],
                'parameters': [
                    {'name': 'id', 'in': 'path', 'required': True}
                ],
                'responses': {
                    '200': {'description': 'OK'},
                    '404': {'description': 'Not Found'}
                }
            }
        }
        definitions['components']['schemas'][table] = {"properties": {}}

        for row_name, row_type in columns.items():
            if row_name != 'id':
                definitions['components']['schemas'][table]["properties"][row_name] = {'type': convert_type(row_type)}

    return definitions
