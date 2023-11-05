from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.urls import reverse
from .models import ReporteDiario, Funda, Imagen, PorcentajeDefecto, Defecto
from .forms import ReporteDiarioForm, PorcentajeDefectoForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from .forms import FundaForm  # Importa el formulario FundaForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Código para la vista de "home"
    return render(request, 'home.html')

@login_required
def vista_protegida(request):
    # Tu lógica para la vista protegida
    return render(request, 'vista_protegida.html')

@login_required
def perfil(request):
    # Obtén los datos del perfil del usuario actual, por ejemplo, desde un modelo de perfil personalizado.
    # profile = Perfil.objects.get(usuario=request.user)  # Asegúrate de tener un modelo de perfil configurado.

    # Luego, pasa estos datos a la plantilla HTML.
    return render(request, 'perfil.html', {'user': request.user})


def mi_imagen(request):
    # Obtén la imagen que deseas mostrar (puedes filtrar por nombre, ID, etc.)
    try:
        logo = Imagen.objects.get(id=1)
    except Imagen.DoesNotExist:
        # Aquí puedes manejar el caso en que la imagen no existe
        logo = None

    return render(request, 'base.html', {'logo': logo})



@login_required
def tu_vista(request):
    
    # Recupera todos los objetos Funda de la base de datos
    fundas = Funda.objects.all()

    context = {
        'fundas': fundas,  # Pasa los objetos Funda al contexto
    }
    # funda = Funda.objects.get(id=1)  # Obtén el objeto funda que deseas usar como valor predeterminado
    # form = FundaForm(initial={'marca': funda.marca})  # Establece el valor predeterminado

    # context = {
    #     'form': form,
    #     'funda': funda,
    # }
    return render(request, 'pdf_template.html', context)

    
@login_required
def ingresar_datos_funda(request):
    if request.method == 'POST':
        form = FundaForm(request.POST)
        if form.is_valid():
            # Guardar los datos de la funda en la base de datos
            form.save()
            return redirect('mostrar_datos_funda')  # Cambia 'pagina_reporte' por la URL de tu página de informe
    else:
        form = FundaForm()
    
    return render(request, 'ingresar_funda.html', {'form': form})
@login_required
def mostrar_datos_funda(request):
    # Obtener todos los datos de la base de datos
    datos_funda = Funda.objects.all()

    # Pasar los datos a la plantilla
    return render(request, 'mostrar_datos_funda.html', {'datos_funda': datos_funda})
@login_required
def eliminar_funda(request, funda_id):
    # Obtener la instancia de Funda que deseas eliminar
    funda = get_object_or_404(Funda, id=funda_id)

 

    if request.method == 'POST':
        # Si se envió una solicitud POST, eliminar la funda y redirigir
        funda.delete()
        return redirect('mostrar_datos_funda')

    # Si no es una solicitud POST, simplemente mostrar una confirmación
    return render(request, 'confirmar_eliminacion.html', {'funda': funda})
@login_required
def eliminar_reporte(request, reporte_id):
    # Obtiene el informe a eliminar o muestra un error 404 si no existe
    informe = get_object_or_404(ReporteDiario, pk=reporte_id)
    
    if request.method == 'POST':
        # Si se envía una solicitud POST, elimina el informe y redirige a una página de confirmación
        informe.delete()
        return redirect('ver-reportes')
    
    # Renderiza la plantilla de confirmación de eliminación
    return render(request, 'confirmacion_eliminacion.html', {'informe': informe})  


@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteDiarioForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)

            if not isinstance(reporte.peso_neto, Decimal):
               reporte.peso_neto = Decimal(reporte.peso_neto)

            # Realiza el cálculo del porcentaje de glaseo
            if reporte.peso_sin_funda_manual == 0:
                reporte.porcentaje_glaseo = None  # O el valor por defecto que desees
            else:
                reporte.porcentaje_glaseo = (reporte.peso_neto / reporte.peso_sin_funda_manual) * 100 - 100

            # Realiza el cálculo de la uniformidad
            if reporte.camarones_grandes is not None and reporte.camarones_pequenos is not None:
                reporte.uniformidad = (reporte.camarones_grandes / reporte.camarones_pequenos) * 100 / 100
            else:
                reporte.uniformidad = None  # O el valor por defecto que desees

            observaciones = request.POST.get('observaciones', '')
            correctivos = request.POST.get('correctivos', '')
            reporte.observaciones = observaciones
            reporte.correctivos = correctivos
        


            reporte.save()

            return redirect('detalle-reporte',  reporte_id=reporte.id)
    else:
        form = ReporteDiarioForm()

    context = {
        'form': form,
        'year': datetime.now().year,  # Asegúrate de importar datetime en tu vista 
    }

    return render(request, 'pdf_template.html', context)  


 
