from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .user_types import USER_TYPES


class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='developer') 


    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    def __str__(self):
        return f"{self.username} ({self.user_type})"


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Framework(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ToolSystem(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class DatabaseKnowledge(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='developer')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True, null=True)

    programming_languages = models.ManyToManyField(ProgrammingLanguage)
    frameworks = models.ManyToManyField(Framework)
    tools_systems = models.ManyToManyField(ToolSystem)
    database_knowledge = models.ManyToManyField(DatabaseKnowledge)

    years_of_experience = models.PositiveIntegerField(blank=True, null=True, default=0)
    project_types = models.TextField()  
    previous_roles = models.TextField()  

    highest_degree = models.CharField(max_length=100, blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    job_type = models.CharField(max_length=100)
    remote_availability = models.BooleanField(default=False)
    relocation_interest = models.BooleanField(default=False)
    desired_salary_range = models.CharField(max_length=100)

    languages_spoken = models.CharField(max_length=100)
    soft_skills = models.TextField()
    professional_interests = models.TextField(blank=True, null=True)

    availability_date = models.DateField(null=True, blank=True)
    additional_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Nombre: {self.name} Email: ({self.email}) Tipo de trabajo: {self.job_type}'

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True, null=True)

    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=100)
    company_description = models.TextField()

    def __str__(self):
        return self.name
class JobPosting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    employment_type = models.CharField(max_length=100)

    required_languages = models.ManyToManyField(ProgrammingLanguage)
    required_frameworks = models.ManyToManyField(Framework)
    required_tools_systems = models.ManyToManyField(ToolSystem)
    required_database_knowledge = models.ManyToManyField(DatabaseKnowledge)

    required_experience = models.PositiveIntegerField()
    project_type_experience = models.TextField()  
    required_education_level = models.CharField(max_length=100)

    soft_skills_required = models.TextField()
    languages_required = models.CharField(max_length=100, blank=True, null=True)
    additional_skills = models.TextField(blank=True, null=True)

    salary_range = models.CharField(max_length=100)
    benefits = models.TextField()
    professional_growth_opportunities = models.TextField()

    interview_process = models.TextField()
    application_deadline = models.DateField()
    contact_email = models.EmailField()

    def __str__(self):
        return self.job_title

class JobRecommendations(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.job.job_title} - {self.developer.name} - {self.score}"
    

