from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import Category, MenuItem,Customer,Coupons,FlashOffer,DeliveryCharge,ScrollingText,Loading,WebsiteOrder,WebsiteItems,UserCoupon
class CategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'move_up_down_links')
    actions = ['move_up', 'move_down']

    def move_up(self, request, queryset):
        for category in queryset:
            category.move(-1)
    move_up.short_description = "Move selected categories up"

    def move_down(self, request, queryset):
        for category in queryset:
            category.move(+1)
    move_down.short_description = "Move selected categories down"
admin.site.register(Category, CategoryAdmin)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

class CouponAdmin(admin.ModelAdmin):
    list_display=('coupon_name','description','coupon_amount')


admin.site.register(MenuItem, MenuItemAdmin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'phone')

# Register the Customer model with the custom admin class
admin.site.register(Customer, CustomerAdmin)
class FlashOfferAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Check if there's already an existing FlashOffer object
        existing_objects_count = FlashOffer.objects.count()
        return existing_objects_count == 0
# Register the FlashOffer model with the custom admin class
admin.site.register(FlashOffer, FlashOfferAdmin)
admin.site.register(ScrollingText)
class DeliveryChargeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'mininum_order')

    def has_add_permission(self, request):
        # Check if there's already an existing DeliveryCharge object
        existing_objects_count = DeliveryCharge.objects.count()
        return existing_objects_count == 0

# Register the DeliveryCharge model with the custom admin class
admin.site.register(DeliveryCharge, DeliveryChargeAdmin)
admin.site.register(Coupons,CouponAdmin)
class LoadingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Check if there's already an existing Loading object
        existing_objects_count = Loading.objects.count()
        return existing_objects_count == 0

# Register the Loading model with the custom admin class
admin.site.register(Loading, LoadingAdmin)

class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'used')
    list_filter = ('used',)
    search_fields = ('user__username', 'coupon__coupon_name')

# Register the UserCoupon model with the custom admin class
admin.site.register(UserCoupon, UserCouponAdmin)

class ItemInline(admin.TabularInline):
    model = WebsiteItems
    extra = 1
@admin.register(WebsiteOrder)
class WebsiteOrderAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'user', 'name', 'phone', 'address', 'order_status', 'total')
    list_filter = ('order_status',)
    inlines=[ItemInline]