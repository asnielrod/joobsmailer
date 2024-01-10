from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
from joobsmatcher.models import (
    ProgrammingLanguage,
    Framework,
    ToolSystem,
    DatabaseKnowledge,
)


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.populate_programming_languages()
            self.populate_frameworks()
            self.populate_tool_systems()
            self.populate_database_knowledge()
            self.stdout.write(self.style.SUCCESS('Successfully populated all tables'))

    def populate_programming_languages(self):
        programming_languages = [
            "Python",
            "Java",
            "JavaScript",
            "C#",
            "Ruby",
            "C++",
            "Swift",
            "Kotlin",
            "Go",
            "TypeScript",
        ]
        for language in programming_languages:
            ProgrammingLanguage.objects.get_or_create(name=language)
        self.stdout.write(self.style.SUCCESS('Successfully populated programming languages'))

    def populate_frameworks(self):
        frameworks = [
            "Django",
            "Spring",
            "React",
            "ASP.NET",
            "Rails",
            "Vue.js",
            "Flutter",
            "Angular",
            "Laravel",
            "Express",
        ]
        for framework in frameworks:
            Framework.objects.get_or_create(name=framework)
        self.stdout.write(self.style.SUCCESS('Successfully populated frameworks'))

    def populate_tool_systems(self):
        tools_systems = [
            "Git",
            "Docker",
            "Kubernetes",
            "Jenkins",
            "AWS",
            "Azure",
            "Ansible",
            "Terraform",
            "RabbitMQ",
            "NGINX",
        ]
        for tool in tools_systems:
            ToolSystem.objects.get_or_create(name=tool)
        self.stdout.write(self.style.SUCCESS('Successfully populated tool systems'))

    def populate_database_knowledge(self):
        database_knowledges = [
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "SQLite",
            "Oracle",
            "Cassandra",
            "Redis",
            "Elasticsearch",
            "Firebase",
            "DynamoDB",
        ]
        for db in database_knowledges:
            DatabaseKnowledge.objects.get_or_create(name=db)
        self.stdout.write(self.style.SUCCESS('Successfully populated database knowledge'))

    
        

    



    
    
    
 