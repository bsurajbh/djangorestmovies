from faker import Factory
from django.contrib.auth.models import User
import factory
from api.movies.models import Movies, UserFeedback
import random

faker = Factory.create()


class RatingChoice(factory.LazyFunction):
    def __init__(self, model_class, field, *args, **kwargs):
        choices = [choice[0] for choice in model_class._meta.get_field(field).choices]
        super(RatingChoice, self).__init__(
            function=lambda: random.choice(choices),
            *args, **kwargs
        )


class UserFactory(factory.DjangoModelFactory):
    password = 'password@123'
    username = faker.first_name() + str(random.randint(0,1000)) + faker.last_name()
    password = password
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()

    class Meta:
        model = User


class MovieFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda _: faker.name())
    year = factory.LazyAttribute(lambda _: faker.year())
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Movies


class UserFeedbackFactory(factory.DjangoModelFactory):
    movie = factory.SubFactory(MovieFactory)
    rating = RatingChoice(UserFeedback, 'rating')
    comment = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=2))
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = UserFeedback
