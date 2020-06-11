import unittest
from inventory_allocator import InventoryAllocator

# to run these tests, please run `python3 inventory_allocator_tests.py`

class InventoryAllocatorTest(unittest.TestCase):

	# test simple happy case of exact inventory match
	def test_exact_match(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 1 }
		warehouse_inventories = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
		expected_result = [{ 'owd': { 'apple': 1 } }]

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when inventory is not enough
	def test_not_enough_inventory(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 1 }
		warehouse_inventories = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }]
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when getting an item is split across warehouses
	def test_split_warehouses(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 10 }
		warehouse_inventories = [
			{ 'name': 'owd', 'inventory': { 'apple': 5 } }, 
			{ 'name': 'dm', 'inventory': { 'apple': 5 }}
		]
		expected_result = [{ 'owd': { 'apple': 5 }}, { 'dm': { 'apple': 5 } }]

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test for no order input
	def test_no_order(self):
		inventory_allocator = InventoryAllocator()

		order_items = { }
		warehouse_inventories = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test for no warehouse input
	def test_no_warehouses(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 1 }
		warehouse_inventories = []
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test for no input at all
	def test_no_input(self):
		inventory_allocator = InventoryAllocator()

		order_items = {}
		warehouse_inventories = []
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test for none input
	def test_none_input(self):
		inventory_allocator = InventoryAllocator()

		order_items = None
		warehouse_inventories = None
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when order has a list of 0 count items
	def test_order_0_counts(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 0, 'orange': 0, 'pikachu': 0 }
		warehouse_inventories = [
			{ 'name': 'owd', 'inventory': { 'apple': 5 }}, 
			{ 'name': 'dm', 'inventory': { 'orange': 5, 'pikachu': 100 }}
		]
		expected_result = []

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when order has an item that the inventory does not have
	def test_no_item_match(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 2, 'pikachu': 1 }
		warehouse_inventories = [
			{ 'name': 'owd', 'inventory': { 'apple': 5 }}, 
			{ 'name': 'dm', 'inventory': { 'orange': 5}}
		]
		expected_result = [{ 'owd': { 'apple': 2 }}]

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when order items are split across mutliple warehouses that are far apart
	# so some warehouses should be skipped
	def test_skip_warehouses(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 10, 'pikachu': 3, 'soccer ball': 2 }
		warehouse_inventories = [
			{ 'name': 'juventus', 'inventory': { 'apple': 0, 'pear': 10 }},
			{ 'name': 'barcelona', 'inventory': { 'apple': 5, 'soccer ball': 2}}, 
			{ 'name': 'real madrid', 'inventory': { 'apple': 2 }}, 
			{ 'name': 'chelsea', 'inventory': { 'apple': 0, 'pikachu': 4 }},
			{ 'name': 'arsenal', 'inventory': { 'banana': 0 }},
			{ 'name': 'liverpool', 'inventory': { 'apple': 6}}
		]
		expected_result = [
			{ 'barcelona': { 'apple': 5, 'soccer ball': 2 }},
			{ 'real madrid': { 'apple': 2 }},
			{ 'chelsea': { 'pikachu': 3 }},
			{ 'liverpool': { 'apple': 3 }}
		]

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)

	# test when items are almost fufilled
	def test_item_partially_fulfilled(self):
		inventory_allocator = InventoryAllocator()

		order_items = { 'apple': 10, 'pikachu': 7 }
		warehouse_inventories = [
			{ 'name': 'canada', 'inventory': { 'apple': 3, 'pikachu': 5 }},
			{ 'name': 'usa', 'inventory': { 'apple': 20, 'pikachu': 0}}, 
			{ 'name': 'korea', 'inventory': { 'apple': 2 }}
		]
		expected_result = [
			{ 'canada': { 'apple': 3, 'pikachu': 5 }},
			{ 'usa': { 'apple': 7 }}
		]

		self.assertEqual(inventory_allocator.shipment(order_items, warehouse_inventories), expected_result)


if __name__ == '__main__':
	unittest.main()



