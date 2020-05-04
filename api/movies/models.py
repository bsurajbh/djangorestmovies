from django.db import models
from django.core import validators
from common.base import BaseModel
from common.constants import MIN_YEAR, MAX_RATING, MIN_RATING
from datetime import datetime


class Movies(BaseModel):
    name = models.CharField(max_length=255, blank=False)
    year = models.IntegerField(
        validators=[
            validators.MinValueValidator(MIN_YEAR),
            validators.MaxValueValidator(datetime.now().year)
        ],
        blank=False
    )

    class Meta:
        verbose_name_plural = 'Movies'
        constraints = [
            models.UniqueConstraint(fields=['name', 'year'], name='unique_movie')
        ]

    def __str__(self):
        return self.name


class UserFeedback(BaseModel):
    RATING_CHOICE = ((x*0.5, x * 0.5) for x in range(MIN_RATING, (MAX_RATING * 2) + 1))
    movie = models.ForeignKey(Movies, related_name='movies_feedback', on_delete=models.CASCADE)
    rating = models.FloatField(choices=RATING_CHOICE, blank=False)
    comment = models.TextField(blank=False)

    def __str__(self):
        return self.movie.name

    class Meta:
        verbose_name_plural = 'User Feedback'
        constraints = [
            models.UniqueConstraint(fields=['movie', 'created_by'], name='unique_feedback')
        ]
