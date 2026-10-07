from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import CoachCoacheesRelation, CoacheesCoach, Meeting


@override_settings(ALLOWED_HOSTS=['testserver'])
class DevSyncAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.coach = User.objects.create_user('coach', password='test-password', role='GES')
        cls.coachee = User.objects.create_user('coachee', password='test-password', role='DEV')
        cls.outsider = User.objects.create_user('outsider', password='test-password', role='DEV')
        relation = CoachCoacheesRelation.objects.create(coach=cls.coach)
        cls.link = CoacheesCoach.objects.create(coachee=cls.coachee, coach_coachees=relation)
        cls.meeting = Meeting.objects.create(coach_coachee=cls.link, note='Original')

    def setUp(self):
        self.api = APIClient()

    def test_first_users_are_not_automatically_superusers(self):
        self.assertFalse(self.coach.is_superuser)
        self.assertFalse(self.coachee.is_superuser)
        self.assertFalse(self.outsider.is_superuser)

    def test_superuser_can_be_created_explicitly(self):
        user = get_user_model().objects.create_superuser('admin', password='test-password')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_outsider_cannot_read_or_update_meeting(self):
        self.api.force_authenticate(self.outsider)
        url = f'/devsync/api/meetings/{self.meeting.id}/'
        self.assertEqual(self.api.get(url).status_code, 404)
        self.assertEqual(self.api.patch(url, {'note': 'Changed'}, format='json').status_code, 404)
        response = self.api.get('/devsync/api/meetings/', {'coachcoachee_id': self.link.id})
        self.assertEqual(response.data['data'], [])

    def test_coachee_can_read_but_cannot_delete(self):
        self.api.force_authenticate(self.coachee)
        url = f'/devsync/api/meetings/{self.meeting.id}/'
        self.assertEqual(self.api.get(url).status_code, 200)
        self.assertEqual(self.api.delete(url).status_code, 404)

    def test_only_responsible_coach_can_create(self):
        payload = {'coachcoachee': {'rel_id': self.link.id}, 'tasks': [], 'note': 'New'}
        self.api.force_authenticate(self.outsider)
        self.assertEqual(self.api.post('/devsync/api/meetings/', payload, format='json').status_code, 403)
        self.api.force_authenticate(self.coach)
        self.assertEqual(self.api.post('/devsync/api/meetings/', payload, format='json').status_code, 201)

    def test_invalid_relation_filter_returns_400(self):
        self.api.force_authenticate(self.coach)
        self.assertEqual(self.api.get('/devsync/api/meetings/?coachcoachee_id=abc').status_code, 400)

    def test_public_home_and_local_login(self):
        response = self.client.get('/devsync/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>DevSync</title>')
        self.assertEqual(self.client.get('/devsync/login/').status_code, 200)

    def test_local_login_preserves_password(self):
        self.assertTrue(self.client.login(username='coach', password='test-password'))
        self.coach.refresh_from_db()
        self.assertTrue(self.coach.check_password('test-password'))

    def test_admin_renders(self):
        admin = get_user_model().objects.create_superuser('admin-ui', password='test-password')
        self.client.force_login(admin)
        self.assertEqual(self.client.get('/devsync/admin/').status_code, 200)
