from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from .filters import MoviesFilter
from .serializers import UserFeedbackSerializer, MovieSerializer, MovieDetailSerializer
from .serializers import UserFeedback
from .models import Movies
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce, Round
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
import logging
from django_filters import rest_framework as filters

logger = logging.getLogger(__name__)


class MovieViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = MovieSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MoviesFilter
    queryset = Movies.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        logger.info("list movies API called by '%s'", request.user)
        try:
            queryset = self.get_queryset().values(
                'id', 'name', 'year'
            ).annotate(
                count=Count('movies_feedback'),
                avg_rating=Coalesce(Avg('movies_feedback__rating'), 0)
            ).order_by('-avg_rating')
            serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception as ex:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            return Response(
                {"message": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        logger.info("movie details API called by '%s'", request.user)
        try:
            pk = kwargs.get('pk')
            queryset = self.get_queryset().filter(
                id=pk
            ).prefetch_related(
                'movies_feedback',
                'movies_feedback__created_by'
            ).annotate(
                avg_rating=(Avg('movies_feedback__rating')),
                count=Count('movies_feedback__rating')
            )
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Movies.DoesNotExist:
            return Response(
                {"message": 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            return Response(
                {"message": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        logger.info("create movie API called by '%s'", request.user)
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.validated_data['created_by'] = request.user
            instance = serializer.save()
            return Response(
                self.get_serializer(instance=instance).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as ex:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            return Response(
                {"message": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserFeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserFeedbackSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = UserFeedback.objects.all()

    def create(self, request, *args, **kwargs):
        logger.info("create feedback API called by '%s'", request.user)
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.validated_data['created_by'] = request.user
            instance = serializer.save()
            return Response(
                self.get_serializer(instance=instance).data,
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {"message": _('Feedback already submitted for this movie')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as ex:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            return Response(
                {"message": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
