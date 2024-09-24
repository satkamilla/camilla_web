from rest_framework import serializers
from .models import Review, ServiceType, Service, Blog, CommentBlog, CommentService, FavoriteService, FavoriteBlog
from django.contrib.auth import get_user_model
from authorization.serializers import UserProfileSerializer
User = get_user_model()
from .models import Blog, CommentBlog, Master, CommentProfile, Client, CustomUser as User
 
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating']
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']

class ServiceSerializer(serializers.ModelSerializer):
    master = serializers.StringRelatedField(read_only=True)
    service_type = serializers.PrimaryKeyRelatedField(queryset=ServiceType.objects.all())

    class Meta:
        model = Service
        fields = ['id', 'master', 'name', 'description', 'price', 'image', 'service_type', 'usage']

class MasterSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Master
        fields = ['user', 'age', 'description', 'experience']
        

class CommentBlogSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CommentBlog
        fields = ['id', 'blog', 'author', 'content', 'created_at']
        

class CommentProfileSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CommentProfile
        fields = ['id', 'profile', 'author', 'content', 'created_at']



class BlogDetailSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    comments = CommentBlogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Blog
        fields = ['id', 'master', 'title', 'content', 'created_at', 'image', 'comments']
        
        
class BlogSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = ['id', 'master', 'title', 'content', 'created_at', 'image']


class CommentServiceSerializer(serializers.ModelSerializer):
    service = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CommentService
        fields = ['id', 'service', 'author', 'content', 'created_at']

class FavoriteServiceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = FavoriteService
        fields = ['id', 'user', 'service']

class FavoriteBlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    blog = BlogSerializer(read_only=True)
    
    class Meta:
        model = FavoriteBlog
        fields = ['id', 'user', 'blog']




from .models import Service, Cart, CartItem



class CartItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'service', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
        
        
class MasterDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    services = ServiceSerializer(many=True, read_only=True)
    blogs = BlogSerializer(many=True, read_only=True)

    class Meta:
        model = Master
        fields = ['user', 'age', 'description', 'experience', 'services', 'blogs']



from .models import Order, OrderItem
from content.serializers import ServiceSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'service', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'created_at']