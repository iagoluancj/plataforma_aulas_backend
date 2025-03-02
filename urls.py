from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

# View simples para testar a API
def api_home(request):
    return JsonResponse({"message": "API funcionando!"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_home),  # Rota para a API
]
