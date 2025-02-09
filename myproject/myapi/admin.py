from django.contrib import admin
from.models import UserDetails, TaskProgress, CompanyDetails, UserFeedback


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ("user_sub", "user_name", "company_id", "start_date", "user_xp", "user_level")
    ordering = ("company_id", "user_name")
    pass


@admin.register(TaskProgress)
class UserTaskListAdmin(admin.ModelAdmin):
    list_display = ("user_sub", "task_id", "completed", "partial")
    ordering = ("user_sub", "task_id")
    pass


@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ("company_id", "company_xp", "charity")
    pass


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ("task_id", "company_id", "answer0", "answer1", "answer2", "answer3", "answer4",
                    "answer5", "answer6", "answer7", "answer8", "answer9", )
    pass


# Register your models here.
