from datetime import datetime, timedelta
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class Product:
    def __init__(self, product_id, name, category, price, min_stock_level=10, supplier=""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.min_stock_level = min_stock_level  # Reorder threshold
        self.supplier = supplier
        self.current_stock = 0
        self.reserved_stock = 0  # Stock reserved for pending orders
        self.created_date = datetime.now()
        self.last_restocked = None
        self.total_sold = 0
    
    @property
    def available_stock(self):
        """Stock available for new orders (current - reserved)"""
        return self.current_stock - self.reserved_stock
    
    def is_low_stock(self):
        """Check if current stock is below minimum level"""
        return self.current_stock <= self.min_stock_level
    
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.current_stock <= 0
    
    def add_stock(self, quantity, cost_per_unit=None):
        """Add stock to inventory"""
        if quantity > 0:
            self.current_stock += quantity
            self.last_restocked = datetime.now()
            print(f"Added {quantity} units of {self.name}. New stock: {self.current_stock}")
            if cost_per_unit:
                print(f"Total restock cost: ${cost_per_unit * quantity:.2f}")
        else:
            print("Quantity must be positive")
    
    def reserve_stock(self, quantity):
        """Reserve stock for an order"""
        if quantity <= self.available_stock:
            self.reserved_stock += quantity
            return True
        return False
    
    def release_reserved_stock(self, quantity):
        """Release reserved stock (order cancelled)"""
        if quantity <= self.reserved_stock:
            self.reserved_stock -= quantity
    
    def fulfill_order(self, quantity):
        """Fulfill an order (remove from both current and reserved stock)"""
        if quantity <= self.reserved_stock and quantity <= self.current_stock:
            self.current_stock -= quantity
            self.reserved_stock -= quantity
            self.total_sold += quantity
            return True
        return False
    
    def get_stock_info(self):
        """Get detailed stock information"""
        status = "OUT OF STOCK" if self.is_out_of_stock() else "LOW STOCK" if self.is_low_stock() else "IN STOCK"
        return {
            'product_id': self.product_id,
            'name': self.name,
            'current_stock': self.current_stock,
            'reserved_stock': self.reserved_stock,
            'available_stock': self.available_stock,
            'min_stock_level': self.min_stock_level,
            'status': status,
            'total_sold': self.total_sold
        }
    
    def __str__(self):
        return f"{self.name} (ID: {self.product_id}) - Stock: {self.current_stock}, Available: {self.available_stock}"

