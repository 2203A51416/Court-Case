from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, CaseRequest, Hearing


# ================= HOME & STATIC PAGES =================

def home(request):
    return render(request, 'home.html')


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')


def search_results(request):
    return render(request, 'search-results.html')


# ================= REGISTER =================

def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')

        # User exists check
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {
                'error': 'User already exists. Please login.'
            })

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        # Profile common data
        profile_data = {
            'user': user,
            'role': role,
            'phone': request.POST.get('phone', ''),
            'gender': request.POST.get('gender', ''),
            'address': request.POST.get('address', ''),
        }

        # Lawyer extra fields
        if role == 'LAWYER':
            profile_data.update({
                'state_bar_council': request.POST.get('state_bar', ''),
                'enrollment_number': request.POST.get('enrollment_no', ''),
            })

        # Client extra
        if role == 'CLIENT':
            profile_data.update({
                'aadhaar': request.POST.get('aadhaar', ''),
            })

        Profile.objects.create(**profile_data)

        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


# ================= LOGIN =================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')   # email
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

        profile = Profile.objects.get(user=user)

        # Role mismatch
        if profile.role != role:
            return render(request, 'login.html', {
                'error': 'Role mismatch! Select correct role'
            })

        login(request, user)

        # 🔥 Correct redirect
        if profile.role == 'LAWYER':
            return redirect('lawyer_dashboard')
        else:
            return redirect('dashboard')

    return render(request, 'login.html')


# ================= CLIENT DASHBOARD =================

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    # If lawyer accidentally hits /dashboard redirect properly
    if profile.role == 'LAWYER':
        return redirect('lawyer_dashboard')

    # 🔍 Search lawyer
    query = request.GET.get('q')

    lawyers = Profile.objects.filter(role='LAWYER', is_available=True)

    if query:
        lawyers = lawyers.filter(
            user__first_name__icontains=query
        ) | lawyers.filter(
            specialization__icontains=query
        )

    # 🔥 Prefetch hearings (CLIENT HEARING VISIBILITY)
    my_cases = CaseRequest.objects.filter(
        client=profile
    ).prefetch_related('hearings')

    return render(request, 'client_dashboard.html', {
        'profile': profile,
        'lawyers': lawyers,
        'cases': my_cases,
        'query': query
    })


# ================= BOOK LAWYER =================

@login_required
def book_lawyer(request, lawyer_id):
    if request.method == 'POST':
        client_profile = Profile.objects.get(user=request.user)
        lawyer_profile = Profile.objects.get(id=lawyer_id)

        CaseRequest.objects.create(
            client=client_profile,
            lawyer=lawyer_profile,
            case_title=request.POST['title'],
            description=request.POST['description']
        )

    return redirect('dashboard')


# ================= ACCEPT / REJECT =================

@login_required
def accept_case(request, case_id):
    case = get_object_or_404(CaseRequest, id=case_id)
    case.status = 'ACCEPTED'
    case.save()
    return redirect('lawyer_dashboard')


@login_required
def reject_case(request, case_id):
    case = get_object_or_404(CaseRequest, id=case_id)
    case.status = 'REJECTED'
    case.save()
    return redirect('lawyer_dashboard')


# ================= LAWYER DASHBOARD =================

@login_required
def lawyer_dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != 'LAWYER':
        return redirect('dashboard')

    pending_cases = CaseRequest.objects.filter(
        lawyer=profile,
        status='PENDING'
    )

    accepted_cases = CaseRequest.objects.filter(
        lawyer=profile,
        status='ACCEPTED'
    )

    rejected_cases = CaseRequest.objects.filter(
        lawyer=profile,
        status='REJECTED'
    )

    # ===== STATS =====
    total_cases = CaseRequest.objects.filter(lawyer=profile).count()
    total_pending = pending_cases.count()
    total_accepted = accepted_cases.count()
    total_rejected = rejected_cases.count()

    total_hearings = sum(case.hearings.count() for case in accepted_cases)

    return render(request, 'lawyer_dashboard.html', {
        'profile': profile,
        'pending_cases': pending_cases,
        'accepted_cases': accepted_cases,

        'total_cases': total_cases,
        'total_pending': total_pending,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
        'total_hearings': total_hearings,
    })


# ================= HEARING CALENDAR =================

@login_required
def hearing_calendar(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'LAWYER':
        hearings = Hearing.objects.filter(
            case__lawyer=profile
        ).order_by('hearing_date')

    else:
        hearings = Hearing.objects.filter(
            case__client=profile
        ).order_by('hearing_date')

    return render(request, 'hearing_calendar.html', {
        'hearings': hearings,
        'profile': profile
    })


# ================= ADD HEARING =================

@login_required
def add_hearing(request, case_id):
    if request.method == 'POST':
        case = get_object_or_404(CaseRequest, id=case_id)

        Hearing.objects.create(
            case=case,
            hearing_date=request.POST.get('date'),
            hearing_time=request.POST.get('time'),
            note=request.POST.get('note', '')
        )

    return redirect('lawyer_dashboard')
