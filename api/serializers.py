from rest_framework import serializers
from .models import Departamento, Sensor, Evento, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # Usar email en vez de username
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }

        return super().validate(credentials)
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','role','password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        pwd = validated_data.pop('password', None)
        user = User(**validated_data)
        if pwd:
            user.set_password(pwd)
        else:
            user.set_password(User.objects.make_random_password())
        user.save()
        return user

    def update(self, instance, validated_data):
        pwd = validated_data.pop('password', None)
        for k,v in validated_data.items():
            setattr(instance, k, v)
        if pwd:
            instance.set_password(pwd)
        instance.save()
        return instance


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def validate_nombre(self, v):
        if len(v.strip()) < 3:
            raise serializers.ValidationError("Nombre debe tener al menos 3 caracteres.")
        return v


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only_fields = ('created_at','updated_at','id')

    def validate_uid(self, v):
        qs = Sensor.objects.filter(uid=v)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("UID ya registrado.")
        return v

    def validate_estado(self, v):
        allowed = [c[0] for c in Sensor.STATE_CHOICES]
        if v not in allowed:
            raise serializers.ValidationError("Estado inválido.")
        return v


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('id','timestamp')
