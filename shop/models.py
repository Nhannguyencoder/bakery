from django.db import models

#Tạo danh mục bánh
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    sale_price = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

#Tạo model đơn hàng   
class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('shipping', 'Đang giao'),
        ('done', 'Hoàn thành'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.name} - {self.phone}"
    def status_color(self):
        if self.status == 'pending':
            return "🟡 Chờ"
        elif self.status == 'shipping':
            return "🚚 Đang giao"
        return "✅ Hoàn thành"

#Lưu chi tiết sản phẩm trong đơn    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

