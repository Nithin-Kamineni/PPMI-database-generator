from django.urls import path
from aipbpk import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('test', views.test),
    path('varibles', views.getVariblesList),
    path('generate', views.getDataFromVariblesList),
    path('check-task-status/<str:task_id>/', views.check_task_status),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
