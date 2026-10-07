"""Seed fictional data and create a temporary session for documentation capture."""
import json
import os
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client
from main.record.models import CoachCoacheesRelation, CoacheesCoach, Meeting, Skill, Task
User = get_user_model()
coach, _ = User.objects.get_or_create(username='demo-coach', defaults={'first_name': 'Mentor', 'last_name': 'Exemplo', 'email': 'mentor@example.com', 'role': 'GES', 'area': 'Engenharia', 'service': 'Desenvolvimento'})
coachee, _ = User.objects.get_or_create(username='demo-coachee', defaults={'first_name': 'Participante', 'last_name': 'Exemplo', 'email': 'participante@example.com', 'role': 'DEV', 'area': 'Engenharia', 'service': 'Desenvolvimento'})
for user, first_name, email, role in [(coach, 'Mentor', 'mentor@example.com', 'GES'), (coachee, 'Participante', 'participante@example.com', 'DEV')]:
    user.first_name, user.last_name, user.email, user.role = first_name, 'Exemplo', email, role
    user.set_unusable_password()
    user.save()
for user, name in [(coach, 'Mentor'), (coachee, 'Participante')]:
    group, _ = Group.objects.get_or_create(name=name)
    user.groups.add(group)
relation, _ = CoachCoacheesRelation.objects.get_or_create(coach=coach)
link, _ = CoacheesCoach.objects.get_or_create(coachee=coachee, defaults={'coach_coachees': relation})
meeting, _ = Meeting.objects.get_or_create(coach_coachee=link, defaults={'note': 'Alinhamos os objetivos do próximo ciclo: melhorar a qualidade das entregas e compartilhar aprendizados com a equipe.'})
skill, _ = Skill.objects.get_or_create(name='Comunicação', level='P')
Task.objects.get_or_create(meeting=meeting, skill=skill, defaults={'description': 'Apresentar aprendizados do projeto', 'status': 'N', 'date_started': '2026-10-01', 'date_concluded': '2026-10-30', 'note': 'Preparar uma apresentação para a equipe.'})
client = Client()
client.force_login(coach)
(root / 'docs/.capture-session.json').write_text(json.dumps({'session': client.cookies['sessionid'].value, 'relation': link.id}))
print('Fictional screenshot data and temporary session prepared.')
