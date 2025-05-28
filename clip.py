
import os
import sys
from datetime import datetime

# Import the inventory classes (assuming they're in the same directory)
try:
    from inventory_system import Product, Inventory, Order, OrderStatus
except ImportError:
    print("Error: inventory_system.py not found in the same directory.")
    print("Please make sure both files are in the same folder.")
    sys.exit(1)


class InventoryCLI:
    def __init__(self):
        self.inventory = None
        self.orders = {}  # Store orders by order_id
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)
    
    def print_menu(self, options):
        """Print menu options"""
        print("\nPlease select an option:")
        for key, value in options.items():
            print(f"  {key}. {value}")
        print()
    
    def get_input(self, prompt, input_type=str, validation_func=None):
        """Get validated input from user"""
        while True:
            try:
                user_input = input(f"{prompt}: ").strip()
                if not user_input and input_type != str:
                    print("Input cannot be empty. Please try again.")
                    continue
                
                # Convert to appropriate type
                if input_type == int:
                    user_input = int(user_input)
                elif input_type == float:
                    user_input = float(user_input)
                
                # Apply validation if provided
                if validation_func and not validation_func(user_input):
                    print("Invalid input. Please try again.")
                    continue
                
                return user_input
            except ValueError:
                print(f"Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None
    
    def pause(self):
        """Pause and wait for user input"""
        input("\nPress Enter to continue...")
    
    def setup_inventory(self):
        """Initial setup of the inventory system"""
        self.clear_screen()
        self.print_header("INVENTORY MANAGEMENT SYSTEM SETUP")
        