# database/seed_data.py
import random
from datetime import date, timedelta
from database.connection import get_connection


def seed_database():
    """Populate the database with realistic retail data using batch inserts."""
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data first
    print("Clearing existing data...")
    cursor.execute("DELETE FROM inventory_log")
    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")
    conn.commit()

    print("Seeding products...")
    seed_products(cursor)
    conn.commit()
    print("  ✅ Products done")

    print("Seeding customers...")
    seed_customers(cursor)
    conn.commit()
    print("  ✅ Customers done")

    print("Seeding sales...")
    seed_sales(cursor)
    conn.commit()
    print("  ✅ Sales done")

    print("Seeding inventory log...")
    seed_inventory_log(cursor)
    conn.commit()
    print("  ✅ Inventory log done")

    conn.close()
    print("\n🎉 Done! Database seeded successfully.")


def seed_products(cursor):
    """Insert 200 products across 8 categories using batch insert."""
    categories = {
        "Electronics": [
            ("iPhone 15 Case", 5.00, 19.99), ("Samsung Galaxy Screen Protector", 2.00, 9.99),
            ("USB-C Cable 2m", 3.00, 12.99), ("Wireless Earbuds", 15.00, 49.99),
            ("Phone Stand", 4.00, 14.99), ("Power Bank 10000mAh", 12.00, 34.99),
            ("Bluetooth Speaker", 18.00, 59.99), ("Laptop Sleeve 15 inch", 8.00, 24.99),
            ("HDMI Cable 3m", 4.00, 14.99), ("Wireless Mouse", 7.00, 22.99),
            ("Keyboard Cover", 3.00, 11.99), ("Car Phone Mount", 5.00, 17.99),
            ("Smart Watch Band", 4.00, 15.99), ("Camera Lens Protector", 2.00, 8.99),
            ("Tablet Stand", 6.00, 19.99), ("USB Hub 4-Port", 8.00, 24.99),
            ("Webcam Cover", 1.00, 4.99), ("Cable Organizer", 3.00, 9.99),
            ("Screen Cleaning Kit", 2.00, 7.99), ("Portable Charger", 10.00, 29.99),
            ("AirPods Case", 3.00, 12.99), ("Ring Light Mini", 8.00, 24.99),
            ("Selfie Stick", 4.00, 14.99), ("VR Headset Basic", 20.00, 59.99),
            ("Gaming Mouse Pad", 5.00, 16.99),
        ],
        "Clothing": [
            ("Cotton T-Shirt White", 5.00, 19.99), ("Cotton T-Shirt Black", 5.00, 19.99),
            ("Polo Shirt", 8.00, 29.99), ("Denim Jeans Slim", 12.00, 44.99),
            ("Denim Jeans Regular", 12.00, 39.99), ("Hoodie Grey", 10.00, 34.99),
            ("Hoodie Black", 10.00, 34.99), ("Formal Shirt White", 9.00, 32.99),
            ("Casual Shorts", 6.00, 22.99), ("Winter Jacket", 25.00, 79.99),
            ("Thobe White", 15.00, 49.99), ("Thobe Brown", 15.00, 49.99),
            ("Abaya Black", 20.00, 69.99), ("Scarf Silk", 8.00, 29.99),
            ("Cap Baseball", 4.00, 14.99), ("Socks Pack of 6", 3.00, 12.99),
            ("Belt Leather", 7.00, 24.99), ("Sunglasses Classic", 5.00, 19.99),
            ("Sports Tracksuit", 15.00, 49.99), ("Pajama Set", 8.00, 27.99),
            ("Rain Jacket", 12.00, 39.99), ("Gym Shorts", 5.00, 18.99),
            ("Dress Shirt Blue", 9.00, 32.99), ("Cardigan Wool", 18.00, 54.99),
            ("Swim Shorts", 6.00, 22.99),
        ],
        "Food & Beverage": [
            ("Arabic Coffee 500g", 8.00, 18.99), ("Green Tea Box 100", 3.00, 9.99),
            ("Dates Premium 1kg", 6.00, 15.99), ("Olive Oil 1L", 5.00, 14.99),
            ("Honey Natural 500g", 7.00, 19.99), ("Rice Basmati 5kg", 4.00, 12.99),
            ("Spice Mix Set", 3.00, 11.99), ("Chocolate Box Premium", 8.00, 24.99),
            ("Instant Noodles Pack 10", 2.00, 6.99), ("Protein Bar Box 12", 6.00, 18.99),
            ("Energy Drink Pack 6", 3.00, 9.99), ("Bottled Water Case 24", 2.00, 7.99),
            ("Nuts Mixed 500g", 5.00, 14.99), ("Saffron 5g", 10.00, 29.99),
            ("Turkish Coffee 250g", 4.00, 12.99), ("Biscuits Variety Pack", 2.00, 7.99),
            ("Jam Strawberry 500g", 2.00, 6.99), ("Peanut Butter 400g", 3.00, 9.99),
            ("Cereal Box 500g", 2.00, 8.99), ("Dried Fruits Mix 300g", 4.00, 12.99),
            ("Tahini 400g", 3.00, 8.99), ("Halva 500g", 3.00, 9.99),
            ("Chips Variety 12 Pack", 2.00, 7.99), ("Juice Box Pack 9", 2.00, 6.99),
            ("Yogurt Pack 6", 2.00, 5.99),
        ],
        "Beauty": [
            ("Face Moisturizer 100ml", 8.00, 29.99), ("Shampoo 500ml", 4.00, 14.99),
            ("Conditioner 500ml", 4.00, 14.99), ("Perfume Oud 50ml", 25.00, 89.99),
            ("Perfume Musk 50ml", 20.00, 74.99), ("Body Lotion 250ml", 5.00, 17.99),
            ("Sunscreen SPF50", 6.00, 22.99), ("Lip Balm Pack 3", 2.00, 7.99),
            ("Hair Oil 100ml", 3.00, 12.99), ("Face Wash 150ml", 4.00, 14.99),
            ("Deodorant 200ml", 3.00, 11.99), ("Hand Cream 75ml", 2.00, 8.99),
            ("Beard Oil 30ml", 5.00, 18.99), ("Toothpaste Pack 3", 2.00, 7.99),
            ("Shower Gel 400ml", 3.00, 12.99), ("Nail Care Kit", 4.00, 14.99),
            ("Eye Cream 30ml", 7.00, 24.99), ("Makeup Remover 200ml", 3.00, 11.99),
            ("Face Mask Pack 5", 3.00, 12.99), ("Hair Brush Set", 4.00, 14.99),
            ("Cotton Pads 100", 1.00, 4.99), ("Razor Pack 5", 3.00, 9.99),
            ("Bath Bomb Set 6", 4.00, 15.99), ("Dental Floss Pack 3", 1.00, 5.99),
            ("Wet Wipes Pack 80", 1.00, 4.99),
        ],
        "Home & Kitchen": [
            ("Coffee Mug Ceramic", 3.00, 12.99), ("Water Bottle 1L", 4.00, 14.99),
            ("Dinner Plate Set 4", 10.00, 34.99), ("Cooking Pot 5L", 12.00, 39.99),
            ("Frying Pan Non-Stick", 8.00, 27.99), ("Knife Set 6pc", 15.00, 44.99),
            ("Cutting Board Bamboo", 5.00, 17.99), ("Glass Set 6", 4.00, 14.99),
            ("Towel Set 4", 6.00, 22.99), ("Pillow Memory Foam", 8.00, 29.99),
            ("Bed Sheet Set Queen", 12.00, 39.99), ("Laundry Basket", 5.00, 17.99),
            ("Storage Box Set 3", 6.00, 19.99), ("Door Mat", 3.00, 12.99),
            ("Candle Set 3", 4.00, 14.99), ("Photo Frame Set 3", 5.00, 17.99),
            ("Wall Clock", 6.00, 22.99), ("Trash Can 10L", 4.00, 14.99),
            ("Broom and Dustpan", 3.00, 11.99), ("Iron Compact", 10.00, 32.99),
            ("Blender Mini", 12.00, 37.99), ("Toaster 2 Slice", 10.00, 29.99),
            ("Kettle Electric 1.5L", 8.00, 24.99), ("Food Container Set 5", 4.00, 15.99),
            ("Spice Rack", 5.00, 18.99),
        ],
        "Sports": [
            ("Yoga Mat", 6.00, 22.99), ("Dumbbell Set 5kg", 8.00, 29.99),
            ("Resistance Band Set", 4.00, 14.99), ("Jump Rope", 2.00, 8.99),
            ("Water Bottle Sports", 3.00, 12.99), ("Gym Bag", 8.00, 27.99),
            ("Running Shoes Insert", 3.00, 12.99), ("Fitness Tracker Band", 10.00, 34.99),
            ("Football", 5.00, 19.99), ("Basketball", 6.00, 24.99),
            ("Tennis Balls Pack 3", 2.00, 8.99), ("Swimming Goggles", 4.00, 14.99),
            ("Cycling Gloves", 3.00, 12.99), ("Sports Towel", 2.00, 9.99),
            ("Arm Band Phone Holder", 3.00, 11.99), ("Knee Support Brace", 4.00, 15.99),
            ("Protein Shaker", 3.00, 11.99), ("Exercise Ball 65cm", 6.00, 22.99),
            ("Foam Roller", 5.00, 18.99), ("Grip Strengthener", 2.00, 7.99),
            ("Badminton Set", 8.00, 27.99), ("Table Tennis Set", 6.00, 22.99),
            ("Hiking Backpack 30L", 12.00, 39.99), ("Camping Lantern", 5.00, 18.99),
            ("First Aid Kit", 4.00, 14.99),
        ],
        "Books & Stationery": [
            ("Notebook A5 Ruled", 1.00, 4.99), ("Notebook A4 Grid", 1.50, 5.99),
            ("Pen Set Blue 10", 1.00, 3.99), ("Pencil Set HB 12", 0.50, 2.99),
            ("Highlighter Set 6", 1.50, 5.99), ("Sticky Notes Pack", 1.00, 3.99),
            ("Planner 2025", 3.00, 12.99), ("Desk Organizer", 4.00, 14.99),
            ("Stapler Set", 2.00, 7.99), ("Tape Dispenser", 1.50, 5.99),
            ("Whiteboard Markers 4", 2.00, 6.99), ("Folder Set 10", 2.00, 7.99),
            ("Calculator Scientific", 5.00, 16.99), ("Ruler Set", 0.50, 2.99),
            ("Eraser Pack 5", 0.50, 1.99), ("Glue Stick Pack 3", 1.00, 3.99),
            ("Scissors", 1.00, 4.99), ("Backpack School", 8.00, 27.99),
            ("Lunch Box", 3.00, 12.99), ("Pencil Case", 2.00, 7.99),
            ("Color Pencils 24", 2.00, 8.99), ("Sketch Pad A3", 2.00, 7.99),
            ("Calligraphy Set", 5.00, 18.99), ("Book Stand", 3.00, 11.99),
            ("Paper Clips Box 100", 0.50, 2.49),
        ],
        "Toys": [
            ("Building Blocks 100pc", 6.00, 22.99), ("Puzzle 500 Pieces", 4.00, 14.99),
            ("RC Car Mini", 8.00, 29.99), ("Board Game Classic", 5.00, 19.99),
            ("Stuffed Animal Bear", 4.00, 16.99), ("Play Dough Set 6", 3.00, 11.99),
            ("Coloring Book Set", 2.00, 7.99), ("Action Figure", 5.00, 17.99),
            ("Doll Set", 6.00, 22.99), ("Card Game Pack", 2.00, 8.99),
            ("Bubble Maker", 2.00, 7.99), ("Water Gun", 3.00, 11.99),
            ("Kite Large", 3.00, 12.99), ("Toy Car Set 5", 4.00, 15.99),
            ("Robot Toy Walking", 7.00, 24.99), ("Dinosaur Set 10", 5.00, 18.99),
            ("Train Set Basic", 8.00, 29.99), ("Sand Toy Set", 3.00, 11.99),
            ("Musical Toy Piano", 6.00, 22.99), ("Telescope Kids", 8.00, 27.99),
            ("Science Kit Basic", 6.00, 22.99), ("Craft Kit", 4.00, 14.99),
            ("Sticker Book 500", 1.00, 4.99), ("Toy Kitchen Set", 10.00, 34.99),
            ("Ball Pit Balls 100", 5.00, 17.99),
        ],
    }

    suppliers = ["Al Rajhi Trading", "Gulf Supplies Co", "Desert Star LLC",
                 "Riyadh Wholesale", "Jeddah Imports", "Eastern Trading"]

    # Build ALL rows first, then insert in one batch
    rows = []
    product_id = 1
    for category, products in categories.items():
        for name, cost, sell in products:
            sku = f"SKU-{product_id:04d}"
            stock = random.randint(0, 150)
            reorder = random.randint(10, 30)
            supplier = random.choice(suppliers)
            rows.append((name, category, sku, cost, sell, stock, reorder, supplier))
            product_id += 1

    # Single batch insert using execute_values pattern
    args_str = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", row).decode("utf-8")
        for row in rows
    )
    cursor.execute(
        "INSERT INTO products (name, category, sku, cost_price, selling_price, "
        "stock_quantity, reorder_level, supplier) VALUES " + args_str
    )


