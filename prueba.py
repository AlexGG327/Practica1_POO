datos_json = [
    {'id': 1, 'nombre': 'Alice'},
    {'id': 2, 'nombre': 'Bob'},
    {'id': 3, 'nombre': 'Alice'}
]

nombre = 'Alice'
for item in datos_json:
    if nombre in item['nombre']:
        print("El nombre ya existe:", item['nombre'])