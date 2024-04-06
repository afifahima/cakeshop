"""
URL configuration for Bakery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app.views import subject
from app import views
from django.contrib.auth import views as auth_view
from app.forms import LoginForm, MyPasswordResetForm


urlpatterns = [

    path('admin/', admin.site.urls),
    path('lesson/',subject),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
   
    path('index',views.Index,name='index'),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/',views.address, name='address'),
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path("remove_cart/<str:cid>", views.remove_cart, name='remove_cart'),

    

    
    path('orders/',views.orders, name='orders'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('showcart/',views.show_cart),
    path('success/', views.Success.as_view(), name='success'),
    
    
   


    #login authentication
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm,next_page='profile'), name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    
]+static(settings.PRODUCT_URL,document_root=settings.PRODUCT_ROOT) 

#admin.site.site_header = "Sweet Cake" 
#admin.site.site_title= "Sweet Cake"
#admin.site.site_index_title= "Welcome to Sweet Cake"

