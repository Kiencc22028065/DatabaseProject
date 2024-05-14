import random
from django.shortcuts import render, redirect
from .forms import * 
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout




def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            else:
                customer = Customer.objects.get(email = user.email)
                
                # customer = Customer.objects.get(email = user.email)
                
                return redirect('homes', pk = customer.person_id)
        else:
            messages.error(request, "User not found !!!!!!")
            return redirect('login')
    else:    
        return render(request, 'login.html', {})
    



    
def log_out(request):
    logout(request)
    return redirect('login')


def add_to_favorite_from_cat(request, category, cus_id, prod_id):  
    prod = Product.objects.get(pro_id=prod_id)
    if prod.inFavList == False:
        prod.inFavList = True
        prod.save()
    return redirect('products_by_category', category = category, cus_id = cus_id,page= 1)

def add_to_favorite_from_all(request, cus_id, prod_id):
    prod = Product.objects.get(pro_id=prod_id)
    if prod.inFavList == False:
        prod.inFavList = True
        prod.save()
    return redirect('show_all_product', pk = cus_id, page  = 1)

def favorite_list(request, cus_id):
    customer = Customer.objects.get(person_id = cus_id)
    product = Product.objects.filter(inFavList = True)
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

    
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    return render(request, 'favoriteList.html', {'fav_count' : fav_count,'total' : total, 'num' : num, 'customer':customer, 'product':product})
    
def delete_from_favlist(request, cus_id, prod_id):
    prod = Product.objects.get(pro_id=prod_id)
    prod.inFavList = False
    prod.save()
    return redirect('favorite_list', cus_id = cus_id)



def products_by_category(request, category, cus_id, page):
    form = SearchForm(request.POST or None)
    # Truy vấn database để lấy các sản phẩm thuộc danh mục cụ thể
    category = Category.objects.get(cat_name = category)
    numPage = page - 1
    i = 0
    list = []
    for prod in category.get_product():
        if i >= numPage*9 and i < page*9:
            list.append(prod)

        i = i + 1

    customer = Customer.objects.get(person_id = cus_id)
    # Trả về trang web với danh sách sản phẩm tương ứng


    newestProduct = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30);")
    newestProduct1st = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3")
    newestProduct2nd = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3 offset 3;")
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0
    
    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    query = ""
    if request.method == 'POST':
        if form.is_valid():
            query = form.cleaned_data['query']
            product = Product.objects.filter(pro_name__icontains=query)

            context = {
                'total' : total,
                'num' : num,
                "form": form,
                'category': category, 
                'customer':customer,
                'query' : query,
                'product' : product,
                "newestProduct" : newestProduct,
                
                "newestProduct1st" : newestProduct1st,
                "newestProduct2nd" : newestProduct2nd,
                "fav_count" : fav_count
            }
            return render(request, 'sort_by_cart.html', context)
        else:
           form = SearchForm() 
    return render(request, 'sort_by_cart.html', {"fav_count" : fav_count, "total" : total, "num" : num, "list" : list, "form": form,'category': category,  'customer':customer, 'query' : query,  "newestProduct" : newestProduct, "newestProduct1st" : newestProduct1st, "newestProduct2nd" : newestProduct2nd})

def show_all_product(request, pk, page):
    form = SearchForm(request.POST or None)
    list = []
    # cate = ["Supplement", "Clothes", "Accessories"]
    # z = 0
    product = Product.objects.all()
    product_count = product.count()  # Count the number of products
    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    for ra in product:
        ra.overallRating = ra.overall()
        ra.save()
    for cpro in Category.objects.all():
        cat = cpro.cat_name
        prod = Product.objects.raw("SELECT * FROM `product` join category_cate_prod on product.pro_id = category_cate_prod.product_id join category on category_cate_prod.category_id = category.cat_id where cat_name = '{0}' order by product.quantitySold desc limit 3;".format(cat))
        list.append((prod, cat))
    numPage = (page - 1) * 9
    product = Product.objects.raw("SELECT * FROM product limit 9 offset {0} ".format(numPage))
    for apr in Product.objects.raw("select * from product WHERE DATEDIFF(NOW(), manufacturing_date) > (6 * 30)  and DATEDIFF(NOW(), manufacturing_date) < (9 * 30)"):
        apr.afterSalePrice = 0
        apr.save()
    #newestProduct = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30);")
    newestProduct = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30);")
    newestProduct1st = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3")
    newestProduct2nd = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3 offset 3;")
    onsaleProduct = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, product.quantityInStocks*product.buyPrice - product.quantitySold*product.sellPrice as loss from product WHERE DATEDIFF(NOW(), manufacturing_date) > (9 * 30) HAVING loss > 0 ")
    for pr in newestProduct:
        pr.afterSalePrice = pr.sellPrice - pr.sellPrice * 12 / 100
        pr.save()
    for pr in onsaleProduct:
        pr.afterSalePrice = pr.sellPrice - pr.sellPrice * 20 / 100
        pr.save()
    customer = Customer.objects.get(person_id = pk)



    order = Order.objects.filter(customer = customer, paymentReceive = False).first()
    total = 0
    num = 0
