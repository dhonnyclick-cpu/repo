import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'inventory-dwh-secret-key-2025'

# Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
UPLOAD_DIR = BASE_DIR / 'static' / 'img' / 'products'
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

PRODUCTS_FILE = DATA_DIR / 'products.json'
WAREHOUSE_FILE = DATA_DIR / 'warehouse.json'
TRANSACTIONS_FILE = DATA_DIR / 'transactions.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def load_json(filepath, default=None):
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default if default is not None else []

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Daftar lokasi tetap ("Kantor" | "Warehouse CTI") - pisahkan dari data JSON agar selalu tersedia
LOCATIONS = [
    {"id": "KTR-001", "code": "KTR-001", "name": "Kantor"},
    {"id": "CTI-001", "code": "CTI-001", "name": "Warehouse CTI"},
]

def get_locations():
    """Kembalikan daftar lokasi dari data JSON jika ada, fallback ke LOCATIONS bawaan."""
    warehouse = load_json(WAREHOUSE_FILE)
    if warehouse and any(w.get("name") in ("Kantor", "Warehouse CTI") for w in warehouse):
        return warehouse
    return LOCATIONS

# Initialize data files
for f, default in [(PRODUCTS_FILE, []), (WAREHOUSE_FILE, []), (TRANSACTIONS_FILE, [])]:
    if not f.exists():
        save_json(f, default)

# ============== ROUTES ==============

@app.route('/')
def index():
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)
    total_products = len(products)
    total_stock = sum(p.get('stock', 0) for p in products)
    low_stock = sum(1 for p in products if p.get('stock', 0) <= p.get('min_stock', 5))
    total_value = sum(p.get('stock', 0) * p.get('price', 0) for p in products)

    stats = {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'total_value': total_value,
        'warehouse_count': len(warehouse)
    }
    return render_template('index.html', stats=stats)

# --- Products CRUD ---
@app.route('/products')
def products():
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)
    return render_template('products.html', products=products, warehouses=warehouse)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    warehouse = get_locations()
    if request.method == 'POST':
        products = load_json(PRODUCTS_FILE)

        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4().hex[:8]}.{ext}"
                file.save(UPLOAD_DIR / image_filename)

        product = {
            'id': str(uuid.uuid4())[:8],
            'sku': request.form.get('sku', '').upper(),
            'name': request.form.get('name', ''),
            'category': request.form.get('category', ''),
            'description': request.form.get('description', ''),
            'price': float(request.form.get('price', 0)),
            'stock': int(request.form.get('stock', 0)),
            'min_stock': int(request.form.get('min_stock', 5)),
            'unit': request.form.get('unit', 'pcs'),
            'warehouse_id': request.form.get('warehouse_id', ''),
            'location': request.form.get('location', ''),
            'image': image_filename,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        products.append(product)
        save_json(PRODUCTS_FILE, products)

        # Log transaction
        log_transaction('IN', product['id'], product['stock'], f"Initial stock for {product['name']}")

        flash('Produk berhasil ditambahkan!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', warehouses=warehouse, product=None)

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = load_json(PRODUCTS_FILE)
    warehouse = get_locations()
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        flash('Produk tidak ditemukan!', 'error')
        return redirect(url_for('products'))

    if request.method == 'POST':
        old_stock = product['stock']

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image
                if product.get('image'):
                    old_path = UPLOAD_DIR / product['image']
                    if old_path.exists():
                        old_path.unlink()
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4().hex[:8]}.{ext}"
                file.save(UPLOAD_DIR / image_filename)
                product['image'] = image_filename

        product.update({
            'sku': request.form.get('sku', '').upper(),
            'name': request.form.get('name', ''),
            'category': request.form.get('category', ''),
            'description': request.form.get('description', ''),
            'price': float(request.form.get('price', 0)),
            'stock': int(request.form.get('stock', 0)),
            'min_stock': int(request.form.get('min_stock', 5)),
            'unit': request.form.get('unit', 'pcs'),
            'warehouse_id': request.form.get('warehouse_id', ''),
            'location': request.form.get('location', ''),
            'updated_at': datetime.now().isoformat()
        })

        save_json(PRODUCTS_FILE, products)

        # Log stock change
        new_stock = product['stock']
        if new_stock != old_stock:
            log_transaction('ADJUST', product_id, new_stock - old_stock, f"Stock adjusted from {old_stock} to {new_stock}")

        flash('Produk berhasil diperbarui!', 'success')
        return redirect(url_for('products'))

    return render_template('product_form.html', warehouses=warehouse, product=product)

