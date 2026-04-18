"""
FreshMart Chatbot — keyword-based NLP engine + AI Shopping Assistant.
All logic lives here; views.py just calls get_response().
"""

import re
from django.db.models import Q
from .models import Product, Order


# ── Store info ────────────────────────────────────────────────────────────────
STORE_INFO = {
    'name':     'FreshMart',
    'phone':    '+91 6205628253',
    'email':    'Rahulkumar@gmail.com',
    'address':  'Kurji, Chasma Center, Food District, Patna - 80010',
    'hours':    'Monday – Saturday: 8:00 AM – 10:00 PM',
    'delivery': 'Free delivery on orders above ₹500. ₹40 delivery charge below ₹500.',
    'returns':  'Easy returns within 24 hours of delivery. Contact support.',
}


# ── AI Shopping Assistant System Prompt (for reference / future OpenAI use) ───
SHOPPING_ASSISTANT_PROMPT = """
You are an intelligent AI Shopping Assistant for FreshMart.
Help users build a smart grocery cart based on their budget and needs.
- Do NOT exceed the budget
- Prioritize essential daily items: milk, bread, rice, vegetables, fruits
- Show: Product Name, Quantity, Price, Total
- If user writes in Hindi, understand and reply in English
"""


# ── Hardcoded grocery suggestion list (fallback) ──────────────────────────────
GROCERY_ITEMS = [
    {'name': 'Rice',          'qty': '1kg',   'price': 70,  'category': 'grains'},
    {'name': 'Wheat Flour',   'qty': '1kg',   'price': 50,  'category': 'grains'},
    {'name': 'Dal (Lentils)', 'qty': '500g',  'price': 55,  'category': 'grains'},
    {'name': 'Milk',          'qty': '1L',    'price': 60,  'category': 'dairy'},
    {'name': 'Egg',           'qty': '6 pcs', 'price': 60,  'category': 'dairy'},
    {'name': 'Paneer',        'qty': '200g',  'price': 80,  'category': 'dairy'},
    {'name': 'Bread',         'qty': '1 pkt', 'price': 40,  'category': 'bakery'},
    {'name': 'Potato',        'qty': '1kg',   'price': 30,  'category': 'vegetables'},
    {'name': 'Tomato',        'qty': '500g',  'price': 25,  'category': 'vegetables'},
    {'name': 'Onion',         'qty': '1kg',   'price': 35,  'category': 'vegetables'},
    {'name': 'Banana',        'qty': '6 pcs', 'price': 40,  'category': 'fruits'},
    {'name': 'Apple',         'qty': '4 pcs', 'price': 80,  'category': 'fruits'},
    {'name': 'Grapes',        'qty': '500g',  'price': 60,  'category': 'fruits'},
    {'name': 'Tea',           'qty': '100g',  'price': 50,  'category': 'beverages'},
    {'name': 'Biscuit',       'qty': '2 pkt', 'price': 30,  'category': 'snacks'},
    {'name': 'Chips',         'qty': '2 pkt', 'price': 40,  'category': 'snacks'},
    {'name': 'Sugar',         'qty': '1kg',   'price': 45,  'category': 'other'},
    {'name': 'Salt',          'qty': '1kg',   'price': 20,  'category': 'other'},
    {'name': 'Cooking Oil',   'qty': '500ml', 'price': 90,  'category': 'other'},
    {'name': 'Chicken',       'qty': '500g',  'price': 120, 'category': 'meat'},
]