#    if create : 
    order_details = orderDetails.objects.filter(order = order)
    
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    #endif

    


    query = ""
    if request.method == 'POST':
        if form.is_valid():
            query = form.cleaned_data['query']
            product = Product.objects.filter(pro_name__icontains=query)
            context = {
                'fav_count' : fav_count,
                "onsaleProduct" : onsaleProduct,
                "customer" : customer,
                "form": form,
                "list" : list,
                "product" : product,
                "newestProduct" : newestProduct,
                "newestProduct2nd" : newestProduct2nd,
                "newestProduct1st" : newestProduct1st,
                "product_count" : product_count,
                'query' : query,
                'total' : total,
                'num' : num
                
            }
            return render(request, 'detail.html', context)
    else:
        form = SearchForm()
    context = {
            'fav_count' : fav_count,
            "onsaleProduct" : onsaleProduct,
            "customer" : customer,
            "form": form,
            "list" : list,
            "product" : product,
            "newestProduct" : newestProduct,
            "newestProduct2nd" : newestProduct2nd,
            "newestProduct1st" : newestProduct1st,
            "product_count" : product_count,
            'query' : query,
            'total' : total,
            'num' : num
        }
    return render(request, 'detail.html', context)

def homes(request, pk):
    form = SearchForm(request.POST or None)
    list = []
    # cate = ["Supplement", "Clothes", "Accessories"]
    # z = 0
    for cpro in Category.objects.all():
        cat = cpro.cat_name
        prod = Product.objects.raw("SELECT * FROM `product` join category_cate_prod on product.pro_id = category_cate_prod.product_id join category on category_cate_prod.category_id = category.cat_id where cat_name = '{0}' order by product.quantitySold desc limit 3;".format(cat))
        list.append((prod, cat))

    product = Product.objects.all()
    for apr in Product.objects.raw("select * from product WHERE DATEDIFF(NOW(), manufacturing_date) > (6 * 30)  and DATEDIFF(NOW(), manufacturing_date) < (9 * 30)"):
        apr.afterSalePrice = 0
        apr.save()

    #ORDER BY IF NEEDED
    newestProduct = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30);")
    newestProduct1st = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3")
    newestProduct2nd = Product.objects.raw("SELECT * FROM product WHERE DATEDIFF(NOW(), manufacturing_date) <= (6 * 30) limit 3 offset 3;")
     
    #ORDER BY IF NEEDED
    onsaleProduct = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, product.quantityInStocks*product.buyPrice - product.quantitySold*product.sellPrice as loss from product WHERE DATEDIFF(NOW(), manufacturing_date) > (9 * 30) HAVING loss > 0 ")
    onsaleProduct1st = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, product.quantityInStocks*product.buyPrice - product.quantitySold*product.sellPrice as loss from product WHERE DATEDIFF(NOW(), manufacturing_date) > (9 * 30) HAVING loss > 0 limit 3 ")
    onsaleProduct2nd = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, product.quantityInStocks*product.buyPrice - product.quantitySold*product.sellPrice as loss from product WHERE DATEDIFF(NOW(), manufacturing_date) > (9 * 30) HAVING loss > 0 limit 3 offset 3")

    #ORDER BY IF NEEDED
    topRatedProduct = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, overallRating as rated from product where overallRating != 0 order by overallRating desc")
    topRatedProduct1st = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, overallRating as rated from product where overallRating != 0 order by overallRating desc limit 3")
    topRatedProduct2nd = Product.objects.raw("select pro_id, pro_name,productImage, sellPrice, overallRating as rated from product where overallRating != 0 order by overallRating desc limit 3 offset 3")
    allCat = Category.objects.all()
   
    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

    for pr in newestProduct:
        pr.afterSalePrice = pr.sellPrice - pr.sellPrice * 12 / 100
        pr.save()
    for pr in onsaleProduct:
        pr.afterSalePrice = pr.sellPrice - pr.sellPrice * 20 / 100
        pr.save()
    customer = Customer.objects.get(person_id = pk)

    order = Order.objects.filter(customer = customer, paymentReceive = False).first()
    total = 0
    num = 0
