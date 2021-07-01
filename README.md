# idpy
[![build](https://github.com/doshmajhan/idpy/actions/workflows/build.yml/badge.svg)](https://github.com/doshmajhan/idpy/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/doshmajhan/idpy/branch/main/graph/badge.svg?token=DL4ST9THVL)](https://codecov.io/gh/doshmajhan/idpy)
[![CodeQL](https://github.com/doshmajhan/idpy/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/doshmajhan/idpy/actions/workflows/codeql-analysis.yml)

Mock SAML Identity Provider in Python for testing SAML Service Provider implementations

### **Still under development*

## Setup

### Requirements
* pip
* npm
* xmlsec1

### Install dependencies
```bash
pip install poetry
poetry install
```
### Install xmlsec1
```bash
apt install xmlsec1
yum install xmlsec1
```

### Install npm
```bash
apt install npm
yum install npm
```

### Create certs
```bash
cd app/pki
./create-cert.sh
```

### Generate metadata
```bash
cd app/metadata
poetry run python generate_metadata.py
```

## Build
```bash
make build
```

## Run
```bash
make run
```

## Development setup
Same as above setup plus a few more steps

### Install git hooks
```bash
make install-hooks
```

### Create test certs
```bash
cd test/pki
./create-cert.sh
```

### Generate test metadata
```bash
cd test/metadata
poetry run python generate_metadata.py
```

### Run tests
```bash
make pytest
```