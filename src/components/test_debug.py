# debug_test.py - Place this in C:\Desktop\mlproject\
import os
import sys
import logging

print("=== PROPER DEBUG TEST ===")

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

print(f"✓ Current directory: {os.getcwd()}")
print(f"✓ Python path: {sys.path}")

# Test 1: Check if src exists
src_path = os.path.join(os.getcwd(), 'src')
print(f"✓ src directory exists: {os.path.exists(src_path)}")

# Test 2: Check if components exists
components_path = os.path.join(src_path, 'components')
print(f"✓ components directory exists: {os.path.exists(components_path)}")

# Test 3: Try to import from src
try:
    from src.logger import logging as project_logger
    print("✓ Successfully imported from src.logger")
    
    # Test logging
    project_logger.info("This is a test from debug script")
    print("✓ Logging call completed")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Check CSV file
csv_path = os.path.join('notebook', 'data', 'stud.csv')
print(f"✓ CSV file exists: {os.path.exists(csv_path)}")

print("=== DEBUG COMPLETED ===")