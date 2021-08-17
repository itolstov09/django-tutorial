import datetime

from django.test import TestCase
from django.utils import timezone

from . models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """возвращает False для тех вопросов, которые имеют дату публикации в будущем"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Возвращает False для вопросов, которые опубликованы позднее суток"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ Возвращет True если вопрос опубликован в течение суток"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
