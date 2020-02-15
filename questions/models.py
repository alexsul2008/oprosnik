from django.contrib.auth.models import Group, User
from django.db import models
from django.shortcuts import reverse


class UsersAnswers(models.Model):
    """Ответы пользователей"""
    user = models.CharField(max_length=20, verbose_name="Пользователь")
    group_user = models.CharField(max_length=50, verbose_name="Группа пользователя")
    session_key = models.CharField(max_length=150, verbose_name="Сессия пользователя")
    not_ok_vop = models.IntegerField(verbose_name="Не правильный вопрос", null=True, default=0)
    not_ok_otv = models.IntegerField(verbose_name="Не правильный ответ", null=True, default=0)
    ok_vop = models.IntegerField(verbose_name="Правильный вопрос", null=True, default=0)
    ok_otv = models.IntegerField(verbose_name="Правильный ответ", null=True, default=0)

    def __str__(self):
        return self.user



class Questions(models.Model):
    """Вопросы"""
    description = models.TextField("Вопрос")
    in_active = models.BooleanField("Активность вопроса", default=True)
    groups = models.ForeignKey(
        Group, verbose_name="группа отдела", on_delete=models.SET_NULL, null=True
    )
    image = models.ImageField("Изображение", upload_to="guestions/", blank=True)
    doc_url = models.CharField("Ссылка на документ", max_length=250, blank=True)

    def get_absolute_url(self):
        return reverse('question_detail_url', kwargs={'pk': self.pk})

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        #return "%s, %s" % (self.id, self.description)
        return '{}'.format(self.description)


    class Meta:
        """Сортировка по полю ID
        ordering: List['id']
        """
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answers(models.Model):
    """Ответы на вопросы"""
    description = models.TextField("Текст ответа")
    vop_id = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name='answer'
    )
    approved = models.BooleanField("Правильность ответа", default=False)

    def __str__(self):
        #return "%s, %s" % (self.vop_id, self.description)
        return "%s, %s" % (self.description, self.approved)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UsersAnswer(models.Model):
    """Ответы пользователей"""
    user = models.CharField(max_length=20, verbose_name="Пользователь")
    group_user = models.CharField(max_length=50, verbose_name="Группа пользователя")
    session_key = models.CharField(max_length=150, verbose_name="Сессия пользователя")
    correct = models.BooleanField(verbose_name="Правильность ответа", default=False)
    vop = models.IntegerField(verbose_name="Вопрос в ответе", null=True, default=0)
    otv = models.IntegerField(verbose_name="Ответ", null=True, default=0)

    def __str__(self):
        return "%s, %s, %s" % (self.correct, self.vop, self.otv)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"


class WorkPermitUsers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # flag = models.BooleanField(verbose_name="Разрешение на опрос", default=False)
    session_key = models.CharField(max_length=150, verbose_name="Сессия пользователя")
    date_passage = models.DateField(verbose_name="Дата прохождения опроса", auto_now_add=True)