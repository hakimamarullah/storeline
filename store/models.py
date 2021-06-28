from django.db import models
from django.contrib.auth.models import User
from .rupiah import rupiah_format

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete= models.CASCADE)
	firstName = models.CharField(max_length=50, null=True)
	lastName = models.CharField(max_length=50, null=True)
	email = models.EmailField()
	phone = models.CharField(max_length=12)

	def __str__(self):
		return (f"{self.firstName} {self.lastName}").title()

	class Meta:
		db_table = "customer"

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	description = models.TextField(max_length=2000, null=True, blank=True)
	is_digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return f"{self.name}".title()

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = 'images/placeholder.png'
		return url
	@property
	def price_rupiah(self):
		return rupiah_format(int(str(self.price).split(".")[0]))
	

	class Meta:
		db_table = "product"

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return f"{str(self.id)}"

	@property
	def get_cart_total(self):
		orderItem = self.orderitem_set.all()
		total = sum([item.get_total for item in orderItem])
		return total

	@property
	def get_cart_items(self):
		orderItem = self.orderitem_set.all()
		return sum([item.quantity for item in orderItem])

	@property
	def get_cart_total_rupiah(self):
		return rupiah_format(int(str(self.get_cart_total).split(".")[0]))

	class Meta:
		db_table = "order"

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Product: {self.product} Quantity: {self.quantity}"

	@property
	def get_total(self):
		total = self.quantity * self.product.price
		return total

	@property
	def get_total_rupiah(self):
		return rupiah_format(int(str(self.get_total).split(".")[0]))


	class Meta:
		db_table = "order_item"

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=200)
	kelurahan = models.CharField(max_length=50)
	kecamatan = models.CharField(max_length=50)
	kabkot = models.CharField(max_length=50)
	provinsi = models.CharField(max_length=50)
	kode_pos = models.CharField(max_length=15)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{str(self.address).title()}"

	class Meta:
		db_table = "shipping_address"



