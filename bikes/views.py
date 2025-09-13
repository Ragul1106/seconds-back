from rest_framework import generics, filters, status
from .models import AboutSection
from .serializers import AboutSectionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Footer
from .serializers import FooterSerializer
from .serializers import SellBikePageSerializer
from .models import SellBikePage
from rest_framework.generics import RetrieveAPIView
from .models import LoginPageContent
from .serializers import LoginPageContentSerializer
from django.contrib.auth.models import User
from .serializers import SignupSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json
from .models import BuyBike
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BuyBikeSerializer
from .models import HeroSection, InfoSection, SupportFeature
from .serializers import HeroSectionSerializer, InfoSectionSerializer, SupportFeatureSerializer
from .filters import BikeFilter  
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import HomepageBanner
from .serializers import HomepageBannerSerializer
from django.shortcuts import get_object_or_404

from .models import BuyBike, Booking
from .serializers import BookingCreateSerializer, BookingDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import LastSection
from .serializers import LastSectionSerializer
from .models import TestimonialsSection, Testimonial
from .serializers import TestimonialsSectionSerializer, TestimonialSerializer
from .models import TrustedSection
from .serializers import TrustedSectionSerializer
from rest_framework.generics import ListAPIView
from .models import FAQ
from .serializers import FAQSerializer



class LastSectionListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: list all sections (most recent first)
    POST: create a new section (admin usage via API if desired)
    """
    queryset = LastSection.objects.all()
    serializer_class = LastSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # restrict POST to authenticated if you want


class LastSectionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = LastSection.objects.all()
    serializer_class = LastSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LastSectionLatestAPIView(generics.GenericAPIView):
    """
    Returns the latest (most recently created) LastSection.
    Useful for `/last-section/` endpoint that front-end will call.
    """
    serializer_class = LastSectionSerializer
    queryset = LastSection.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().order_by("-created_at").first()
        if not obj:
            return Response({"detail": "No sections found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(obj, context={"request": request})
        return Response(serializer.data)


# Create booking: server computes amounts and marks the BuyBike as booked
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [AllowAny]  # change if you require auth

    def create(self, request, *args, **kwargs):
        # validate incoming payload
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        buybike = serializer.validated_data.get("buybike")
        test_drive_fee = float(serializer.validated_data.get("test_drive_fee", 0) or 0)

        # server-side compute: subtotal from buybike.price, gst 18%
        subtotal = float(getattr(buybike, "price", 0) or 0)
        gst_amount = round(subtotal * 0.18, 2)
        total_amount = round(subtotal + gst_amount + test_drive_fee, 2)

        user = request.user if request.user and request.user.is_authenticated else None

        booking = Booking.objects.create(
            buybike=buybike,
            user=user,
            amount=subtotal,
            gst_amount=gst_amount,
            test_drive_fee=test_drive_fee,
            total_amount=total_amount,
            status="created",
        )

        # mark the product as booked in the buybike table (for admin visibility)
        buybike.is_booked = True
        buybike.save(update_fields=["is_booked"])

        out = BookingDetailSerializer(booking, context={"request": request})
        headers = self.get_success_headers(out.data)
        return Response(out.data, status=status.HTTP_201_CREATED, headers=headers)


# Booking detail (used by payment page to show amounts)
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.select_related("buybike").all()
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Optional: lightweight confirm endpoint that only toggles booking.status to 'paid' (no payment details saved)
class BookingConfirmPaymentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        if booking.status == "paid":
            return Response({"detail": "Already paid"}, status=status.HTTP_400_BAD_REQUEST)

        # toggle paid — do NOT save payment_method or payment_reference (as requested)
        booking.status = "paid"
        booking.save(update_fields=["status"])

        return Response({"detail": "Booking marked as paid"}, status=status.HTTP_200_OK)



class HeroSectionList(generics.ListAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer

class InfoSectionList(generics.ListAPIView):
    queryset = InfoSection.objects.all()
    serializer_class = InfoSectionSerializer

class SupportFeatureList(generics.ListAPIView):
    queryset = SupportFeature.objects.all()
    serializer_class = SupportFeatureSerializer

class BuyBikeList(generics.ListAPIView):
    queryset = BuyBike.objects.all()
    serializer_class = BuyBikeSerializer

    # enable django-filter + DRF search & ordering
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BikeFilter

    ordering_fields = ["created_at", "price", "kilometers", "year"]
    ordering = ["-created_at"]
    # keep DRF search, but our BikeFilter also provides 'search' param; both can coexist
    search_fields = ["title", "brand", "category", "description", "location__name"]


class BuyBikeDetail(generics.RetrieveAPIView):
    queryset = BuyBike.objects.select_related("location").all()
    serializer_class = BuyBikeSerializer

class HomepageBannerAPIView(APIView):
    def get(self, request, *args, **kwargs):
        banner = HomepageBanner.objects.filter(is_active=True).order_by("-created_at").first()
        if not banner:
            return Response({"detail": "No banner configured."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HomepageBannerSerializer(banner, context={"request": request})
        return Response(serializer.data)
    
class TestimonialsAPIView(APIView):
    """
    Returns:
    {
      "section": { "title": "...", "subtitle": "..."},
      "testimonials": [ { id,name,role,quote,image_url }, ... ]
    }
    """
    def get(self, request, *args, **kwargs):
        # pick latest active section (or none)
        section = TestimonialsSection.objects.filter(is_active=True).order_by("-created_at").first()
        section_data = TestimonialsSectionSerializer(section).data if section else None

        # get visible testimonials ordered by 'order'
        testimonials_qs = Testimonial.objects.filter(is_visible=True).order_by("order", "created_at")
        serializer = TestimonialSerializer(testimonials_qs, many=True, context={"request": request})
        return Response({"section": section_data, "testimonials": serializer.data})
    
class TrustedSectionAPIView(APIView):
    """
    Returns the latest active TrustedSection (GET /api/trusted-section/).
    """
    def get(self, request, *args, **kwargs):
        obj = TrustedSection.objects.filter(is_active=True).order_by("-created_at").first()
        if not obj:
            return Response({"detail": "Not configured"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TrustedSectionSerializer(obj, context={"request": request})
        return Response(serializer.data)
    
class FAQListAPIView(ListAPIView):
    queryset = FAQ.objects.filter(is_active=True).order_by("order")
    serializer_class = FAQSerializer

@csrf_exempt
def contact_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        reason = data.get("reason")
        find_us = data.get("find_us")
        message = data.get("message")

        # Save to DB
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            reason=reason,
            find_us=find_us,
            message=message
        )
        print("✅ Saved contact:", contact.id)

        # Prepare confirmation email
        subject = "Thank you for contacting Drive RP"
        body = f"""
        Hi {name},

        Thank you for reaching out to us. We received your message:

        Reason: {reason}
        Message: {message}

        Our team will get back to you soon.

        Regards,
        Drive RP Team
        """

        email_msg = EmailMessage(
            subject,
            body,
            from_email="rockyranjith1121@gmail.com",
            to=[email],   # Send to user
            bcc=["rockyranjith1121@gmail.com"],  # Keep a copy for yourself
        )

        print("📩 Contact form received:", name, email)
        try:
            email_msg.send(fail_silently=False)
            return JsonResponse({"success": True, "message": "Message sent"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"success": True, "message": "Login successful"})
    else:
        return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def signup_view(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    # Send confirmation email to user
    subject_user = "Welcome to Drive RP!"
    body_user = f"Hi {username},\n\nYou have successfully registered at Drive RP.\n\nThank you!"
    EmailMessage(subject_user, body_user, to=[email]).send(fail_silently=True)

    # Notify admin
    subject_admin = "New User Registration"
    body_admin = f"New user registered:\n\nUsername: {username}\nEmail: {email}"
    EmailMessage(subject_admin, body_admin, to=["rockyranjith1121@gmail.com"]).send(fail_silently=True)

    return Response({"success": True, "message": "User registered successfully"})



class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class LoginPageContentView(APIView):
    def get(self, request):
        content = LoginPageContent.objects.last()
        serializer = LoginPageContentSerializer(content, context={"request": request})
        return Response(serializer.data)

class AboutSectionListAPIView(generics.ListAPIView):
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    


class SellBikePageView(RetrieveAPIView):
    queryset = SellBikePage.objects.all()
    serializer_class = SellBikePageSerializer

    def get_object(self):
        return SellBikePage.objects.first()

class FooterAPIView(APIView):
    def get(self, request):
        footer = Footer.objects.last()  
        serializer = FooterSerializer(footer, context={"request": request})
        return Response(serializer.data)