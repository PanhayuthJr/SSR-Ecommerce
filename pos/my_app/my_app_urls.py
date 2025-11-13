from itertools import product

from django.urls import path

from my_app import views
from .my_views import category_views
from .my_views import student_views
from .my_views import subject_views
from .my_views import teacher_views
from my_app.my_views import product_views


urlpatterns = [
    path("",views.home,name="/"),
    path("find_by_id/<id>",views.find_by_id),

    path("content",views.content),
    #route category
    path("category/index",category_views.index),
    path("category/show",category_views.show),
    path("category/create",category_views.create),

    path("category/delete_by_id/<int:id>", category_views.delete_by_id, name="delete_category"),

    path("category/edit_by_id/<int:id>", category_views.edit_by_id, name="edit_category"),
    path("category/update_by_id/<int:id>", category_views.update_by_id, name="update_category"),
    #work with student

    #path('students/create/', student_views.create),

    path('student/index/', student_views.index, name='student_index'),
    path('students/create/', student_views.create, name='create_student'),
    path('student/delete/<int:id>/', student_views.delete_by_id, name='delete_student'),
    path('student/edit/<int:id>/', student_views.edit_by_id, name='edit_student'),
    path('student/update/<int:id>/', student_views.update_by_id, name='update_student'),
# Subject URLs
    path('subject/index/', subject_views.index, name='subject_index'),
    path('subject/show/', subject_views.show),
    path('subject/create/', subject_views.create),
    path('subject/delete_by_id/<int:id>/', subject_views.delete_by_id),
    path('subject/edit_by_id/<int:id>/', subject_views.edit_by_id),
    path('subject/update_by_id/<int:id>/', subject_views.update_by_id),
    # Teacher CRUD
    path('teacher/index/', teacher_views.index, name='teacher_index'),
    path('teachers/create/', teacher_views.create, name='create_teacher'),
    path('teacher/delete/<int:id>/', teacher_views.delete_by_id, name='delete_teacher'),
    path('teacher/edit/<int:id>/', teacher_views.edit_by_id, name='edit_teacher'),
    path('teacher/update/<int:id>/', teacher_views.update_by_id, name='update_teacher'),

    #route product
    path('product/index', product_views.index, name='product_index'),
    path('product/show', product_views.show, name='show_product'),
    path('product/create', product_views.create, name='create_product'),
    path('product/edit/<int:id>/', product_views.edit, name='edit_product'),
    path('product/update_by_id/<int:id>/', product_views.update_by_id, name='update_product'),
    path('product/delete/<int:id>/', product_views.delete, name='delete_product'),



]
