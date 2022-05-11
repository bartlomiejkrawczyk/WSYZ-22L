import yaml
import csv
import re

with open("results.yml", mode="r") as f:
    data = yaml.safe_load(f)

with open("results/shipment_to_shops.csv", mode="w", newline="") as to_shops_f, \
        open("results/shipment_to_warehouses.csv", mode="w", newline="") as to_warehouses_f, \
        open("results/shop_storage.csv", mode="w", newline="") as storage_f:

    to_shops_w = csv.writer(to_shops_f)
    to_shops_w.writerow(["Warehouse", "Shop", "Week", "Vegetable", "Value"])

    to_warehouses_w = csv.writer(to_warehouses_f)
    to_warehouses_w.writerow(["Farm", "Warehouse", "Vegetable", "Value"])

    storage_w = csv.writer(storage_f)
    storage_w.writerow(["Shop", "Week", "Vegetable", "Value"])

    for text, value_obj in data["Solution"][1]["Variable"].items():
        text_match = re.match(r"^([A-Za-z_]+)\[([A-Za-z0-9,_]*)\]$", text)
        variable_name = text_match[1]

        row = text_match[2].split(",")
        row.append(value_obj["Value"])

        if variable_name == "shipment_to_shops":
            row[3] = row[3].title()
            to_shops_w.writerow(row)
        elif variable_name == "shipment_to_warehouses":
            row[2] = row[2].title()
            to_warehouses_w.writerow(row)
        elif variable_name == "shop_storage":
            row[2] = row[2].title()
            storage_w.writerow(row)
        else:
            assert False, f"invalid variable name: {variable_name!r}"
