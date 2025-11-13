from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from my_app.models import Teacher
from django.db.models import Q

# List teachers with optional search
def index(request):
    search_query = request.GET.get('search_item')

    if search_query:
        teachers = Teacher.objects.filter(first_name__icontains=search_query) | Teacher.objects.filter(last_name__icontains=search_query)
    else:
        teachers = Teacher.objects.all()

    paginator = Paginator(teachers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {"teachers": page_obj, "count_item": teachers.count()}
    return render(request, 'pages/teachers/index.html', context=data)

# Show Create Teacher Form
def show(request):
    return render(request, "pages/teachers/create.html")

# Create Teacher
def create(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        salary = request.POST.get('salary')

        teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            address=address,
            salary=salary
        )
        teacher.full_clean()  # validate fields
        teacher.save()
        messages.success(request, "Teacher created successfully")
        return redirect('teacher_index')

    return render(request, 'pages/teachers/create.html')

# Delete teacher
def delete_by_id(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    teacher.delete()
    messages.success(request, "Teacher deleted successfully")
    return redirect('teacher_index')

# Edit teacher form
def edit_by_id(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    data = {"teacher": teacher}
    return render(request, "pages/teachers/edit.html", context=data)

# Update teacher
def update_by_id(request, id):
    teacher_existing = get_object_or_404(Teacher, pk=id)

    if request.method == "POST":
        teacher_existing.first_name = request.POST.get('first_name')
        teacher_existing.last_name = request.POST.get('last_name')
        teacher_existing.gender = request.POST.get('gender')
        teacher_existing.dob = request.POST.get('dob')
        teacher_existing.address = request.POST.get('address')
        teacher_existing.salary = request.POST.get('salary')

        teacher_existing.full_clean()
        teacher_existing.save()
        messages.success(request, "Teacher updated successfully")
        return redirect('teacher_index')

    data = {"teacher": teacher_existing}
    return render(request, "pages/teachers/edit.html", context=data)
