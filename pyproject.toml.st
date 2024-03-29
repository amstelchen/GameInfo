[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "GameInfo"
description = "System info tool for gamers"
authors = [ { name= "Michael John", email= "michael.john@gmx.at" } ]
readme = "README.md"
keywords = ["gaming", "tool", "wine", "proton", "steam", "lutris"]
license = {text = "GPL"}
classifiers = [
    "Programming Language :: Python :: 3",
]
dependencies = [
    "requests",
    'importlib-metadata; python_version>="3.8"',
]
dynamic = ["version"]

[project.optional-dependencies]
#pdf = ["ReportLab>=1.2", "RXP"]
#rest = ["docutils>=0.3", "pack ==1.1, ==1.3"]

[project.urls]
homepage = "https://github.com/amstelchen/GameInfo"
repository = "https://github.com/amstelchen/GameInfo"
documentation = "https://github.com/amstelchen/GameInfo"

[project.scripts]
gameinfo = "GameInfo.GameInfo:main"

[tool.setuptools.dynamic]
version = {attr = "GameInfo.VERSION"}