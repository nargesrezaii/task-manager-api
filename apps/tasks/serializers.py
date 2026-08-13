from rest_framework import serializers
from django.utils import timezone

from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source = "owner.username"    
    )

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty."    
        )
        
        if len(value)>200:
            raise serializers.ValidationError(
                "Title cannot exceed 200 characters."
            )

        return value
    
    def validate(self, attrs):
        status = attrs.get("status")
        due_date = attrs.get("due_date")

        if (
            status == "COMPLETED"
            and due_date
            and due_date > timezone.now()
        ): 
            raise serializers.ValidationError(
                "A completed task cannot have a future due date."    
            )
        return attrs

    class Meta:
        model = Task
        fields = "__all__"
        
        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )