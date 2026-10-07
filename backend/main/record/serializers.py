from rest_framework import serializers

from core.users.models import User
from .models import CoachCoacheesRelation, CoacheesCoach, Meeting, Task


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'area', 'service', 'name')

    def get_name(self, obj):
        return (obj.first_name and obj.last_name) and f'{obj.first_name} {obj.last_name}' or obj.username

    def get_role(self, obj):
        return obj.get_role_display()


class UserFullSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    coachees = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'area', 'service', 'name', 'picture', 'coach', 'coachees')

    def get_name(self, obj):
        return (obj.first_name and obj.last_name) and f'{obj.first_name} {obj.last_name}' or obj.username

    def get_role(self, obj):
        return obj.get_role_display()

    def get_picture(self, obj):
        result = None
        if 'request' in self.context:
            req = self.context['request']
            if hasattr(req, '_request'):
                req = req._request

            if (
                hasattr(req, 'identity_context_data')
                and hasattr(req.identity_context_data, 'userpicture')
            ):
                result = req.identity_context_data.userpicture

        return result


    def get_coach(self, obj):
        result = None

        coachcoachees = obj.coachcoachees_coachee.first()
        if coachcoachees:
            last_meeting_info = coachcoachees.meetings.order_by('-date_update', '-id').values('date_update', 'note').first()
            result = {
                'coachcoachee_id': coachcoachees.id,
                **UserSerializer(instance=coachcoachees.coach_coachees.coach).data,
                **(last_meeting_info and last_meeting_info or {})
            }

        return result

    def get_coachees(self, obj):
        result = None

        coachcoachees = obj.coachcoachees_coach.first()
        if coachcoachees:
            result = []
            for cc in coachcoachees.coachees.through.objects.filter(coach_coachees__coach_id=obj.id):
                if cc.coachee.id != obj.id:
                    last_meeting_info = cc.meetings.order_by('-date_update', '-id').values('date_update', 'note').first()
                    result.append(
                        {
                            'coachcoachee_id': cc.id,
                            **UserSerializer(instance=cc.coachee).data,
                            **(last_meeting_info and last_meeting_info or {})
                        }
                    )

        return result

    def to_representation(self, instance):
        user_full_data = super().to_representation(instance)
        user_full_data.update(
            {
                'is_coachee': user_full_data['coach'] is not None,
                'is_coach': user_full_data['coachees'] is not None and len(user_full_data['coachees']) > 0,
            }
        )
        return user_full_data


class CoachCoacheesRelationSerializer(serializers.ModelSerializer):

    coach = UserSerializer()

    class Meta:
        model = CoachCoacheesRelation
        fields = ('id', 'coach')


class CoacheesCoachSerializer(serializers.ModelSerializer):

    # coach_rel = CoachCoacheesRelationSerializer(source='coach_coachees')
    # coachee = UserSerializer()

    rel_id = serializers.IntegerField(source='id', required=False)

    coach = serializers.SerializerMethodField()
    coachee = serializers.SerializerMethodField()

    class Meta:
        model = CoacheesCoach
        fields = ('rel_id', 'coach', 'coachee')

    def get_coach(self, obj):
        # se o usuário atual não for o coachee,
        # ele só pode ser o coach
        return CoachCoacheesRelationSerializer(instance=obj.coach_coachees).data['coach']

    def get_coachee(self, obj):
        # se o usuário atual não for o coachee,
        # ele só pode ser o coach
        return UserSerializer(instance=obj.coachee).data


class TaskSerializer(serializers.ModelSerializer):

    task_id = serializers.IntegerField(source='id', required=False)
    skill_id = serializers.IntegerField(source='skill.id', required=False)

    class Meta:
        model = Task
        exclude = ('id', 'skill', 'meeting', 'date_task_create', 'date_task_update',)


class MeetingSerializer(serializers.ModelSerializer):

    coachcoachee = CoacheesCoachSerializer(source='coach_coachee')
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Meeting
        exclude = ('coach_coachee',)

    def create(self, validated_data):
        coachcoachee_id = validated_data.pop('coach_coachee')['id']
        tasks = validated_data.pop('tasks')

        validated_data['coach_coachee_id'] = coachcoachee_id
        instance = super().create(validated_data)

        Task.objects.bulk_create(
            [
                Task(
                    **{
                        'meeting_id': instance.id,
                        'skill_id': t.pop('skill')['id'],
                        **t
                    }
                )
                for t in tasks
            ]
        )

        return instance


    def update(self, instance, validated_data):

        validated_data.pop('coach_coachee', None)
        tasks = validated_data.pop('tasks')

        instance = super().update(instance, validated_data)

        all_tasks = Task.objects.filter(meeting_id=instance.id)

        tasks_for_create = []
        for t in tasks:
            task_id = t.pop('id', None)
            if task_id is not None: # existente
                skill_id = t.pop('skill')['id']
                all_tasks.filter(id=task_id).update(skill_id=skill_id, **t)
            else:
                tasks_for_create.append(t)

        Task.objects.bulk_create(
            [
                Task(
                    **{
                        'meeting_id': instance.id,
                        'skill_id': t.pop('skill')['id'],
                        **t
                    }
                )
                for t in tasks_for_create
            ]
        )

        return instance
