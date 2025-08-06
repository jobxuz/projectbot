
from rest_framework import serializers
from ...models import User




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm password")
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2') 
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')