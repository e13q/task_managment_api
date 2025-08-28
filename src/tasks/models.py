from django.conf import settings
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание (HTML)')
    deadline = models.DateTimeField(verbose_name='Срок')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        verbose_name='Приоритет'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @property
    def is_completed(self):
        return not self.assignees.filter(task_resolved=False).exists()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f"{self.title} - {self.is_completed}"


class TaskAssignee(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="assignees",
        on_delete=models.CASCADE,
        verbose_name='Задача'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    task_resolved = models.BooleanField(
        default=False,
        verbose_name='Выполнение задачи'
    )

    class Meta:
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'
        unique_together = ['task', 'user']

    def __str__(self):
        return f"{self.task.title} - {self.user} - {self.task_resolved}"
