from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    # 자원에 대한 행위(method) 를 보여주지 않는 것이 원칙이라고 한다.
    # 그러나 copy 를 명시하지 않으면 DRF 에서는 어떤 기능을 하는지 구현을 해봐야 알 수 있다는 것
    path('products/<int:pk>/copy/', views.ProductCopyInstance.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