# ── FAQ bank ──────────────────────────────────────────────────────────────────
FAQS = [
    {
        'keywords': ['timing', 'time', 'open', 'close', 'hour', 'working', 'schedule'],
        'answer': (
            "🕐 We are open <b>Monday – Saturday, 8:00 AM – 10:00 PM</b>.<br>"
            "Sunday: 9:00 AM – 8:00 PM.<br>"
            "You can place orders 24/7 on our website!"
        ),
    },
    {
        'keywords': ['payment', 'pay', 'method', 'upi', 'card', 'cod', 'cash', 'online'],
        'answer': (
            "💳 We accept the following payment methods:<br>"
            "• <b>UPI</b> — Google Pay, PhonePe, Paytm, BHIM<br>"
            "• <b>Credit / Debit Card</b> — Visa, Mastercard, RuPay<br>"
            "• <b>QR Code</b> — Scan & pay instantly<br>"
            "• <b>Cash on Delivery (COD)</b> — Pay when your order arrives"
        ),
    },
    {
        'keywords': ['deliver', 'delivery', 'shipping', 'ship', 'fast', 'when', 'arrive', 'reach'],
        'answer': (
            "🚚 Delivery details:<br>"
            "• Orders within Patna: delivered within <b>2–4 hours</b><br>"
            "• Free delivery on orders ₹500 and above<br>"
            "• ₹40 delivery charge for orders below ₹500<br>"
            "• Track your order in <b>My Orders</b> section"
        ),
    },
    {
        'keywords': ['return', 'refund', 'exchange', 'replace', 'damage', 'broken', 'wrong'],
        'answer': (
            "🔄 Our return policy:<br>"
            "• Returns accepted within <b>24 hours</b> of delivery<br>"
            "• Refund processed within 3–5 business days<br>"
            f"• Contact us at <b>{STORE_INFO['email']}</b> "
            f"or call <b>{STORE_INFO['phone']}</b>"
        ),
    },
    {
        'keywords': ['place', 'how', 'order', 'buy', 'purchase', 'shop', 'add', 'cart'],
        'answer': (
            "🛒 How to place an order:<br>"
            "1. Browse products on the <b>Home</b> page<br>"
            "2. Click <b>Add to Cart</b> on any product<br>"
            "3. Go to <b>Cart</b> and review your items<br>"
            "4. Click <b>Proceed to Payment</b><br>"
            "5. Choose a payment method and confirm<br>"
            "That's it — your groceries are on their way! 🎉"
        ),
    },
    {
        'keywords': ['cancel', 'cancellation', 'stop', 'abort'],
        'answer': (
            "❌ To cancel an order:<br>"
            "• Go to <b>My Orders</b><br>"
            "• Click <b>Cancel Order</b> (only for Pending/Processing orders)<br>"
            "• Stock is restored automatically after cancellation<br>"
            "• Shipped or delivered orders cannot be cancelled"
        ),
    },
    {
        'keywords': ['account', 'register', 'signup', 'sign up', 'login',
                     'log in', 'password', 'forgot'],
        'answer': (
            "👤 Account help:<br>"
            "• <a href='/register/'>Register here</a> to create a free account<br>"
            "• <a href='/login/'>Login here</a> if you already have one<br>"
            "• Forgot password? Use the "
            "<a href='/forgot-password/'>Reset Password</a> link on the login page"
        ),
    },
    {
        'keywords': ['contact', 'support', 'help', 'reach', 'phone',
                     'email', 'address', 'location'],
        'answer': (
            f"📞 Contact FreshMart:<br>"
            f"• 📱 Phone: <b>{STORE_INFO['phone']}</b><br>"
            f"• 📧 Email: <b>{STORE_INFO['email']}</b><br>"
            f"• 📍 Address: {STORE_INFO['address']}<br>"
            f"• 🕐 Hours: {STORE_INFO['hours']}"
        ),
    },
    {
        'keywords': ['discount', 'offer', 'coupon', 'promo', 'deal', 'sale', 'cheap'],
        'answer': (
            "🏷️ Current offers:<br>"
            "• <b>Free delivery</b> on orders above ₹500<br>"
            "• Check the home page regularly for seasonal deals<br>"
            "• Subscribe to our newsletter for exclusive offers!"
        ),
    },
    {
        'keywords': ['stock', 'available', 'availability', 'out of stock', 'in stock'],
        'answer': (
            "📦 Product availability:<br>"
            "• Products marked <b>Available</b> are in stock<br>"
            "• Out-of-stock products cannot be added to cart<br>"
            "• Type a product name to check its availability instantly!"
        ),
    },
    {
        'keywords': ['hi', 'hello', 'hey', 'hii', 'helo',
                     'good morning', 'good evening', 'namaste', 'namaskar'],
        'answer': (
            "👋 Hello! Welcome to <b>FreshMart Assistant</b>!<br>"
            "I can help you with:<br>"
            "• 🛒 Budget grocery cart (e.g. <b>₹200 me grocery</b>)<br>"
            "• 📦 Order tracking<br>"
            "• 🔍 Product search & availability<br>"
            "• 💳 Payment & delivery info<br>"
            "• 🕐 Store timings & contact<br><br>"
            "What can I help you with today?"
        ),
    },
    {
        'keywords': ['thank', 'thanks', 'bye', 'goodbye', 'ok', 'okay', 'great', 'nice', 'awesome'],
        'answer': (
            "😊 You're welcome! Happy shopping at <b>FreshMart</b>!<br>"
            "If you need anything else, I'm right here. 🛒"
        ),
    },
]


# ── Helper: clean & tokenise ──────────────────────────────────────────────────

def _clean(text: str) -> str:
    return re.sub(r'[^\w\s]', ' ', text.lower()).strip()


def _tokens(text: str) -> list:
    return _clean(text).split()


# ── FAQ matcher ───────────────────────────────────────────────────────────────

def _match_faq(text: str):
    cleaned    = _clean(text)
    tokens     = set(_tokens(text))
    best_score = 0
    best_ans   = None

    for faq in FAQS:
        score = sum(1 for kw in faq['keywords'] if kw in cleaned or kw in tokens)
        if score > best_score:
            best_score = score
            best_ans   = faq['answer']

    return best_ans if best_score > 0 else None


