from django.contrib import admin
from django.urls import path, include
from reporte_diario import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración de Django
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('vista_protegida/', views.vista_protegida, name='vista_protegida'),
    path('perfil/', views.perfil, name='perfil'),
    # path('home/', views.home, name='home'),
    path('mi_imagen/', views.mi_imagen, name='mi_imagen'),
    path('ingresar_fundas/', views.ingresar_datos_funda, name='ingresar_funda'),
    path('mostrar_datos_funda/', views.mostrar_datos_funda, name='mostrar_datos_funda'),
    path('eliminar_funda/<int:funda_id>/', views.eliminar_funda, name='eliminar_funda'),
    path('tu_vista/', views.tu_vista, name='tu_vista'),
    path('crear/', views.crear_reporte, name='crear-reporte'),
    path('ver_reportes/', views.ver_reportes, name='ver-reportes'),
    path('detalle/<int:reporte_id>/', views.detalle_reporte, name='detalle-reporte'),
    #path('procesar_defectos/<int:reporte_id>/', views.procesar_defectos, name='procesar-defectos'),
    path('eliminar-reporte/<int:reporte_id>/', views.eliminar_reporte, name='eliminar-reporte'),
    path('generar-pdf/<int:reporte_id>/', views.generar_pdf, name='generar-pdf'),
    #path('reporte_diario/', include('reporte_diario.urls')),
 # Incluir las URLs de la aplicación reporte_diario
    # Otras URLs de tu proyecto si las tienes
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)