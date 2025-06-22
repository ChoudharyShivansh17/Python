from django.contrib import admin
from .models import Employee, Role, Department

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'dept', 'role',
        'salary', 'bonus', 'phone', 'hire_date'
    )
    list_filter = ('dept', 'role', 'hire_date')
    search_fields = ('first_name', 'last_name', 'phone')
    ordering = ('-hire_date',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')
