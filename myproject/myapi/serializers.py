from rest_framework import serializers
from .models import CompanyDetails, UserDetails, TaskProgress, UserFeedback


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ['company_id', 'company_xp', 'charity']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['user_sub', 'user_name', 'company_id', 'start_date', 'user_xp', 'user_level']


class TaskFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProgress
        fields = ['id', 'task_id', 'completed', 'partial']


class UserTaskSerializer(serializers.ModelSerializer):
    tasks = TaskFieldsSerializer(many=True)

    class Meta:
        model = UserDetails
        fields = ['tasks']


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProgress
        fields = ['id', 'user_sub', 'task_id', 'completed', 'partial']


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'
