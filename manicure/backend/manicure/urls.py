"""
URL configuration for manicure project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from content.views import index, masters
from django.conf import settings
from django.conf.urls.static import static
from authorization.views import LoginView, RegisterView, UserProfileView, UserProfileUpdateView
from content.views import (ServiceListView, ServiceDetailView,
CartView, AddToCartView,
RemoveFromCartView,
BlogCreateView,
MasterBlogListView, ServiceCreateView, ServiceTypeListView, 
BlogDetailView, BlogListView, MasterListView, 
MasterDetailView, MasterBlogsListView, MasterServicesListView,
UserServiceListView, CommentCreateView,
CheckoutView, OrderHistoryView, CommentProfileListView, CommentProfileCreateView)
from messenger.views import UserConversationsView, ConversationMessagesView, CreateMessageView, CreateConversationView, CreateOrGetConversationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('masters/', masters, name="masters"),
    
    
    #api
    path('api/v1/login/', LoginView.as_view(), name="login"),
    path('api/v1/register/', RegisterView.as_view(), name="register"),
    
    path('api/v1/services/', ServiceListView.as_view(), name='service-list'),
    path('api/v1/services/<int:id>/', ServiceDetailView.as_view(), name='service-detail'),

    path('api/v1/cart/', CartView.as_view(), name='cart-detail'),
    path('api/v1/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/v1/cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('api/v1/checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/v1/orders/', OrderHistoryView.as_view(), name='order-history'),
    path('api/v1/profile/', UserProfileView.as_view(), name='profile-detail'),
    path('api/v1/profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    
    path('api/v1/master-blogs/', MasterBlogListView.as_view(), name='master-blogs'),
    path('api/v1/blogs/', BlogListView.as_view(), name='blog-list'),
    path('api/v1/blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('api/v1/blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('api/v1/blogs/<int:blog_id>/comments/', CommentCreateView.as_view(), name='add-comment'),

    path('api/v1/profiles/<int:profile_id>/comments/', CommentProfileCreateView.as_view(), name='comment-profile-create'),
    path('api/v1/profiles/<int:profile_id>/comments/all/', CommentProfileListView.as_view(), name='comment-profile-list'),
    
    
    path('api/v1/services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('api/v1/service-types/', ServiceTypeListView.as_view(), name='service-types'),
    path('api/v1/user-services/', UserServiceListView.as_view(), name='user-services'),

    path('api/v1/conversations/', UserConversationsView.as_view(), name='user-conversations'),
    path('api/v1/conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
    path('api/v1/conversations/<int:conversation_id>/messages/create/', CreateMessageView.as_view(), name='create-message'),
    path('api/v1/conversations/create/<int:user_id>/', CreateConversationView.as_view(), name='create-conversation'),
    path('api/v1/conversations/create_or_get/', CreateOrGetConversationView.as_view(), name='create-or-get-conversation'),

    path('api/v1/masters/', MasterListView.as_view(), name='master-list'),
    path('api/v1/masters/<int:user_id>/', MasterDetailView.as_view(), name='master-detail'),

    path('api/v1/masters/<int:pk>/services/', MasterServicesListView.as_view(), name='master-services'),
    path('api/v1/masters/<int:pk>/blogs/', MasterBlogsListView.as_view(), name='master-blogs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)