@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    products = load_json(PRODUCTS_FILE)
    product = next((p for p in products if p['id'] == product_id), None)

    if product:
        if product.get('image'):
            img_path = UPLOAD_DIR / product['image']
            if img_path.exists():
                img_path.unlink()
        products = [p for p in products if p['id'] != product_id]
        save_json(PRODUCTS_FILE, products)
        flash('Produk berhasil dihapus!', 'success')
    else:
        flash('Produk tidak ditemukan!', 'error')
    return redirect(url_for('products'))

@app.route('/products/<product_id>')
def product_detail(product_id):
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)
    transactions = load_json(TRANSACTIONS_FILE)

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Produk tidak ditemukan!', 'error')
        return redirect(url_for('products'))

    wh = next((w for w in warehouse if w['id'] == product.get('warehouse_id')), None)
    product_transactions = [t for t in transactions if t['product_id'] == product_id]
    product_transactions.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('product_detail.html', product=product, warehouse=wh, transactions=product_transactions)

# --- Warehouse CRUD ---
@app.route('/warehouses')
def warehouses():
    warehouse = load_json(WAREHOUSE_FILE)
    products = load_json(PRODUCTS_FILE)

    # Add product count to each warehouse
    for wh in warehouse:
        wh['product_count'] = sum(1 for p in products if p.get('warehouse_id') == wh['id'])
        wh['total_stock'] = sum(p.get('stock', 0) for p in products if p.get('warehouse_id') == wh['id'])

    return render_template('warehouses.html', warehouses=warehouse)

@app.route('/warehouses/add', methods=['GET', 'POST'])
def add_warehouse():
    if request.method == 'POST':
        warehouse = load_json(WAREHOUSE_FILE)
        wh = {
            'id': str(uuid.uuid4())[:8],
            'code': request.form.get('code', '').upper(),
            'name': request.form.get('name', ''),
            'address': request.form.get('address', ''),
            'manager': request.form.get('manager', ''),
            'phone': request.form.get('phone', ''),
            'capacity': int(request.form.get('capacity', 0)),
            'created_at': datetime.now().isoformat()
        }
        warehouse.append(wh)
        save_json(WAREHOUSE_FILE, warehouse)
        flash('Gudang berhasil ditambahkan!', 'success')
        return redirect(url_for('warehouses'))
    return render_template('warehouse_form.html', warehouse=None)

@app.route('/warehouses/edit/<wh_id>', methods=['GET', 'POST'])
def edit_warehouse(wh_id):
    warehouse = load_json(WAREHOUSE_FILE)
    wh = next((w for w in warehouse if w['id'] == wh_id), None)

    if not wh:
        flash('Gudang tidak ditemukan!', 'error')
        return redirect(url_for('warehouses'))

    if request.method == 'POST':
        wh.update({
            'code': request.form.get('code', '').upper(),
            'name': request.form.get('name', ''),
            'address': request.form.get('address', ''),
            'manager': request.form.get('manager', ''),
            'phone': request.form.get('phone', ''),
            'capacity': int(request.form.get('capacity', 0))
        })
        save_json(WAREHOUSE_FILE, warehouse)
        flash('Gudang berhasil diperbarui!', 'success')
        return redirect(url_for('warehouses'))

    return render_template('warehouse_form.html', warehouse=wh)

@app.route('/warehouses/delete/<wh_id>', methods=['POST'])
def delete_warehouse(wh_id):
    warehouse = load_json(WAREHOUSE_FILE)
    warehouse = [w for w in warehouse if w['id'] != wh_id]
    save_json(WAREHOUSE_FILE, warehouse)
    flash('Gudang berhasil dihapus!', 'success')
    return redirect(url_for('warehouses'))

# --- Stock Movement ---
@app.route('/stock/move', methods=['GET', 'POST'])
def stock_move():
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        movement_type = request.form.get('type')  # IN, OUT, TRANSFER
        quantity = int(request.form.get('quantity', 0))
        notes = request.form.get('notes', '')
        from_wh = request.form.get('from_warehouse', '')
        to_wh = request.form.get('to_warehouse', '')

        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            flash('Produk tidak ditemukan!', 'error')
            return redirect(url_for('stock_move'))

        if movement_type == 'IN':
            product['stock'] += quantity
            log_transaction('IN', product_id, quantity, notes)
        elif movement_type == 'OUT':
            if product['stock'] < quantity:
                flash('Stok tidak mencukupi!', 'error')
                return redirect(url_for('stock_move'))
            product['stock'] -= quantity
            log_transaction('OUT', product_id, quantity, notes)
        elif movement_type == 'TRANSFER':
            if product['stock'] < quantity:
                flash('Stok tidak mencukupi untuk transfer!', 'error')
                return redirect(url_for('stock_move'))
            product['stock'] -= quantity
            product['warehouse_id'] = to_wh
            log_transaction('TRANSFER_OUT', product_id, quantity, f"Transfer to {to_wh}: {notes}")
            log_transaction('TRANSFER_IN', product_id, quantity, f"Transfer from {from_wh}: {notes}")

        product['updated_at'] = datetime.now().isoformat()
        save_json(PRODUCTS_FILE, products)
        flash('Pergerakan stok berhasil dicatat!', 'success')
        return redirect(url_for('stock_move'))

    return render_template('stock_move.html', products=products, warehouses=warehouse)

