from typing import NamedTuple
from itertools import product
import requests
import time
import csv


class Point(NamedTuple):
    name: str
    lat: float
    lon: float


Farms = list[Point]
Warehouses = list[Point]
Shops = list[Point]


def load_points() -> tuple[Farms, Warehouses, Shops]:
    farms: Farms = []
    warehouses: Warehouses = []
    shops: Shops = []

    with open("dane/lokalizacje.csv", mode="r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            pt = Point(row["name"], float(row["lat"]), float(row["lon"]))

            match row["type"]:
                case "farm":
                    farms.append(pt)
                case "warehouse":
                    warehouses.append(pt)
                case "grocery":
                    shops.append(pt)

    return farms, warehouses, shops


def get_distance(start: Point, end: Point) -> float:
    r = requests.get(
        "https://routing.openstreetmap.de/routed-car/route/v1/driving/"
        f"{start.lon},{start.lat};{end.lon},{end.lat}"
    )
    r.raise_for_status()
    data = r.json()
    assert data["code"].casefold() == "ok"
    return data["routes"][0]["distance"] / 1000.0


if __name__ == "__main__":
    farms, warehouses, shops = load_points()

    with open("dane/odleglosci.csv", mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["from", "to", "km"])

        for farm, warehouse in product(farms, warehouses):
            print(farm.name, warehouse.name)
            time.sleep(1)
            dist = get_distance(farm, warehouse)
            writer.writerow([farm.name, warehouse.name, round(dist, 4)])

        for warehouse, shop in product(warehouses, shops):
            print(warehouse.name, shop.name)
            time.sleep(1)
            dist = get_distance(warehouse, shop)
            writer.writerow([warehouse.name, shop.name, round(dist, 4)])
