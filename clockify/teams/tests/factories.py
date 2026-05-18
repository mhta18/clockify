import factory
from teams.models import Team
from users.tests.factories import UserFactory


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
        skip_postgeneration_save = True
    name = factory.Sequence(lambda n: f"Engineeering Team {n}")
    description = factory.Faker("paragraph", nb_sentences=3)

    supervisor = factory.SubFactory(UserFactory, is_active=True)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        # chack if they have saved in db
        if not create:
            return

        # membering the supervisor
        self.members.add(self.supervisor)

        if extracted:
            for member in extracted:
                self.members.add(member)
    
        self.save()
        
