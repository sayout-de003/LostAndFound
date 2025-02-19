from django.urls import path
from .views import lost_item_page, found_item_page, match_item_page, match_results_page

urlpatterns = [
    path("report-lost/", lost_item_page, name="report_lost"),
    path("report-found/", found_item_page, name="report_found"),
    path("match-item/", match_item_page, name="match_item"),
    path("match-results/<int:lost_item_id>/", match_results_page, name="match_results"),
]
