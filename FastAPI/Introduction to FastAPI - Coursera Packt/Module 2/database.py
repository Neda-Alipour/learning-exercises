import sqlite3
from typing import Any

from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS shipment (
            id INTEGER PRIMARY KEY, 
            content TEXT, 
            weight REAL, 
            status TEXT
            )"""
        )
        self.conn.commit()

    def create(self, shipment: ShipmentCreate):
        self.cur.execute("SELECT MAX(id) FROM shipment")
        new_id = self.cur.fetchone()[0] + 1
        self.cur.execute(
            "INSERT INTO shipment (id, content, weight, status) VALUES (:id, :content, :weight, :status)",
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed",
            }
        )
        self.conn.commit()

    def get(self, id: int) -> dict[str, Any]:
        self.cur.execute("SELECT * FROM shipment WHERE id = ?", (id,))
        row = self.cur.fetchone()
        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        } if row else None
    
    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cur.execute(
            "UPDATE shipment SET status = :status WHERE id = :id", {
                "id": id,
                **shipment.model_dump(),
            }
        )
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("DELETE FROM shipment WHERE id = ?", (id,))
        self.conn.commit()

    def fetch_shipments(self):
        self.cur.execute("SELECT * FROM shipment")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()



# JSON file db
# import json

# shipments = {}

# with open("shipments.json", "r") as json_file:
#     data = json.load(json_file)

#     for value in data:
#         shipments[value["id"]] = value


# def save():
#     with open("shipments.json", "w"):
#         json.dump(list(shipments.values()))
