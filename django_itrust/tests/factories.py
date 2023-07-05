import factory
from factory.django import DjangoModelFactory

from django_itrust.models import ITrustUser


class ITrustUserFactory(DjangoModelFactory):
    class Meta:
        model = ITrustUser
        django_get_or_create = ["username"]

    @staticmethod
    def get_username(obj):
        return f"{obj.first_name[0]}{obj.last_name}".lower()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(lambda obj: ITrustUserFactory.get_username(obj))
    email = factory.LazyAttribute(
        lambda obj: f"{ITrustUserFactory.get_username(obj)}@example.net"
    )
    is_staff = False
    is_superuser = False

    netid = factory.LazyAttribute(lambda obj: ITrustUserFactory.get_username(obj))
    ferpa_supress = False
    itrust_uin = factory.Sequence(lambda n: 1000 + n)
    itrust_affiliation = ["student"]  # Or 'staff

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if create:
            return

        raw_password = extracted or "admin"
        obj.set_password(raw_password)
        obj.save()
