from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
     path('dashboard/', views.dashboard, name='dashboard'),

    # ----- BOOKING FLOW -----
    path('book/<int:lawyer_id>/', views.book_lawyer, name='book_lawyer'),
    path('accept/<int:case_id>/', views.accept_case, name='accept_case'),
    path('reject/<int:case_id>/', views.reject_case, name='reject_case'),

    path('lawyer-dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('accept-case/<int:case_id>/', views.accept_case, name='accept_case'),
    path('reject-case/<int:case_id>/', views.reject_case, name='reject_case'),

    path('hearings/', views.hearing_calendar, name='hearing_calendar'),
    path('add-hearing/<int:case_id>/', views.add_hearing, name='add_hearing'),

]
