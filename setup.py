#!/usr/bin/env python

from distutils.core import setup

setup(
    name="DigitalFootprintsBackend",
    version="0.31",
    description="Backend API for the DigitalFootprintsLab",
    author="Kasper Welbers",
    author_email="kasperwelbers@gmail.com",
    packages=["DigitalFootprintsBackend"],
    include_package_data=True,
    zip_safe=False,
    keywords=["API", "Data Donation"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "pydantic",
        'authlib',
        'bcrypt',
        "requests",
        "lxml"
    ],
    extras_require={
        'dev': [
            'uvicorn[standard]',
            'gunicorn',
            'pytest',
            'codecov',
            'python-multipart'
        ]
    },
)
