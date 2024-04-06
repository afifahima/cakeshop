from django.contrib import admin
from . models import Customer, Product, Cart

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['id','title','selling_Price','description','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display =['id','user','product','quantity']