def seed_customers(cursor):
    """Insert 500 customers in one batch."""
    first_names = ["Mohammed", "Ahmed", "Ali", "Omar", "Khalid", "Fahad", "Sultan",
                   "Abdullah", "Faisal", "Saad", "Nasser", "Ibrahim", "Hassan",
                   "Yousef", "Turki", "Fatima", "Noura", "Sara", "Maryam", "Aisha",
                   "Huda", "Reem", "Lina", "Dana", "Layla"]
    last_names = ["Al-Saud", "Al-Rashid", "Al-Qahtani", "Al-Ghamdi", "Al-Harbi",
                  "Al-Shehri", "Al-Otaibi", "Al-Zahrani", "Al-Malki", "Al-Dossari",
                  "Al-Mutairi", "Al-Subaie", "Al-Tamimi", "Al-Ahmad", "Al-Salem"]

    rows = []
    for i in range(500):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"+966{random.randint(500000000, 599999999)}"
        total_purchases = round(random.uniform(50, 5000), 2)
        visit_count = random.randint(1, 50)
        days_ago = random.randint(1, 365)
        last_visit = date.today() - timedelta(days=days_ago)
        rows.append((name, phone, total_purchases, visit_count, last_visit))

    args_str = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s)", row).decode("utf-8")
        for row in rows
    )
    cursor.execute(
        "INSERT INTO customers (name, phone, total_purchases, visit_count, last_visit) VALUES " + args_str
    )


