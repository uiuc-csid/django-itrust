import factory
from factory.django import DjangoModelFactory

from django_itrust.models import ITrustUser


class ITrustUserFactory(DjangoModelFactory):
    class Meta:
        model = ITrustUser
        django_get_or_create = ["username"]

    email = factory.Faker("safe_email")
    username = factory.LazyAttribute(lambda obj: obj.email)
    password = factory.PostGenerationMethodCall("set_password", "adm1n")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_superuser = False

    netid = factory.Faker("user_name")
    ferpa_supress = False
    itrust_uin = factory.Sequence(lambda n: 1000 + n)
    itrust_affiliation = ["student"]  # Or 'staff
