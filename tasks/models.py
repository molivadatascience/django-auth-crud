from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    NOMBRE_CLIENTES_CHOICES = [
        ('CCU', 'CCU'),
        ('AGROSUPER', 'AGROSUPER'),
        ('COCA-COLA', 'COCA-COLA'),
    ]
    KAM_CHOICES = [
        ('Francisca', 'Francisca'),
        ('María Jesús', 'María Jesús'),
        ('Rolando', 'Rolando'),
    ]
    TIPOIMPORTACION_CHOICES = [
        ('Aéreo', 'Aéreo'),
        ('Ambas', 'Ambas'),
        ('Marítimo', 'Marítimo'),
    ]

    PAISDESTINO_CHOICES = [
        ('Chile', 'Chile'),
        ('Colombia', 'Colombia'),
        ('México', 'México'),
        ('Perú', 'Perú'),
    ]

    campaña = models.CharField(max_length=100)
    fecha_solicitud = models.DateField(default=timezone.now) 
    nombre_cliente = models.CharField(max_length=100,choices=NOMBRE_CLIENTES_CHOICES)
    kam = models.CharField(max_length=100,choices=KAM_CHOICES)
    valor_oportunidad = models.IntegerField()
    margen = models.FloatField(default=30.0)
    tipo_importacion= models.CharField(max_length=100,choices=TIPOIMPORTACION_CHOICES)
    pais_destino = models.CharField(max_length=100,choices=PAISDESTINO_CHOICES)
    fecha_entrega_propuesta = models.DateTimeField(null=True, blank=True)
    fecha_entrega_productos = models.DateTimeField(null=True, blank=True)
    descripcion = models.CharField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    datecompleted = models.DateTimeField(null=True, blank=True) #permite valores nulos
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title+ '- by '+ self.user.username



class DetalleOportunidad(models.Model):

    CATEGORIA_A_COTIZAR_CHOICES = [
        ('Insumos', 'Insumos'),        
        ('Merch', 'Merch'),
        ('Textil', 'Textil'),
        ('Visibilidad', 'Visibilidad'),
        ('Otra', 'Otra'),
    ]
    MUESTRA_PPS_CHOICES = [
        ('Digital', 'Digital'),
        ('Física', 'Física'),
    ]
    task = models.ForeignKey(Task, related_name='detalles', on_delete=models.CASCADE)
    id_detalle_venta = models.AutoField(primary_key=True)
    categoria_a_cotizar = models.CharField(max_length=100,choices=CATEGORIA_A_COTIZAR_CHOICES)    
    producto = models.CharField(max_length=100)
    margen_producto = models.FloatField(default=30.0)
    precio_objetivo = models.IntegerField(null=True, blank=True)
    unidades = models.IntegerField()
    unidades_2 = models.IntegerField(null=True, blank=True)
    unidades_3 = models.IntegerField(null=True, blank=True)
    unidades_4 = models.IntegerField(null=True, blank=True)    
    tamano = models.CharField(max_length=100,null=True, blank=True)
    color = models.CharField(max_length=100,null=True, blank=True)
    branding = models.CharField(max_length=100)
    cantidad_de_disenos = models.IntegerField()
    muestra_materialidad = models.BooleanField()
    aprobacion_muestra_pps = models.CharField(max_length=100,choices=MUESTRA_PPS_CHOICES)
    observaciones = models.CharField(max_length=100,null=True, blank=True)
    precio_unitario = models.IntegerField()
    packaging_master_unidades = models.CharField(max_length=100)
    packaging_inner_unidades = models.CharField(max_length=100)
    packaging_unitario_unidades = models.CharField(max_length=100)
    packaging_master_tipo = models.CharField(max_length=100)
    packaging_inner_tipo = models.CharField(max_length=100)
    packaging_diseno_tipo = models.CharField(max_length=100)
    packaging_master_diseno = models.BooleanField()
    packaging_inner_diseno = models.BooleanField()
    packaging_unitario_diseno = models.BooleanField()
    archivos_adjuntos = models.FileField(upload_to='archivos_adjuntos/',null=True, blank=True)
    #archivos_adjuntos = models.ManyToManyField('ArchivoAdjunto', related_name='detalles_oportunidad')

#class ArchivoAdjunto(models.Model):
#    detalle_oportunidad = models.ForeignKey(DetalleOportunidad, on_delete=models.CASCADE, related_name='archivos_adjuntos')
#    archivo = models.CharField(max_length=255)

 #   class Meta:
 #       db_table = 'archivoadjunto'
#
#    def __str__(self):
#        return self.archivo

class Costeo(models.Model):
    SI_NO_CHOICES = [(True, 'Sí'), (False, 'No')]
    RESPONSABLE_CHOICES = [('Pedro', 'Pedro'), ('Juan', 'Juan'), ('Diego', 'Diego')]
    PROVEEDOR_CHOICES = [('Proveedor A', 'Proveedor A'), ('Proveedor B', 'Proveedor B'), ('Proveedor C', 'Proveedor C')]
    IMPORTACION_COSTEO_CHOICES = [('aéreo', 'aéreo'), ('marítimo', 'marítimo')]
    PAIS_CHOICES = [('China', 'China'), ('Perú', 'Perú'), ('México', 'México')]
    PUERTO_CHOICES = [('puerto 1', 'puerto 1'), ('puerto 2', 'puerto 2'), ('puerto 3', 'puerto 3')]
    TAMAÑO_MUESTRA_CHOICES = [('pequeño', 'pequeño'), ('mediano', 'mediano'), ('grande', 'grande')]
    PORTAL_LICITACIONES_CHOICES = [('Ariba', 'Ariba'), ('No', 'No'), ('Wherex', 'Wherex')]

    id_detalle_venta = models.ForeignKey('DetalleOportunidad', on_delete=models.CASCADE)
    prov_elegido = models.BooleanField(choices=SI_NO_CHOICES)
    responsable = models.CharField(max_length=50, choices=RESPONSABLE_CHOICES)
    nombre_producto = models.CharField(max_length=100)
    fecha_costeo = models.DateField(default=timezone.now)
    hscode = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=50, choices=PROVEEDOR_CHOICES)
    tipo_importacion_costeo = models.CharField(max_length=50, choices=IMPORTACION_COSTEO_CHOICES)
    pais = models.CharField(max_length=50, choices=PAIS_CHOICES)
    ciudad = models.CharField(max_length=100)
    puerto = models.CharField(max_length=50, choices=PUERTO_CHOICES)
    margen = models.FloatField()
    cantidad_uu = models.FloatField()
    costo_unit_usd = models.FloatField()
    costo_muestra = models.FloatField()
    refundable = models.BooleanField(choices=SI_NO_CHOICES)
    unidades_por_master_box = models.FloatField()
    largo = models.FloatField()
    ancho = models.FloatField()
    alto = models.FloatField()
    peso_por_master_box = models.FloatField()
    importacion_muestra = models.BooleanField(choices=SI_NO_CHOICES)
    tamaño_muestra = models.CharField(max_length=50, choices=TAMAÑO_MUESTRA_CHOICES)
    portal_licitaciones = models.CharField(max_length=50, choices=PORTAL_LICITACIONES_CHOICES)
    dias_muestra = models.FloatField()
    dias_prod_final = models.FloatField()
    advalorem = models.FloatField()
    payment_terms = models.FloatField()
    
    def __str__(self):
        return self.nombre_producto