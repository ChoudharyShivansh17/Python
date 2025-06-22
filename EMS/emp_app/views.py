from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer

@api_view(['GET'])
def employee_api(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# Only admin users allowed
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(is_admin)
def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'all_emp.html', context)

@login_required
@user_passes_test(is_admin)
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = int(request.POST.get('salary'))
        bonus = int(request.POST.get('bonus'))
        phone = int(request.POST.get('phone'))
        dept_id = int(request.POST.get('dept'))
        role_id = int(request.POST.get('role'))

        try:
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Department.DoesNotExist:
            return HttpResponse("Invalid Department ID")
        except Role.DoesNotExist:
            return HttpResponse("Invalid Role ID")

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=dept,
            role=role,
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse("Employee added successfully!")

    elif request.method == 'GET':
        roles = Role.objects.all()
        depts = Department.objects.all()
        return render(request, 'add_emp.html', {'roles': roles, 'depts': depts})
    else:
        return HttpResponse("An error occurred. Employee not added.")

@login_required
@user_passes_test(is_admin)
def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully.")
        except Employee.DoesNotExist:
            return HttpResponse("Invalid Employee ID.")

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

@login_required
@user_passes_test(is_admin)
def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    return render(request, 'filter_emp.html')
