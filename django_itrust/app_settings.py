from pathlib import Path

import saml2.saml
from django.conf import settings

##### APP CONFIGURATION #####

LOGIN_URL = "/saml2/login/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_REDIRECT

SAML_ATTRIBUTE_MAPPING = {
    "eduPersonPrincipalName": ("username",),
    "mail": ("email",),
    "givenName": ("first_name",),
    "sn": ("last_name",),
    "uid": ("netid",),
    "iTrustSuppress": ("ferpa_supress",),
    "iTrustUIN": ("itrust_uin",),
    "isMemberOf": ("itrust_groups",),
    "iTrustAffiliation": ("itrust_affiliation",),
}
SAML_DJANGO_USER_MAIN_ATTRIBUTE = "username"
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = "__iexact"
SAML2_DISCO_URL = "https://discovery.illinois.edu/discovery/DS"

####### PYSAML CONFIG #######

_BASE_URLS = settings.SAML_BASE_URLS
_SAML_KEY_FILE = settings.SAML_KEY_FILE
_SAML_CERT_FILE = settings.SAML_CERT_FILE
_ENTITY_NAME = settings.SAML_ENTITY_NAME
_ENTITY_ID = settings.SAML_ENTITY_ID
_CONTACT_PERSON = settings.SAML_CONTACT_PERSON
_SAML_CONFIG_DIR = Path(__file__).parent / "saml_config"


SAML_CONFIG = {
    "entityid": _ENTITY_ID,
    "service": {
        "sp": {
            "name": _ENTITY_NAME,
            "name_id_format": saml2.saml.NAMEID_FORMAT_TRANSIENT,
            # 'allow_unsolicited': True,
            # 'force_authn': False,
            "endpoints": {
                "assertion_consumer_service": [
                    (base_url + "/saml2/acs/", saml2.BINDING_HTTP_POST)
                    for base_url in _BASE_URLS
                ],
                "single_logout_service": [
                    f"{base_url}/{suffix}"
                    for suffix in ["saml2/ls/", "saml2/ls/post"]
                    for base_url in _BASE_URLS
                ],
            },
            "required_attributes": ["eduPersonPrincipalName"],
            "optional_attributes": [
                "mail",
                "givenName",
                "sn",
                "uid",
                "iTrustSuppress",
                "iTrustUIN",
                "isMemberOf",
                "iTrustAffiliation",
            ],
            "idp": {
                "urn:mace:incommon:uiuc.edu": {
                    "single_sign_on_service": {
                        saml2.BINDING_HTTP_POST: "https://shibboleth.illinois.edu/idp/profile/SAML2/POST/SSO",
                        saml2.BINDING_HTTP_REDIRECT: "https://shibboleth.illinois.edu/idp/profile/SAML2/Redirect/SSO",
                    },
                    "single_logout_service": {
                        saml2.BINDING_HTTP_REDIRECT: "https://shibboleth.illinois.edu/idp/profile/Logout",
                    },
                },
            },
        }
    },
    "xmlsec_binary": "/usr/bin/xmlsec1",
    "attribute_map_dir": str(_SAML_CONFIG_DIR / "attribute_maps"),
    "allow_unknown_attributes": True,
    "metadata": {
        "mdq": [
            {
                "url": "https://mdq.incommon.org/",
                "cert": _SAML_CONFIG_DIR / "certs" / "inc-md-cert-mdq.pem",
            }
        ]
    },
    # set to 1 to output debugging information
    "debug": 1,
    # certificate and key
    "key_file": _SAML_KEY_FILE,
    "cert_file": _SAML_CERT_FILE,
    "encryption_keypairs": [
        {
            "key_file": _SAML_KEY_FILE,
            "cert_file": _SAML_CERT_FILE,
        }
    ],
    # own metadata settings
    "contact_person": _CONTACT_PERSON,
    "valid_for": 4,  # how long is our metadata valid
}
