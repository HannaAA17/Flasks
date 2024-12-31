COLUMNS = [
    {'data': 'name', 'searchable': True, 'orderable': True},
    {'data': 'age', 'searchable': True, 'orderable': True},
    {'data': 'address', 'searchable': True, 'orderable': True},
    {'data': 'phone', 'searchable': True, 'orderable': True},
    {'data': 'email', 'searchable': True, 'orderable': True},
]

def generate_data():
    from random import randint
    return [
        {
            'name': 'name',
            'age': randint(1, 1000),
            'address': 'address',
            'phone': 'phone',
            'email': 'email',
        }

        for i in range(500)
    ]