# ── Product search ────────────────────────────────────────────────────────────

def _search_products(text: str):
    words = [w for w in _tokens(text) if len(w) > 2]
    if not words:
        return None
    q = Q()
    for w in words:
        q |= Q(name__icontains=w) | Q(description__icontains=w) | Q(category__icontains=w)
    products = Product.objects.filter(q, is_available=True)[:3]
    return products if products.exists() else None


def _build_product_reply(products) -> str:
    lines = ["🔍 Here's what I found:<br>"]
    for p in products:
        if p.stock > 5:
            stock_label = "✅ In Stock"
        elif p.stock > 0:
            stock_label = f"⚠️ Only {p.stock} left"
        else:
            stock_label = "❌ Out of Stock"
        lines.append(
            f"<div class='chat-product-card'>"
            f"<b>{p.name}</b> — ₹{p.price}<br>"
            f"<small>{p.get_category_display()} &nbsp;|&nbsp; {stock_label}</small>"
            f"</div>"
        )
    lines.append(
        "<small>Visit the <a href='/'>Home page</a> "
        "to add items to your cart.</small>"
    )
    return "".join(lines)


# ── Order status ──────────────────────────────────────────────────────────────

def _get_order_status(user) -> str:
    if not user or not user.is_authenticated:
        return "🔐 Please <a href='/login/'>log in</a> to check your order status."

    orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
    if not orders.exists():
        return "📭 You haven't placed any orders yet. <a href='/'>Start shopping!</a>"

    lines = ["📦 Your recent orders:<br>"]
    for o in orders:
        pay_badge = {'success': '✅', 'failed': '❌', 'pending': '⏳'}.get(
            o.payment_status, '⏳'
        )
        lines.append(
            f"<div class='chat-order-card'>"
            f"<b>Order #{o.id}</b> — ₹{o.total_amount}<br>"
            f"<small>Status: <b>{o.get_status_display()}</b> &nbsp;|&nbsp; "
            f"Payment: {pay_badge} {o.get_payment_status_display()}<br>"
            f"Placed: {o.created_at:%d %b %Y}</small>"
            f"</div>"
        )
    lines.append("<a href='/orders/'>View all orders →</a>")
    return "".join(lines)


# ── Budget detection ──────────────────────────────────────────────────────────

BUDGET_KEYWORDS = {
    'budget', 'rs', 'rupee', 'rupees', 'under', 'within',
    'mujhe', 'chahiye', 'grocery', 'groceries', 'cart', 'list',
    'shopping', 'items', 'suggest', 'recommend',
    'healthy', 'snacks', 'fruits', 'vegetables', 'daily',
}


def _is_budget_request(text: str) -> bool:
    cleaned    = _clean(text)
    tokens     = set(_tokens(text))
    has_amount = bool(re.search(r'[₹₨]|\brs\b|\d+', cleaned))
    has_budget = bool(tokens & BUDGET_KEYWORDS)
    has_hindi  = any(w in cleaned for w in
                     ['mujhe', 'chahiye', 'mera', 'mere', 'karo', 'dena'])
    return (has_amount and has_budget) or has_hindi


def _extract_budget(text: str):
    cleaned = _clean(text)
    cleaned = (cleaned
               .replace('₹', '')
               .replace('rs', '')
               .replace('rupees', '')
               .replace('rupee', ''))
    numbers = re.findall(r'\d+', cleaned)
    return max(int(n) for n in numbers) if numbers else None


# ── Budget cart builder ───────────────────────────────────────────────────────

def _build_budget_cart(budget: int) -> str:

    # ── Try real DB products first ────────────────────────────────────────────
    db_products = Product.objects.filter(
        is_available=True, stock__gt=0
    ).order_by('price')

    if db_products.exists():
        cart      = []
        remaining = budget
        priority  = ['grains', 'dairy', 'vegetables', 'fruits',
                      'bakery', 'beverages', 'snacks', 'other']
        used_cats = set()

        for cat in priority:
            if remaining <= 0:
                break
            product = db_products.filter(
                category=cat, price__lte=remaining
            ).first()
            if product and cat not in used_cats:
                cart.append({
                    'name':  product.name,
                    'qty':   '1',
                    'price': float(product.price),
                })
                remaining -= float(product.price)
                used_cats.add(cat)

        # Fill remaining budget
        names_in_cart = [i['name'] for i in cart]
        for product in db_products.filter(price__lte=remaining):
            if remaining <= 0:
                break
            if product.name not in names_in_cart:
                cart.append({
                    'name':  product.name,
                    'qty':   '1',
                    'price': float(product.price),
                })
                remaining     -= float(product.price)
                names_in_cart.append(product.name)

        if cart:
            return _format_cart(cart, budget)

    # ── Fallback: hardcoded list ───────────────────────────────────────────────
    cart      = []
    remaining = budget
    priority  = ['grains', 'dairy', 'vegetables', 'fruits',
                  'bakery', 'beverages', 'snacks', 'other']
    used_cats = set()

    for cat in priority:
        if remaining <= 0:
            break
        candidates = [
            i for i in GROCERY_ITEMS
            if i['category'] == cat
            and i['price'] <= remaining
            and cat not in used_cats
        ]
        if candidates:
            item = candidates[0]
            cart.append(item)
            remaining -= item['price']
            used_cats.add(cat)

    # Fill remaining
    for item in GROCERY_ITEMS:
        if remaining <= 0:
            break
        if item not in cart and item['price'] <= remaining:
            cart.append(item)
            remaining -= item['price']

    if not cart:
        return (
            f"😔 Budget of ₹{budget} is too low for suggestions.<br>"
            "Please try with ₹100 or more."
        )

    return _format_cart(cart, budget)


