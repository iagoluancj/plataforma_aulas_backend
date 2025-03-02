from uuid import UUID
from rest_framework import serializers

def validate_uuid(value):
    try:
        return str(UUID(value))
    except ValueError:
        raise serializers.ValidationError("ID inválido")
