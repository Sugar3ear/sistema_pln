import re
import unicodedata
from collections import Counter

# Lista de stopwords en español (incluyendo versiones acentuadas)
STOPWORDS_ES = {
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 
    'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 
    'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 
    'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 
    'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 
    'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 
    'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 
    'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 
    'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 
    'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 
    'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 
    'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 
    'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 
    'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 
    'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 
    'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 
    'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 
    'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 
    'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá', 
    'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 
    'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 
    'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 
    'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 
    'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 
    'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 
    'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 
    'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 
    'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 
    'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 
    'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 
    'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 
    'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 
    'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 
    'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 
    'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 
    'tenidos', 'tenidas', 'tened', 'él', 'ésta', 'éstas', 'éste', 'éstos', 'última', 'últimas', 
    'último', 'últimos', 'aún', 'dónde', 'cómo', 'cuándo', 'cuánto', 'cuánta', 'cuántos', 
    'cuántas', 'qué', 'quiénes', 'también', 'además', 'mientras', 'aunque', 'pero', 'sino', 
    'porque', 'aquel', 'aquella', 'aquellos', 'aquellas', 'ése', 'ésa', 'ésos', 'ésas', 
    'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 
    'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 
    'vuestras', 'cuyo', 'cuya', 'cuyos', 'cuyas'
}

def normalizar_acentos(texto):
    """
    Normaliza los caracteres acentuados para mejorar la coincidencia
    pero preserva las letras ñ y ü que son importantes en español
    """
    # Separar la ñ y ü para que no se normalicen
    texto = texto.replace('ñ', '__n_tilde__').replace('ü', '__u_dieresis__')
    texto = texto.replace('Ñ', '__N_tilde__').replace('Ü', '__U_dieresis__')
    
    # Normalizar acentos (á -> a, é -> e, etc.)
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    
    # Restaurar la ñ y ü
    texto = texto.replace('__n_tilde__', 'ñ').replace('__u_dieresis__', 'ü')
    texto = texto.replace('__N_tilde__', 'Ñ').replace('__U_dieresis__', 'Ü')
    
    return texto

def limpiar_texto(texto):
    """
    Función para limpiar el texto:
    1. Convertir a minúsculas
    2. Eliminar símbolos de puntuación
    3. Eliminar stopwords en español
    """
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Normalizar acentos pero preservar ñ y ü
    texto = normalizar_acentos(texto)
    
    # Eliminar símbolos de puntuación y caracteres especiales (manteniendo letras, números, ñ, ü y espacios)
    texto_limpio = re.sub(r'[^\w\sñü]', ' ', texto)
    
    # Tokenizar
    palabras = texto_limpio.split()
    
    # Normalizar stopwords para comparación (también sin acentos)
    stopwords_normalizadas = {normalizar_acentos(palabra) for palabra in STOPWORDS_ES}
    
    # Eliminar stopwords y palabras de un solo carácter
    palabras_filtradas = [
        palabra for palabra in palabras 
        if palabra not in stopwords_normalizadas and len(palabra) > 1
    ]
    
    return palabras_filtradas

def procesar_texto(contenido):
    """
    Función principal para procesar el texto y generar estadísticas
    """
    # Limpiar el texto
    palabras_limpias = limpiar_texto(contenido)
    
    # Generar histograma con el texto limpio
    contador_palabras = Counter(palabras_limpias)
    palabras_comunes = contador_palabras.most_common(20)  # Top 20 palabras
    
    return {
        'palabras_comunes': palabras_comunes,
        'total_palabras': len(palabras_limpias),
        'palabras_limpias': palabras_limpias
    }
    
def obtener_estadisticas_procesamiento(texto_original, palabras_limpias):
    """
    Función para obtener estadísticas detalladas del procesamiento
    """
    palabras_originales = texto_original.split()
    
    return {
        'total_palabras_original': len(palabras_originales),
        'total_palabras_limpias': len(palabras_limpias),
        'stopwords_eliminadas': len(palabras_originales) - len(palabras_limpias),
        'texto_procesado': ' '.join(palabras_limpias)
    }

def generar_ngramas(tokens, n=2):
    """
    Genera n-gramas a partir de una lista de tokens
    
    Args:
        tokens (list): Lista de tokens
        n (int): Tamaño de los n-gramas (2 para bigramas, 3 para trigramas, etc.)
    
    Returns:
        list: Lista de n-gramas
    """
    if n <= 1 or len(tokens) < n:
        return []
    
    ngramas = []
    for i in range(len(tokens) - n + 1):
        ngrama = ' '.join(tokens[i:i+n])
        ngramas.append(ngrama)
    
    return ngramas

def procesar_texto_completo(contenido, n_grama=1):
    """
    Función principal para procesar el texto y generar estadísticas incluyendo n-gramas
    """
    # Limpiar el texto
    palabras_limpias = limpiar_texto(contenido)
    
    # SIEMPRE generar histograma con palabras individuales
    contador_palabras = Counter(palabras_limpias)
    palabras_comunes = contador_palabras.most_common(20)  # Top 20 palabras
    
    # Generar n-gramas solo si se solicita (n > 1) y hay suficientes palabras
    ngramas_comunes = []
    if n_grama > 1 and len(palabras_limpias) >= n_grama:
        ngramas = generar_ngramas(palabras_limpias, n_grama)
        if ngramas:
            contador_ngramas = Counter(ngramas)
            ngramas_comunes = contador_ngramas.most_common(20)  # Top 20 n-gramas
    
    return {
        'palabras_comunes': palabras_comunes,  # SIEMPRE incluido
        'ngramas_comunes': ngramas_comunes,    # Solo cuando n > 1
        'total_palabras': len(palabras_limpias),
        'palabras_limpias': palabras_limpias,
        'n_grama': n_grama
    }
