from django.contrib import admin
from django.db.models import Q

from core.users.models import User
from .models import CoachCoacheesRelation, CoacheesCoach, Meeting, Task, Skill, Document


class CoacheesCoachAdmin(admin.TabularInline):
    model = CoacheesCoach

    def get_extra(self, request, obj=None, **kwargs):
        return obj is None and 1 or 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        all_coachees = CoacheesCoach.objects.all()
        if obj is not None:
            all_coachees = all_coachees.exclude(
                coachee_id__in=list(obj.coachees.values_list('id', flat=True))
            )

        formset.form.base_fields['coachee'].queryset = User.objects.filter(
            Q(groups__name='Participante')
            & ~Q(
                pk__in=list(all_coachees.values_list('coachee_id', flat=True))
            )
        )

        return formset

class CoachCoacheesRelationAdmin(admin.ModelAdmin):

    inlines = (CoacheesCoachAdmin,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        all_coachcoachees = CoachCoacheesRelation.objects.all()
        if obj is not None:
            all_coachcoachees = all_coachcoachees.exclude(coach_id=obj.coach_id)

        form.base_fields['coach'].queryset = User.objects.filter(
            Q(groups__name='Mentor')
            & ~Q(
                pk__in=list(all_coachcoachees.values_list('coach_id', flat=True))
            )
        )

        return form



class TaskAdmin(admin.StackedInline):
    model = Task
    extra = 0

class MeetingAdmin(admin.ModelAdmin):
    inlines = (TaskAdmin,)

    def has_change_permission(self, request, obj=None):
        has_change_permission = super().has_change_permission(request, obj)

        if (
            has_change_permission
            and obj is not None
            and obj.coach_coachee.coach_coachees.coach_id != request.user.id
        ):
            has_change_permission = False

        return has_change_permission

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(
            Q(coach_coachee__coachee_id=request.user.id)
            | Q(coach_coachee__coach_coachees__coach_id=request.user.id)
        )
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if 'coach_coachee' in form.base_fields:
            form.base_fields['coach_coachee'].queryset = CoacheesCoach.objects.filter(
                Q(coach_coachees__coach_id=request.user.id)
            )

        return form


admin.site.register(CoachCoacheesRelation, CoachCoacheesRelationAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Skill)
admin.site.register(Document)
