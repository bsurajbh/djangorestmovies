from django.contrib.auth.models import User
from django.core.management import BaseCommand
from factories import MovieFactory, UserFactory, UserFeedbackFactory
from api.movies.models import Movies


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('seed', type=int, help='Number of users to be created')

    def handle(self, *args, **kwargs):
        try:
            seed = kwargs['seed']
            if seed:
                print('populating database...')
                for _ in range(seed):
                    user = UserFactory.create()
                    movies = MovieFactory.create_batch(5, created_by=user)
                    for movie in movies:
                        UserFeedbackFactory(created_by=user, movie=movie)

                # random comments
                
                users = User.objects.all()[:10]
                movies = Movies.objects.exclude(movies_feedback__created_by__in=users)[:20]
                for user in users:
                    for movie in movies:
                        UserFeedbackFactory(created_by=user, movie=movie)

                print('populating database complete')

        except Exception as ex:
            print(ex)
            print('database constraint issue please try again')
