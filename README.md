# 🛒 FreshMart — Grocery Store Management System

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📌 Introduction

**FreshMart** is a full-featured, web-based **Grocery Store Management System**
built with **Django (Python)**. It provides a complete online shopping experience
for customers and a powerful control panel for administrators.

The system includes an integrated **AI-powered Shopping Assistant** that helps
users build optimized grocery carts based on their budget and daily needs —
making grocery shopping smarter, faster, and more affordable.

> 🎯 Built as a real-world Django project covering authentication, payments,
> order management, admin control, email notifications, and AI chat assistance.

---

## ✨ Features

### 👤 User Features
- ✅ User Registration & Login (secure authentication)
- ✅ Forgot Password with email-based secure reset link
- ✅ Browse products with search & category filter
- ✅ Add to Cart / Remove / Update quantity
- ✅ Checkout with multiple payment methods
- ✅ QR Code payment generation (UPI)
- ✅ Order tracking & cancellation
- ✅ Order history (active & cancelled)
- ✅ AI Shopping Assistant (budget-based smart cart)
- ✅ Real-time chatbot support

### 🛠️ Admin Features
- ✅ Full Admin Panel with custom branding
- ✅ Product Management (Add / Edit / Delete)
- ✅ Order Management with status updates
- ✅ User Management with order history inline
- ✅ Cart Management & monitoring
- ✅ Chat History logs
- ✅ Daily Sales Report (CSV & Print)
- ✅ Revenue charts & analytics dashboard
- ✅ Low stock alerts

### 📧 Email System
- ✅ Password reset emails via Gmail SMTP
- ✅ Password change confirmation emails
- ✅ HTML-formatted professional emails
- ✅ Secure token-based reset (expires in 5 minutes)

---

## 🤖 AI Shopping Assistant

FreshMart includes a smart **AI-powered chatbot** embedded on every page
(bottom-right corner, WhatsApp-style).

### How it works:
1. User types their budget — e.g., `₹200 me grocery chahiye`
2. The assistant **automatically generates** an optimized cart
3. Items are selected based on **daily essentials first**
   (grains → dairy → vegetables → fruits → snacks)
4. Total stays **within the given budget**
5. Shows savings and a direct link to shop

### Example:
🛍️ Your Cart:
   1. Rice — 1kg — ₹70
   2. Milk — 1L  — ₹60
   3. Bread — 1 pkt — ₹40
   4. Potato — 1kg — ₹30
   5. Banana — 6 pcs — ₹40
   6. Dal (Lentils) — 500g — ₹55

   ### Other chatbot capabilities:
| Query Type | Example |
|---|---|
| Budget Cart | `₹200 me grocery`, `snacks under 100` |
| Product Search | `Show me milk`, `is rice available?` |
| Order Tracking | `Where is my order?`, `my order status` |
| Store Info | `What are your timings?`, `contact` |
| Payment Help | `What payment methods?`, `UPI` |
| Returns | `Return policy`, `refund` |
| Hindi Support | `mujhe grocery chahiye`, `kya available hai` |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.14** | Backend language |
| **Django 6.0** | Web framework |
| **SQLite** | Default database (development) |
| **HTML5 / CSS3** | Frontend structure & styling |
| **Bootstrap 5.3** | Responsive UI components |
| **JavaScript (ES6)** | Frontend interactivity |
| **Chart.js** | Sales analytics charts |
| **qrcode (PIL)** | QR code generation for UPI |
| **Gmail SMTP** | Email sending (password reset, notifications) |
| **Django ORM** | Database queries & management |

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher installed
- pip package manager
- Git installed
- A Gmail account with 2-Step Verification enabled

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/freshmart.git
cd freshmart
```

---

### Step 2 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install django
pip install qrcode[pil]
pip install pillow
```

Or if a `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

---

### Step 4 — Navigate to Project Folder

```bash
cd grocery_store_management_system
```

---

### Step 5 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 6 — Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter your preferred:
- Username
- Email address
- Password (min 8 characters, must include letters + numbers)

---

### Step 7 — Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:

---

## 📧 Email Configuration (Gmail SMTP)

To enable real email sending (Forgot Password, notifications):

### Step 1 — Enable Gmail 2-Step Verification
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Turn on **2-Step Verification**

### Step 2 — Generate App Password
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. App name: type `Django` → click **Create**
3. Copy the **16-character password** shown

### Step 3 — Update `settings.py`

```python
# At the bottom of settings.py
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 465
EMAIL_USE_SSL       = True
EMAIL_USE_TLS       = False
EMAIL_HOST_USER     = 'your_gmail@gmail.com'       # ← your Gmail
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'        # ← 16-char App Password
DEFAULT_FROM_EMAIL  = 'FreshMart <your_gmail@gmail.com>'
PASSWORD_RESET_TIMEOUT = 300                       # 5 minutes
```

### Step 4 — Test Email in Django Shell

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'FreshMart email is working!',
    settings.DEFAULT_FROM_EMAIL,
    [settings.EMAIL_HOST_USER],
    fail_silently=False,
)
print('✅ Email sent successfully!')
```

