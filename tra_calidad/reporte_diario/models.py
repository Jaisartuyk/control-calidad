from django.db import models






class Imagen(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='imagenes/')


class Funda(models.Model):
    marca = models.CharField(max_length=50)
    peso_funda = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) :
        return self.marca


class ReporteDiario(models.Model):
    nombre_analista = models.CharField(max_length=100,default="N/A")  # Nombre del analista
    turno = models.CharField(max_length=50,default="N/A")  # Turno (por ejemplo, mañana, tarde, noche)
    presentacion = models.TextField(default="N/A")
    lote = models.CharField(max_length=50,default="N/A")
    hora = models.TimeField()
    fecha = models.DateField()
    clasificacion_choices = [
        ('16-20', '16-20'),
        ('21-25', '21-25'),
        ('26-30', '26-30'),
        ('31-35', '31-35'),
        ('36-40', '36-40'),
        ('51-60', '51-60'),
        ('61-70', '61-70'),
        ('71-90', '71-90'),
    ]
    
    clasificacion = models.CharField(max_length=10, choices=clasificacion_choices, default='16-20')

    cuenta_lbs = models.PositiveIntegerField()
    total_camaron = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    camarones_grandes = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    camarones_pequenos = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    uniformidad = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    porcentaje_glaseo = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    peso_neto = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    observaciones = models.TextField(blank=True)  # Puedes usar CharField si prefieres campos de texto cortos.
    correctivos = models.TextField(blank=True)


    # Agregamos los campos para el peso sin funda y la marca de funda ingresados manualmente
    peso_sin_funda_manual = models.DecimalField(max_digits=10, decimal_places=2)
    marca_funda_manual = models.CharField(max_length=50)

    # Actualizar los campos de porcentaje_glaseo y uniformidad al guardar
    def save(self, *args, **kwargs):
        # Calcular el porcentaje de glaseo
        if self.peso_neto is not None and self.peso_sin_funda_manual is not None:
            self.porcentaje_glaseo = (self.peso_neto / self.peso_sin_funda_manual) *100 - 100
        else:
            self.porcentaje_glaseo = None  # O el valor por defecto que desees
        
        if self.camarones_pequenos is not None and self.camarones_grandes is not None:
            self.uniformidad = (self.camarones_grandes / self.camarones_pequenos) * 100
        else:
            self.uniformidad = None  # O el valor por defecto que desees



        # Calcular la uniformidad
        

        super(ReporteDiario, self).save(*args, **kwargs)

    #Sfunda = models.ForeignKey(Funda, on_delete=models.SET_NULL, null=True, blank=True)
    # Puedes agregar más campos según tus necesidades

class Defecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    # Puedes agregar más campos según tus necesidades
defectos = [
    ("Picado", "Picado"),
    ("Rosado leve", "Rosado leve"),
    ("Deshidratado", "Deshidratado"),
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
]


for defecto in defectos:
    Defecto.objects.get_or_create(nombre=defecto, descripcion=f'Descripción de {defecto}')

class PorcentajeDefecto(models.Model):
    reporte = models.ForeignKey(ReporteDiario, on_delete=models.CASCADE)
    defecto = models.ForeignKey(Defecto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.defecto} - {self.cantidad}"

# Create your models here.
