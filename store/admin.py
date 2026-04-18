from django.contrib             import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.utils.html          import format_html
from django.db.models           import Sum, Count
from .forms                     import ProductForm
from .models                    import Product, Cart, Order, OrderItem, ChatHistory


# ── Unregister defaults so we can re-register with customization ──────────────
admin.site.unregister(User)
admin.site.unregister(Group)


# ── Admin site branding ───────────────────────────────────────────────────────
admin.site.site_header  = '🛒 FreshMart Admin'
admin.site.site_title   = 'FreshMart Admin Portal'
admin.site.index_title  = 'Welcome to FreshMart Admin Panel'


# ════════════════════════════════════════════════════════
# PRODUCT ADMIN
# ════════════════════════════════════════════════════════
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form            = ProductForm          # reuse the same validated form
    list_display    = ['name', 'category_badge', 'price_display',
                       'stock_display', 'is_available', 'created_at']
    list_filter     = ['category', 'is_available', 'created_at']
    search_fields   = ['name', 'description', 'category']
    list_editable   = ['is_available']
    ordering        = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page   = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Category')
    def category_badge(self, obj):
        colors = {
            'fruits':    '#28a745',
            'dairy':     '#17a2b8',
            'bakery':    '#fd7e14',
            'beverages': '#6610f2',
            'snacks':    '#e83e8c',
            'grains':    '#795548',
            'meat':      '#dc3545',
            'frozen':    '#0dcaf0',
            'personal':  '#6f42c1',
            'household': '#20c997',
            'other':     '#6c757d',
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 8px;'
            'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, obj.get_category_display()
        )

    @admin.display(description='Price')
    def price_display(self, obj):
        return format_html('<strong>₹{}</strong>', obj.price)

    @admin.display(description='Stock')
    def stock_display(self, obj):
        if obj.stock == 0:
            color, label = '#dc3545', 'Out of Stock'
        elif obj.stock <= 5:
            color, label = '#ffc107', f'⚠ {obj.stock} left'
        else:
            color, label = '#28a745', str(obj.stock)
        return format_html(
            '<span style="color:{};font-weight:600;">{}</span>',
            color, label
        )


# ════════════════════════════════════════════════════════
# ORDER ITEM INLINE (used inside OrderAdmin)
# ════════════════════════════════════════════════════════
class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    extra           = 0
    readonly_fields = ['product', 'quantity', 'price', 'line_total']
    can_delete      = False

    @admin.display(description='Line Total')
    def line_total(self, obj):
        return format_html('<strong>₹{}</strong>', obj.get_total_price())


# ════════════════════════════════════════════════════════
# ORDER ADMIN  ← FIXED: status in list_display so list_editable works
# ════════════════════════════════════════════════════════
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # ↓ 'status' is the raw field — required for list_editable to work
    list_display    = ['order_id', 'customer', 'total_display',
                       'payment_badge', 'status', 'pay_status_badge', 'created_at']
    list_filter     = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields   = ['id', 'user__username', 'user__email', 'transaction_id']
    list_editable   = ['status']   # works because 'status' is in list_display above
    inlines         = [OrderItemInline]
    ordering        = ['-created_at']
    readonly_fields = ['user', 'total_amount', 'payment_method',
                       'payment_status', 'transaction_id', 'created_at', 'updated_at']
    list_per_page   = 20

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'total_amount', 'status')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Order #')
    def order_id(self, obj):
        # ↓ typo fixed: was '#{}}'  now '#{}'
        return format_html('<strong>#{}</strong>', obj.id)

    @admin.display(description='Customer')
    def customer(self, obj):
        return format_html(
            '<span title="{}">{}</span>',
            obj.user.email, obj.user.username
        )

    @admin.display(description='Amount')
    def total_display(self, obj):
        return format_html('<strong>₹{}</strong>', obj.total_amount)

    @admin.display(description='Payment Method')
    def payment_badge(self, obj):
        colors = {
            'upi':  '#6610f2',
            'card': '#0d6efd',
            'cod':  '#28a745',
            'qr':   '#fd7e14',
        }
        color = colors.get(obj.payment_method, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:10px;font-size:11px;">{}</span>',
            color, obj.get_payment_method_display()
        )

    @admin.display(description='Pay Status')
    def pay_status_badge(self, obj):
        colors = {
            'success': '#28a745',
            'failed':  '#dc3545',
            'pending': '#ffc107',
        }
        text_colors = {
            'success': '#fff',
            'failed':  '#fff',
            'pending': '#000',
        }
        color = colors.get(obj.payment_status, '#6c757d')
        tc    = text_colors.get(obj.payment_status, '#fff')
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;">{}</span>',
            color, tc, obj.get_payment_status_display()
        )


