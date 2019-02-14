# -*- coding: UTF-8 -*-
from setuptools import setup

setup(
    name='rc-car',
    author='Mihael Šinkec',
    url='https://github.com/msinkec/rpi-ip-car',
    license='MIT',
    py_modules=['rc_car'],
    install_requires=[
        gpiozero
    ]
)

