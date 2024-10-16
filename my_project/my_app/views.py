from django.shortcuts import render, redirect, get_object_or_404
from .models import Tower
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import Towerform

# Home page view
def home(request):
    return render(request, 'home.html')

# Dashboard view - allows only authenticated users
@login_required(login_url='login')
def dashboard(request):
    obj = Tower.objects.all()
    context = {"obj": obj}
    return render(request, 'dashboard.html', context)

# Detailed view - allows only authenticated users, with editing allowed
@login_required(login_url='login')
def detailedview(request, id):
    obj = get_object_or_404(Tower, id=id)

    # Check if a file is associated with this tower before attempting to load it
    if not obj.file:
        error_message = "No data file uploaded for this tower."
        return render(request, 'dashboard.html', {'obj': Tower.objects.all(), 'error_message': error_message})

    # If file exists, proceed to load the data
    if request.method == "POST" and request.user.is_staff:
        name = request.POST.get('name')
        location = request.POST.get('location')
        file = request.FILES.get('file')
        
        obj.name = name
        obj.location = location
        if file:
            obj.file = file  # Update the file only if a new one is uploaded
        obj.save()
        return redirect('dashboard')  # Redirect to the dashboard after update

    # Load the data from the uploaded Excel file
    try:
        df = pd.read_excel(obj.file.path)

        # Ensure that the DataFrame has columns for charts
        df.columns = df.columns.str.strip()
        if 'TIME' in df.columns:
            df['TIME'] = df['TIME'].astype(str)
        else:
            return HttpResponse("The 'TIME' column was not found in the Excel file.", status=404)

        # Extract columns from the DataFrame and pass them to the template
        context = {
            'obj': obj,
            'time': df['TIME'].tolist(),
            'sensor_status': df['SENSOR Status'].tolist(),
            'cabin_door_status': df['CABIN DOOR status'].tolist(),
            'clean_duct_status': df['CLEAN DUCT Status'].tolist(),
            'generator_status': df['Generator_status'].tolist(),
            'fuel_cap_status': df['FUEL CAP status'].tolist(),
            'fuel_liters': df['FUEL Ltr'].tolist(),
        }
        return render(request, 'dashboard_detailed_page.html', context)

    except FileNotFoundError:
        error_message = "No data file uploaded for this tower."
        return render(request, 'dashboard.html', {'obj': Tower.objects.all(), 'error_message': error_message})

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

# Register (Sign-up) view
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

# Login view
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

# Logout view
def logout(request):
    auth.logout(request)
    return redirect('login')

# Check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# Upload view (only for admin users)
@login_required
@user_passes_test(is_admin)
def upload_file(request):
    if request.method == 'POST':
        form = Towerform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Tower created successfully!')  # Set a success message
            return redirect('dashboard')  # Redirect to the dashboard after creation
    else:
        form = Towerform()
    return render(request, 'upload.html', {'form': form})

# Edit view for tower
@login_required
@user_passes_test(is_admin)
def edit_view(request, id):
    tower = get_object_or_404(Tower, id=id)

    if request.method == 'POST':
        tower.name = request.POST.get('name')
        tower.location = request.POST.get('location')
        file = request.FILES.get('file')
        
        if file:
            tower.file = file  # Update the file only if a new one is uploaded

        tower.save()
        messages.success(request, 'Tower details updated successfully!')
        return redirect('dashboard')  # Redirect to the dashboard after editing

    return render(request, 'edit.html', {'tower': tower})

# Delete file view
@login_required
@user_passes_test(is_admin)
def delete_file(request, file_id):
    file = get_object_or_404(Tower, id=file_id)  # Fetch the file by ID
    file.delete()  # Delete the file from the database
    # messages.success(request, 'Tower deleted successfully!')
    return redirect('dashboard')  # Redirect to dashboard after deletion
