from setuptools import setup, find_packages


setup(
    name="django-payme",
    version="0.1",
    description="Yet another merchant payment app for Django",

    author="Bradley Ayers",
    author_email="bradley.ayers@gmail.com",
    url='https://github.com/bradleyayers/django-payme/',

    packages=find_packages(exclude=["example", "example.*"]),
    include_package_data=True,  # declarations in MANIFEST.in

    install_requires=["Django >=1.1"],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
