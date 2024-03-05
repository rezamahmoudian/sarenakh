from rest_framework import serializers
from .models import *


class HomeSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, help_text=("string"))
    model = serializers.CharField(required=True, help_text=("string"))


