from django.urls import path
from .views import *

urlpatterns = [
    path('giftset/', GiftViewSet.as_view(), name="giftset"),
    path('auth/', AuthUsers.as_view(), name="auth"),
    path('social/auth/', SocialAuth.as_view(), name='social_auth'),
    path('gift/add/', AddNewGift.as_view(), name='add_new_gift'),
    path('gift/update_image/', UpdateImage.as_view(), name='update_gift'),
    path('gift/add_request/', NewRequest.as_view(), name="add_request"),
    path('account/signup/', SinguUp.as_view(), name="sign_up"),
    path('requests/all/', DisplayRequests.as_view(), name="display_all_requests"),

]