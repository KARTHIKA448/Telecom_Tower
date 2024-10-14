from django.shortcuts import render
from .models import *
import os
import pandas as pd
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request,'home.html')

def dashboard(request):
    obj = Tower.objects.all()
    context = {"obj":obj}
    return render(request,'dashboard.html',context)

def data(request):
    return render(request,'data.html')

def detailedview(request, id):
    # Retrieve the Tower object based on the provided id
    obj = Tower.objects.get(id=id)

    # Handle POST request for updating the Tower object
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        obj.name = name
        obj.location = location
        obj.save()
        return redirect('home')  # Redirect to the home page after update

    # Load the data from an Excel file
    file_path = os.path.join('E:\\tower\\my_project\\my_app\\', 'Data.xlsx')
    df = pd.read_excel(file_path)

    # Print the column names for debugging
    print("Columns in the DataFrame:", df.columns)

    # Ensure that the Time column is treated as a string for easy rendering in charts
    df.columns = df.columns.str.strip()  # Strip any whitespace from column names
    if 'TIME' in df.columns:
        df['TIME'] = df['TIME'].astype(str)
    else:
        return HttpResponse("The 'Time' column was not found in the Excel file.", status=404)

    # Extract columns from the dataframe and pass them to the template
    context = {
        'obj': obj,  # Pass the Tower object to the template
        'time': df['TIME'].tolist(),
        'sensor_status': df['SENSOR Status'].tolist(),
        'cabin_door_status': df['CABIN DOOR status'].tolist(),
        'clean_duct_status': df['CLEAN DUCT Status'].tolist(),
        'generator_status': df['Generator_status'].tolist(),
        'fuel_cap_status': df['FUEL CAP status'].tolist(),
        'fuel_liters': df['FUEL Ltr'].tolist(),
    }

    return render(request, 'dashboard_detailed_page.html', context)