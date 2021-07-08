from setuptools import setup

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="discord-helpers",
    packages=["discord.ext.helpers"],
    version="0.0.5",
    license="MIT",
    description="A helper module for discord.py",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Dorukyum",
    url="https://github.com/Dorukyum/discord-helpers",
    keywords="discord, discord.py, API",
    install_requires=open("requirements.txt").read().split("\n"),
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/Dorukyum/discord-helpers"},
)
