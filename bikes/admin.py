from django.contrib import admin
from .models import Footer
from .models import AboutSection, AboutSection3Image
from .models import SellBikePage, HowItWorks
from .models import LoginPageContent
from .models import Contact
from .models import HeroSection, HeroBikeImage, InfoSection, SupportFeature
from .models import Location, BuyBike
from .models import LastSection, LastSectionImage
from django.utils.html import format_html   
from .models import HomepageBanner, StatItem
from .models import TestimonialsSection, Testimonial
from .models import TrustedSection
from .models import FAQ


class LastSectionImageInline(admin.TabularInline):
    model = LastSectionImage
    extra = 1
    fields = ("image_preview", "image", "title", "order_no", "alt_text")
    readonly_fields = ("image_preview",)
    ordering = ("order_no",)

    def image_preview(self, obj):
        # defensive: obj might be None in the "add new" inline row
        if obj and getattr(obj, "image", None):
            try:
                return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
            except Exception:
                # if image.url access fails for some reason, return a placeholder text
                return "(image)"
        return ""
    image_preview.short_description = "Preview"


@admin.register(LastSection)
class LastSectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "created_at", "updated_at")
    inlines = [LastSectionImageInline]
    search_fields = ("heading",)
    ordering = ("-created_at",)




class HeroBikeImageInline(admin.TabularInline):  # or StackedInline if you prefer
    model = HeroBikeImage
    extra = 1  # show 1 empty form by default
    fields = ("image", "order")
    ordering = ("order",)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text")
    list_display_links = ("title",)
    inlines = [HeroBikeImageInline]

@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ("order","id","button_text")
    list_editable = ("order",)
    list_display_links = ("id",)

@admin.register(SupportFeature)
class SupportFeatureAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "arrow")
    list_editable = ("order",)
    list_display_links = ("title",)
    search_fields = ("title", "subtitle", "description")
   

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)



@admin.register(BuyBike)
class BuyBikeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "brand", "bike_model", "bike_variant", "price",
        "year", "kilometers", "owners", "transmission", "is_booked"
    )
    list_filter = (
        "brand", "category", "year", "fuel_type", "color", "is_booked",
        "refurbished", "registration_certificate", "finance", "insurance", "warranty",
        "owners", "transmission", "location"
    )
    search_fields = ("title", "brand", "description", "bike_model", "bike_variant")

    readonly_fields = (
        "created_at", "updated_at", 
        "featured_image_preview", 
        "variant1_preview", "variant2_preview",
        "variant3_preview", "variant4_preview", "variant5_preview"
    )

    def featured_image_preview(self, obj):
        if obj and obj.featured_image:
            return format_html('<img src="{}" style="max-height:120px;"/>', obj.featured_image.url)
        return ""
    featured_image_preview.short_description = "Featured preview"

    def variant1_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;"/>', obj.variant_image1.url) if obj.variant_image1 else ""
    def variant2_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;"/>', obj.variant_image2.url) if obj.variant_image2 else ""
    def variant3_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;"/>', obj.variant_image3.url) if obj.variant_image3 else ""
    def variant4_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;"/>', obj.variant_image4.url) if obj.variant_image4 else ""
    def variant5_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;"/>', obj.variant_image5.url) if obj.variant_image5 else ""

    fieldsets = (
        ("Basic", {
            "fields": (
                "title",
                "description",
                ("price", "location"),
                "featured_image_preview",
                ("featured_image", "card_bg_image"),
            )
        }),
        ("Variant Thumbnails", {
            "fields": (
                "variant1_preview", "variant_image1",
                "variant2_preview", "variant_image2",
                "variant3_preview", "variant_image3",
                "variant4_preview", "variant_image4",
                "variant5_preview", "variant_image5",
            )
        }),
        ("Identity", {
            "fields": (
                ("brand", "category"),
                ("bike_model", "bike_variant"),
                ("year", "registration_year"),
            )
        }),
        ("Specifications", {
            "classes": ("wide",),
            "fields": (
                ("color", "fuel_type"),
                ("ignition_type", "transmission"),
                ("front_brake_type", "rear_brake_type"),
                ("abs", "odometer", "wheel_type"),
                ("engine_cc", "kilometers"),
            ),
        }),
        ("Ownership & RTO", {
            "fields": (
                ("owner", "owners"),
                ("rto_state", "rto_city"),
            )
        }),
        ("Flags & Status", {
            "fields": (
                "refurbished",
                "registration_certificate",
                "finance",
                "insurance",
                "warranty",
                "is_booked",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )


class StatItemInline(admin.TabularInline):
    model = StatItem
    extra = 1
    fields = ("icon", "value", "caption", "order", "is_visible")

@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    inlines = [StatItemInline]
    # show banner images in the form
    fieldsets = (
        (None, {
            "fields": ("title", "logo", "is_active")
        }),
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_visible", "order", "created_at")
    list_filter = ("is_visible",)
    search_fields = ("name", "role", "quote")
    ordering = ("order",)

@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    fields = ("title", "subtitle", "is_active")
    
@admin.register(TrustedSection)
class TrustedSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    fields = ("title", "description", "image", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question", "answer")
    ordering = ("order",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "reason", "find_us", "created_at")
    search_fields = ("name", "email", "phone", "reason", "find_us")
    list_filter = ("reason", "find_us", "created_at")
    readonly_fields = ("created_at",)

    fields = ("name", "email", "phone", "reason", "find_us", "message", "created_at")


@admin.register(LoginPageContent)
class LoginPageContentAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
class HowItWorksInline(admin.TabularInline):
    model = HowItWorks
    extra = 1

@admin.register(SellBikePage)
class SellBikePageAdmin(admin.ModelAdmin):
    list_display = ["id", "top_banner_text", "second_banner_top_text"]
    inlines = [HowItWorksInline]

@admin.register(HowItWorks)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ["title", "page"]


class AboutSection3ImageInline(admin.TabularInline):
    model = AboutSection3Image
    extra = 1
    max_num = 5  

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['section', 'title']
    inlines = [AboutSection3ImageInline]

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj and obj.section == 'section3':
            inlines = [AboutSection3ImageInline(self.model, self.admin_site)]
        return inlines




@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ["id", "website", "phone"]