# --- Reports / Data Warehouse ---
@app.route('/reports')
def reports():
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)
    transactions = load_json(TRANSACTIONS_FILE)

    # Summary stats
    total_products = len(products)
    total_stock = sum(p.get('stock', 0) for p in products)
    total_value = sum(p.get('stock', 0) * p.get('price', 0) for p in products)
    low_stock_items = [p for p in products if p.get('stock', 0) <= p.get('min_stock', 5)]
    out_of_stock = [p for p in products if p.get('stock', 0) == 0]

    # Category breakdown
    categories = {}
    for p in products:
        cat = p.get('category', 'Uncategorized')
        if cat not in categories:
            categories[cat] = {'count': 0, 'stock': 0, 'value': 0}
        categories[cat]['count'] += 1
        categories[cat]['stock'] += p.get('stock', 0)
        categories[cat]['value'] += p.get('stock', 0) * p.get('price', 0)

    # Warehouse breakdown
    wh_stats = {}
    for wh in warehouse:
        wh_products = [p for p in products if p.get('warehouse_id') == wh['id']]
        wh_stats[wh['id']] = {
            'name': wh['name'],
            'code': wh['code'],
            'products': len(wh_products),
            'stock': sum(p.get('stock', 0) for p in wh_products),
            'value': sum(p.get('stock', 0) * p.get('price', 0) for p in wh_products)
        }

    # Recent transactions
    recent_tx = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)[:50]

    return render_template('reports.html',
        total_products=total_products,
        total_stock=total_stock,
        total_value=total_value,
        low_stock_count=len(low_stock_items),
        out_of_stock_count=len(out_of_stock),
        low_stock_items=low_stock_items[:10],
        out_of_stock=out_of_stock[:10],
        categories=categories,
        wh_stats=wh_stats,
        recent_transactions=recent_tx
    )

@app.route('/api/stock-chart')
def stock_chart():
    products = load_json(PRODUCTS_FILE)
    # Top 10 products by stock
    top_products = sorted(products, key=lambda x: x.get('stock', 0), reverse=True)[:10]
    return jsonify({
        'labels': [p['name'][:20] for p in top_products],
        'data': [p.get('stock', 0) for p in top_products]
    })

@app.route('/api/category-chart')
def category_chart():
    products = load_json(PRODUCTS_FILE)
    categories = {}
    for p in products:
        cat = p.get('category', 'Uncategorized')
        categories[cat] = categories.get(cat, 0) + p.get('stock', 0)
    return jsonify({
        'labels': list(categories.keys()),
        'data': list(categories.values())
    })

@app.route('/api/warehouse-chart')
def warehouse_chart():
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)
    wh_data = {}
    for wh in warehouse:
        wh_products = [p for p in products if p.get('warehouse_id') == wh['id']]
        wh_data[wh['name']] = sum(p.get('stock', 0) for p in wh_products)
    return jsonify({
        'labels': list(wh_data.keys()),
        'data': list(wh_data.values())
    })

# --- Transactions ---
@app.route('/transactions')
def transactions():
    transactions = load_json(TRANSACTIONS_FILE)
    products = load_json(PRODUCTS_FILE)
    warehouse = load_json(WAREHOUSE_FILE)

    # Enrich transactions
    for t in transactions:
        p = next((p for p in products if p['id'] == t['product_id']), None)
        t['product_name'] = p['name'] if p else 'Unknown'
        t['product_sku'] = p['sku'] if p else ''

    transactions.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('transactions.html', transactions=transactions)

# --- Helper ---
def log_transaction(tx_type, product_id, quantity, notes=''):
    transactions = load_json(TRANSACTIONS_FILE)
    tx = {
        'id': str(uuid.uuid4())[:8],
        'type': tx_type,
        'product_id': product_id,
        'quantity': quantity,
        'notes': notes,
        'timestamp': datetime.now().isoformat()
    }
    transactions.append(tx)
    save_json(TRANSACTIONS_FILE, transactions)

# --- Static file serving for uploads ---
@app.route('/static/img/products/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)