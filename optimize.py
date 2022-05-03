from pyomo.environ import *
import csv


def load_csv_data(table_name):
    result = {}
    with open(f"dane/{table_name}.csv", mode="r", newline="") as f:
        reader = csv.DictReader(f)
        last_col = reader.fieldnames[-1]
        for row in reader:
            if "week" in row: row["week"] = int(row["week"])
            k = tuple(row[col] for col in reader.fieldnames[:-1])
            v = float(row[last_col])
            result[k] = v
    return result


model = ConcreteModel()

# Helper sets
model.vegetables = Set(initialize=["potato", "cabbage", "beetroot", "carrot"])
model.farms = Set(initialize=[f"P{i}" for i in range(1, 7)])
model.warehouses = Set(initialize=["M1", "M2", "M3"])
model.shops = Set(initialize=[f"S{i}" for i in range(1, 11)])
model.weeks = Set(initialize=range(1, 53))

# Parameters
model.demand = Param(model.shops, model.weeks, model.vegetables, initialize=load_csv_data("demand"))
model.shop_storage_min = Param(model.shops, model.vegetables, initialize=load_csv_data("shop_storage_min"))
model.shop_storage_cap = Param(model.shops, initialize=load_csv_data("shop_storage_cap"))
model.warehouse_cap = Param(model.warehouses, initialize=load_csv_data("warehouse_cap"))
model.farm_output = Param(model.farms, model.vegetables, initialize=load_csv_data("farm_output"))
model.farm_warehouse_distance = Param(model.farms, model.warehouses, initialize=load_csv_data("farm_warehouse_distance"))
model.warehouse_shop_distance = Param(model.warehouses, model.shops, initialize=load_csv_data("warehouse_shop_distance"))
model.price_per_km_tonne = Param(initialize=4.0)

# Variables
model.shipment_to_warehouses = Var(model.farms, model.warehouses, model.vegetables, within=NonNegativeReals)
model.shipment_to_shops = Var(model.warehouses, model.shops, model.weeks, model.vegetables, within=NonNegativeReals)
model.shop_storage = Var(model.shops, model.weeks, model.vegetables, within=NonNegativeReals)
model.shop_leftovers = Var(model.shops, model.weeks, model.vegetables, within=NonNegativeReals)

# Goal
def goal_func(model):
    return (
        sum(
            sum(model.shipment_to_warehouses[farm, warehouse, vegetable] for vegetable in model.vegetables)
            * model.farm_warehouse_distance[farm, warehouse]
            for farm in model.farms
            for warehouse in model.warehouses
        )
        +
        sum(
            sum(
                model.shipment_to_shops[warehouse, shop, week, vegetable]
                for week in model.weeks
                for vegetable in model.vegetables
            )
            * model.warehouse_shop_distance[warehouse, shop]
            for warehouse in model.warehouses
            for shop in model.shops
        )
    ) * model.price_per_km_tonne

model.goal = Objective(rule=goal_func, sense=minimize)

#####################
#    CONSTRAINTS    #
#####################

# Shop storage constraints

model.shop_has_enough_veggies = Constraint(
    model.shops, model.weeks, model.vegetables,
    rule=lambda model, shop, week, veggie: model.shop_storage[shop, week, veggie] >= model.demand[shop, week, veggie],
)

model.shop_does_not_exceed_capacity = Constraint(
    model.shops, model.weeks,
    rule=lambda model, shop, week: sum(model.shop_storage[shop, week, veggie] for veggie in model.vegetables) \
                                    <= model.shop_storage_cap[shop]
)

model.shop_has_minimum_veggies = Constraint(
    model.shops, model.weeks, model.vegetables,
    rule=lambda model, shop, week, veggie: model.shop_storage[shop, week, veggie] >= model.shop_storage_min[shop, veggie]
)

# Warehouse to shop shipment
def constraint_calc_leftovers(model, shop, week, veggie):
    prev_leftovers = 0.0 if week == 1 else model.shop_leftovers[shop, week - 1 , veggie]
    return model.shop_leftovers[shop, week, veggie] == \
        prev_leftovers \
        + sum(model.shipment_to_shops[w, shop, week, veggie] for w in model.warehouses) \
        - model.demand[shop, week, veggie]

model.calc_shop_leftovers = Constraint(model.shops, model.weeks, model.vegetables, rule=constraint_calc_leftovers)


def constraint_shop_shipment(model, shop, week, veggie):
    return sum(model.shipment_to_shops[warehouse, shop, week, veggie] for warehouse in model.warehouses) \
        + model.shop_leftovers[shop, week, veggie] \
        >= model.demand[shop, week, veggie]

model.shop_shipment = Constraint(model.shops, model.weeks, model.vegetables, rule=constraint_shop_shipment)

# Warehouse constraints
model.warehouse_does_not_exceed_capacity = Constraint(
    model.warehouses,
    rule=lambda model, warehouse: sum(model.shipment_to_warehouses[farm, warehouse, veggie]
                                      for farm in model.farms for veggie in model.vegetables) \
                                  <= model.warehouse_cap[warehouse]
)

model.warehouse_shipments_does_not_exceed_stored_vegetables = Constraint(
    model.warehouses, model.vegetables,
    rule=lambda model, warehouse, veggie: \
        sum(model.shipment_to_shops[warehouse, shop, week, veggie] for shop in model.shops for week in model.weeks) \
        <= sum(model.shipment_to_warehouses[farm, warehouse, veggie] for farm in model.farms)
)

# Farm constraint
model.farm_shipment_does_not_exceed_output = Constraint(
    model.farms, model.vegetables,
    rule=lambda model, farm, veggie: sum(model.shipment_to_warehouses[farm, w, veggie] for w in model.warehouses) \
        <= model.farm_output[farm, veggie]
)