def seed_sales(cursor):
    """Insert 30,000 sales in batches of 1000."""
    locations = ["Riyadh", "Jeddah", "Dammam"]
    location_weights = [0.50, 0.30, 0.20]
    payment_methods = ["cash", "card", "mada", "apple_pay"]
    payment_weights = [0.25, 0.25, 0.40, 0.10]

    # Get actual product IDs from database
    cursor.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]

    batch_size = 1000
    total = 30000

    for batch_start in range(0, total, batch_size):
        rows = []
        for _ in range(batch_size):
            product_id = random.choice(product_ids)
            quantity = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
            amount = round(random.uniform(5, 90) * quantity, 2)
            days_ago = random.randint(0, 365)
            sale_date = date.today() - timedelta(days=days_ago)
            location = random.choices(locations, weights=location_weights)[0]
            payment = random.choices(payment_methods, weights=payment_weights)[0]
            rows.append((product_id, quantity, amount, sale_date, location, payment))

        args_str = ",".join(
            cursor.mogrify("(%s,%s,%s,%s,%s,%s)", row).decode("utf-8")
            for row in rows
        )
        cursor.execute(
            "INSERT INTO sales (product_id, quantity_sold, total_amount, "
            "sale_date, store_location, payment_method) VALUES " + args_str
        )
        print(f"    Inserted {batch_start + batch_size}/{total} sales...")


def seed_inventory_log(cursor):
    """Insert 5,000 inventory movements in one batch."""
    reasons_in = ["restock", "return", "transfer_in"]
    reasons_out = ["sale", "damaged", "expired", "transfer_out"]

    # Get actual product IDs from database
    cursor.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]


    rows = []
    for _ in range(5000):
        product_id = random.choice(product_ids)
        days_ago = random.randint(0, 365)
        log_date = date.today() - timedelta(days=days_ago)

        if random.random() < 0.6:
            movement_type = "out"
            quantity = random.randint(1, 10)
            reason = random.choice(reasons_out)
        else:
            movement_type = "in"
            quantity = random.randint(10, 100)
            reason = random.choice(reasons_in)

        rows.append((product_id, movement_type, quantity, reason, log_date))

    args_str = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s)", row).decode("utf-8")
        for row in rows
    )
    cursor.execute(
        "INSERT INTO inventory_log (product_id, movement_type, quantity, reason, log_date) VALUES " + args_str
    )


if __name__ == "__main__":
    seed_database()
