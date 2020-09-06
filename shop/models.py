from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    cutprice = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    you_save = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    image2 = models.ImageField(upload_to="shop/images", default="", blank=True)
    image3 = models.ImageField(upload_to="shop/images", default="", blank=True)
    image4 = models.ImageField(upload_to="shop/images", default="", blank=True)
    image5 = models.ImageField(upload_to="shop/images", default="", blank=True)
    Number_of_images = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    revid = models.IntegerField(default=0)
    name = models.CharField(max_length=500, default="")
    email = models.CharField(max_length=50)
    rating = models.IntegerField()
    review = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'review_id: {}, email: {}'.format(self.review_id, str(self.email))


class CurrentUser(models.Model):
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")

    def __str__(self):
        return 'email: {}, password: {}'.format(self.email, self.password)


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=30, default="")
    password = models.CharField(max_length=50, default="")

    def __str__(self):
        return 'id: {}, email: {}, pass: {}'.format(self.id, str(self.email), self.password)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    itemsJson = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=500, default="")
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    landmark = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=12, default="")
    p_name1 = models.CharField(max_length=50, default="")
    p_id1 = models.CharField(max_length=50, default="")
    p_quantity1 = models.CharField(max_length=50, default="")
    p_name2 = models.CharField(max_length=50, default="", blank=True)
    p_id2 = models.CharField(max_length=50, default="", blank=True)
    p_quantity2 = models.CharField(max_length=50, default="", blank=True)
    p_name3 = models.CharField(max_length=50, default="", blank=True)
    p_id3 = models.CharField(max_length=50, default="", blank=True)
    p_quantity3 = models.CharField(max_length=50, default="", blank=True)
    p_name4 = models.CharField(max_length=50, default="", blank=True)
    p_id4 = models.CharField(max_length=50, default="", blank=True)
    p_quantity4 = models.CharField(max_length=50, default="", blank=True)
    p_name5 = models.CharField(max_length=50, default="", blank=True)
    p_id5 = models.CharField(max_length=50, default="", blank=True)
    p_quantity5 = models.CharField(max_length=50, default="", blank=True)
    p_name6 = models.CharField(max_length=50, default="", blank=True)
    p_id6 = models.CharField(max_length=50, default="", blank=True)
    p_quantity6 = models.CharField(max_length=50, default="", blank=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'order_id: {}, email: {}'.format(self.order_id, str(self.email))


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Order ID: {}, Desc: {}'.format(self.order_id, self.update_desc[0:15] + "...")
