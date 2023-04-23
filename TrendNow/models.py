from django.db import models
import datetime
import os

# user : admin
# pass : 123

# Create your models here.

today = datetime.datetime.now()

def get_file_path(request, filename):
    orginal_file_name = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, orginal_file_name)
    return os.path.join('uploads/', filename)


class user_login(models.Model):
    user_name = models.CharField(max_length=100, null=False, blank=False)
    user_email = models.CharField(max_length=100, null=False, blank=False)
    user_phone = models.CharField(max_length=100, null=False, blank=False)    
    user_addr = models.CharField(max_length=100, null=False, blank=False)
    user_pass = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return  str(self.id) +" "+ self.user_name



class category(models.Model):
    slug = models.CharField( max_length=150,null=False,blank=False)
    name = models.CharField( max_length=150,null=False,blank=False)
    brand = models.CharField( max_length=150,null=True,blank=False)
    image = models.ImageField(upload_to=get_file_path,null= False, blank= False)
    description = models.TextField(max_length=500, null= False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    meta_title = models.CharField(max_length=150,null= True, blank= False)
    meta_keyword = models.CharField(max_length=150,null= True, blank= False)
    meta_description = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add =True)

    def  __str__(self):
        return self.name



class Product(models.Model):
    catergory = models.ForeignKey(category, on_delete=models.CASCADE,null=True)
    slug = models.CharField( max_length=150,null=True,blank=False)
    name = models.CharField( max_length=150,null=True,blank=False)
    brand = models.CharField( max_length=150,null=True,blank=False)
    product_image = models.ImageField(("Product Image"), upload_to=get_file_path,null= True, blank= False)
    small_description = models.CharField(max_length=250, null= True, blank=False)
    quatity = models.IntegerField(null=True, blank=False)
    description = models.TextField(max_length=500, null= True, blank=False)
    orignal_price = models.FloatField(null=True, blank=False)
    selling_price = models.FloatField(null=True, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField( max_length=150,null=True,blank=False)
    meta_title = models.CharField(max_length=150,null= True, blank= False)
    meta_keyword = models.CharField(max_length=150,null= True, blank= False)
    meta_description = models.TextField(max_length=500, null= True, blank=False)

    def  __str__(self):
        return self.name



class contactUs(models.Model):
    fname = models.CharField(("First name"), max_length=50)
    lname = models.CharField(("Last name"), max_length=50)
    email = models.CharField(("Email"), max_length=50)
    subject = models.CharField(("Subject"), max_length=500)
    msg = models.TextField(("message"), max_length=500)

    def  __str__(self):
        return self.fname + ' ' + self.lname



class cart(models.Model):
    loged_user = models.ForeignKey(user_login, on_delete=models.CASCADE, null=False, blank=False)
    product_user = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_qty = models.IntegerField(("Quantity"),null=True, blank=True, default= "1")
    created_d_t = models.DateTimeField(default=today)

    def __str__(self):
        return str(self.loged_user)

class wishlist(models.Model):
    loged_user = models.ForeignKey(user_login, on_delete=models.CASCADE, null=True, blank=False)
    product_user = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    created_d_t = models.DateTimeField(default=today,null=True, blank=True)

    def __str__(self):
        return str(self.loged_user)
    

class user_order(models.Model):
    loged_user = models.ForeignKey(user_login,verbose_name=("Login User Data "), on_delete=models.CASCADE, null=True, blank=False)
    fname = models.CharField(("First Name "), max_length=50, null=False, blank=False)
    lname = models.CharField(("Last Name "), max_length=50, null=False, blank=False)
    user_email = models.CharField(("Email "), max_length=500, null=False, blank=False)
    user_addr = models.CharField(("address"), max_length=500, null=False, blank=False)
    city = models.CharField(("City"), max_length=500, null=False, blank=False)
    country = models.CharField(("Country"), max_length=500, null=False, blank=False)
    zipcode = models.CharField(("Zip Code"), max_length=500, null=False, blank=False)
    telephone = models.CharField(("Telephone"), max_length=500, null=False, blank=False)
    total_price = models.FloatField(("Total Price"), max_length=5000, null= False, blank=False)
    payment_mode = models.CharField(("Payment Mode"), max_length=5000, null= False, blank=False)
    payment_id = models.CharField(("Payment ID"), max_length=5000, null=True)
    order_status = [
        ('Pending', 'pending'),
        ('Out of Shiping', 'out of shiping'),
        ('Completed', 'completed'),
    ]
    status = models.CharField(("Status"), choices=order_status, max_length=100, default='Pending', null= False, blank=False)
    message = models.TextField(("Message"), max_length=5000, null= False, blank=False)
    tracking_no = models.CharField(("Tracing NO"), max_length=5000, null= False, blank=False)
    created_dt = models.DateTimeField(("Created Date"), auto_now_add=True)
    update_dt = models.DateTimeField(("Update Date"), auto_now=True)

    def __str__(self):
        return (f'ID : {str(self.id)} -- Tracking No : {self.tracking_no}')

class order_item(models.Model):
    user_order_det = models.ForeignKey(user_order, verbose_name=("Order Items"), on_delete=models.CASCADE, null=True, blank=True)
    user_product = models.ForeignKey(Product, verbose_name=("Product Order"), on_delete=models.CASCADE)
    price = models.FloatField(("Price"), null=False)
    qty = models.IntegerField(("Quatity"), null=False, blank=True)

    def __str__(self):
        return (f' ID : {str(self.user_order_det.id)} -- Tracking No : {self.user_order_det.tracking_no}')
    
class profile(models.Model):
    user = models.OneToOneField(user_login, verbose_name=("User Data"), on_delete=models.CASCADE)
    address = models.TextField(("Address"), max_length=500, null=True, blank=True)
    city = models.CharField(("City"), max_length=50, null=True, blank=True)
    country = models.CharField(("Country"), max_length=50, null=True, blank=True)
    zipcode = models.CharField(("Zip Code"), max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=today,null=True, blank=True)

    def __str__(self):
        return self.user.user_name                                                                                                                                                                                                                       
