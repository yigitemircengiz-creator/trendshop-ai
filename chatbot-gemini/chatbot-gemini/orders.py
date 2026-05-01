"""
Mock e-commerce database - Replace with PostgreSQL/MongoDB in production.
"""

ORDERS = {
    "TS-10042": {
        "order_id": "TS-10042",
        "customer_name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "status": "in_transit",
        "status_detail": "Package is with the courier, expected delivery tomorrow",
        "cargo_company": "FedEx",
        "tracking_number": "FX7834521098",
        "items": [
            {"name": "Nike Air Max 270", "size": "US 9", "color": "Black", "quantity": 1, "price": 149.99},
            {"name": "Sports Socks Pack (5 pairs)", "quantity": 1, "price": 12.99}
        ],
        "total": 162.98,
        "order_date": "2025-04-27",
        "estimated_delivery": "2025-05-02",
        "address": "Brooklyn, New York"
    },
    "TS-10038": {
        "order_id": "TS-10038",
        "customer_name": "James Carter",
        "email": "james.c@gmail.com",
        "status": "delivered",
        "status_detail": "Delivered 2 days ago",
        "cargo_company": "UPS",
        "tracking_number": "UPS9012345678",
        "items": [
            {"name": "Samsung Galaxy Tab A9", "storage": "128GB", "quantity": 1, "price": 349.99},
            {"name": "Tablet Case", "color": "Navy Blue", "quantity": 1, "price": 24.99}
        ],
        "total": 374.98,
        "order_date": "2025-04-22",
        "delivery_date": "2025-04-29",
        "address": "Austin, Texas"
    },
    "TS-10055": {
        "order_id": "TS-10055",
        "customer_name": "Sophie Williams",
        "email": "sophie.williams@hotmail.com",
        "status": "processing",
        "status_detail": "Your order is being prepared at the warehouse",
        "items": [
            {"name": "Levi's 501 Jeans", "size": "28/32", "color": "Light Blue", "quantity": 2, "price": 79.99},
            {"name": "White Basic T-Shirt", "size": "M", "quantity": 3, "price": 14.99}
        ],
        "total": 204.95,
        "order_date": "2025-04-30",
        "estimated_delivery": "2025-05-04",
        "address": "Chicago, Illinois"
    },
    "TS-10021": {
        "order_id": "TS-10021",
        "customer_name": "Daniel Brown",
        "email": "daniel.brown@email.com",
        "status": "return_in_progress",
        "status_detail": "Return approved, shipping label sent to your email",
        "items": [
            {"name": "Adidas Superstar", "size": "US 10", "color": "White", "quantity": 1, "price": 99.99}
        ],
        "total": 99.99,
        "order_date": "2025-04-15",
        "return_reason": "Wrong size",
        "refund_eta": "2025-05-05"
    }
}

PRODUCTS = [
    {
        "id": "P001",
        "name": "Nike Air Max 270",
        "category": "Footwear",
        "price": 149.99,
        "stock": 23,
        "sizes": ["US 6", "US 7", "US 8", "US 9", "US 10", "US 11", "US 12"],
        "colors": ["Black", "White", "Red"],
        "rating": 4.8,
        "description": "Max Air cushioning for all-day comfort"
    },
    {
        "id": "P002",
        "name": "Samsung Galaxy Tab A9",
        "category": "Electronics",
        "price": 349.99,
        "stock": 7,
        "storage": ["64GB", "128GB"],
        "colors": ["Gray", "Silver", "Navy"],
        "rating": 4.6,
        "description": "11-inch display, 8000mAh battery"
    },
    {
        "id": "P003",
        "name": "Levi's 501 Original Jeans",
        "category": "Clothing",
        "price": 79.99,
        "stock": 0,
        "sizes": ["28/30", "28/32", "30/30", "30/32", "32/32", "34/32"],
        "colors": ["Light Blue", "Dark Blue", "Black"],
        "rating": 4.9,
        "description": "Classic straight fit, 100% cotton",
        "stock_note": "Out of stock, restocking in 1-2 weeks"
    },
    {
        "id": "P004",
        "name": "Dyson V15 Detect",
        "category": "Home Appliances",
        "price": 749.99,
        "stock": 3,
        "rating": 4.9,
        "description": "Laser dust detection, 60-minute battery"
    },
    {
        "id": "P005",
        "name": "Adidas Superstar",
        "category": "Footwear",
        "price": 99.99,
        "stock": 15,
        "sizes": ["US 5", "US 6", "US 7", "US 8", "US 9", "US 10", "US 11"],
        "colors": ["White/Black", "Black/White", "Gold"],
        "rating": 4.7,
        "description": "Iconic shell-toe street style sneaker"
    }
]


def get_order_by_id(order_id: str) -> dict | None:
    return ORDERS.get(order_id.upper())


def get_orders_by_email(email: str) -> list:
    return [
        order for order in ORDERS.values()
        if order.get('email', '').lower() == email.lower()
    ]


def get_all_products() -> list:
    return PRODUCTS


def get_product_by_name(name: str) -> dict | None:
    name_lower = name.lower()
    for product in PRODUCTS:
        if name_lower in product['name'].lower():
            return product
    return None
