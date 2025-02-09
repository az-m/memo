from django.urls import path, include
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('users/', views.get_update_user),
    path('create_user/', views.create_user),
    path('companies/<int:cid>/', views.get_update_company),
    path('user_tasks/', views.get_user_tasks),
    path('tasks/<int:tid>/', views.update_task),
    path('tasks/', views.add_task),
    path('feedback/<int:fid>/', views.delete_feedback),
    path('feedback/', views.add_feedback)
]