from setuptools import find_packages, setup
from glob import glob
import os

# Nombre del paquete ROS (el de package.xml)
package_name = 'meshtastic_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Índice de ament
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        # package.xml
        ('share/' + package_name, ['package.xml']),
        # (opcional) ficheros estáticos y de datos, si los usas
        (os.path.join('share', package_name, 'static'),
         glob(os.path.join('static', '*'))),
        (os.path.join('share', package_name, 'data'),
         glob(os.path.join('data', '*'))),
    ],
    install_requires=[
        'setuptools',
        'paho-mqtt',
        'meshtastic',
        'cryptography',
        'tkintermapview',
    ],
    zip_safe=True,
    maintainer='Alex Guada',
    maintainer_email='alexgg327th@gmail.com',
    description='Nodo ROS2 con GUI Tkinter para Meshtastic + Turtlebot4',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # OJO: aquí va el paquete Python, que es la carpeta meshtastic_package
            'meshtastic_node = meshtastic_package.meshtastic_node:main',
        ],
    },
)

