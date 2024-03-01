from django.urls import path
from .views import menu,payment_view, payment_success_view,initiate_payment
from .views import firebase_login_save,logout_view,edit_customer,save_order,get_all_website_orders
from django.conf.urls.static import static
from foodporium import settings
urlpatterns = [
    path('', menu, name='menu'),
    path('logout/', logout_view, name='logout'),
    path('payment/', payment_view, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    path('initiate_payment/', initiate_payment, name='initiate_payment'),
    path('firebase_login_save/', firebase_login_save),
    path('edit-customer/', edit_customer, name='edit_customer'),
    path('save_order/', save_order, name='save_order'),
    path('orders/', get_all_website_orders, name='get_all_website_orders'),
              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)