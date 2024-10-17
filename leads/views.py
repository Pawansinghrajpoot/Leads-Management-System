# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Lead
from .forms import LeadForm
import pandas as pd
from datetime import datetime
from .forms import UserLoginForm  # Adjust the import based on your project structure
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
# Handle lead data form and save to Excel
from django.utils import timezone

def get_today():
    return timezone.now().date()


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLoginForm

def login_view(request):
    form = UserLoginForm(data=request.POST or None)
    if form.is_valid():
        # Get the cleaned data from the form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is an admin
            if user.username == 'admin':
                return redirect('master_dashboard')  # Redirect to admin dashboard for admin users
            else:
                return redirect('index')  # Redirect to index page for all other users
        else:
            form.add_error(None, "Invalid username or password")  # Add a general error if authentication fails

    return render(request, 'login.html', {'form': form})


def index(request):
    success_message = None
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Data added successfully!'

            # Excel management
            excel_path = r'C:\Users\Admin\Downloads\minproject (3)\minproject\Data\Demo_data_interns.xlsx'  # Fetch the file path from settings
            try:
                excel_data_df = pd.read_excel(excel_path)
            except FileNotFoundError:
                excel_data_df = pd.DataFrame()  # Create a new dataframe if file not found

            # Prepare new data
            new_data = pd.DataFrame([{
                'Name': form.cleaned_data['name'],
                'Number': form.cleaned_data['number'],
                'Database': form.cleaned_data['database'],
                'demo lecture attended?': form.cleaned_data['demo_lecture_attended'],
                'interested in': form.cleaned_data['interested_in'],
                'last Whatsapp blast': form.cleaned_data['last_whatsapp_blast'].replace(tzinfo=None) if form.cleaned_data['last_whatsapp_blast'] else None,
                'response to whatsappblast': form.cleaned_data['response_to_whatsapp_blast'],
                'last call date': form.cleaned_data['last_call_date'],
                'Followup of last call': form.cleaned_data['followup_of_last_call'],
                'Close Reason': form.cleaned_data['close_reason'],
            }])

            # Append new data and save to Excel
            updated_data = pd.concat([excel_data_df, new_data], ignore_index=True)
            updated_data.to_excel(excel_path, index=False)

            # Reset form after successful save
            form = LeadForm()  
    else:
        form = LeadForm()

    return render(request, 'index.html', {'form': form, 'success_message': success_message})

# Show the leads data, with filtering and pagination
def leads_data(request):
    excel_path = r'C:\Users\Admin\Downloads\minproject (3)\minproject\Data\Demo_data_interns.xlsx'  # Ensure you're using the correct file path

    # Read the Excel file
    try:
        excel_data_df = pd.read_excel(excel_path)
    except FileNotFoundError:
        excel_data_df = pd.DataFrame()  # Handle case where file is not found

    # Convert datetime columns
    if 'last Whatsapp blast' in excel_data_df.columns:
        excel_data_df['last Whatsapp blast'] = pd.to_datetime(excel_data_df['last Whatsapp blast'], errors='coerce')

    if 'last call date' in excel_data_df.columns:
        excel_data_df['last call date'] = pd.to_datetime(excel_data_df['last call date'], errors='coerce').dt.date

    # Replace NaT or None values with a placeholder
    excel_data_df.fillna('N/A', inplace=True)

    # Get filter values from request
    database_filter = request.GET.get('database', '')
    demo_lecture_filter = request.GET.get('demo_lecture_attended', '')
    interested_in_filter = request.GET.get('interested_in', '')

    # Apply filters to the DataFrame
    if database_filter:
        excel_data_df = excel_data_df[excel_data_df['Database'].str.contains(database_filter, case=False, na=False)]
    
    if demo_lecture_filter:
        demo_lecture_value = True if demo_lecture_filter.lower() == 'yes' else False
        excel_data_df = excel_data_df[excel_data_df['demo lecture attended?'] == demo_lecture_value]

    if interested_in_filter:
        excel_data_df = excel_data_df[excel_data_df['interested in'].str.contains(interested_in_filter, case=False, na=False)]

    # Convert the filtered DataFrame to a dictionary
    excel_data = excel_data_df.to_dict(orient='records')

    # Pagination: Show 50 records per page
    paginator = Paginator(excel_data, 50)  # 50 records per page

    # Get the current page number from request, default to 1
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Populate dropdown filter values dynamically
    database_options = excel_data_df['Database'].unique() if not excel_data_df.empty else []
    interested_in_options = excel_data_df['interested in'].unique() if not excel_data_df.empty else []

    return render(request, 'leads_data.html', {
        'excel_data': page_obj,
        'database_options': database_options,
        'interested_in_options': interested_in_options,
        'page_obj': page_obj,  # Pass the paginator object to the template
    })



