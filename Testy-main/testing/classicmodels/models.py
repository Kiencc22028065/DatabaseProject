from django.db import models
from datetime import date, timedelta

Gender = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )

# Create your models here.

class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=30, null=True,blank=True)
    shop_address = models.CharField(max_length=256)
    shop_phone = models.CharField(max_length=16, blank=True)

    class Meta:
        db_table = 'Shop'

    def __str__(self):
        return self.shop_name



class Product(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_name = models.CharField(max_length=200)
    pro_description = models.TextField()
    quantityInStocks = models.IntegerField()
    quantitySold = models.IntegerField(default=0)
    buyPrice = models.DecimalField(max_digits=50, decimal_places=0)
    sellPrice = models.DecimalField(max_digits=50, decimal_places=0)
    afterSalePrice  = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    manufacturing_date = models.DateTimeField(auto_now_add=True)
    supplierShop = models.ManyToManyField(Shop)
    productImage = models.ImageField(null=True, blank=True, upload_to="images/")
    #overallRating = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    overallRating = models.IntegerField(default=0)



    pro_quick_description = models.TextField(default="")
    pro_info = models.TextField(default="")
    pro_weight = models.DecimalField(default=0, max_digits=2, decimal_places=1)



    def roundy():
        
        return round(overallRating)

    def get_shop(self):
        return self.supplierShop.all()
    
    def overall(self):
        review = CustomerReview.objects.filter(product = self)
        overall = 0
        cnt = 0
        if review:
            for rate in review:
                overall += rate.rating
                cnt += 1
            overall /= cnt
        
        return overall
    
    def count_fav_item(self):
        prod = self.objects.filter(inFavList = True)
        i = 0
        for pr in prod:
            i = i + 1
        return i

    class Meta:
        db_table = 'Product'

    # def sale_or_not(self):
    #     if self.quantityInStocks * self.buyPrice - self.quantitySold * self.sellPrice > 0:
    #         self.afterSalePrice = self.sellPrice - self.sellPrice * 20 / 100
    #     else:
    #         self.afterSalePrice = 0
    #     return self.afterSalePrice
    def cost(self):
        return self.quantityInStocks * self.buyPrice
        

    def __str__(self):
        return self.pro_name
    
    
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=40)
    cate_prod = models.ManyToManyField(Product)
    description = models.TextField()
    catImg = models.ImageField(null=True, blank=True, upload_to="images/")

    class Meta:
        db_table = 'Category'


    def get_product(self):
        return self.cate_prod.all()
    
    def counting(self):
        prod = self.cate_prod.all()
        return prod.count()

    def __str__(self):
        return self.cat_name

from django.contrib.auth.models import User
class Customer(models.Model):
    person_id = models.AutoField(primary_key=True)
    personName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=32)
    gender = models.CharField(choices=Gender, max_length=30)
    cusAddress = models.CharField(max_length=256)
    email = models.EmailField(blank=True)
    postCode = models.CharField(max_length=30, null=True,blank=True)
    username = models.CharField(max_length=32, default="")
    password = models.CharField(max_length=100, default="")

    class Meta: 
        db_table = 'Customer'

    def __str__(self):
        return self.personName

class Shipper(models.Model):
    person_id = models.AutoField(primary_key=True)
    personName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=32)
    gender = models.CharField(choices=Gender, max_length=30)
    license_plate = models.CharField(max_length=40)
    workplace = models.CharField(max_length=50, null=True,blank=True)


    class Meta:
        db_table = 'Shipper' 


    def __str__(self):
        return self.personName





ShippingStatus = (
        ("Haven't Ordered", "Haven't Ordered"),
        ("In Transit", "In Transit"),
        ("Shipped", "Shipped")
    )
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    dateOrdered = models.DateTimeField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=50,decimal_places=0, default= 0)
    paymentReceive = models.BooleanField(default=False)
    shippingStatus = models.CharField(choices=ShippingStatus,max_length=50, default = "Haven't Ordered")
    shipper = models.ForeignKey(Shipper, null=True,on_delete=models.SET_NULL)

    class Meta:
        db_table =  'Order'

    # def get_order_items(self):
    #     return self.items.all()

    # def get_am(self):
    #     temp = self.am % 10
    #     self.am = self.am // 10
    #     return temp

    # def get_total(self):
    #     sum = 0
    #     for item in self.items.all():
    #         if item.product.afterSalePrice == 0:
    #             sum += item.amount * item.product.sellPrice
    #         else :
    #             sum += item.amount * item.product.afterSalePrice
    #     return sum

    def __str__(self):
        return self.customer.personName + str(self.order_id)

class orderDetails(models.Model):
    detail_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.SmallIntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    

    class Meta:
        db_table =  'OrderDetails'

    def get_pro_id(self):
        return self.product.pro_id
    
    def get_amount(self):
        return self.amount * self.product.sellPrice
    
    def get_amountAf(self):
        return self.amount * self.product.afterSalePrice

    def __str__(self):
        return self.product.pro_name


class FavoriteList(models.Model):
    list_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, null=True,on_delete=models.SET_NULL)

    class Meta:
        db_table =  'FavoriteList'

    def __str__(self):
        return self.customer.personName + " favorite list"

class FavoriteItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    favoriteList = models.ForeignKey(FavoriteList, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table =  'FavoriteItem'

    def __str__(self):
        return self.product.pro_name
    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    order = models.OneToOneField(Order,null=True, on_delete=models.SET_NULL)
    totalAmount = models.DecimalField(max_digits=50,decimal_places=0, default= 0)
    success = models.BooleanField(default=False)
    payDate = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table =  'Transaction'

    def __str__(self):
        return self.customer.personName + " payment"


class credit(models.Model):
    creditNumber = models.CharField(max_length=20,primary_key=True, default="",blank=True)
    owner = models.OneToOneField(Customer, null=True,on_delete=models.SET_NULL)
    balance = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    class Meta:
        db_table =  'Credit'

    def __str__(self):
        return self.owner.personName
RatingChoice = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class CustomerReview(models.Model):
    reviewID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    rating = models.SmallIntegerField(choices=RatingChoice, default=0)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    class Meta:
        db_table =  'CustomerReview'

    def get_person(self):
        return self.customer.person_id

    def __str__(self):
        return self.product.pro_name


    
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.pro_name
    


class BlogTag(models.Model):
    tagID = models.AutoField(primary_key=True)
    tagName = models.CharField(max_length=40)

    class Meta:
        db_table = 'Blog_Tag'

    def __str__(self):
        return self.tagName


class BlogPost(models.Model):
    postID = models.AutoField(primary_key=True)
    titleImage = models.ImageField(upload_to='post/', null = True, blank=True)
    file = models.FileField(upload_to='blog/') 
    header = models.CharField(max_length=200) 
    author = models.CharField(max_length=80)
    written_at = models.DateField(auto_now_add=True)
    tag = models.ForeignKey(BlogTag,null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table =  'Blog'

    def __str__(self):
        return self.header

