from django.db import models
from django.contrib.auth.models import User
from .rupiah import rupiah_format

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete= models.CASCADE)
	firstName = models.CharField(max_length=50, null=True)
	lastName = models.CharField(max_length=50, null=True)
	email = models.EmailField()
	phone = models.CharField(max_length=12, null=True, blank=True)

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

	@property
	def is_digital_category(self):
		return "Non-Digital" if not self.is_digital else "Digital"
	

	class Meta:
		db_table = "product"

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
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

	@property
	def shipping(self):
		is_shipping = False
		shipping = []
		for item in self.orderitem_set.all():
			shipping.append(False) if item.product.is_digital else shipping.append(True)
		for ship in shipping:
			is_shipping = is_shipping or ship
		return is_shipping

	class Meta:
		db_table = "order"

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
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

class CustomerAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	address = models.CharField(max_length=200, null=True)
	kelurahan = models.CharField(max_length=50, null=True)
	kecamatan = models.CharField(max_length=50, null=True)
	kabkot = models.CharField(max_length=50, null=True)
	provinsi = models.CharField(max_length=50, null=True)
	kode_pos = models.CharField(max_length=15, null=True)
	date_added = models.DateTimeField(auto_now_add=True, null=True)
	is_default = models.BooleanField(default=False, null=True)

	def __str__(self):
		return f"{str(self.address).title()}"

	@property
	def is_default_address(self):
		return "" if not self.is_default else "Default"

	class Meta:
		db_table = "customer_address"

class ShippingAddress(models.Model):
	customer_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return f"{str(self.customer_address.address).title()}"

	class Meta:
		db_table = "shipping_address"
		verbose_name_plural="ShippingAddresses"

class Pesanan(models.Model):
	CHOICES =(
		("PRO","On Process"),
		("PND","Pending"),
		("COM","Complete"),
		("CNC","Canceled"),
	)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	shipping = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True)
	status = models.CharField(max_length=15, choices=CHOICES, default="PND")
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Name: {str(self.customer.firstName).title()} ID: {self.customer.id}"

	class Meta:
		db_table = "pesanan"
		verbose_name_plural = "pesanan"



