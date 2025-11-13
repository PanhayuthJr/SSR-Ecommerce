from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from my_app.models import Subject
from django.core.paginator import Paginator

def index(request):
    search_query = request.GET.get('search_item')  # use GET now
    if search_query:
        subjects = Subject.objects.filter(subject_name__icontains=search_query)
    else:
        subjects = Subject.objects.all()

    paginator = Paginator(subjects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {"subjects": page_obj, "count_item": subjects.count()}
    return render(request, 'pages/subjects/index.html', context=data)

def show(request):
    return render(request, 'pages/subjects/create.html')


def create(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')  # match your HTML input name

        if subject_name:  # simple validation
            subject = Subject(subject_name=subject_name)
            subject.full_clean()
            subject.save()
            messages.success(request, "Subject created successfully")
            return redirect('/subject/index')  # update to your list page
        else:
            messages.error(request, "Subject name is required")

    return render(request, 'pages/subjects/create.html')

def delete_by_id(request, id):
    subject = get_object_or_404(Subject, pk=id)
    subject.delete()
    messages.success(request, "Subject deleted successfully")
    return redirect('/subject/index/')

def edit_by_id(request, id):
    subject = get_object_or_404(Subject, pk=id)
    return render(request, 'pages/subjects/edit.html', {"subject": subject})

def update_by_id(request, id):
    subject = get_object_or_404(Subject, pk=id)

    if request.method == "POST":
        subject.subject_name = request.POST.get('subject_name')  # <- MUST match form input name
        subject.full_clean()
        subject.save()
        messages.success(request, "Subject updated successfully")
        return redirect('/subject/index/')  # or redirect('subject_index')

    return render(request, 'pages/subjects/edit.html', {'subject': subject})