# Master dashboard with employee list
@login_required
def master_dashboard(request):
    employees = User.objects.filter(is_master=False)
    return render(request, 'master_dashboard.html', {'employees': employees})


# Show Excel data with filtering and pagination
def excel_data(request):
    excel_path = r'C:\Users\Admin\Downloads\minproject (3)\minproject\Data\Demo_data_interns.xlsx'  # Ensure you're using the correct file path

    # Read the Excel file
    try:
        excel_data_df = pd.read_excel(excel_path)
    except FileNotFoundError:
        excel_data_df = pd.DataFrame()  # Handle case where file is not found

    # Replace NaT or None values with a placeholder
    excel_data_df.fillna('N/A', inplace=True)

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        excel_data_df = excel_data_df[excel_data_df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

    # Convert the filtered DataFrame to a dictionary
    excel_data = excel_data_df.to_dict(orient='records')

    # Pagination: Show 50 records per page
    paginator = Paginator(excel_data, 50)  # 50 records per page

    # Get the current page number from request, default to 1
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'excel_data.html', {
        'excel_data': page_obj,
        'query': query,
        'page_obj': page_obj,  # Pass the paginator object to the template
    })

@login_required
def alerts_view(request):
    today = datetime.now().date()
    alerts = Lead.objects.filter(last_call_date=today)

    return render(request, 'alerts.html', {'alerts': alerts})

# View for managing call alerts and reminders
def alert_leads(request):
    today = datetime.now().date()

    # Get leads that need to be called today
    leads_due_for_call = Lead.objects.filter(followup_of_last_call=today)

    # Separate leads into those called and those pending
    calls_made = leads_due_for_call.filter(call_made=True)
    calls_pending = leads_due_for_call.filter(call_made=False)

    # Mark a lead as called
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        lead = Lead.objects.get(id=lead_id)
        lead.call_made = True
        lead.save()
        return redirect('alerts')

    return render(request, 'alerts.html', {
        'calls_made': calls_made,
        'calls_pending': calls_pending,
        'total_calls': leads_due_for_call.count(),
        'calls_completed': calls_made.count(),
        'calls_remaining': calls_pending.count(),
    })
from django.shortcuts import render, redirect
from .forms import LeadForm
from django.conf import settings
import pandas as pd

def index(request):
    success_message = None
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()  # Ensure the follow-up date is saved
            success_message = 'Data added successfully!'
            # Optional: Update Excel logic here if needed
    else:
        form = LeadForm()

    return render(request, 'index.html', {'form': form, 'success_message': success_message})

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Lead
from django.utils import timezone
import pytz

@login_required


def leads_data(request):
    # Set your local timezone
    local_tz = pytz.timezone('Asia/Kolkata')  # or your appropriate timezone

    # Get current UTC time and convert it to local time
    current_time = timezone.now()
    local_time = current_time.astimezone(local_tz)
    
    today = local_time.date()  # Get today's date in local timezone

    # Handle marking a call as completed
    if request.method == 'POST' and 'complete_call' in request.POST:
        lead_id = request.POST.get('lead_id')
        try:
            lead = Lead.objects.get(id=lead_id)
            lead.call_made = True
            lead.last_call_date = today  # Update last call date to today
            lead.followup_of_last_call = today + timezone.timedelta(days=7)  # Set next follow-up date
            lead.save()
            print(f"Lead {lead_id} marked as completed.")
        except Lead.DoesNotExist:
            print(f"Lead {lead_id} does not exist.")  # Debugging statement
        return redirect('leads_data')

    # Get today's follow-ups and completed calls
    leads_due_today = Lead.objects.filter(followup_of_last_call=today, call_made=False)
    completed_calls_today = Lead.objects.filter(last_call_date=today, call_made=True)

    # Print statements for debugging
    print(f"Today's Date: {today}")
    print(f"Leads Due Today: {leads_due_today.count()} leads")
    print(f"Completed Calls Today: {completed_calls_today.count()} leads")

    # Get all leads for pagination
    all_leads = Lead.objects.all()
    paginator = Paginator(all_leads, 50)  # Show 50 leads per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'leads_data.html', {
        'leads_due_today': leads_due_today,
        'completed_calls_today': completed_calls_today,
        'page_obj': page_obj,
    })