#    if create : 
    order_details = orderDetails.objects.filter(order = order)
    
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    #endif
        
    query = ""
    if request.method == 'POST':
        if form.is_valid():
            query = form.cleaned_data['query']
            product = Product.objects.filter(pro_name__icontains=query)
            context = {
                "onsaleProduct" : onsaleProduct,
                "onsaleProduct1st" : onsaleProduct1st,
                "onsaleProduct2nd" : onsaleProduct2nd,
                "customer" : customer,
                "form": form,
                "list" : list,
                "allCat" : allCat,
                "product" : product,
                "newestProduct" : newestProduct,
                "newestProduct2nd" : newestProduct2nd,
                "newestProduct1st" : newestProduct1st,
                "fav_count" : fav_count,
                "topRatedProduct" : topRatedProduct,
                "topRatedProduct1st" : topRatedProduct1st,
                "topRatedProduct2nd" : topRatedProduct2nd,
                
                'query' : query,
                'total' : total,
                'num' : num
            }
            return render(request, 'home.html', context)
    else:
        form = SearchForm()
    context = {
            "onsaleProduct" : onsaleProduct,
            "onsaleProduct1st" : onsaleProduct1st,
            "onsaleProduct2nd" : onsaleProduct2nd,
            "customer" : customer,
            "fav_count" : fav_count,
            "form": form,
            "list" : list,
            "allCat" : allCat,
            "product" : product,
            "newestProduct" : newestProduct,
            "newestProduct2nd" : newestProduct2nd,
            "newestProduct1st" : newestProduct1st,

            "topRatedProduct" : topRatedProduct,
            "topRatedProduct1st" : topRatedProduct1st,
            "topRatedProduct2nd" : topRatedProduct2nd,

            'query' : query,
            'total' : total,
            'num' : num
        }
    return render(request, 'home.html', context)


def each_product(request, cus_id, prod_id):
    form = AmountOrdered(request.POST or None)
    prod = Product.objects.get(pro_id = prod_id)
    prod.pro_description = prod.pro_description.replace('\n', '<br>')
    image = Image.objects.filter(product = prod)
    review = CustomerReview.objects.filter(product = prod)
    
    # overall = 0
    # cnt = 0
    # for rate in review:
    #     overall += rate.rating
    #     cnt += 1
    # overall /= cnt
    # prod.overallRating = 
    customer = Customer.objects.get(person_id = cus_id)

    totalReview = 0
    list = Category.objects.filter(cate_prod = prod)


    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

    for rv in review:
        totalReview += 1

    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_order, created = Order.objects.get_or_create(customer=customer, paymentReceive = False)
    
            order_item, status = orderDetails.objects.get_or_create(product=prod,  order = user_order)

            order_item.amount += amount
            order_item.save()
            
            user_order.save()
            return redirect('each_product', cus_id = cus_id, prod_id = prod_id)
        
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
   # shop = Product.supplierShop.all()
    return render(request, 'eachProd.html', {'fav_count' : fav_count, 'total' : total, 'num' : num, 'form' : form, 'image' : image, 'prod' : prod, 'review' : review, 'customer' : customer, 'totalReview' : totalReview, 'list' : list})


def show_all_order(request, pk):
    customer = Customer.objects.get(person_id = pk)
    order = Order.objects.filter(customer = customer, paymentReceive = True)

    currentOrder = Order.objects.filter(customer = customer, paymentReceive = False).first()
    total = 0
    num = 0


    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
#    if create : 
    order_details = orderDetails.objects.filter(order = currentOrder)
    
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1

    return render(request, 'all_order.html', {'fav_count' : fav_count, 'total' : total, 'num' : num, 'order':order, 'customer':customer})

def each_order(request,cus_id, order_id):
    customer = Customer.objects.get(person_id = cus_id)
    order = Order.objects.get(order_id = order_id)
    
    order_details = orderDetails.objects.filter(order = order)
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details2 = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0
    

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

    for item in order_details2:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details2:
        num += 1
    

    return render(request, 'eachOrder.html', {'fav_count' : fav_count, 'total' : total, 'num':num,'order_details' : order_details, 'order':order, 'customer':customer})


from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('add_customer')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')




