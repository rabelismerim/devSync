from django.db.models import Q

from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Meeting, Skill, Task
from .serializers import UserFullSerializer, MeetingSerializer


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserFullSerializer

    def get_object(self):
        return self.request.user


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MeetingSerializer

    queryset = Meeting.objects.all()

    def get_queryset(self):
        coachcoachee_id = self.request.query_params.get('coachcoachee_id', None)
        queryset = super().get_queryset().filter(
            Q(coach_coachee__coachee=self.request.user)
            | Q(coach_coachee__coach_coachees__coach=self.request.user)
        )
        if self.action in ('partial_update', 'update', 'destroy'):
            queryset = queryset.filter(coach_coachee__coach_coachees__coach=self.request.user)
        if coachcoachee_id is not None:
            try:
                queryset = queryset.filter(coach_coachee_id=int(coachcoachee_id))
            except ValueError:
                raise ValidationError({'coachcoachee_id': 'Informe um identificador válido.'})
        elif self.action == 'list':
            queryset = queryset.filter(coach_coachee__coachee=self.request.user)
        return queryset

    def perform_create(self, serializer):
        from .models import CoacheesCoach
        relation_id = serializer.validated_data.get('coach_coachee', {}).get('id')
        if not CoacheesCoach.objects.filter(id=relation_id, coach_coachees__coach=self.request.user).exists():
            raise PermissionDenied('Somente o mentor responsável pode criar reuniões.')
        serializer.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        all_skills = Skill.objects.all()

        response.data = {
            'metadata': {
                'task_skills_metadata': [
                    {
                        'value': id,
                        'display_name': name.capitalize(),
                        'children': [
                            {
                                'value': s.id,
                                'display_name': s.name.capitalize()
                            }
                            for s in all_skills.filter(level=id)
                        ],
                    }
                    for id, name in Skill.level.field.choices
                ],
                'task_status_metadata': [
                    {
                        'value': id,
                        'display_name': name.capitalize()
                    }
                    for id, name in Task.status.field.choices
                ]
            },
            'data': response.data
        }

        return response
