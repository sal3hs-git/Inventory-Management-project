import logging
import traceback
from functools import wraps

# Configure debug logging
debug_logger = logging.getLogger('inventory_debug')
debug_logger.setLevel(logging.DEBUG)

# Create file handler for debug logs
debug_handler = logging.FileHandler('inventory_debug.log')
debug_handler.setLevel(logging.DEBUG)

# Create console handler for debug logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
debug_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
debug_logger.addHandler(debug_handler)
debug_logger.addHandler(console_handler)

def debug_method(func):
    """Decorator to add debug logging to methods"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        debug_logger.debug(f"Calling {func.__name__} with args: {args[1:]} kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            debug_logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            debug_logger.error(f"Error in {func.__name__}: {str(e)}")
            debug_logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    return wrapper

class InventoryDebugger:
    """Debug utilities for inventory management"""
    
    @staticmethod
    def validate_inventory(inventory):
        """Validate inventory state and report issues"""
        print("\nINVENTORY VALIDATION REPORT")
        print("=" * 50)
        
        issues = []
        
        # Check for duplicate product IDs
        product_ids = [p.product_id for p in inventory.products.values()]
        if len(product_ids) != len(set(product_ids)):
            issues.append("Duplicate product IDs found")
        else:
            print("No duplicate product IDs")
        
        # Check for negative stock
        negative_stock = [p for p in inventory.products.values() if p.current_stock < 0]
        if negative_stock:
            issues.append(f" {len(negative_stock)} products with negative stock")
            for product in negative_stock:
                print(f"   - {product.name}: {product.current_stock}")
        else:
            print("No negative stock found")
        
        # Check for invalid reserved stock
        invalid_reserved = [p for p in inventory.products.values() if p.reserved_stock > p.current_stock]
        if invalid_reserved:
            issues.append(f"{len(invalid_reserved)}