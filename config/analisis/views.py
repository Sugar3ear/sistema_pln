# views.py - Actualizar las importaciones
import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from .utils import procesar_texto_completo, limpiar_texto  # Cambiar a procesar_texto_completo

def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'subir.html', {'form': form})

def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'lista.html', {'textos': textos})

def analizar_texto(request, texto_id, n_grama=1):
    if 'n_grama' in request.GET:
        try:
            n_grama = int(request.GET.get('n_grama', 1))
            # Validar que n_grama esté en un rango razonable
            if n_grama < 1:
                n_grama = 1
            elif n_grama > 10:  # Límite máximo para evitar problemas de rendimiento
                n_grama = 10
        except (ValueError, TypeError):
            n_grama = 1
    
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    
    # Leer el contenido del archivo
    try:
        with texto_obj.archivo.open('r') as archivo:
            contenido = archivo.read()
    except:
        contenido = ""
    
    # Procesar el texto usando la nueva funcionalidad que incluye n-gramas
    resultado = procesar_texto_completo(contenido, n_grama)
    
    # Guardar el contenido original y procesado en la sesión para mostrarlo después
    request.session['texto_original'] = contenido
    request.session['texto_procesado'] = ' '.join(resultado['palabras_limpias'])
    
    return render(request, 'resultado.html', {
        'texto': texto_obj,
        'palabras_comunes': resultado['palabras_comunes'],
        'ngramas_comunes': resultado['ngramas_comunes'],
        'total_palabras': resultado['total_palabras'],
        'n_grama': n_grama,  # Asegurar que esta variable se pasa
        'texto_id': texto_id
    })

def ver_procesamiento(request, texto_id):
    """Vista para mostrar los detalles del procesamiento aplicado"""
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    
    # Leer el contenido del archivo
    try:
        with texto_obj.archivo.open('r') as archivo:
            contenido = archivo.read()
    except:
        contenido = ""
    
    # Obtener el texto original y procesado
    texto_original = contenido
    palabras_limpias = limpiar_texto(contenido)
    texto_procesado = ' '.join(palabras_limpias)
    
    # Contar estadísticas
    palabras_originales = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+\b', texto_original.lower())
    stopwords_eliminadas = len(palabras_originales) - len(palabras_limpias)
    
    # Encontrar símbolos eliminados
    simbolos_eliminados = set()
    for palabra in texto_original.split():
        simbolos = re.findall(r'[^\w\sáéíóúñüÁÉÍÓÚÑÜ]', palabra)
        simbolos_eliminados.update(simbolos)
    
    # Encontrar palabras con acentos en el texto original
    palabras_con_acentos = []
    for palabra in palabras_originales:
        if re.search(r'[áéíóúÁÉÍÓÚñÑüÜ]', palabra):
            palabras_con_acentos.append(palabra)
    
    return render(request, 'procesamiento.html', {
        'texto': texto_obj,
        'texto_original': texto_original,
        'texto_procesado': texto_procesado,
        'total_palabras_original': len(palabras_originales),
        'total_palabras_limpias': len(palabras_limpias),
        'stopwords_eliminadas': stopwords_eliminadas,
        'simbolos_eliminados': ', '.join(simbolos_eliminados) if simbolos_eliminados else 'Ninguno',
        'palabras_con_acentos': palabras_con_acentos[:20]  # Mostrar hasta 20 palabras con acentos
    })