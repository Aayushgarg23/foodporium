from django.shortcuts import render, redirect
from django.conf import settings
from .models import MenuItem, Category,Customer,Coupons,FlashOffer,ScrollingText,DeliveryCharge,Loading,WebsiteItems,WebsiteOrder,UserCoupon
import razorpay
import json
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize


client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
@csrf_exempt
def initiate_payment(request):
    amount = int(request.POST.get('amount', 0))
    data = {
        'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture the payment after successful authorization
    }
    response = client.order.create(data=data)
    return JsonResponse({'id': response['id']})



def payment_view(request):
    amount = 10  # Set the amount dynamically or based on your requirements
    order_id = initiate_payment(amount)
    context = {
        'order_id': order_id,
        'amount': amount
    }
    return render(request, 'payment.html', context)
def payment_success_view(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        print(params_dict)
        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment signature verification successful
            # Perform any required actions (e.g., update the order status)
            return render(request, 'payment_success.html')
        except razorpay.errors.SignatureVerificationError as e:
            # Payment signature verification failed
            # Handle the error accordingly
            return render(request, 'payment_failure.html')
    return HttpResponse("hi")

def menu(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            used_coupons = UserCoupon.objects.filter(user=user, used=True)
            customer = Customer.objects.get(user=request.user)
            print("authorized")
            if used_coupons.exists():
                used_coupon_ids = used_coupons.values_list('coupon__id', flat=True)
                for_one_time_coupons = Coupons.objects.filter(id__in=used_coupon_ids, for_one_time=True)
                coupons = Coupons.objects.exclude(id__in=used_coupon_ids)
                print(coupons)
            else:
                # No used coupons found for the user
                coupons = Coupons.objects.all()
            try:
                flash_offers = FlashOffer.objects.get(visibility=True)
            except:
                flash_offers="flash_offers"
                pass
            selected_category_ids = MenuItem.objects.values_list('category__id', flat=True).distinct()
            selected_categories = Category.objects.filter(id__in=selected_category_ids)
            texts = ScrollingText.objects.all()
            delivery_charge = DeliveryCharge.objects.first()  # Assuming there's only one delivery charge instance
            # categories = Category.objects.all()
            menu_items = MenuItem.objects.all()
            return render(request,'index.html', {'categories': selected_categories, 'menu_items': menu_items,'customer': customer,'coupons':coupons,'flash_offer': flash_offers,'movingtext':texts,'delivery':delivery_charge})
        else:
            gif = Loading.objects.first()
            print(gif)
            return render(request,"login_firebase.html",{'gif': gif})
    except:
        gif = Loading.objects.first()
        return render(request,"login_firebase.html",{'gif': gif})


@csrf_exempt
def firebase_login_save(request):
    data = json.loads(request.body)
    # Extract the required parameters
    username = data.get('username')
    provider = data.get('provider')
    token = data.get('token')
    print(username)
    print(provider)
    print(token)
    user = authenticate(request,username=username,password='12121212')
    print(user)

    if user is not None:
        print("authorized")
        login(request, user)

    else:
        # User doesn't exist, create a new one
        user = User.objects.create_user(username=username, password='12121212')
        customer = Customer.objects.create(user=user, name='', address='', phone='')
        login(request, user)
        print("else")
    # return HttpResponse("Login Request")
    # firbase_response=loadDatafromFirebaseApi(token)
    # firbase_dict=json.loads(firbase_response)
    # if "users" in firbase_dict:
    #     user=firbase_dict["users"]
    #     if len(user)>0:
    #         user_one=user[0]
    #         if "phoneNumber" in user_one:
    #             if user_one["phoneNumber"]==email:
    #                 data=proceedToLogin(request,email, username, token, provider)
    #                 return HttpResponse(data)
    #             else:
    #                 return HttpResponse("Invalid Login Request")
    #         else:
    #             if email==user_one["email"]:
    #                 provider1=user_one["providerUserInfo"][0]["providerId"]
    #                 if user_one["emailVerified"]==1 or user_one["emailVerified"]==True or user_one["emailVerified"]=="True" or provider1=="facebook.com":
    #                     data=proceedToLogin(request,email,username,token,provider)
    #                     return HttpResponse(data)
    #                 else:
    #                     return HttpResponse("Please Verify Your Email to Get Login")
    #             else:
    #                 return HttpResponse("Unknown Email User")
    #     else:
    #         return HttpResponse("Invalid Request User Not Found")
    # else:
    return render(request,"index.html")
def logout_view(request):
    logout(request)
    # Redirect to a page after logout (you can customize this URL)
    return render(request,'login_firebase.html')

from .forms import CustomerForm

@login_required
def edit_customer(request):
    customer = request.user.customer

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return menu(request)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'edit_customer.html', {'form': form})
@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        order_data = json.loads(data)
        coupon = order_data.get('coupon')
        print(coupon)
        if (coupon !="Null"):
            try:
                coufromcou = Coupons.objects.get(coupon_name=coupon,for_one_time='True')
                UserCoupon.objects.create(user= request.user,coupon=coufromcou,used='True')
            except:
                pass
        name = order_data.get('name')
        address = order_data.get('address')
        phone=order_data.get('phone')
        total=order_data.get('total')
        items = order_data.get('items', [])
        print(items)
        order = WebsiteOrder.objects.create(
            user=request.user,  # Assuming there's a logged-in user
            name=name,
            phone=phone,
            address=address,
            total=total,
            order_status=1,  # Set the initial order status as 'In', adjust as needed
        )

        # Create WebsiteItems instances related to the saved WebsiteOrder
        for item_data in order_data['items']:
            WebsiteItems.objects.create(
                order_link=order,
                name=item_data['name'],
                price=item_data['price'],
            )
    return JsonResponse({'status': 'success', 'message': 'Order saved successfully'})

@csrf_exempt
def get_all_website_orders(request):
    return render(request, 'order.html')