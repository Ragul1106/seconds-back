from rest_framework import serializers
from .models import AboutSection, AboutSection3Image, Footer
from rest_framework import serializers
from .models import SellBikePage, HowItWorks, Contact
from .models import LoginPageContent
from django.contrib.auth.models import User
from .models import HeroSection, HeroBikeImage, InfoSection, SupportFeature
from .models import BuyBike, Location
from .models import Booking, BuyBike
from .models import LastSection, LastSectionImage
from .models import HomepageBanner, StatItem
from .models import TestimonialsSection, Testimonial
from .models import TrustedSection
from .models import FAQ



class LastSectionImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = LastSectionImage
        fields = ["id", "title", "image", "image_url", "alt_text", "order_no"]
        read_only_fields = ["id", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class LastSectionSerializer(serializers.ModelSerializer):
    images = LastSectionImageSerializer(many=True, read_only=True)

    class Meta:
        model = LastSection
        fields = ["id", "heading", "subtitle", "created_at", "updated_at", "images"]
        read_only_fields = ["id", "created_at", "updated_at", "images"]


class BookingCreateSerializer(serializers.ModelSerializer):
    buybike = serializers.PrimaryKeyRelatedField(queryset=BuyBike.objects.all())

    class Meta:
        model = Booking
        fields = ("id", "buybike", "test_drive_fee")

    def create(self, validated_data):
        bike = validated_data["buybike"]
        subtotal = float(getattr(bike, "price", 0) or 0)
        test_drive_fee = float(validated_data.get("test_drive_fee", 0) or 0)
        gst_amount = round(subtotal * 0.18, 2)
        total_amount = subtotal + gst_amount + test_drive_fee

        booking = Booking.objects.create(
            buybike=bike,
            amount=subtotal,
            gst_amount=gst_amount,
            test_drive_fee=test_drive_fee,
            total_amount=total_amount,
            status="created",
        )
        bike.is_booked = True
        bike.save(update_fields=["is_booked"])
        return booking

class BookingDetailSerializer(serializers.ModelSerializer):
    buybike_obj = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "buybike",
            "buybike_obj",
            "amount",
            "gst_amount",
            "test_drive_fee",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_buybike_obj(self, obj):
        return {
            "id": obj.buybike.id,
            "title": obj.buybike.title,
            "price": obj.buybike.price,
            "featured_image_url": (obj.buybike.featured_image.url if obj.buybike.featured_image else None),
        }


class AbsoluteImageMixin:
    def get_absolute_url(self, obj, field_name, request):
        field = getattr(obj, field_name)
        if field and hasattr(field, "url"):
            return request.build_absolute_uri(field.url) if request else field.url
        return None
    
class HeroBikeImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroBikeImage
        fields = ["id", "image", "image_url", "order"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url  


class HeroSectionSerializer(serializers.ModelSerializer):
    trapezoid_image_url = serializers.SerializerMethodField()
    bike_images = HeroBikeImageSerializer(many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = [
            "id",
            "title",
            "description",
            "button_text",
            "trapezoid_image",
            "trapezoid_image_url",
            "bike_images",
        ]

    def get_trapezoid_image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.trapezoid_image.url)
        return obj.trapezoid_image.url


class InfoSectionSerializer(serializers.ModelSerializer):
    bike_image_url = serializers.SerializerMethodField()

    class Meta:
        model = InfoSection
        fields = ["id","description","button_text","bike_image","bike_image_url","order"]

    def get_bike_image_url(self, obj):
        request = self.context.get("request")
        return AbsoluteImageMixin().get_absolute_url(obj, "bike_image", request)


class SupportFeatureSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    arrow_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SupportFeature
        fields = ["id","title","subtitle","description","image","image_url","arrow_image","arrow_image_url","arrow","order"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return AbsoluteImageMixin().get_absolute_url(obj, "image", request)

    def get_arrow_image_url(self, obj):
        request = self.context.get("request")
        return AbsoluteImageMixin().get_absolute_url(obj, "arrow_image", request)
   

class LocationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["id", "name", "image", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class BuyBikeSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    card_bg_image_url = serializers.SerializerMethodField()

    
    variant_image1_url = serializers.SerializerMethodField()
    variant_image2_url = serializers.SerializerMethodField()
    variant_image3_url = serializers.SerializerMethodField()
    variant_image4_url = serializers.SerializerMethodField()
    variant_image5_url = serializers.SerializerMethodField()

    location_obj = LocationSerializer(source="location", read_only=True)

    class Meta:
        model = BuyBike
        fields = [
            "id", "title", "description", "price", "location", "location_obj",
            "brand", "bike_model", "bike_variant", "year", "registration_year",
            "kilometers", "engine_cc", "fuel_type", "color",
            "category", "owner", "owners", "transmission",
            "rto_state", "rto_city",
            "refurbished", "registration_certificate", "finance", "insurance", "warranty",
            "is_booked",
            "ignition_type", "front_brake_type", "rear_brake_type", "abs", "odometer", "wheel_type",
         
            "featured_image", "featured_image_url",
            "card_bg_image", "card_bg_image_url",
            "variant_image1", "variant_image1_url",
            "variant_image2", "variant_image2_url",
            "variant_image3", "variant_image3_url",
            "variant_image4", "variant_image4_url",
            "variant_image5", "variant_image5_url",
            "created_at", "updated_at"
        ]

    def get_featured_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.featured_image.url) if obj.featured_image and request else (obj.featured_image.url if obj.featured_image else None)

    def get_card_bg_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.card_bg_image.url) if obj.card_bg_image and request else (obj.card_bg_image.url if obj.card_bg_image else None)

    def get_variant_image1_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.variant_image1.url) if obj.variant_image1 and request else (obj.variant_image1.url if obj.variant_image1 else None)

    def get_variant_image2_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.variant_image2.url) if obj.variant_image2 and request else (obj.variant_image2.url if obj.variant_image2 else None)

    def get_variant_image3_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.variant_image3.url) if obj.variant_image3 and request else (obj.variant_image3.url if obj.variant_image3 else None)

    def get_variant_image4_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.variant_image4.url) if obj.variant_image4 and request else (obj.variant_image4.url if obj.variant_image4 else None)

    def get_variant_image5_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.variant_image5.url) if obj.variant_image5 and request else (obj.variant_image5.url if obj.variant_image5 else None)

    
class StatItemSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = StatItem
        fields = ("id", "icon_url", "value", "caption", "order", "is_visible")

    def get_icon_url(self, obj):
        request = self.context.get("request")
        if obj.icon and hasattr(obj.icon, "url"):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None

class HomepageBannerSerializer(serializers.ModelSerializer):
    stats = StatItemSerializer(many=True, read_only=True)
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = HomepageBanner
        fields = (
            "id", "title", "logo_url", 
            "is_active", "created_at", "stats"
        )

    def _abs_url(self, field):
        request = self.context.get("request")
        if field and hasattr(field, "url"):
            return request.build_absolute_uri(field.url) if request else field.url
        return None

    def get_logo_url(self, obj): return self._abs_url(obj.logo)
    

class TestimonialSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ("id", "name", "role", "quote", "image_url", "is_visible", "order")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class TestimonialsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialsSection
        fields = ("id", "title", "subtitle", "is_active")
        
class TrustedSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TrustedSection
        fields = ("id", "title", "description", "image_url", "is_active", "created_at")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "order")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

class LoginPageContentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = LoginPageContent
        fields = ["id", "title", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class HowItWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorks
        fields = ["id", "title", "image"]

class SellBikePageSerializer(serializers.ModelSerializer):
    how_it_works = HowItWorksSerializer(many=True, read_only=True)

    class Meta:
        model = SellBikePage
        fields = [
            "id",
            "top_banner_image",
            "top_banner_text",
            "second_banner_image",
            "second_banner_top_text",
            "second_banner_bottom_text",
            "brand_options",
            "model_options",
            "variant_options",
            "kms_options",
            "owner_options",
            "third_title",
            "how_it_works",
        ]


class AboutSection3ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection3Image
        fields = ['id', 'image']

class AboutSectionSerializer(serializers.ModelSerializer):
    images = AboutSection3ImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutSection
        fields = ['id', 'section', 'title', 'description', 'image', 'images', 'overlay_title', 'overlay_description']


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = "__all__"