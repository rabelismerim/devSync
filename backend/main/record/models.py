from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from core.users.models import User


# Classes e métodos para a feature de "Relacionamento entre 1 coach e muitos coachees"
def coach_user_validator(user_id):
    if not Group.objects.filter(name='Mentor', user__pk=user_id).exists():
        raise ValidationError(
            'The user (id=%(value)s) is not a coach.',
            params={'value': user_id}
        )

def coachee_user_validator(user_id):
    if not Group.objects.filter(name='Participante', user__pk=user_id).exists():
        raise ValidationError(
            'The user (id=%(value)s) is not a coachee.',
            params={'value': user_id}
        )


class CoachCoacheesRelation(models.Model):
    coach = models.ForeignKey(User, unique=True, validators=[coach_user_validator,], on_delete=models.CASCADE, related_name='coachcoachees_coach', verbose_name='Mentor')
    coachees = models.ManyToManyField(User, through='CoacheesCoach')

    class Meta:
        verbose_name = 'Relação Mentor-Participantes'
        verbose_name_plural = 'Relações Mentor-Participantes'

    def __str__(self):
        return self.coach.username


class CoacheesCoach(models.Model):
    coachee = models.ForeignKey(User, unique=True, validators=[coachee_user_validator,], on_delete=models.CASCADE, verbose_name='Participante', related_name='coachcoachees_coachee')
    coach_coachees = models.ForeignKey(CoachCoacheesRelation, on_delete=models.CASCADE, related_name='coachcoachees')

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'

    def __str__(self):
        return f'{self.coach_coachees.coach.username} | {self.coachee.username}'
# /Classes e métodos para a feature de "Relacionamento entre 1 coach e muitos coachees"


class Meeting(models.Model):
    coach_coachee = models.ForeignKey(CoacheesCoach, on_delete=models.CASCADE, related_name='meetings', verbose_name='Mentor | Participante')
    note = models.TextField(blank=True, verbose_name='Comentário')
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)

    class Meta:
        verbose_name='Reunião'
        verbose_name_plural='Reuniões'
        ordering = ['-date_update', '-id']

    def __str__(self):
        return f'{self.coach_coachee.coach_coachees.coach.username} | {self.coach_coachee.coachee.username} ({self.date_update})'


class Skill(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nome')
    level = models.CharField(
        max_length=2,
        verbose_name='Tipo',
        choices=(
            ('L','liderança'), ('P', 'profissional')
        )
    )

    class Meta:
        verbose_name='Competência'
        verbose_name_plural='Competências'

    def __str__(self):
        return f'{self.name} ({self.level})'


class Task(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='tasks', verbose_name='Reunião')
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING, related_name='task', verbose_name='Competência')
    description = models.TextField(verbose_name='Descrição')
    status = models.CharField(
        max_length=1,
        default='N',
        verbose_name='Status',
        choices=(('N', 'em andamento'), ('P', 'em atraso'), ('C', 'concluído'))
    )

    date_task_create = models.DateField(auto_now_add=True)
    date_task_update = models.DateField(auto_now=True)

    date_started = models.DateField(null=True, blank=True, verbose_name='Data de início')
    date_concluded = models.DateField(null=True, blank=True, verbose_name='Data de conclusão')
    note = models.TextField(blank=True, verbose_name='Comentário')

    class Meta:
        verbose_name='Tarefa'
        verbose_name_plural='Tarefas'
        ordering = ['-date_task_update', '-id']

    def __str__(self):
        return f'Tarefa - {self.meeting} ({self.date_task_update})'


class Document(models.Model):
    name = models.CharField(max_length=10, verbose_name='Nome')
    file = models.FileField(verbose_name='Arquivo')

    class Meta:
        verbose_name='Documento'
        verbose_name_plural='Documentos'

    def __str__(self):
        return self.name
