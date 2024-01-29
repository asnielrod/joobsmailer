from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import JobRecommendations, Developer, JobPosting
from django.contrib.auth import get_user_model
from .models import ProgrammingLanguage, Framework, ToolSystem, DatabaseKnowledge, Developer, Employer

User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')

            user.user_type = user_type
            user.save()
            if user_type == 'developer':
                Developer.objects.create(user=user, email=user.email)
            else:
                Employer.objects.create(user=user, email=user.email)
            login(request, user)
            messages.success(request, 'You have been registered!')

            if user_type == 'developer':
                return redirect('complete_developer_profile')
            elif user_type == 'employer':
                return redirect('complete_employer_profile')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('login')

def home(request):
    context = {}
    if request.user.is_authenticated:
        try:
            developer = request.user.developer
            recommendations = JobRecommendations.objects.filter(developer=developer)
            context['recommendations'] = recommendations
        except Developer.DoesNotExist:
            context['recommendations'] = None
    return render(request, 'home.html', context)




def complete_developer_profile(request):
    if request.method == 'POST':
        user = request.user
        developer = Developer.objects.get(user=user)
        developer.email = request.POST['email']
        developer.location = request.POST['location']
        developer.linkedin_url = request.POST['linkedin_url']
        developer.years_of_experience = request.POST['years_of_experience']
        developer.project_types = request.POST['project_types']
        developer.previous_roles = request.POST['previous_roles']
        developer.highest_degree = request.POST['highest_degree']
        developer.certifications = request.POST['certifications']
        developer.job_type = request.POST['job_type']
        developer.remote_availability = request.POST.get('remote_availability') == 'on'
        developer.relocation_interest = request.POST.get('relocation_interest') == 'on'
        developer.desired_salary_range = request.POST['desired_salary_range']
        developer.languages_spoken = request.POST['languages_spoken']
        developer.soft_skills = request.POST['soft_skills']
        developer.professional_interests = request.POST['professional_interests']
        developer.availability_date = request.POST['availability_date']
        developer.additional_comments = request.POST['additional_comments']

        programming_languages = request.POST.getlist('programming_languages')
        frameworks = request.POST.getlist('frameworks')
        tools_systems = request.POST.getlist('tools_systems')
        database_knowledge = request.POST.getlist('database_knowledge')

        developer.programming_languages.set(ProgrammingLanguage.objects.filter(id__in=programming_languages))
        developer.frameworks.set(Framework.objects.filter(id__in=frameworks))
        developer.tools_systems.set(ToolSystem.objects.filter(id__in=tools_systems))
        developer.database_knowledge.set(DatabaseKnowledge.objects.filter(id__in=database_knowledge))

        developer.save()
        messages.success(request, "Your Profile Has Been Updated!")
        return redirect('home')
    else:
        context = {
            'programming_languages': ProgrammingLanguage.objects.all(),
            'frameworks': Framework.objects.all(),
            'tools_systems': ToolSystem.objects.all(),
            'database_knowledge': DatabaseKnowledge.objects.all(),
            'username': request.user.username,
        }
        return render(request, 'complete_developer_profile.html', context)

    return render(request, 'complete_developer_profile.html', {})

  
    
def complete_employer_profile(request):
    if request.method == 'POST':
        user = request.user
        employer, created = Employer.objects.get_or_create(user=user)
        employer.name = request.POST.get('name')
        employer.email = request.POST.get('email')
        employer.location = request.POST.get('location')
        employer.linkedin_url = request.POST.get('linkedin_url', '')
        employer.company_name = request.POST.get('company_name')
        employer.industry = request.POST.get('industry')
        employer.company_size = request.POST.get('company_size')
        employer.company_description = request.POST.get('company_description')

        try:
            employer.save()
            messages.success(request, "Your Profile Has Been Updated!")
            return redirect('my_offers')
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")

   
    return render(request, 'complete_employer_profile.html', {})



def some_error_handling_view(request):
    return render(request, 'home.html', {})


#esta funcion me devuelve los trabajos que he publicado
def my_offers(request):
    context = {}
    if request.user.is_authenticated:
        try:
            employer = request.user.employer
            job_postings = JobPosting.objects.filter(employer=employer)
            context['job_postings'] = job_postings
        except Employer.DoesNotExist:
            context['job_postings'] = None

    return render(request, 'my_offers.html', context)



