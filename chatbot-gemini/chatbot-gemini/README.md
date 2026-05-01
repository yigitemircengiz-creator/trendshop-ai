# TrendShop AI Customer Chatbot

An e-commerce customer service chatbot powered by Claude API, built with Flask.

## Features

- **Order lookup** — Instant info by order number (TS-XXXXX) or email address
- **Product & stock info** — Prices, availability, size/color options
- **Return guidance** — Policy explanations and step-by-step instructions
- **Shipping tracking** — Tracking number and estimated delivery
- **Conversation memory** — Context is maintained throughout the session

## Setup

```bash
# 1. Enter the project folder
cd chatbot-en

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env
# Fill in your ANTHROPIC_API_KEY in the .env file

# 5. Run
python app.py
```

App runs at http://localhost:5000

## Test Data

| Order No   | Status             | Customer        |
|------------|--------------------|-----------------|
| TS-10042   | In transit         | Alice Johnson   |
| TS-10038   | Delivered          | James Carter    |
| TS-10055   | Processing         | Sophie Williams |
| TS-10021   | Return in progress | Daniel Brown    |

Email lookup: `alice.johnson@email.com`

## Project Structure

```
chatbot-en/
├── app.py              # Flask backend, Claude API integration
├── orders.py           # Mock order database
├── requirements.txt
├── .env.example
└── templates/
    └── index.html      # Chat UI
```

## Moving to Production

Replace the mock data in `orders.py` with real database queries:

```python
import psycopg2

def get_order_by_id(order_id: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    return cur.fetchone()
```

## Ideas for Further Development

- [ ] User authentication (customer login)
- [ ] Real database integration (PostgreSQL)
- [ ] Webhook-based order update notifications
- [ ] Multi-language support
- [ ] Admin dashboard (conversation history tracking)
- [ ] WhatsApp / Telegram integration
