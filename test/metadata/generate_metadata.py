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
IDP_METADATA_FILE = "test-idp.xml"
SP_METADATA_FILE = "test-sp.xml"
IDP_CONFIG_FILE_NAME = "../test_idp_config.py"  # TODO figure out how to import this
SP_CONFIG_FILE_NAME = "../test_sp_config.py"  # TODO figure out how to import this
NAME_SPACE_PAIR = {"xs": "http://www.w3.org/2001/XMLSchema"}
IDP_CONFIG_FILE = os.path.join(Path(__file__).parent, IDP_CONFIG_FILE_NAME)
SP_CONFIG_FILE = os.path.join(Path(__file__).parent, SP_CONFIG_FILE_NAME)


if __name__ == "__main__":
    sp_config = Config().load_file(SP_CONFIG_FILE)
    sp_config.valid_for = METADATA_VALID_FOR
    sp_sec_context = security_context(sp_config)
    sp_eid = entity_descriptor(sp_config)
    sp_eid, sp_xml_doc = sign_entity_descriptor(sp_eid, None, sp_sec_context)

    valid_instance(sp_eid)
    sp_xml_doc = metadata_tostring_fix(sp_eid, NAME_SPACE_PAIR, sp_xml_doc)
    with open(SP_METADATA_FILE, "w+") as metadata_file:
        metadata_file.write(sp_xml_doc)

    idp_config = Config().load_file(IDP_CONFIG_FILE)
    idp_config.valid_for = METADATA_VALID_FOR
    idp_sec_context = security_context(idp_config)
    idp_eid = entity_descriptor(idp_config)
    idp_eid, idp_xml_doc = sign_entity_descriptor(idp_eid, None, idp_sec_context)

    valid_instance(idp_eid)
    idp_xml_doc = metadata_tostring_fix(idp_eid, NAME_SPACE_PAIR, idp_xml_doc)
    with open(IDP_METADATA_FILE, "w+") as metadata_file:
        metadata_file.write(idp_xml_doc)
