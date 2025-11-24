from setuptools import find_packages, setup
import os

package_name = 'meshtastic_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Copiar toda la carpeta static al share
        (os.path.join('share', package_name, 'static'), 
            ['meshtastic_package/static/config.json']),
        # Copiar cualquier otro archivo de datos si hace falta
        (os.path.join('share', package_name, 'data'), 
            ['meshtastic_package/data/contactos.json',
             'meshtastic_package/data/mensaje_posicion_recibido.json',
             'meshtastic_package/data/mensaje_telemetria_recibido.json',
             'meshtastic_package/data/mensaje_texto_recibido.json']),
    ],
    install_requires=[
        'setuptools',
        'meshtastic',
        'paho-mqtt',
        'tkintermapview',
        'cryptography'
        ],
    zip_safe=True,
    maintainer='alexg',
    maintainer_email='alexgg327th@gmail.com',
    description='Nodo Meshtastic para TurtleBot4',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'meshtastic_node = meshtastic_package.meshtastic_node:main'
        ],
    },
)
