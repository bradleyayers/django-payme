from setuptools import setup, find_packages


setup(
    name="mamona",
    version="0.1",
    description="mamona app",

    author="Bradley Ayers",
    author_email="bradley.ayers@gmail.com",
    url='https://github.com/bradleyayers/mamona/',

    packages=find_packages(exclude=["example", "example.*"]),
    include_package_data=True,  # declarations in MANIFEST.in

    install_requires=["Django >=1.1"],

    classifiers=[
        "Development Status :: 0.1 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
