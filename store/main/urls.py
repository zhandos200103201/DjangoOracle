from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginUser, RegisterUser, logout_user, index, admin, show_category, show_gender, show_type, show_color

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin, name='admin'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('category/<int:category_id>', show_category, name='category'),
    path('gender/<int:gender_id>', show_gender, name='gender'),
    path('type/<int:type_id>', show_type, name='type'),
    path('color/<int:color_id>', show_color, name='color'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
