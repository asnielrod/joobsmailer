from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import JobRecommendations, Developer, JobPosting
from django.contrib.auth import get_user_model

User = get_user_model()

# views.py
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardamos todavía en la base de datos
            user_type = form.cleaned_data.get('user_type')

            # Establece el tipo de usuario
            user.user_type = user_type
            user.save()  # Ahora guardamos el usuario con el tipo establecido

            # Iniciar sesión y redirigir
            login(request, user)
            messages.success(request, 'You have been registered!')

            # Redirigir a una página para completar el perfil según el tipo de usuario
            if user_type == 'developer':
                return redirect('complete_developer_profile')
            # Redirigin para completar tipo employer
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


#completar el prtfil de desarrollador
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProgrammingLanguage, Framework, ToolSystem, DatabaseKnowledge, Developer

def complete_developer_profile(request):
    if request.method == 'POST':
        developer = request.user.developer
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

        # Actualizar campos ManyToMany
        programming_languages = request.POST.getlist('programming_languages')
        frameworks = request.POST.getlist('frameworks')
        tools_systems = request.POST.getlist('tools_systems')
        database_knowledge = request.POST.getlist('database_knowledge')

        developer.programming_languages.set(programming_languages)
        developer.frameworks.set(frameworks)
        developer.tools_systems.set(tools_systems)
        developer.database_knowledge.set(database_knowledge)

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
        employer = request.user.employer
        employer.name = request.POST['name']
        employer.email = request.POST['email']
        employer.location = request.POST['location']
        employer.linkedin_url = request.POST['linkedin_url']
        employer.company_name = request.POST['company_name']
        employer.industry = request.POST['industry']
        employer.company_size = request.POST['company_size']
        employer.company_description = request.POST['company_description']
        employer.save()
        messages.success(request, "Your Profile Has Been Updated!")
        return redirect('home')
    return render(request, 'complete_employer_profile.html', {})