def add_customer(request):
    form = RawCustomerData(request.POST or None)
    customer = None#here is the issue
    temp = 71
    product = Product.objects.all()
    for prod in product:
        prod.inFavList = False
        prod.save()
    if request.method == 'POST':
        if form.is_valid():
            checkEmail = form.cleaned_data['email']
            if Customer.objects.filter(email = checkEmail):
                messages.info(request, 'This email has been registered')
                return render(request, 'customer.html', {'form' : form,  'customer' : customer})
            else:
                saverecord = form.save()
                temp = saverecord.person_id
                # customer = Customer.objects.get(person_id = saverecord.person_id)
                username = saverecord.username
                email = saverecord.email
                password = saverecord.password
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_active=False
                user.save()
               # send_otp(request)
                activateEmail(request, user, email)

                #return render(request, 'customer.html',{'form' : form, 'customer' : customer})
                return redirect('login')
    customer = Customer.objects.get(person_id = temp)
    return render(request, 'customer.html', {'form' : form,  'customer' : customer})
        

def add_to_order(request, cus_id, pk):
    customer = Customer.objects.get(person_id = cus_id)
    product = Product.objects.get(pro_id=pk)
   
    user_order, created = Order.objects.get_or_create(customer=customer, paymentReceive = False)
    
    order_item, status = orderDetails.objects.get_or_create(product=product, order = user_order)

    # if created:
    #     orderDetails.objects.update(amount = 0)
    #     order_item.amount -= order_item.amount
    order_item.amount += 1
    order_item.save()
    #user_order.items.add(order_item)
    
    user_order.save()
    return redirect('show_all_product', pk = cus_id, page = 1)

