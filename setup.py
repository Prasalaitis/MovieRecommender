from setuptools import find_packages, setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="Capstone",
    version="0.1.0",
    author="Edgaras Gacionis",
    author_email="gyvenimasritmu@gmail.com",
    description="A python based movie recommendation system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TuringCollegeSubmissions/egacio-DE1.v2.4.1/",
    license="Turing",
    packages=find_packages(),  # Automatically find all packages and subpackages
    classifiers=[  # Classifiers to categorize your package
        "Programming Language :: Python :: 3",
        "License :: Turing :: Custom License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
