from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authorization.models import Master, Client, CustomUser
from .serializers import MasterSerializer
from .models import Service, Cart, CartItem, Blog, ServiceType
from .serializers import ServiceSerializer, CartSerializer, CartItemSerializer, BlogSerializer, ServiceTypeSerializer, BlogDetailSerializer, MasterDetailSerializer
from rest_framework.exceptions import NotFound
import logging
from rest_framework.views import exception_handler
from .serializers import OrderSerializer, OrderItemSerializer, CommentProfileSerializer, CommentBlogSerializer
from .models import Order, OrderItem, CommentProfile
from content import serializers

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    print(f"Error: {exc}")
    return response
def index(request):
    return render(request, 'index.html')

def masters(request):
    return render(request, 'masters.html')

class UserServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(master=self.request.user.master_profile)
class MasterListView(generics.ListAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    
    
class MasterDetailView(generics.RetrieveAPIView):
    serializer_class = MasterDetailSerializer

    def get_object(self):
        try:
            user_id = self.kwargs['user_id']
            return Master.objects.get(user_id=user_id)
        except Master.DoesNotExist:
            raise NotFound("Master profile not found")
        
        
class MasterServicesListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        master_id = self.kwargs['pk']
        return Service.objects.filter(master_id=master_id)

class MasterBlogsListView(generics.ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        master_id = self.kwargs['pk']
        return Blog.objects.filter(master_id=master_id)


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]
class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'
    
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    
class MasterBlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_master:
            return Blog.objects.filter(master=user.master_profile)
        return Blog.objects.none()
       
class ServiceCreateView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(master=self.request.user.master_profile)

class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(master=self.request.user.master_profile)


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        service = Service.objects.get(id=request.data['service_id'])
        quantity = request.data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({'status': 'service added to cart'}, status=status.HTTP_200_OK)
    
    
class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        service = Service.objects.get(id=request.data['service_id'])
        cart_item = CartItem.objects.get(cart=cart, service=service)
        cart_item.delete()
        return Response({'status': 'service removed from cart'}, status=status.HTTP_200_OK)
    
    

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = request.user.cart.first()
        if not cart:
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, total_price=sum(item.service.price * item.quantity for item in cart.items.all()))
        for item in cart.items.all():
            OrderItem.objects.create(order=order, service=item.service, quantity=item.quantity, price=item.service.price * item.quantity)
        
        cart.items.all().delete()  # Clear the cart after ordering
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    

class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        if cart.items.count() == 0 and 'service_id' not in request.data:
            return Response({'status': 'cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if 'service_id' in request.data:
            service = Service.objects.get(id=request.data['service_id'])
            quantity = request.data.get('quantity', 1)
            order = Order.objects.create(user=request.user, total_price=service.price * int(quantity))
            OrderItem.objects.create(order=order, service=service, quantity=quantity, price=service.price)
        else:
            order = Order.objects.create(user=request.user, total_price=sum(item.service.price * item.quantity for item in cart.items.all()))
            for item in cart.items.all():
                OrderItem.objects.create(order=order, service=item.service, quantity=item.quantity, price=item.service.price)
            cart.items.all().delete()

        return Response({'status': 'order created successfully'}, status=status.HTTP_200_OK)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentBlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            blog_id = self.kwargs['blog_id']
            print(f"Received blog_id: {blog_id}")
            blog = Blog.objects.get(id=blog_id)
            author = self.request.user
            print(f"Creating comment for blog: {blog_id} by author: {author.email}")
            serializer.save(blog=blog, author=author)
        except Exception as e:
            print(f"Error creating comment: {str(e)}")
            raise serializers.ValidationError({'detail': str(e)})
        
        

class CommentProfileCreateView(generics.CreateAPIView):
    serializer_class = CommentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile_id = self.kwargs['profile_id']
        profile = CustomUser.objects.get(id=profile_id)
        serializer.save(author=self.request.user, profile=profile)

class CommentProfileListView(generics.ListAPIView):
    serializer_class = CommentProfileSerializer

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return CommentProfile.objects.filter(profile_id=profile_id)