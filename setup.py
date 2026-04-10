from setuptools import setup

setup(
    name="smart-commit",
    version="1.0.0",
    description="AI-powered Git commit message generator using Claude",
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
)