def _format_cart(cart: list, budget: int) -> str:
    total = sum(i['price'] for i in cart)
    lines = [
        "✅ <b>I created a budget-friendly cart for you!</b><br><br>",
        "🛍️ <b>Your Cart:</b><br>",
    ]
    for idx, item in enumerate(cart, 1):
        price = item['price']
        lines.append(
            f"<b>{idx}.</b> {item['name']} "
            f"— {item['qty']} "
            f"— <b>₹{price:.0f}</b><br>"
        )
    lines.append(f"<br>💰 <b>Total: ₹{total:.0f}</b>")
    lines.append(f" &nbsp;|&nbsp; Budget: ₹{budget}")
    saved = budget - total
    if saved > 0:
        lines.append(f"<br>💵 You saved: <b>₹{saved:.0f}</b>")
    lines.append(
        "<br><br>💡 <b>Tip:</b> Visit our "
        "<a href='/'>Home page</a> to add these to your cart!"
    )
    return "".join(lines)


# ── Keyword sets ──────────────────────────────────────────────────────────────

ORDER_KEYWORDS = {
    'order', 'orders', 'track', 'tracking', 'status',
    'where', 'shipped', 'delivered', 'my order',
}
PRODUCT_STOP_WORDS = {
    'what', 'when', 'how', 'why', 'is', 'the', 'are', 'does',
    'do', 'can', 'tell', 'show', 'about', 'much', 'cost', 'price',
}


# ── Main entry point ──────────────────────────────────────────────────────────

def get_response(text: str, user=None) -> str:
    """
    Called by views.py chatbot_api.
    Returns an HTML string shown in the chat bubble.
    """
    if not text or not text.strip():
        return "Please type a message and I'll be happy to help! 😊"

    cleaned = _clean(text)
    tokens  = set(_tokens(text))

    # 1. Greeting / farewell — highest priority
    greet_words = {
        'hi', 'hello', 'hey', 'hii', 'namaste',
        'bye', 'goodbye', 'thank', 'thanks',
    }
    if tokens & greet_words:
        answer = _match_faq(text)
        if answer:
            return answer

    # 2. Budget / shopping cart request
    if _is_budget_request(text):
        budget = _extract_budget(text)
        if budget:
            return _build_budget_cart(budget)
        return (
            "💰 Please mention your budget amount!<br>"
            "Examples:<br>"
            "• <b>₹200 me grocery chahiye</b><br>"
            "• <b>Healthy items under ₹300</b><br>"
            "• <b>Snacks under ₹100</b>"
        )

    # 3. Order tracking
    if tokens & ORDER_KEYWORDS:
        faq = _match_faq(text)
        if faq and ('how' in tokens or 'place' in tokens or 'buy' in tokens):
            return faq
        return _get_order_status(user)

    # 4. FAQ matching
    faq_answer = _match_faq(text)
    if faq_answer:
        return faq_answer

    # 5. Product search
    search_tokens = tokens - PRODUCT_STOP_WORDS - ORDER_KEYWORDS
    if search_tokens:
        products = _search_products(text)
        if products:
            return _build_product_reply(products)

    # 6. Fallback
    return (
        "🤔 I'm not sure about that. Here's what I can help with:<br>"
        "<ul style='margin:6px 0 0 16px;padding:0'>"
        "<li>Type <b>₹200 me grocery</b> for a budget cart</li>"
        "<li>Type a <b>product name</b> to check price & availability</li>"
        "<li>Ask about <b>my order</b> to see order status</li>"
        "<li>Ask about <b>delivery</b>, <b>payment</b>, or <b>timings</b></li>"
        "<li>Type <b>contact</b> for support details</li>"
        "</ul>"
    )