# ════════════════════════════════════════════════════════
# ORDER ITEM ADMIN
# ════════════════════════════════════════════════════════
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display    = ['id', 'order_link', 'product', 'quantity',
                       'unit_price', 'line_total']
    search_fields   = ['order__id', 'product__name', 'order__user__username']
    list_filter     = ['product__category']
    ordering        = ['-order__created_at']
    readonly_fields = ['order', 'product', 'quantity', 'price']
    list_per_page   = 25

    @admin.display(description='Order')
    def order_link(self, obj):
        return format_html(
            '<strong>Order #{}</strong> — {}',
            obj.order.id, obj.order.user.username
        )

    @admin.display(description='Unit Price')
    def unit_price(self, obj):
        return format_html('₹{}', obj.price)

    @admin.display(description='Line Total')
    def line_total(self, obj):
        return format_html('<strong>₹{}</strong>', obj.get_total_price())


# ════════════════════════════════════════════════════════
# CART ADMIN
# ════════════════════════════════════════════════════════
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display    = ['id', 'user', 'product', 'quantity',
                       'item_total', 'added_at']
    search_fields   = ['user__username', 'user__email', 'product__name']
    list_filter     = ['added_at', 'product__category']
    ordering        = ['-added_at']
    readonly_fields = ['user', 'product', 'added_at']
    list_per_page   = 25

    @admin.display(description='Item Total')
    def item_total(self, obj):
        return format_html('₹{}', obj.get_total_price())


# ════════════════════════════════════════════════════════
# CHAT HISTORY ADMIN
# ════════════════════════════════════════════════════════
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display    = ['id', 'user_display', 'message_preview',
                       'response_preview', 'created_at']
    list_filter     = ['created_at']
    search_fields   = ['user__username', 'message', 'session_key']
    ordering        = ['-created_at']
    readonly_fields = ['user', 'session_key', 'message', 'response', 'created_at']
    list_per_page   = 30

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description='User')
    def user_display(self, obj):
        if obj.user:
            return format_html(
                '<span style="font-weight:600;color:#198754;">{}</span>',
                obj.user.username
            )
        return format_html('<span style="color:#aaa;">Guest</span>')

    @admin.display(description='Message')
    def message_preview(self, obj):
        text = obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
        return format_html('<span title="{}">{}</span>', obj.message, text)

    @admin.display(description='Response')
    def response_preview(self, obj):
        from django.utils.html import strip_tags
        plain = strip_tags(obj.response)
        text  = plain[:60] + '...' if len(plain) > 60 else plain
        return format_html('<span style="color:#666;">{}</span>', text)


# ════════════════════════════════════════════════════════
# ORDER INLINE (used inside UserAdmin)
# ════════════════════════════════════════════════════════
class OrderInline(admin.TabularInline):
    model               = Order
    extra               = 0
    max_num             = 5
    readonly_fields     = ['total_amount', 'status', 'payment_method',
                           'payment_status', 'created_at']
    can_delete          = False
    verbose_name        = 'Recent Order'
    verbose_name_plural = 'Recent Orders'
    fields              = ['total_amount', 'status', 'payment_method',
                           'payment_status', 'created_at']
    ordering            = ['-created_at']


# ════════════════════════════════════════════════════════
# USER ADMIN (enhanced)
# ════════════════════════════════════════════════════════
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['username', 'email', 'full_name', 'is_staff',
                     'is_active', 'date_joined', 'order_count']
    list_filter   = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering      = ['-date_joined']
    list_per_page = 25
    inlines       = [OrderInline]

    @admin.display(description='Full Name')
    def full_name(self, obj):
        name = f'{obj.first_name} {obj.last_name}'.strip()
        return name or format_html('<span style="color:#aaa;">—</span>')

    @admin.display(description='Orders')
    def order_count(self, obj):
        count = Order.objects.filter(user=obj).count()
        if count:
            return format_html(
                '<span style="background:#198754;color:#fff;padding:2px 8px;'
                'border-radius:10px;font-size:11px;">{} order{}</span>',
                count, 's' if count != 1 else ''
            )
        return format_html('<span style="color:#aaa;">0 orders</span>')


# ════════════════════════════════════════════════════════
# GROUP ADMIN
# ════════════════════════════════════════════════════════
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass