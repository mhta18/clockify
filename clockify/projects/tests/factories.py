import uuid
import factory
from projects.models import Project
from teams.tests.factories import (
    TeamFactory,
)  # Import your Team factory if you have one


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("catch_phrase")
    color = "#D1D5DB"

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                self.teams.add(team)
