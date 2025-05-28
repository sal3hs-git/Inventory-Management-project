
class Inventory:
    def __init__(self, business_name=""):
        self.business_name = business_name
        self.products = {}  # {product_id: Product}
        self.low_stock_alerts = []
        self.reorder_history = []
    
    def add_product(self, product):
        """Add a new product to inventory"""
        if isinstance(product, Product):
            self.products[product.product_id] = product
            print(f"Added product: {product.name} to inventory")
        else:
            print("Invalid product object")
    
    def remove_product(self, product_id):
        """Remove a product from inventory"""
        if product_id in self.products:
            product = self.products.pop(product_id)
            print(f"Removed product: {product.name} from inventory")
        else:
            print(f"Product ID {product_id} not found")
    
    def get_product(self, product_id):
        """Get a product by ID"""
        return self.products.get(product_id)
    
    def search_products(self, search_term="", category=""):
        """Search products by name or category"""
        results = []
        for product in self.products.values():
            if (search_term.lower() in product.name.lower() and 
                (not category or category.lower() == product.category.lower())):
                results.append(product)
        return results
    
    def restock_product(self, product_id, quantity, cost_per_unit=None):
        """Restock a specific product"""
        if product_id in self.products:
            product = self.products[product_id]
            product.add_stock(quantity, cost_per_unit)
            # Remove from low stock alerts if restocked above minimum
            if not product.is_low_stock() and product_id in [alert['product_id'] for alert in self.low_stock_alerts]:
                self.low_stock_alerts = [alert for alert in self.low_stock_alerts if alert['product_id'] != product_id]
            
            # Record restock history
            self.reorder_history.append({
                'product_id': product_id,
                'product_name': product.name,
                'quantity': quantity,
                'cost_per_unit': cost_per_unit,
                'total_cost': cost_per_unit * quantity if cost_per_unit else None,
                'date': datetime.now()
            })
        else:
            print(f"Product ID {product_id} not found")
    
    def check_low_stock(self):
        """Check for low stock items and generate alerts"""
        self.low_stock_alerts = []
        for product in self.products.values():
            if product.is_low_stock():
                alert = {
                    'product_id': product.product_id,
                    'product_name': product.name,
                    'current_stock': product.current_stock,
                    'min_stock_level': product.min_stock_level,
                    'supplier': product.supplier,
                    'alert_date': datetime.now()
                }
                self.low_stock_alerts.append(alert)
        return self.low_stock_alerts
    
    def get_inventory_value(self):
        """Calculate total inventory value"""
        total_value = sum(product.current_stock * product.price for product in self.products.values())
        return total_value
    
    def get_categories(self):
        """Get all unique product categories"""
        return list(set(product.category for product in self.products.values()))
    
    def generate_inventory_report(self):
        """Generate comprehensive inventory report"""
        if not self.products:
            return "No products in inventory"
        
        report = f"\n{'='*60}\n"
        report += f"INVENTORY REPORT - {self.business_name}\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"{'='*60}\n\n"
        
        # Summary statistics
        total_products = len(self.products)
        total_stock_units = sum(p.current_stock for p in self.products.values())
        total_value = self.get_inventory_value()
        low_stock_count = len([p for p in self.products.values() if p.is_low_stock()])
        out_of_stock_count = len([p for p in self.products.values() if p.is_out_of_stock()])
        
        report += f"SUMMARY:\n"
        report += f"  Total Products: {total_products}\n"
        report += f"  Total Stock Units: {total_stock_units:,}\n"
        report += f"  Total Inventory Value: ${total_value:,.2f}\n"
        report += f"  Low Stock Items: {low_stock_count}\n"
        report += f"  Out of Stock Items: {out_of_stock_count}\n\n"
        
        # Category breakdown
        categories = self.get_categories()
        if categories:
            report += f"CATEGORY BREAKDOWN:\n"
            for category in sorted(categories):
                cat_products = [p for p in self.products.values() if p.category == category]
                cat_value = sum(p.current_stock * p.price for p in cat_products)
                report += f"  {category}: {len(cat_products)} products, ${cat_value:,.2f} value\n"
            report += "\n"
        
        # Low stock alerts
        low_stock_items = self.check_low_stock()
        if low_stock_items:
            report += f"LOW STOCK ALERTS:\n"
            for alert in low_stock_items:
                report += f"   {alert['product_name']} (ID: {alert['product_id']})\n"
                report += f"     Current: {alert['current_stock']}, Min: {alert['min_stock_level']}\n"
                if alert['supplier']:
                    report += f"     Supplier: {alert['supplier']}\n"
            report += "\n"
        
        # Detailed product list
        report += f"DETAILED PRODUCT LIST:\n"
        report += f"{'ID':<8} {'Name':<25} {'Category':<15} {'Stock':<8} {'Available':<10} {'Price':<10} {'Value':<12} {'Status':<12}\n"
        report += "-" * 110 + "\n"
        
        for product in sorted(self.products.values(), key=lambda x: x.name):
            status = "OUT" if product.is_out_of_stock() else "LOW" if product.is_low_stock() else "OK"
            value = product.current_stock * product.price
            report += f"{product.product_id:<8} {product.name[:24]:<25} {product.category[:14]:<15} "
            report += f"{product.current_stock:<8} {product.available_stock:<10} "
            report += f"${product.price:<9.2f} ${value:<11.2f} {status:<12}\n"
        
        return report
    
    def __str__(self):
        return f"Inventory: {len(self.products)} products, ${self.get_inventory_value():.2f} total value"
