import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado


def subir_texto(request):
    """
    Vista para subir un nuevo texto a analizar.
    """
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    
    return render(request, 'subir.html', {'form': form})


def lista_textos(request):
    """
    Vista que muestra la lista de todos los textos subidos,
    ordenados por fecha de subida (más recientes primero).
    """
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'lista.html', {'textos': textos})


def _procesar_contenido_texto(contenido):
    """
    Función auxiliar para procesar el contenido del texto:
    - Extrae palabras (incluyendo caracteres en español)
    - Convierte a minúsculas
    - Cuenta frecuencia de palabras
    
    Args:
        contenido (str): Texto a procesar
        
    Returns:
        tuple: (lista de palabras, Counter de palabras, total de palabras)
    """
    # Expresión regular que incluye caracteres en español (áéíóúñ)
    patron_palabras = r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b'
    palabras = re.findall(patron_palabras, contenido.lower())
    
    contador_palabras = Counter(palabras)
    total_palabras = len(palabras)
    
    return palabras, contador_palabras, total_palabras


def _leer_archivo_texto(archivo):
    """
    Función auxiliar para leer el contenido de un archivo de texto.
    
    Args:
        archivo: Objeto de archivo de Django
        
    Returns:
        str: Contenido del archivo o cadena vacía si hay error
    """
    try:
        with archivo.open('r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        # Intentar con otra codificación si utf-8 falla
        try:
            with archivo.open('r', encoding='latin-1') as f:
                return f.read()
        except:
            return ""


def analizar_texto(request, texto_id):
    """
    Vista para analizar un texto específico y mostrar:
    - Las 20 palabras más comunes
    - El total de palabras encontradas
    
    Args:
        request: HttpRequest object
        texto_id (int): ID del texto a analizar
        
    Returns:
        HttpResponse: Página con resultados del análisis
    """
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    
    # Leer y procesar el contenido del archivo
    contenido = _leer_archivo_texto(texto_obj.archivo)
    palabras, contador_palabras, total_palabras = _procesar_contenido_texto(contenido)
    
    # Obtener las 20 palabras más comunes
    palabras_comunes = contador_palabras.most_common(20)
    
    return render(request, 'resultado.html', {
        'texto': texto_obj,
        'palabras_comunes': palabras_comunes,
        'total_palabras': total_palabras
    })


def detalles_procesamiento(request, texto_id):
    """
    Vista adicional (si es necesaria) para mostrar detalles del procesamiento
    como se ve en el HTML proporcionado anteriormente.
    """
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    contenido = _leer_archivo_texto(texto_obj.archivo)
    
    # Procesar el texto para obtener detalles
    palabras, contador_palabras, total_palabras = _procesar_contenido_texto(contenido)
    
    # Aquí podrías añadir más lógica de procesamiento según lo que necesites
    # mostrar en tu template de detalles
    
    return render(request, 'detalles_procesamiento.html', {
        'texto': texto_obj,
        'texto_original': contenido,
        'total_palabras_original': total_palabras,
        # Agregar más variables según necesites para el template
    })