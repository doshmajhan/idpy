import os.path
from pathlib import Path

from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT, BINDING_SOAP
from saml2.saml import (
    NAME_FORMAT_URI,
    NAMEID_FORMAT_PERSISTENT,
    NAMEID_FORMAT_TRANSIENT,
)

try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin"])
else:
    xmlsec_path = "/usr/bin/xmlsec1"

BASEDIR = Path(__file__).parent


def full_path(local_file):
    return os.path.join(BASEDIR, local_file)


HOST = "localhost"
PORT = 8080

HTTPS = False

if HTTPS:
    BASE = "https://%s:%s" % (HOST, PORT)
else:
    BASE = "http://%s:%s" % (HOST, PORT)

# HTTPS cert information
SERVER_CERT = "pki/cert.pem"
SERVER_KEY = "pki/key.pem"
CERT_CHAIN = ""
SIGN_ALG = None
DIGEST_ALG = None


CONFIG = {
    "entityid": "%s/idp.xml" % BASE,
    "description": "Mock IDP",
    "valid_for": 168,
    "service": {
        "idp": {
            "name": "idpy",
            "endpoints": {
                "single_sign_on_service": [
                    ("%s/sso" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/sso" % BASE, BINDING_HTTP_POST),
                ],
                "single_logout_service": [
                    ("%s/slo" % BASE, BINDING_SOAP),
                    ("%s/slo" % BASE, BINDING_HTTP_POST),
                    ("%s/slo" % BASE, BINDING_HTTP_REDIRECT),
                ],
            },
            "policy": {
                "default": {
                    "lifetime": {"minutes": 15},
                    "attribute_restrictions": None,
                    "name_form": NAME_FORMAT_URI,
                },
            },
            "name_id_format": [NAMEID_FORMAT_TRANSIENT, NAMEID_FORMAT_PERSISTENT],
        },
    },
    "debug": 1,
    "key_file": full_path("pki/key.pem"),
    "cert_file": full_path("pki/cert.pem"),
    "organization": {
        "display_name": "idpy",
        "name": "idpy",
        "url": "http://localhost",
    },
    "xmlsec_binary": xmlsec_path,
    "metadata": {"local": [full_path("resources/metadata/idp.xml")]},
    "logging": {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s] %(message)s",
            },
        },
        "handlers": {
            "stderr": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "level": "DEBUG",
                "formatter": "simple",
            },
        },
        "loggers": {
            "saml2": {"level": "DEBUG"},
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
            ],
        },
    },
}
