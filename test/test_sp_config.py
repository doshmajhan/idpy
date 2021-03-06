import os
from pathlib import Path

from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.saml import NAME_FORMAT_URI

try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None


if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin", "/usr/local/bin"])
else:
    xmlsec_path = "/usr/local/bin/xmlsec1"

BASEDIR = Path(__file__).parent


def full_path(local_file):
    return os.path.join(BASEDIR, local_file)


BASE = "http://localhost:8080"

CONFIG = {
    "entityid": BASE + "/sp",
    "description": "Mock SP",
    "service": {
        "sp": {
            "want_response_signed": False,
            "want_assertion_signed": True,
            "allow_unsolicited": True,
            "authn_requests_signed": True,
            "logout_requests_signed": True,
            "endpoints": {
                "assertion_consumer_service": [
                    ("%s/acs/post" % BASE, BINDING_HTTP_POST)
                ],
                "single_logout_service": [
                    ("%s/slo/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/slo/post" % BASE, BINDING_HTTP_POST),
                ],
            },
        },
    },
    "key_file": full_path("pki/key.pem"),
    "cert_file": full_path("pki/cert.pem"),
    "xmlsec_binary": xmlsec_path,
    "name_form": NAME_FORMAT_URI,
}
