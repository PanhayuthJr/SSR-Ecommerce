from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from my_app.models import Student
from django.db.models import Q

# List students with optional search
def index(request):
    # Use GET instead of POST
    search_query = request.GET.get('search_item')  # <-- change here

    if search_query:
        students = Student.objects.filter(first_name__icontains=search_query) | Student.objects.filter(last_name__icontains=search_query)
    else:
        students = Student.objects.all()

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {"students": page_obj, "count_item": students.count()}
    return render(request, 'pages/students/index.html', context=data)

# Show Create Student Form
def show(request):
    return render(request, "pages/students/create.html")

# Create Student
def create(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        student = Student(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            address=address
        )
        student.full_clean()  # validate fields
        student.save()
        messages.success(request, "Student created successfully")
        return redirect('student_index')  # Use a named URL

    return render(request, 'pages/students/create.html')

# Delete student
def delete_by_id(request, id):
    student = get_object_or_404(Student, pk=id)
    student.delete()
    messages.success(request, "Student deleted successfully")
    return redirect('student_index')  # Use a named URL

# Edit student form
def edit_by_id(request, id):
    student = get_object_or_404(Student, pk=id)
    data = {"student": student}
    return render(request, "pages/students/edit.html", context=data)

# Update student
def update_by_id(request, id):
    student_existing = get_object_or_404(Student, pk=id)

    if request.method == "POST":
        # Update fields individually
        student_existing.first_name = request.POST.get('first_name')
        student_existing.last_name = request.POST.get('last_name')
        student_existing.gender = request.POST.get('gender')
        student_existing.dob = request.POST.get('dob')
        student_existing.address = request.POST.get('address')

        student_existing.full_clean()
        student_existing.save()
        messages.success(request, "Student updated successfully")
        return redirect('student_index')  # Redirect to student list

    # If GET request, show the edit form
    data = {"student": student_existing}
    return render(request, "pages/students/edit.html", context=data)
