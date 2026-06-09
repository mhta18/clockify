import factory
from teams.models import Team,Task


from users.tests.factories import UserFactory

from django.utils import timezone
from datetime import timedelta

class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
        skip_postgeneration_save = True
    name = factory.Sequence(lambda n: f"Engineeering Team {n}")
    description = factory.Faker("paragraph", nb_sentences=3)

    supervisor = factory.SubFactory(UserFactory,gender="other", is_active=True, age=34)
    logo = factory.django.ImageField(filename="alpha_team_logo.png")
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


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: f"Task Specification Blueprint #{n}")
    description = factory.Faker("paragraph", nb_sentences=3)

    priority = Task.Priority.MEDIUM
    status = Task.Status.TODO

    deadline = factory.LazyAttribute(lambda o: timezone.now() + timedelta(days=7))

    team = factory.SubFactory(TeamFactory)
    created_by = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)
