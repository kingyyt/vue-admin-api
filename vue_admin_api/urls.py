"""
URL configuration for vue_admin_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api.views import account,demo,jsonList
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# 自动化文档
schema_view = get_schema_view(
    openapi.Info(
        title="接口文档",# 必传
        default_version='v1',# 必传
        description="接口文档",
        terms_of_service="",
        contact=openapi.Contact(email="yeyiteng@163.com"),
        license=openapi.License(name="BSD License")
    ),
    public=True,
)

urlpatterns = [
    path('api/login/', account.LoginView.as_view()),
    path('api/register/', account.RegisterView.as_view()),
    path('api/jsonList/', jsonList.jsonListView.as_view()),
    path('api/jsonListDetail/<int:pk>/', jsonList.jsonDetailView.as_view()),
    path('api/demo/', demo.DemoView.as_view()),
    path('api/uni/jsonListDetail/<int:pk>/', jsonList.uniJsonDetailView.as_view()),
    # 自动化文档
    path('swagger/',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc')
]
