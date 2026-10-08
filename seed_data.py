"""Seed sample data for InvenWarehouse so the dashboard has something to show.
Run once:  python3 seed_data.py
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent
DATA = BASE / 'data'
DATA.mkdir(exist_ok=True)

WAREHOUSES = [
    {"id": "wh-001", "code": "KTR-001", "name": "Kantor", "address": "Jl. Raya Industri No. 10, Jakarta", "manager": "Budi Santoso", "phone": "021-555-0101", "capacity": 5000, "created_at": datetime.now().isoformat()},
    {"id": "wh-002", "code": "CTI-001", "name": "Warehouse CTI", "address": "Jl. Industri Raya No. 88, Bekasi", "manager": "Siti Rahayu", "phone": "021-555-0202", "capacity": 3000, "created_at": datetime.now().isoformat()},
]

PRODUCTS = [
    {"id": "prd-001", "sku": "ELK-001", "name": "Laptop Lenovo ThinkPad E14", "category": "Elektronik", "description": "Laptop bisnis 14 inch, RAM 8GB", "price": 12500000, "stock": 25, "min_stock": 5, "unit": "pcs", "warehouse_id": "wh-001", "location": "Rak A-01", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-002", "sku": "ELK-002", "name": "Monitor Dell 24 inch", "category": "Elektronik", "description": "Monitor IPS Full HD", "price": 2800000, "stock": 40, "min_stock": 10, "unit": "pcs", "warehouse_id": "wh-001", "location": "Rak A-02", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-003", "sku": "ELK-003", "name": "Keyboard Mechanical", "category": "Elektronik", "description": "Keyboard gaming RGB", "price": 850000, "stock": 3, "min_stock": 10, "unit": "pcs", "warehouse_id": "wh-001", "location": "Rak A-03", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-004", "sku": "ATK-001", "name": "Kertas A4 80gsm (rim)", "category": "Alat Tulis", "description": "Kertas HVS A4, isi 500 lembar", "price": 55000, "stock": 120, "min_stock": 30, "unit": "rim", "warehouse_id": "wh-002", "location": "Rak B-01", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-005", "sku": "ATK-002", "name": "Pulpen Pilot BP-1", "category": "Alat Tulis", "description": "Pulpen hitam isi 12 pcs/box", "price": 32000, "stock": 80, "min_stock": 20, "unit": "box", "warehouse_id": "wh-002", "location": "Rak B-02", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-006", "sku": "MKN-001", "name": "Kopi Arabika 1kg", "category": "Konsumsi", "description": "Biji kopi arabika premium", "price": 180000, "stock": 15, "min_stock": 5, "unit": "kg", "warehouse_id": "wh-001", "location": "Rak C-01", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-007", "sku": "MKN-002", "name": "Air Mineral 600ml (karton)", "category": "Konsumsi", "description": "Air mineral isi 24 botol", "price": 45000, "stock": 0, "min_stock": 10, "unit": "karton", "warehouse_id": "wh-001", "location": "Rak C-02", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-008", "sku": "PRN-001", "name": "Printer Epson L3210", "category": "Elektronik", "description": "Printer inkjet dengan tank", "price": 2400000, "stock": 8, "min_stock": 3, "unit": "pcs", "warehouse_id": "wh-002", "location": "Rak B-05", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-009", "sku": "PRN-002", "name": "Tinta Printer Hitam", "category": "Elektronik", "description": "Tinta refill 100ml", "price": 95000, "stock": 50, "min_stock": 15, "unit": "pcs", "warehouse_id": "wh-002", "location": "Rak B-06", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
    {"id": "prd-010", "sku": "ATK-003", "name": "Spidol Whiteboard", "category": "Alat Tulis", "description": "Spidol whiteboard isi 12 pcs", "price": 48000, "stock": 60, "min_stock": 15, "unit": "box", "warehouse_id": "wh-001", "location": "Rak A-05", "image": None, "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat()},
]

TRANSACTIONS = []
base = datetime.now() - timedelta(days=30)
for i, p in enumerate(PRODUCTS):
    TRANSACTIONS.append({
        "id": f"tx-{i+1:03d}",
        "type": "IN",
        "product_id": p["id"],
        "quantity": p["stock"] if p["stock"] > 0 else 10,
        "notes": "Stok awal",
        "timestamp": (base + timedelta(days=i)).isoformat()
    })

(DATA / 'warehouse.json').write_text(json.dumps(WAREHOUSES, indent=2, ensure_ascii=False), encoding='utf-8')
(DATA / 'products.json').write_text(json.dumps(PRODUCTS, indent=2, ensure_ascii=False), encoding='utf-8')
(DATA / 'transactions.json').write_text(json.dumps(TRANSACTIONS, indent=2, ensure_ascii=False), encoding='utf-8')

print(f"Seeded {len(WAREHOUSES)} warehouses, {len(PRODUCTS)} products, {len(TRANSACTIONS)} transactions.")
