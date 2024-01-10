from django.contrib import admin
from django import forms
from .models import Developer, ProgrammingLanguage, Framework, ToolSystem, DatabaseKnowledge, JobPosting, JobRecommendations, User, Employer

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DeveloperForm, self).__init__(*args, **kwargs)
        # Filtrar los usuarios que son developers
        self.fields['user'].queryset = User.objects.filter(user_type='developer')

class DeveloperAdmin(admin.ModelAdmin):
    form = DeveloperForm

admin.site.register(Developer, DeveloperAdmin)
admin.site.register(ProgrammingLanguage)
admin.site.register(Framework)
admin.site.register(ToolSystem)
admin.site.register(DatabaseKnowledge)
admin.site.register(JobPosting)
admin.site.register(JobRecommendations)
admin.site.register(User)
admin.site.register(Employer)
