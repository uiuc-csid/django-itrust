import logging
from datetime import datetime

from dateutil.parser import isoparse
from django.core.cache import cache
from djangosaml2.backends import Saml2Backend

logger = logging.getLogger(__name__)


class ModifiedSaml2Backend(Saml2Backend):
    """Custom backend to handle group mapping etc...

    https://djangosaml2.readthedocs.io/contents/setup.html#custom-user-attributes-processing
    """

    def _update_user(
        self, user, attributes: dict, attribute_mapping: dict, force_save: bool = False
    ):
        return super()._update_user(user, attributes, attribute_mapping, force_save)

    def save_user(self, user, *args, **kwargs):
        return super().save_user(user, *args, **kwargs)

    def is_authorized(
        self,
        attributes: dict,
        attribute_mapping: dict,
        idp_entityid: str,
        assertion: dict,
        **kwargs
    ) -> bool:
        if not assertion:
            return True

        assertion_id = assertion.get("assertion_id")
        if cache.get(assertion_id):
            logger.warn("Received SAMLResponse assertion has been already used.")
            return False

        expiration_time = assertion.get("not_on_or_after")
        time_delta = isoparse(expiration_time) - datetime.now(datetime.timezone.utc)
        cache.set(assertion_id, "True", ex=time_delta)
        return True
