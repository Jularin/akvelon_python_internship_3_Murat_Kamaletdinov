# akvelon_python_internship_3_Murat_Kamaletdinov
tasks for intership in akvelon company

### Up postgres database
```
docker-compose up -d --build
```

### Install poetry package manager
```
pip3 install poetry
```

### Install dependences
```
cd src && poetry install
```

### Activate virtual environment
```
poetry shell
```

### Run tests and check code coverage
```
coverage run -m pytest && coverage report --rcfile=.coveragerc
```

### Run only tests
```
pytest
```
