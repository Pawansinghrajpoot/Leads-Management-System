from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.login_view, name='login'),  # Root URL will now direct to login
    path('accounts/login/', views.login_view, name='login'),  # If you want this for consistency
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Logout and redirect to login
    path('index/', views.index, name='index'),  # Index after successful login
    path('leads_data/', views.leads_data, name='leads_data'),
    path('master-dashboard/', views.master_dashboard, name='master_dashboard'),
    path('excel_data/', views.excel_data, name='excel_data'),
    path('alerts/', views.alerts_view, name='alerts'),
]
