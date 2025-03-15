from django.contrib import admin
from django.urls import path, include, get_resolver
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="API for library management where users can search for books, and borrow them + admin panel",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def home(request):
    resolver = get_resolver()
    urls = sorted(set(
        path_info.pattern._route for path_info in resolver.url_patterns
    ))

    url_list = "".join(f'<li><a href="/{url}">{url}</a></li>' for url in urls if url)
    return HttpResponse(f"<h1>Welcome to Library Management API</h1><ul>{url_list}</ul>")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/library/', include('library.urls')),
    path('api/users/', include('users.urls')),
    path('api/loans/', include('loans.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]