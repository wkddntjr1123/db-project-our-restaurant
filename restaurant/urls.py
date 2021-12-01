from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.index, name="index"),
    path("bulk_insert/", views.bulkInsert, name="bulkInsert"),
    path("get-overlay-info/<int:post_id>/", views.getOverlayInfo),
    path("get-boundary-post/", views.getBoundaryPost),
    path("get-post-data/<int:id>/", views.getPostData),
    path("get-paged-post/<int:page>/", views.getPagedPost),
    path("create-comment/", views.createComment),
    path("delete-comment/", views.deleteComment),
    path("get-group-review-data/<int:id>/", views.getGroupReviewData),
]
