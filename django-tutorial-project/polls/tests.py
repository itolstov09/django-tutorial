import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from . models import Question


def create_question(question_text, days):
    """Создает вопрос используя текст вопроса и количество дней.

        Количество дней может быть положительным и отрицательным, для создания
        вопроса с 'прошлой датой' публикации"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text,
        publication_date=time
    )
        

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """Если вопросы отсутствуют, то выводится правильное сообщение"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_past_question(self):
        """Вопросы опубликованные в прошлом отображаются на странице index"""
        question = create_question(
            question_text='Past questuion',
            days=-30
        )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )
    
    def test_future_question(self):
        """Вопросы, опубликованные в 'будущем' не отображаются на странице index."""
        create_question(
            question_text='Future questuion',
            days=30
        )
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question_and_past_question(self):
        """Даже если существуют запрос из будущего, он отображаться не будет"""
        question = create_question(
            question_text='Past questuion',
            days=-30
        )
        create_question(
            question_text='Future questuion',
            days=30
        )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
            )
        
    def test_two_past_questions(self):
        """На странице index может отображаться несколько вопросов"""

        question1 = create_question(
            question_text='Past questuion 1',
            days=-30
        )
        question2 = create_question(
            question_text='Past questuion 2',
            days=-5
        )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )


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

