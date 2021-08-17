import datetime

from django.test import TestCase
from django.utils import timezone

from . models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() возвращает False для тех вопросов, которые имеют дату публикации в будущем"""
        time_ = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time_)
        self.assertIs(future_question.was_published_recently(), False)


