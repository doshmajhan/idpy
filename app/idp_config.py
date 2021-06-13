import os.path
from pathlib import Path

from saml2 import (
    BINDING_HTTP_ARTIFACT,
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    BINDING_SOAP,
    BINDING_URI,
)
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
    print(BASEDIR)
    print(local_file)
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
# SIGN_ALG = ds.SIG_RSA_SHA512
# DIGEST_ALG = ds.DIGEST_SHA512


CONFIG = {
    "entityid": "%s/idp.xml" % BASE,
    "description": "Mock IDP",
    "valid_for": 168,
    "service": {
        "aa": {
            "endpoints": {"attribute_service": [("%s/attr" % BASE, BINDING_SOAP)]},
            "name_id_format": [NAMEID_FORMAT_TRANSIENT, NAMEID_FORMAT_PERSISTENT],
        },
        "aq": {
            "endpoints": {"authn_query_service": [("%s/aqs" % BASE, BINDING_SOAP)]},
        },
        "idp": {
            "name": "idpy",
            "endpoints": {
                "single_sign_on_service": [
                    ("%s/sso/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/sso/post" % BASE, BINDING_HTTP_POST),
                    ("%s/sso/art" % BASE, BINDING_HTTP_ARTIFACT),
                    ("%s/sso/ecp" % BASE, BINDING_SOAP),
                ],
                "single_logout_service": [
                    ("%s/slo/soap" % BASE, BINDING_SOAP),
                    ("%s/slo/post" % BASE, BINDING_HTTP_POST),
                    ("%s/slo/redirect" % BASE, BINDING_HTTP_REDIRECT),
                ],
                "artifact_resolve_service": [("%s/ars" % BASE, BINDING_SOAP)],
                "assertion_id_request_service": [("%s/airs" % BASE, BINDING_URI)],
                "manage_name_id_service": [
                    ("%s/mni/soap" % BASE, BINDING_SOAP),
                    ("%s/mni/post" % BASE, BINDING_HTTP_POST),
                    ("%s/mni/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/mni/art" % BASE, BINDING_HTTP_ARTIFACT),
                ],
                "name_id_mapping_service": [
                    ("%s/nim" % BASE, BINDING_SOAP),
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