#revisar esta funcion
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employer, JobPosting  # Asegúrate de importar JobPosting
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employer, JobPosting, ProgrammingLanguage, Framework, ToolSystem, DatabaseKnowledge
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employer, JobPosting, ProgrammingLanguage, Framework, ToolSystem, DatabaseKnowledge
from datetime import datetime

def jobposting(request):
    if request.method == 'POST':
        user = request.user
        employer, created = Employer.objects.get_or_create(user=user)

        # Actualiza la información del empleador
        employer.name = request.POST.get('name')
        employer.email = request.POST.get('email')
        employer.location = request.POST.get('location')
        employer.linkedin_url = request.POST.get('linkedin_url', '')
        employer.company_name = request.POST.get('company_name')
        employer.industry = request.POST.get('industry')
        employer.company_size = request.POST.get('company_size')
        employer.company_description = request.POST.get('company_description')

        # Crear o actualizar el JobPosting
        job_posting, created = JobPosting.objects.get_or_create(employer=employer)

        # Actualizar los atributos de JobPosting
        job_posting.company_name = request.POST.get('company_name')
        job_posting.industry = request.POST.get('industry')
        job_posting.location = request.POST.get('location')
        job_posting.job_title = request.POST.get('job_title')
        job_posting.job_description = request.POST.get('job_description')
        job_posting.employment_type = request.POST.get('employment_type')

        # Manejo de campos Many-to-Many para required_languages
        languages_data = request.POST.getlist('required_languages')
        job_posting.required_languages.clear()
        for lang_id in languages_data:
            language = ProgrammingLanguage.objects.get(id=lang_id)
            job_posting.required_languages.add(language)

        # Manejo de campos Many-to-Many para required_frameworks
        frameworks_data = request.POST.getlist('required_frameworks')
        job_posting.required_frameworks.clear()
        for framework_id in frameworks_data:
            framework = Framework.objects.get(id=framework_id)
            job_posting.required_frameworks.add(framework)

        # Manejo de campos Many-to-Many para required_tools_systems
        tools_systems_data = request.POST.getlist('required_tools_systems')
        job_posting.required_tools_systems.clear()
        for tool_system_id in tools_systems_data:
            tool_system = ToolSystem.objects.get(id=tool_system_id)
            job_posting.required_tools_systems.add(tool_system)

        # Manejo de campos Many-to-Many para required_database_knowledge
        database_knowledge_data = request.POST.getlist('required_database_knowledge')
        job_posting.required_database_knowledge.clear()
        for db_knowledge_id in database_knowledge_data:
            database_knowledge = DatabaseKnowledge.objects.get(id=db_knowledge_id)
            job_posting.required_database_knowledge.add(database_knowledge)

        # Actualizar otros campos
        job_posting.required_experience = request.POST.get('required_experience')
        job_posting.project_type_experience = request.POST.get('project_type_experience')
        job_posting.required_education_level = request.POST.get('required_education_level')
        job_posting.soft_skills_required = request.POST.get('soft_skills_required')
        job_posting.languages_required = request.POST.get('languages_required', '')
        job_posting.additional_skills = request.POST.get('additional_skills', '')

        job_posting.salary_range = request.POST.get('salary_range')
        job_posting.benefits = request.POST.get('benefits')
        job_posting.professional_growth_opportunities = request.POST.get('professional_growth_opportunities')
        job_posting.interview_process = request.POST.get('interview_process')
        job_posting.contact_email = request.POST.get('contact_email')

        # Convertir la fecha de texto a objeto datetime y guardarla
        application_deadline_str = request.POST.get('application_deadline')
        if application_deadline_str:
            job_posting.application_deadline = datetime.strptime(application_deadline_str, '%Y-%m-%d')

        try:
            employer.save()
            job_posting.save()
            messages.success(request, "Your Job Posting Has Been Created/Updated!")
            return redirect('some_view')  # Cambia 'some_view' al nombre de tu vista deseada
        except Exception as e:
            messages.error(request, f"Error creating/updating job posting: {e}")

    return render(request, 'jobposting.html', {})

