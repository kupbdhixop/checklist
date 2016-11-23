from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Checklist, Task

base_fields = ('url', 'created', 'modified')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'is_staff',
            'password',
        )


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the default list view of tasks
    """
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    def create(self, validated_data):
	request = self.context['request']
	serializer = TaskSerializer(data=request.data)
	# make sure they have access to this list
	if serializer.is_valid(raise_exception=True) and validated_data['checklist'].has_perm(request.user):
            return Task.objects.create(owner=request.user, **validated_data)
        raise serializers.ValidationError('Unable to create tasks on checklist', 400)

    class Meta:
        model = Task
        fields = base_fields + (
            'description',
            'checklist',
            'completed',
            'owner',
	)


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the default list view of checklist
    """
    shared = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', many=True)

    def create(self, validated_data):
	# custom save to add creator as owner
        shared = validated_data.pop('shared', None)
        checklist = Checklist.objects.create(owner=self.context['request'].user, **validated_data)
        # need a checklist instance before adding shared relations
        if shared:
            checklist.shared = shared
            checklist.save()
	return checklist

    class Meta:
        model = Checklist
        fields = base_fields + (
            'name',
            'description',
            'shared',
        )


class ChecklistDetailSerializer(serializers.HyperlinkedModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='task_set')
    shared = UserSerializer(many=True)

    def create(self, validated_data):
        # custom save to add creator as owner
        checklist = Checklist.objects.create(owner=self.context['request'].user, **validated_data)
	return checklist

    class Meta:
        model = Checklist
        fields = base_fields + (
             'created',
             'name',
             'tasks',
             'owner',
             'shared',
	)

