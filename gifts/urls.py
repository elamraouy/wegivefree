from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="acceuil"),
    path('gifts/', index, name="gifts_list_url"),
    path('add/', new_gift, name="new_gift"),
    path('accounts/logout/', logout_view, name="logout"),
    path('users/', user_gifts, name="users"),
    path('show/', show_gift, name="show_gift_url"),
    path('check_auth/', check_auth, name="demande" ),
    path('add_request/', new_gift_request, name="new_gift_request"),
    path('display_requests/', display_requests, name="display_requests"),
    path('delete/', delete_gift, name="delete_gift" ),
    path('manage_request/', manage_requests, name="manage_request"),
    path('manage_notifications/', manage_notifications , name="manage_notifications"),
    path('get_all_conversation/', get_all_conversation, name="get_all_conversation"),
    path('get_gift_message/', get_gift_messages, name="get_gift_message"),
    path('update_messages/', update_messages, name="update_messages"),
    path('sned_response_to/', send_response_to, name="send_response_to"),
    path('save_profile/', save_profile, name="save_profile"),
    path('notifications/', show_all_notifications, name="notifications")
]