---

## 🚀 Usage Guide

### For Customers

| Action | Steps |
|---|---|
| **Register** | Go to `/register/` → Fill in name, username, email, password |
| **Login** | Go to `/login/` → Enter username & password |
| **Browse Products** | Home page — search by name or filter by category |
| **Add to Cart** | Click **Add to Cart** on any product |
| **Checkout** | Go to Cart → Proceed to Payment → Choose method → Place Order |
| **Track Order** | Go to **My Orders** → See live status |
| **Cancel Order** | My Orders → Cancel (only Pending/Processing orders) |
| **Forgot Password** | Login page → Forgot Password? → Enter email → Check inbox |
| **AI Assistant** | Click 🛒 chat button (bottom-right) → Type your budget |

### For AI Shopping Assistant

---

## 🔐 Admin Panel

Access the admin panel at: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created.

### Admin Capabilities

| Section | What Admin Can Do |
|---|---|
| **Products** | Add, Edit, Delete products — manage price, stock, category, image |
| **Orders** | View all orders, update status (Pending → Processing → Shipped → Delivered) |
| **Order Items** | View individual items per order with line totals |
| **Users** | View all registered users, see their order history inline |
| **Carts** | Monitor active carts across all users |
| **Chat History** | View all chatbot conversations (read-only log) |
| **Groups** | Manage user permission groups |

### Custom Admin Dashboard

Go to `/dashboard/` for:
- 📊 Revenue chart (last 7 days)
- 🥧 Top products doughnut chart
- 📦 Today's product sales table
- ⚠️ Low stock alerts
- 🕐 Recent orders summary
- 📥 Export CSV report
- 🖨️ Print sales report

---

## 📁 Project Structure


grocery_store_management_system/
│
├── grocery_store_management_system/   # Django project config
│   ├── settings.py                    # All settings (DB, email, static)
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── store/                             # Main application
│   ├── models.py                      # Product, Cart, Order, OrderItem, ChatHistory
│   ├── views.py                       # All view functions
│   ├── urls.py                        # App URL patterns (22+ routes)
│   ├── forms.py                       # RegisterForm, LoginForm, ProductForm
│   ├── admin.py                       # Custom admin panel configuration
│   └── chatbot.py                     # AI chatbot engine
│
├── templates/store/                   # All HTML templates
│   ├── base.html                      # Base template with chatbot widget
│   ├── home.html                      # Product listing page
│   ├── login.html / register.html     # Auth pages
│   ├── cart.html                      # Shopping cart
│   ├── payment.html                   # Payment & QR code
│   ├── order_history.html             # User orders
│   ├── admin_dashboard.html           # Admin analytics dashboard
│   ├── forgot_password.html           # Password reset flow
│   └── emails/                        # HTML email templates
│       ├── password_reset_email.html
│       └── password_changed_email.html
│
├── static/css/
│   └── style.css                      # Custom styles
│
├── media/products/                    # Uploaded product images
├── db.sqlite3                         # SQLite database
├── manage.py                          # Django management utility
└── README.md                          # This file


---

## 🔮 Future Enhancements

- [ ] 🎙️ **Voice Search** — Search products using voice input
- [ ] 🤖 **OpenAI Integration** — Connect real GPT API for smarter chatbot responses
- [ ] 📊 **Advanced Analytics** — Weekly/monthly sales trends, profit margins
- [ ] 📱 **Mobile App** — React Native or Flutter mobile version
- [ ] 🏷️ **Coupon / Promo Codes** — Discount code system at checkout
- [ ] ⭐ **Product Reviews** — Customer ratings and review system
- [ ] 🔔 **Push Notifications** — Real-time order status notifications
- [ ] 🌍 **Multi-language Support** — Hindi & regional language UI
- [ ] 💳 **Real Payment Gateway** — Razorpay / Stripe live integration
- [ ] 📦 **Delivery Tracking** — Real-time delivery location tracking
- [ ] 🧾 **Invoice Generation** — PDF invoice download per order
- [ ] 📧 **Newsletter System** — Email marketing for offers and deals

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|---|---|
| `SMTPAuthenticationError 535` | Use Gmail App Password, not your login password |
| `admin.E122 list_editable error` | Ensure field is in `list_display` before `list_editable` |
| `No module named qrcode` | Run `pip install qrcode[pil]` |
| `TemplateDoesNotExist` | Check template folder path and `TEMPLATES DIRS` in settings |
| `Port 587 timeout` | Switch to `EMAIL_PORT = 465` with `EMAIL_USE_SSL = True` |

---

## 👨‍💻 Author

**Rahul Kumar**
- 🎓 B.Sc. IT Student — CIMAGE College, Patna
- 📧 Email: rahul.bscitstudent23.12239@cimage.in
- 🌐 Project: FreshMart Grocery Store Management System
- 📅 Year: 2026

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this project with attribution.

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

Made with ❤️ using Django & Python

</div>



grocery_store_management_system/   ← your project root
│
├── README.md                      ← place it HERE
├── manage.py
├── db.sqlite3
├── store/
└── grocery_store_management_system/