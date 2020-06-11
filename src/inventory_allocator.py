import copy

class InventoryAllocator:

	# computes and returns the best way an order can be shipped
	# given inventory across a set of warehouses.
	# assume warehouses are pre-sorted based on cost. So the first warehouse
	# is less expensive to ship than from the second warehouse.

	def shipment(self, order_items, warehouse_inventories):
		shipment_order = []

		if order_items is None or warehouse_inventories is None:
			return shipment_order

		# copy the input
		items = copy.deepcopy(order_items)
		warehouses = copy.deepcopy(warehouse_inventories)

		# keep track of how many orders there are
		total_order = sum(order_items.values())

		# for each warehouse, find how much it can fulfill shipment
		for warehouse in warehouses:
			# if the order has been fulfilled, we are done
			if total_order == 0:
				break

			warehouse_name = warehouse['name']
			warehouse_inventory = warehouse['inventory']
			shipment = {}

			for item_name in items:
				if items[item_name] == 0:
					continue

				# if the warehouse has this item in stock
				if (item_name in warehouse_inventory and warehouse_inventory[item_name] > 0):
					old_count = items[item_name]

					shipment[item_name] = min(items[item_name], warehouse_inventory[item_name])
					items[item_name] = max(items[item_name] - warehouse_inventory[item_name], 0)

					# check how many total orders left must be fulfilled
					total_order = total_order - old_count + items[item_name]

			if shipment:
				shipment_order.append({warehouse_name : shipment})

		return shipment_order