def delete_from_cart(request, cus_id, pk):
    item_to_delete = orderDetails.objects.filter(detail_id=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect('order_details', cus_id = cus_id)

def order_details(request, cus_id):
    customer = Customer.objects.get(person_id = cus_id)
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1

    context = {
        'existing_order': existing_order,
        'customer': customer,
        'order_details' : order_details,
        'total' : total,
        'num' : num,
        'fav_count': fav_count
    }
    return render(request, 'order_summary.html', context)


from django.conf import settings
from twilio.rest import Client

def send_otp_via_sms(recipient_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_body = f"Your OTP is: {otp}"
    
    try:
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return True
    except Exception as e:
        print(e)
        return False
    
def send_otp(request):
    if request.method == 'POST':
        # recipient_number = request.POST.get('recipient_number')

        # otp = generate_otp()
        if send_otp_via_sms('+84375812092', "123456"):
            print(1)
            # request.session['otp'] = otp
            return redirect("add_customer")
        else:
            return redirect("add_customer")




def bank(request, cus_id):
    customer = Customer.objects.get(person_id=cus_id)
    newbalance = credit.objects.filter(owner=customer).first()

    ######## self add
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1

 
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
  

    #########

    if not newbalance:
        form = BankAcc(request.POST or None)  
    else:
        form = Deposit(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            saverec = form.save(commit=False)  # Không lưu ngay vào cơ sở dữ liệu
            #newbalance = credit.objects.filter(owner=customer).first()
            if not newbalance:
                newbalance = credit(creditNumber = saverec.creditNumber, owner=customer, balance=saverec.balance)
                newbalance.save()
            else:
                newbalance.balance += saverec.balance
                newbalance.save()
                
            
            return redirect('bank', cus_id=cus_id)
        
    return render(request, 'bank_account.html', {'fav_count' : fav_count, 'form': form, 'customer': customer, 'newbalance' : newbalance, 'num' : num,'total' : total})
    

def check_out(request, cus_id, order_id):
    customer = Customer.objects.get(person_id = cus_id)
    order = Order.objects.get(order_id = order_id)
    order_details = orderDetails.objects.filter(order = order)


    total = 0
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice
    #Nếu khách hàng chưa tạo bank mà đã checkout thì sẽ lỗi
    try:
        bank = credit.objects.get(owner = customer)
    except credit.DoesNotExist:
        messages.info(request, 'You do not have a bank account')
        return redirect('order_details',cus_id = cus_id)
    
    payment = Transaction.objects.create(customer = customer, order = order)
    all_shippers = Shipper.objects.all()
    order_total = total
    if bank.balance < order_total:
        messages.error(request,'Not enough balance')
        return redirect('order_details',cus_id = cus_id)
    #Trừ tiền vào bank account
    bank.balance -= order_total
    bank.save()
    #Transaction đã trả thành công và lưu tổng tiền
    payment.success = True
    payment.totalAmount = order_total
    payment.save()



    #res = 0
    # previous_order_items = order.items.all()
    for item in order_details:
         #res = res * 10 + item.amount
         item.product.quantitySold += item.amount
         item.product.save()
    #Lưu biến amount của từng item thành 1 dãy để sau chuyển thành từng số 1
    
    #order.am = res
    
    #Chọn ngẫu nhiên 1 shipper trong list và gán shipper vào đơn hàng
    random_shipper = random.choice(all_shippers)
    order.shipper = random_shipper
    #Lưu tổng tiền và đã thanh toán chưa
    order.totalAmount = order_total
    order.paymentReceive = True

    order.shippingStatus = "In Transit"
    for it in Product.objects.all():
            if it.quantityInStocks * it.buyPrice - it.quantitySold * it.sellPrice <= 0:
                it.afterSalePrice = 0
                it.save()
    order.save()

    messages.info(request, "Payment success!")
    return redirect('show_all_product', pk = cus_id, page = 1)


def ship(request,cus_id, prod_id):
    customer = Customer.objects.get(person_id = cus_id)
    product = Product.objects.get(pro_id=prod_id)
    form = Review(request.POST or None)
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    if request.method == 'POST':
        if form.is_valid():
            saverecord = form.save()
            saverecord.product = product
            saverecord.customer = customer
            saverecord.save()
            #return render(request, 'customer.html',{'form' : form, 'customer' : customer})
            return redirect('show_all_product', pk = cus_id, page = 1)
    return render(request, 'review.html', {'fav_count' : fav_count, 'total' : total, 'num' : num, 'form' : form,  'customer' : customer, 'product': product})


def mark_as_shipped(request, cus_id, order_id):
    order = Order.objects.get(order_id=order_id)
    customer = Customer.objects.get(person_id = cus_id)
    order.shippingStatus = "Shipped"
    order.save()
    return redirect('each_order', cus_id = cus_id, order_id = order_id)

from django.db import connection

months = ['0', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def show_revenue(request, cus_id):
    # with connection.cursor() as cursor:
    #     cursor.execute("select sum(transaction.totalAmount) as revenue from transaction;")
    customer = Customer.objects.get(person_id = cus_id)
    revenue = Transaction.objects.raw("select transaction_id, (select sum(transaction.totalAmount) from transaction) as revenue from transaction where transaction_id = 1")
    list = []
    for i in range (1, 13):
        rev = Transaction.objects.raw("select transaction_id, (select sum(transaction.totalAmount) as revenue from transaction where month(transaction.payDate) = {0}) as revenue from transaction limit 1".format(i))
        
        list.append((rev, months[i]))
    
    best = Transaction.objects.raw("select transaction_id, month(transaction.payDate) as month, (select sum(transaction.totalAmount) as revenue from transaction group by month(transaction.payDate) order by revenue desc limit 1) as best from transaction where transaction_id = 1")
    bestProd = Product.objects.raw("select pro_id, pro_name, quantitySold from product order by quantitySold desc limit 1")
    
    cost = 0
    for item in Product.objects.all():
        cost += item.cost()
    #profit = Transaction.objects.raw("select transaction_id, sum(transaction.totalAmount) - {0} as profit from transaction ".format(cost))
    profit = Transaction.objects.raw("select transaction_id, (select sum(transaction.totalAmount) - {0} as profit from transaction) as profit from transaction limit 1".format(cost))
    bestCustomer = Transaction.objects.raw("SELECT t.transaction_id,t.customer_id AS id,c.personName AS name,subquery.id AS best_customer_id,subquery.name AS best_customer_name,subquery.bestCustomer AS best_customer_amount FROM transaction t INNER JOIN customer c ON c.person_id = t.customer_id INNER JOIN ( SELECT t2.customer_id AS id,c2.personName AS name,SUM(t2.totalAmount) AS bestCustomer FROM transaction t2 RIGHT JOIN customer c2 ON c2.person_id = t2.customer_id GROUP BY c2.person_id ORDER BY bestCustomer DESC LIMIT 1) AS subquery ON subquery.id = t.customer_id limit 1")

    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    jun = 0
    jul = 0
    aug = 0
    sep = 0
    oct = 0
    nov = 0
    dec = 0
    for pr in list[0][0]:
        jan = pr.revenue

    for pr in list[1][0]:
        feb = pr.revenue

    for pr in list[2][0]:
        mar = pr.revenue

    for pr in list[3][0]:
        apr = pr.revenue

    for pr in list[4][0]:
        may = pr.revenue

    for pr in list[5][0]:
        jun = pr.revenue

    for pr in list[6][0]:
        jul = pr.revenue

    for pr in list[7][0]:
        aug = pr.revenue

    for pr in list[8][0]:
        sep = pr.revenue

    for pr in list[9][0]:
        oct = pr.revenue

    for pr in list[10][0]:
        nov = pr.revenue

    for pr in list[11][0]:
        dec = pr.revenue
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    context = {

        'total' : total,
        'fav_count' : fav_count,
        'num' : num,
        'revenue': revenue, 
        'customer': customer, 
        'list' : list,
        'best' : best,
        'bestProd':bestProd,
        'profit' : profit,
        'bestCustomer': bestCustomer,
        'jan' : jan,
        'feb' : feb,
        'mar' : mar,
        'apr': apr,
        'may' : may,
        'jun' : jun,
        'jul' : jul,
        'aug' : aug,
        'sep' : sep,
        'oct' : oct,
        'nov' : nov,
        'dec' : dec
        }
    
    return render(request, 'revenue.html', context)

def bar_chart_view(request):
    # Your data (example)
    data = [10, 20, 30, 40, 50]  # Sample data (replace this with your data)
    labels = ['A', 'B', 'C', 'D', 'E']  # Sample labels (replace this with your labels)

    context = {
        'data': data,
        'labels': labels,
    }
    return render(request, 'your_template.html', context)




def contact(request, cus_id):
    customer = Customer.objects.get(person_id = cus_id)
    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1


    return render(request, 'contact.html', {'customer' : customer ,  'total' : total, 'fav_count' : fav_count, 'num' : num})

from .forms import DocumentForm
import mammoth
bootstrap_css = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
bootstrap_js = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>'
custom_styles = """ 
                    u => u.initialism
                    p[style-name='Heading 1'] => h1.card
                    table => table.table.table-hover
                    
                    """

def convert_docx_to_html(docx_file):
    result = mammoth.convert_to_html('media/' + docx_file, style_map = custom_styles)
    html_content = result.value
    return bootstrap_css + html_content + bootstrap_js

def each_blog(request, cus_id, post_id):
    blog = BlogPost.objects.get(postID = post_id)
    customer = Customer.objects.get(person_id = cus_id)
    html_content = convert_docx_to_html(str(blog.file))

    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)
    other_blog = BlogPost.objects.filter(tag = blog.tag)

    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1
    return render(request, 'each_blog.html', {'other_blog' : other_blog,'customer' : customer, 'blog' : blog, 'html_content': html_content, 'total' : total, 'num' : num, 'fav_count' : fav_count})

def blog(request, cus_id):
    blog = BlogPost.objects.all()
    customer = Customer.objects.get(person_id = cus_id)
   

    existing_order = Order.objects.filter(customer=customer, paymentReceive = False).first()
    order_details = orderDetails.objects.filter(order = existing_order)

    recent_blog = BlogPost.objects.raw("select * from blog order by written_at desc limit 3")

    tag = BlogTag.objects.all()

    total = 0
    num = 0

    fav_count = 0
    for prod in Product.objects.filter(inFavList = True):
        fav_count = fav_count + 1
    
    for item in order_details:
        if item.product.afterSalePrice == 0:
            total += item.amount * item.product.sellPrice
        else :
            total += item.amount * item.product.afterSalePrice

    for item in order_details:
        num += 1

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newBlog = BlogPost.objects.create()
            #uploaded_file = request.FILES['docfile']
            
            newBlog.header = request.POST['header']
            # Xử lý file tải lên
            newBlog.titleImage = form.cleaned_data['titlePhoto']
            newBlog.file = request.FILES['docfile']
            newBlog.author = request.POST['author']
            
            #newBlog.content = convert_docx_to_html(uploaded_file)
            newBlog.save()
            #html_content = convert_docx_to_html(str(uploaded_file))
            return redirect('blog', cus_id = cus_id)
    else:
        form = DocumentForm()

    return render(request, 'blog.html', {' recent_blog' :  recent_blog, 'tag' : tag, 'customer' : customer, 'form': form, 'blog' : blog, 'total' : total, 'num' : num, 'fav_count' : fav_count})


def blog_by_tag(request, cus_id, tag_name):
    tag = BlogTag.objects.get(tagName = tag_name)
    blog = BlogPost.objects.filter(tag = tag)
    customer = Customer.objects.get(person_id = cus_id)
    return render(request, 'blog_by_tag.html', {'customer':customer, 'blog' : blog})