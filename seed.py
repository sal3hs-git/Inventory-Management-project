import random
from datetime import datetime, timedelta

def seed_inventory():
    """Create comprehensive sample inventory data for testing"""
    print(" Seeding inventory with sample data...")
     
    
    # Add products to inventory with realistic scenarios
    total_products = len(sample_products)
    for i, product_data in enumerate(sample_products, 1):
        product = Product(
            product_id=product_data["id"],
            name=product_data["name"],
            category=product_data["category"],
            price=product_data["price"],
            min_stock_level=product_data["min_stock"],
            supplier=product_data["supplier"]
        )
        
        
        product.add_stock(product_data["initial_stock"], cost_per_unit=None)
        
    
        demand_level = product_data.get("demand", "medium")
        
        if demand_level == "high":
        
            sales_percentage = random.uniform(0.3, 0.6)  
            reserve_percentage = random.uniform(0.1, 0.25)  
        elif demand_level == "medium":
            
            sales_percentage = random.uniform(0.15, 0.35)  
            reserve_percentage = random.uniform(0.05, 0.15) 
        else:  
            
            sales_percentage = random.uniform(0.05, 0.2)  
            reserve_percentage = random.uniform(0.02, 0.08)  
        
    
        max_sales = int(product_data["initial_stock"] * sales_percentage)
        if max_sales > 0:
            sold_quantity = random.randint(1, max_sales)
            product.current_stock -= sold_quantity
            product.total_sold = sold_quantity
        
        
        max_reserve = int(product.available_stock * reserve_percentage)
        if max_reserve > 0 and product.available_stock > 0:
            reserve_quantity = random.randint(1, min(max_reserve, product.available_stock))
            product.reserve_stock(reserve_quantity)
        
        
        if random.random() < 0.3:  
            days_ago = random.randint(1, 30)
            product.last_restocked = datetime.now() - timedelta(days=days_ago)
        
        inventory.add_product(product)
        
        
        if i % 10 == 0 or i == total_products:
            print(f"   Added {i}/{total_products} products...")
    
    
    print("   Generating reorder history...")
    for _ in range(15):  
        product_id = random.choice(list(inventory.products.keys()))
        quantity = random.randint(10, 50)
        cost = random.uniform(10, 100)
        days_ago = random.randint(7, 90)
        
        inventory.reorder_history.append({
            'product_id': product_id,
            'product_name': inventory.products[product_id].name,
            'quantity': quantity,
            'cost_per_unit': cost,
            'total_cost': cost * quantity,
            'date': datetime.now() - timedelta(days=days_ago)
        })
    
    print(f" Successfully seeded inventory with {len(sample_products)} products")
    print(f"Categories: {len(inventory.get_categories())}")
    print(f"Total stock units: {sum(p.current_stock for p in inventory.products.values()):,}")
    print(f"Total inventory value: ${inventory.get_inventory_value():,.2f}")
    print(f"Low stock alerts: {len(inventory.check_low_stock())}")
    print(f"Reorder history entries: {len(inventory.reorder_history)}")
    
    return inventory

def create_test_scenarios(inventory):
    """Create specific test scenarios for debugging and testing"""
    print("\n Creating test scenarios...")
    
    out_of_stock_product = Product(
        product_id=999,
        name="Test Out of Stock Item",
        category="Test",
        price=99.99,
        min_stock_level=5,
        supplier="Test Supplier"
    )
    inventory.add_product(out_of_stock_product)
    

    low_stock_product = Product(
        product_id=998,
        name="Test Low Stock Item",
        category="Test",
        price=49.99,
        min_stock_level=20,
        supplier="Test Supplier"
    )
    low_stock_product.add_stock(15)  
    inventory.add_product(low_stock_product)
    
    
    reserved_stock_product = Product(
        product_id=997,
        name="Test Reserved Stock Item",
        category="Test",
        price=199.99,
        min_stock_level=5,
        supplier="Test Supplier"
    )
    reserved_stock_product.add_stock(50)
    reserved_stock_product.reserve_stock(30)  
    inventory.add_product(reserved_stock_product)
    
    print("Test scenarios created successfully")
    
    return inventory

def seed_with_scenarios():
    """Seed inventory and add test scenarios"""
    inventory = seed_inventory()
    inventory = create_test_scenarios(inventory)
    return inventory