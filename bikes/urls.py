from django.urls import path, include
from .views import (
    AboutSectionListAPIView, FooterAPIView, SellBikePageView,
    LoginPageContentView, SignupView, login_view, signup_view,
    ContactViewSet, contact_view
)
from .views import HeroSectionList, InfoSectionList, SupportFeatureList
from .views import BuyBikeList, BuyBikeDetail, BookingCreateView, BookingDetailView, BookingConfirmPaymentAPIView
from .views import LastSectionLatestAPIView
from .views import HomepageBannerAPIView
from .views import TestimonialsAPIView
from .views import TrustedSectionAPIView
from .views import FAQListAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename="contact")

urlpatterns = [
    path("api/hero/", HeroSectionList.as_view(), name="hero-section"),
    path("api/info/", InfoSectionList.as_view(), name="info-section"),
    path("api/support/", SupportFeatureList.as_view(), name="support-features"),
    path("api/homepage-banner/", HomepageBannerAPIView.as_view(), name="homepage-banner"),
    path("api/buybikes/", BuyBikeList.as_view(), name="buybike-list"),
    path("api/buybikes/<int:pk>/", BuyBikeDetail.as_view(), name="buybike-detail"),
    path("api/bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("api/bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("api/bookings/<int:pk>/confirm-payment/", BookingConfirmPaymentAPIView.as_view(), name="booking-confirm"),
    path("api/last-section/", LastSectionLatestAPIView.as_view(), name="last-section-latest"),
    path("api/testimonials/", TestimonialsAPIView.as_view(), name="testimonials"),
    path("api/trusted-section/", TrustedSectionAPIView.as_view(), name="trusted-section"),
    path("api/faqs/", FAQListAPIView.as_view(), name="faq-list"),
    
    
    path("api/about/", AboutSectionListAPIView.as_view(), name='api-about'),
    path("api/footer/", FooterAPIView.as_view(), name="footer"),
    path("api/sellbike/", SellBikePageView.as_view(), name="sellbike-page"),
    path("api/login-content/", LoginPageContentView.as_view(), name="login-content"),
    path("api/login/", login_view, name="login"),
    path("api/signup/", signup_view, name="signup"),
    path("api/", include(router.urls)),
    path("api/contact-form/", contact_view),
]
