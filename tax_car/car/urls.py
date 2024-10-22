from django.urls import path
from car.views import CarCategoryApiView, CarCategoryDetailApiView

urlpatterns = [
    path('category', CarCategoryApiView.as_view()),
    path('category/<int:category_id>/', CarCategoryDetailApiView.as_view())
]