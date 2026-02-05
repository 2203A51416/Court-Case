from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from courtapp.models import Profile, CaseRequest
def home(request):
    return render(request, 'home.html')
def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        role = request.POST['role']
        username = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=username,
            password=password,
            first_name=request.POST['name']
        )

        profile = Profile.objects.create(
            user=user,
            role=role,
            phone=request.POST['phone'],
            gender=request.POST['gender'],
            address=request.POST['address'],
            state_bar=request.POST.get('state_bar', ''),
            enrollment_no=request.POST.get('enrollment_no', ''),
            experience=request.POST.get('experience') or None,
            aadhaar=request.POST.get('aadhaar', '')
        )

        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'LAWYER':
        requests = CaseRequest.objects.filter(lawyer=request.user)
        return render(request, 'lawyer_dashboard.html', {'requests': requests})

    else:
        lawyers = Profile.objects.filter(role='LAWYER')
        my_cases = CaseRequest.objects.filter(client=request.user)
        return render(request, 'client_dashboard.html', {
            'lawyers': lawyers,
            'cases': my_cases
        })


def book_lawyer(request, lawyer_id):
    if request.method == 'POST':
        CaseRequest.objects.create(
            client=request.user,
            lawyer=User.objects.get(id=lawyer_id),
            case_title=request.POST['title'],
            description=request.POST['description']
        )
    return redirect('dashboard')


def accept_case(request, case_id):
    case = CaseRequest.objects.get(id=case_id)
    case.status = 'ACCEPTED'
    case.save()
    return redirect('dashboard')


def reject_case(request, case_id):
    case = CaseRequest.objects.get(id=case_id)
    case.status = 'REJECTED'
    case.save()
    return redirect('dashboard')
