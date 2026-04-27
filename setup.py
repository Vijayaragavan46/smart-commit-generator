from setuptools import setup

setup(
    name="smart-commit-generator",
    version="1.1.0",
    author="Vijayaragavan46",
    author_email="",
    description="AI-powered Git commit message generator using Claude",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vijayaragavan46/smart-commit-generator",
    py_modules=["smart_commit"],
    install_requires=[
        "anthropic>=0.40.0",
    ],
    entry_points={
        "console_scripts": [
            "smart-commit=smart_commit:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    keywords="git commit ai claude anthropic conventional-commits cli developer-tools",
)
