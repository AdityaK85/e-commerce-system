from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from .models import *
from math import ceil
import json
from django.contrib import messages
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.utils.html import strip_tags
from online_shop import settings 
import datetime
# Create your views here.



def login(request):
    return render(request, 'login.html')


@csrf_exempt
def login_handle(request):
    user_email = request.POST.get('user_email')
    user_pass = request.POST.get('user_pass')

    if not user_login.objects.filter(user_email=user_email, user_pass = user_pass).exists():
        return HttpResponse("1")
    else :
        obj = user_login.objects.get(user_email=user_email, user_pass=user_pass)
        request.session['user_id'] = str(obj.id)
        return HttpResponse('0')



def signup(request):
    return render(request, 'signup.html')

@csrf_exempt
def signup_handle(request):
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    user_phone = request.POST.get('user_phone')
    user_addr = request.POST.get('user_addr')
    user_pass = request.POST.get('user_pass')

    user_login.objects.create(
        
        user_name = user_name,
        user_email = user_email,
        user_phone = user_phone,
        user_addr = user_addr,
        user_pass = user_pass

        )
    return HttpResponse('0')




def home(request):
    if request.session.get('user_id'):
        # obj = Product.objects.all()
        obj = Product.objects.filter(trending = 1)
        obj1 = Product.objects.filter(status = 0 )
        ses_id = int(request.session['user_id']) 
        username = user_login.objects.get(id=ses_id).user_name
        view = cart.objects.filter(loged_user_id = ses_id)
        viewWish = wishlist.objects.filter(loged_user_id = ses_id)

        
        context  = {
            "obj":obj,
            "obj1":obj1,
            'user':username,
            'viewCart':view,
            'viewWish':viewWish,
            
        }
        return render(request, 'index.html', context)


@csrf_exempt
def signout(request):
    del request.session['user_id']
    return redirect('/')


