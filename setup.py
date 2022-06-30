from setuptools import setup

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="discord-helpers",
    packages=["discord.ext.helpers"],
    version="0.2.0",
    license="MIT",
    description="A helper module for discord.py",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Dorukyum",
    url="https://github.com/Dorukyum/discord-helpers",
    keywords="discord, discord.py, API",
    install_requires=["aiohttp"],
    extras_require={"sqlite": "aiosqlite"},
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/Dorukyum/discord-helpers"},
)