@login_required
def ver_reportes(request):
    # Consulta a la base de datos para obtener todos los reportes
    reportes = ReporteDiario.objects.all()

    return render(request, 'lista_reportes.html', {'reportes': reportes})
@login_required
def detalle_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteDiario, id=reporte_id)
    
    if request.method == 'POST':
        defecto_nombre = request.POST.get('defecto')
        cantidad_str = request.POST.get('cantidad')

        if defecto_nombre and cantidad_str:
            try:
                cantidad = Decimal(cantidad_str)
            except ValueError:
                return HttpResponse("Cantidad no válida")

            defecto = get_object_or_404(Defecto, nombre=defecto_nombre)
            porcentaje = (cantidad / reporte.total_camaron) * 100
            porcentaje_redondeado = round(porcentaje, 2)

            porcentaje_defecto = PorcentajeDefecto(
                defecto=defecto,
                cantidad=cantidad,
                porcentaje=porcentaje_redondeado,
                reporte=reporte
            )
            porcentaje_defecto.save()

            # Redirige a la misma página después de guardar
            return redirect('detalle-reporte', reporte_id=reporte_id)

    # Obtén los defectos guardados relacionados con el informe después de guardar
    defectos_guardados = PorcentajeDefecto.objects.filter(reporte=reporte)
    total_porcentaje = sum(porcentaje_defecto.porcentaje for porcentaje_defecto in defectos_guardados)

    return render(request, 'detalle_reporte.html', {
        'reporte': reporte,
        'defectos_guardados': defectos_guardados,
        'total_porcentaje': total_porcentaje
    })

def create_defectos():
    defectos = [
        ("Picado", "Descripción de Picado"),
        ("Rosado leve", "Descripción de Rosado leve"),
        ("Deshidratado", "Descripción de Deshidratado"),
        ("Dañados o piezas", "Dañados o piezas"),
        ("Mudado", "Mudado"),
        ("Suave o quebrado", "Suave o quebrado"),
        ("Mal descabezado", "Mal descabezado"),
        ("Sin telson", "Sin telson"),
        ("Cascara", "Cascara"),
        ("Corte profundo", "Corte profundo"),
        ("Falta de corte", "Falta de corte"),
        ("Intestino / vena", "Intestino / vena"),
        ("Semi crudo", "Semi crudo"),
        ("Pequeño", "Pequeño"),
        ("Otros", "Otros"),
        # Agrega más defectos aquí
    ]

    for nombre, descripcion in defectos:
        defectos, creado = Defecto.objects.get_or_create(nombre=nombre, descripcion=descripcion)

        if creado:
            print(f'Se creó el defecto: {nombre}')
        else:
            print(f'El defecto {nombre} ya existe en la base de datos.')

if __name__ == '__main__':
    create_defectos()




""" def detalle_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteDiario, id=reporte_id)

    if request.method == 'POST':
        defecto_nombre = request.POST.get('defecto')

        if not defecto_nombre:
            return HttpResponse("Debes elegir un defecto válido")
        cantidad_str = request.POST.get('cantidad') # Recuperar cantidad como cadena

        try:
            cantidad = Decimal(cantidad_str)  # Convertir cantidad a Decimal
        except ValueError:
            # Manejar errores de conversión, por ejemplo, si la entrada no es un número válido
            return HttpResponse("Cantidad no válida")

        defecto = get_object_or_404(Defecto, nombre=defecto_nombre)
        porcentaje = (cantidad / reporte.total_camaron) * 100
        porcentaje_redondeado = round(porcentaje, 2)  # Redondear a 2 decimales

        porcentaje_defecto = PorcentajeDefecto(
            defecto=defecto,
            cantidad=cantidad,
            porcentaje= porcentaje_redondeado,

            reporte=reporte  # Asigna el informe relacionado
        )
        porcentaje_defecto.save()

        porcentajedefecto = [porcentaje_defecto]  # Crear una lista con el objeto PorcentajeDefecto 
        

        return render(request, 'detalle_reporte.html', {
            'reporte': reporte,
            'porcentajedefecto': porcentajedefecto
        })

    return render(request, 'detalle_reporte.html', {
        'reporte': reporte,
    }) 
 """

        





def generar_pdf(request, reporte_id):
    # Obtener los datos del informe
    reporte = get_object_or_404(ReporteDiario, id=reporte_id)
    defectos_guardados = PorcentajeDefecto.objects.filter(reporte=reporte)  # Obtener los defectos guardados
    total_porcentaje = sum(porcentaje_defecto.porcentaje for porcentaje_defecto in defectos_guardados)
    # Cargar la plantilla HTML
    template = get_template('detalle_reporte.html')  # Usar la plantilla existente
    context = {'reporte': reporte, 'defectos_guardados': defectos_guardados,'total_porcentaje': total_porcentaje, 'year': datetime.now().year}

    # Rellenar la plantilla con los datos
    html = template.render(context)
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{reporte_id}.pdf"'
    
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response




