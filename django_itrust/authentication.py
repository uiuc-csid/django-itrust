import logging
from datetime import datetime, timezone
from typing import Dict

from dateutil.parser import isoparse
from django.core.cache import cache
from djangosaml2.backends import Saml2Backend

logger = logging.getLogger(__name__)


class ModifiedSaml2Backend(Saml2Backend):
    """Custom backend to handle group mapping etc...

    https://djangosaml2.readthedocs.io/contents/setup.html#custom-user-attributes-processing
    """

    def is_authorized(
        self,
        attributes: Dict,
        attribute_mapping: Dict,
        idp_entityid: str,
        assertion: Dict[str, str],
        **kwargs,
    ) -> bool:
        if not assertion:
            return True

        assertion_id = assertion.get("assertion_id")
        if cache.get(assertion_id):
            logger.warn("Received SAMLResponse assertion has been already used.")
            return False

        expiration_time = assertion.get("not_on_or_after")
        time_delta = isoparse(expiration_time) - datetime.now(timezone.utc)
        cache.set(assertion_id, "True", timeout=int(time_delta.total_seconds()))
        return True
