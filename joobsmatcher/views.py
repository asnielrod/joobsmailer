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
        return redirect('home.html')
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



def my_offers(request):
    context = {}
    if request.user.is_authenticated:
        try:
            employer = request.user.employer
            offers = JobPosting.objects.filter(employer=employer)
            context['offers'] = offers
        except Employer.DoesNotExist:
            context['offers'] = None
    return render(request, 'my_offers.html', context)





