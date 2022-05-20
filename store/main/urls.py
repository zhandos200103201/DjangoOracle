from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginUser, RegisterUser, logout_user, index, admin, show_category, show_gender, show_type, \
    show_color, search, view, cart, checkout, updateItem, deleteItem

urlpatterns = [
                  path('', index, name='home'),
                  path('admin/', admin, name='admin'),
                  path('login/', LoginUser.as_view(), name='login'),
                  path('logout/', logout_user, name='logout'),
                  path('register/', RegisterUser.as_view(), name='register'),
                  path('category/<int:category_id>/', show_category, name='category'),
                  path('gender/<int:gender_id>/', show_gender, name='gender'),
                  path('type/<int:type_id>/', show_type, name='type'),
                  path('color/<int:color_id>/', show_color, name='color'),
                  path('search/', search, name='search'),
                  path('cart/', cart, name='cart'),
                  path('checkout/', checkout, name='checkout'),
                  path('view/<int:product_id>/', view, name='view'),
                  path('update_item/', updateItem, name='update_item'),
                  path('delete_item/<int:product_id>/', deleteItem, name='delete_item'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
