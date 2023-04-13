import logging

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)


class ITrustUser(AbstractUser):
    """A base class for iTrust compatible django apps

    https://itrust.illinois.edu/federationregistry/registration/sp
    https://answers.uillinois.edu/illinois/page.php?id=48465
    https://answers.uillinois.edu/illinois/page.php?id=48435
    """

    class Meta(AbstractUser.Meta):
        abstract = True

    # username: (eduPersonPrincipalName) -> oid:1.3.6.1.4.1.5923.1.1.1.6
    # first_name: (givenName) -> oid:2.5.4.42
    # last_name: (sn) -> oid:2.5.4.4
    # email: (mail) -> oid:0.9.2342.19200300.100.1.3

    # netid: (uid, netid) -> oid:0.9.2342.19200300.100.1.1
    netid = models.CharField(max_length=256)
    # ferpa_supress: (iTrustSuppress) -> oid:1.3.6.1.4.1.11483.101.3
    ferpa_supress = models.BooleanField(default=False)
    # uin: (iTrustUIN) -> oid:1.3.6.1.4.1.11483.101.4
    itrust_uin = models.IntegerField(default=-1)
    # itrust_groups: (isMemberOf) -> oid:1.3.6.1.4.1.5923.1.5.1.1
    itrust_groups = models.JSONField(null=True, blank=True, default=list)
    # iTrustAffiliation:  oid:1.3.6.1.4.1.11483.101.1
    itrust_affiliation = models.JSONField(null=True, blank=True, default=list)

    # eduPersonOrgDN: oid:1.3.6.1.4.1.5923.1.1.1.3
    # eduPersonPrimaryAffiliation:  oid:1.3.6.1.4.1.5923.1.1.1.5
    # eduPersonTargetedID:  oid:1.3.6.1.4.1.5923.1.1.1.10
    # generationQualifier:  oid:2.5.4.44
    # homeOrganizationType:  oid:1.3.6.1.4.1.25178.1.2.10
    # iTrustMiddleName:  oid:1.3.6.1.4.1.11483.101.2
    # organizationName:  oid:2.5.4.10
    # eduPersonNickname:  oid:1.3.6.1.4.1.5923.1.1.1.2
    # iTrustHomeDeptCode:  oid:1.3.6.1.4.1.11483.101.5
    # organizationalUnit:  oid:2.5.4.11

    def process_groups(self, groups):
        if set(settings.SAML_SUPERUSER_GROUPS) & set(groups):
            self.is_staff = True
            self.is_superuser = True

        logger.debug(f"{groups = }")
        self.itrust_groups = groups

    def process_affiliations(self, affiliations):
        logger.debug(f"{affiliations = }")
        self.itrust_affiliation = affiliations

    def process_ferpa_supress(self, ferpa_supress):
        logger.debug(f"{ferpa_supress = }")
        value = str(ferpa_supress).lower()
        self.ferpa_supress = value in ["t", "y", "true", "1", "yes"]
