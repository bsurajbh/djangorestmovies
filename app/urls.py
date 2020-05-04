from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.users.urls'), name='users'),
    path('api/', include('api.movies.urls'), name='movies'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