def store(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id'])
        username = user_login.objects.get(id=ses_id).user_name
        view = cart.objects.filter(loged_user_id = ses_id)
        viewWish = wishlist.objects.filter(loged_user_id = ses_id)

        # prodCategory = category.objects.filter(trending = 1)
        prodCategory = category.objects.all()

        slug_list = Product.objects.filter(status = 0).distinct() 
        print(list(set(slug_list)))
        slug_items = []
        for i in prodCategory:
            if i is not slug_list:
                slug_items.append(i)
            
        context = {
            'category' : prodCategory,
            'slug_items':slug_list,
            'user':username,
            'viewCart':view,
            'viewWish':viewWish,
        }
        return render(request, 'store.html',context)

@csrf_exempt
def add_to_cart(request):
    if request.session.get('user_id'):
        id = int(request.session['user_id']) 
        user = user_login.objects.get(id= id).user_name
        prod_id = request.POST.get('prod_id')
        prod_qty = int(request.POST.get('prod_qty'))
        obj = Product.objects.get(id = prod_id)
        if (obj):
            if cart.objects.filter(loged_user_id = id, product_user_id = prod_id):
                return HttpResponse("Alerdy added")
            else:
                if (obj.quatity >= prod_qty ):
                    cart.objects.create(
                        loged_user_id = id,
                        product_user_id = prod_id,
                        product_qty = prod_qty
                        )
                    return HttpResponse("new added")
                else:
                    return HttpResponse("quatity high")
    else:
        return HttpResponse("1")

@csrf_exempt
def add_to_cart_home(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        prod_id = request.POST.get('item_id')
        prod_qty = int(request.POST.get('prod_qty'))
        obj = Product.objects.get(id = prod_id)
        if (obj):
            if cart.objects.filter(loged_user_id = ses_id, product_user_id = prod_id):
                return HttpResponse("Alerdy added")
            else:
                if (obj.quatity >= prod_qty ):
                    cart.objects.create(
                        loged_user_id = ses_id,
                        product_user_id = prod_id,
                        product_qty = prod_qty
                        )
                    return HttpResponse("added")
                else:
                    return HttpResponse("quatity high")
    else:
        return HttpResponse("1")



@csrf_exempt
def add_to_wishlist(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        prod_id = request.POST.get('item_id')
        obj = Product.objects.get(id = prod_id)
        if not wishlist.objects.filter(loged_user = ses_id, product_user_id = prod_id).exists():
            print(wishlist.objects.filter(loged_user_id = ses_id, product_user_id = prod_id))
            wishlist.objects.create(
                loged_user_id = ses_id, 
                product_user_id = prod_id
            )
            return HttpResponse("added")
        else:
            return HttpResponse("already add")
    return HttpResponse('1')
            

def removeWishlist(request, id):
    get_wish = request.POST.get(id)
    rem_wish = wishlist.objects.get(id=id).delete()
    return redirect("/home")

def removeCart(request, id):
    get_cart = request.POST.get(id)
    rem_cart = cart.objects.get(id=id).delete()
    return redirect("/home")


def hotDeals(request):
    if request.session.get('user_id'):
        
        obj = Product.objects.all()
        if (category.objects.filter()):
            context = {
                'listProd': obj
            }

            return render(request, 'hotDeals.html')



@csrf_exempt
def search_products(request):
    searchProd = request.POST.get('searchProd')
    obj = Product.objects.filter(name__icontains = searchProd) or Product.objects.filter(meta_keyword__icontains = searchProd) or Product.objects.filter(slug__icontains = searchProd)
    if (obj):
    
        print(obj)
        context = {
            'obj':obj
        }
        rendered = render_to_string('searched_product.html', context)
        return HttpResponse(rendered)
    else: 
        return HttpResponse("not")

    


def collections_view(request, slug):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        view = cart.objects.filter(loged_user_id = ses_id)
        viewWish = wishlist.objects.filter(loged_user_id = ses_id)
        obj = Product.objects.all()
        username = user_login.objects.get(id=ses_id).user_name
        view = cart.objects.filter(loged_user_id = ses_id)
        prodCategory = category.objects.filter(status = 0)
        if (category.objects.filter(slug=slug, status = 0)):
            products = Product.objects.filter(catergory__slug = slug)
            category_name = category.objects.filter(slug = slug).first()
            
            context = {
                'products':products ,
                'catergory_name':category_name,
                'category' : prodCategory,
                'user':username,
                'viewCart':view,
                'viewWish':viewWish,
            }
            return render(request, 'collectionsView.html', context)
        else :
                messages.warning(request, 'No items found you search')
                redirect('/store')


def about_Us(request):
    pass

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def add_new_cont(request):
    if request.session.get('user_id') :
        obj = Product.objects.all()
        if request.method == "POST":
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            msg = request.POST.get('msg')

            contactUs.objects.create(
                fname = fname,
                lname = lname,
                email = email,
                subject = subject,
                msg = msg
            )
            return HttpResponse('success')

@csrf_exempt
def product_view(request, id):
        if request.session.get('user_id'):
            ses_id = int(request.session['user_id'])
            username = user_login.objects.get(id=ses_id).user_name
            view = cart.objects.filter(loged_user_id = ses_id)
            viewWish = wishlist.objects.filter(loged_user_id = ses_id)
            obj = Product.objects.all()
            obj = Product.objects.filter(id=id)
            context = {
                'obj' : obj,
                'viewCart':view,
                'viewWish':viewWish,
                'user':username
            }

            return render(request, 'product.html',context)

def tracker(request):
    if request.session.get('user_id'):
            ses_id = int(request.session['user_id'])
            username = user_login.objects.get(id=ses_id).user_name
            view = cart.objects.filter(loged_user_id = ses_id)
            viewWish = wishlist.objects.filter(loged_user_id = ses_id)
            context = {
                'viewCart':view,
                'viewWish':viewWish,
                'user':username
            }
    return render(request, 'tracker.html', context)


@csrf_exempt
def track_product(request):
        if request.method == "POST":
            user_email = request.POST.get('user_email')
            track_no = request.POST.get('track_no')

            if not user_order.objects.filter(user_email=user_email, tracking_no=track_no).exists():
                return HttpResponse('not found')
            else:
                obj = user_order.objects.get(user_email=user_email, tracking_no=track_no)
                get_id = user_order.objects.all()
                ids = 0
                for i in get_id:
                    ids = i.id 
                obj1 = order_item.objects.filter(user_order_det_id = ids)
                for i in obj1:
                    print(i.user_product.name)
                    print(i.qty)
                    total_price = i.user_order_det.total_price
                context = {
                    'obj' : obj1,
                    'total_price':total_price
                }
                rendered = render_to_string('ordered_product.html', context)
                return HttpResponse(rendered)
                


def checkout(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        username = user_login.objects.get(id=ses_id).user_name
        obj = cart.objects.filter(loged_user_id = ses_id)
        view = cart.objects.filter(loged_user_id = ses_id)
        viewWish = wishlist.objects.filter(loged_user_id = ses_id)
        for i in obj:
            if i.product_qty > i.product_user.quatity:
                cart.objects.delete(loged_use_id =i.id)
        cartItems = cart.objects.filter(loged_user_id = ses_id)
        userProfile = profile.objects.filter(user_id = ses_id).first()
        total_price = 0
        for i in cartItems:
            total_price += i.product_user.selling_price * i.product_qty

        context = {
            'cartItems': cartItems,
            'total_price' : total_price,
            'userProfile':userProfile,
            'viewCart':view,
            'viewWish':viewWish,
            'user':username
        }
        return render(request, 'checkout.html', context)



def order_view(request):
    return HttpResponse("Payment Succesfully Proceeds ")



@csrf_exempt   
def order_details(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        if request.method == "POST":
            newOrder = user_order()
            newOrder.fname = request.POST.get('fname')
            newOrder.lname = request.POST.get('lname')
            newOrder.user_email = request.POST.get('user_email')
            newOrder.user_addr = request.POST.get('user_addr')
            newOrder.city = request.POST.get('city')
            newOrder.country = request.POST.get('country')
            newOrder.zipcode = request.POST.get('zipcode')
            
            newOrder.payment_mode = request.POST.get('payment_mode')
            cartOrder = cart.objects.filter(loged_user_id = ses_id)
            cart_total_price = 0
            for i in cartOrder:
                cart_total_price = cart_total_price + i.product_user.selling_price * i.product_qty

            newOrder.total_price = cart_total_price
            track_no = 'Ecom'+str(random.randint(111111111, 999999999))
            while user_order.objects.filter(tracking_no = track_no) is None:
                track_no = 'Ecom'+str(random.randint(111111111, 999999999))

            newOrder.tracking_no = track_no
            newOrder.save()

            for i in cartOrder:
                order_item.objects.create(
                    user_order_det_id = newOrder,
                    user_product = i.product_user,
                    price = i.product_user.selling_price ,
                    qty = i.product_qty
                )
            orderproduct = Product.objects.filter(id= i.product_user_id).first()
            orderproduct.quatity = orderproduct.quatity  - i.product_qty
            orderproduct.save()

            cartDetails = cart.objects.get(loged_user_id = ses_id).product_user
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            user_email = request.POST.get('user_emal')
            user_addr = request.POST.get('user_addr')
            city = request.POST.get('city')
            country = request.POST.get('country')
            zipcode = request.POST.get('zipcode')
            tracking_no = track_no
            content = {
                'fname':fname,
                'lname':lname,
                'user_email':user_email,
                'user_addr':user_addr,
                'city':city,
                'country':country,
                'zipcode':zipcode,
                'tracking_no':tracking_no,
                'cartDetails':cartDetails,
                'total':cart_total_price
            }
            html_File = render_to_string("email_template.html", content)
            text_content = strip_tags(html_File)
            to = "adityakothekar79@gmail.com"  

            email = EmailMultiAlternatives(
                "All Servicing Details",
                text_content,
                settings.EMAIL_HOST_USER,
                [to]
            )
            email.attach_alternative(html_File, "text/html")
            email.send()                                                            

            
            

            cartOrder.delete()
        return redirect('/home')
    

def payment(request, id):
    get_data = Product.objects.get(id=id)
    context = {
        'prod' : get_data,
    }
    return render(request, 'buy_product.html', context)

@csrf_exempt
def get_payment(request):
    if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        id = request.POST.get('id')
        if request.method == "POST":
            newOrder = user_order()
            newOrder.fname = request.POST.get('fname')
            newOrder.lname = request.POST.get('lname')
            newOrder.user_email = request.POST.get('user_email')
            newOrder.user_addr = request.POST.get('user_addr')
            newOrder.city = request.POST.get('city')
            newOrder.country = request.POST.get('country')
            newOrder.zipcode = request.POST.get('zipcode')
            newOrder.payment_mode = request.POST.get('payment_mode')
            newOrder.payment_id = request.POST.get('payment_id')


            obj1 = Product.objects.get(id= id)
            total = obj1.selling_price
            newOrder.total_price = total

            track_no = 'Ecom'+str(random.randint(111111111, 999999999))
            while user_order.objects.filter(tracking_no = track_no) is None:
                track_no = 'Ecom'+str(random.randint(111111111, 999999999))

            newOrder.tracking_no = track_no
            newOrder.save()

            # cart_prod = cart.objects.filter(loged_user_id = ses_id)
            cart_prod = Product.objects.filter(id= id)
            for i in cart_prod:
                order_item.objects.create(
                    user_order_det = newOrder,
                    user_product = obj1 ,
                    price = total,
                    qty = 1
                )
                break

            obj1.quatity = obj1.quatity - 1
            
            obj1.save()
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            user_email = request.POST.get('user_email')
            user_addr = request.POST.get('user_addr')
            city = request.POST.get('city')
            country = request.POST.get('country')
            zipcode = request.POST.get('zipcode')
            tracking_no = track_no
            content = {
                'fname':fname,
                'lname':lname,
                'user_email':user_email,
                'user_addr':user_addr,
                'city':city,
                'country':country,
                'zipcode':zipcode,
                'tracking_no':tracking_no,
                'order_details':obj1,
                'total':total
            }
            html_File = render_to_string("email_page_template.html", content)
            text_content = strip_tags(html_File)
            to = user_email 

            email = EmailMultiAlternatives(
                "ECOM-Express-12",
                text_content,
                settings.EMAIL_HOST_USER,
                [to]
            )
            email.attach_alternative(html_File, "text/html")
            email.send()
            return HttpResponse("0")
            
        return HttpResponse('done')
    
@csrf_exempt
def recived_pay(request):
    id = request.POST.get("id")
    get_price = Product.objects.get(id=id).selling_price
    context = {'get_price':get_price}
    return JsonResponse(context)


@csrf_exempt
def proceeds_to_pay(request):
     if request.session.get('user_id'):
        ses_id = int(request.session['user_id']) 
        obj = cart.objects.filter(loged_user_id = ses_id)
        total_price = 0
        for i in obj:
            total_price = total_price + i.product_user.selling_price * i.product_qty
        context = {
            'total_price':total_price
        }
        return JsonResponse(context)
            
