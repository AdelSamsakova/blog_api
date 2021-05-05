from rest_framework import serializers

from .models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'image')

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Заголовок не может повторяться')
        return title


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', )

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Заголовок не может повторяться')
        return title


class PostSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='slug')

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = Post.objects.create(author=user, **validated_data)
        return post

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
            fields.pop('text')
            fields.pop('tags')
            fields.pop('category')
            fields.pop('created_at')
        elif action == 'create':
            fields.pop('slug')
            fields.pop('author')
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category, context=self.context).data
        representation['tags'] = TagSerializer(instance.tags.all(), many=True, context=self.context).data
        return representation
