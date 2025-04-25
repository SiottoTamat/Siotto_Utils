from setuptools import setup, find_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="File_handler",
    version="1.0.0",
    author="Andrea Siotto",
    author_email="siotto.andrea@temple.edu",
    description="A personal Python utility library.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # <--- important for markdown
    url="https://github.com/yourusername/File_handler",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["pandas", "openpyxl"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
