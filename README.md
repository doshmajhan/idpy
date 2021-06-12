# IdPy
Mock SAML IDP in Python for testing

## Setup
### Install `poetry`
```bash
pip install poetry
```
### Install xmlsec1
```bash
apt install xmlsec1
yum install xmlsec1
```

### Create certs
```bash
cd app/pki
./create_cert.sh
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
