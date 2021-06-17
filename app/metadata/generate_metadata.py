#!/usr/bin/env python
"""
Script that creates a SAML2 metadata file from a pysaml2 entity configuration file
"""
import os
from pathlib import Path

from saml2.config import Config
from saml2.metadata import (
    entity_descriptor,
    metadata_tostring_fix,
    sign_entity_descriptor,
)
from saml2.sigver import security_context
from saml2.validate import valid_instance

METADATA_VALID_FOR = 365 * 24
IDP_METADATA_FILE = "idp.xml"
IDP_CONFIG_FILE_NAME = "../idp_config.py"  # TODO figure out how to import this
NAME_SPACE_PAIR = {"xs": "http://www.w3.org/2001/XMLSchema"}
CONFIG_FILE = os.path.join(Path(__file__).parent, IDP_CONFIG_FILE_NAME)


if __name__ == "__main__":
    conf = Config().load_file(CONFIG_FILE)
    conf.valid_for = METADATA_VALID_FOR
    secc = security_context(conf)
    eid = entity_descriptor(conf)
    eid, xmldoc = sign_entity_descriptor(eid, None, secc)

    valid_instance(eid)
    xmldoc = metadata_tostring_fix(eid, NAME_SPACE_PAIR, xmldoc)
    with open(IDP_METADATA_FILE, "w+") as metadata_file:
        metadata_file.write(xmldoc)
