from setuptools import setup, find_packages

setup(
    name="harshe",
    version="1.0.0",
    description="Harshen Shirye-shiryen Kwamfuta a Yaren Hausa (Hausa Programming Language)",
    author="Harshe Core Team",
    packages=find_packages(),
    py_modules=["harshe_cli"],
    entry_points={
        "console_scripts": [
            "harshe=harshe_cli:main",
        ],
    },
    python_requires=">=3.10",
)
