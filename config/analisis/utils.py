import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

@dataclass
class ProcesamientoResultado:
    palabras_comunes: List[Tuple[str, int]]
    total_palabras: int
    palabras_limpias: List[str]
    estadisticas: Dict[str, int]
    texto_procesado: str

class ProcesadorTextoEspanol:
    """Procesador de texto especializado para español"""
    
    def __init__(self):
        self.stopwords = self._cargar_stopwords()
        self.caracteres_especiales = {'ñ', 'ü', 'Ñ', 'Ü'}
    
    def _cargar_stopwords(self) -> Set[str]:
        """Carga y normaliza las stopwords en español"""
        stopwords_base = {
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
        
        return {self._normalizar_acentos(palabra) for palabra in stopwords_base}
    
    def _normalizar_acentos(self, texto: str) -> str:
        """
        Normaliza caracteres acentuados preservando ñ y ü
        """
        # Proteger caracteres especiales del español
        caracteres_protegidos = {}
        for i, char in enumerate(self.caracteres_especiales):
            texto = texto.replace(char, f'__CHAR_{i}__')
            caracteres_protegidos[f'__CHAR_{i}__'] = char
        
        # Normalizar acentos
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
        
        # Restaurar caracteres especiales
        for placeholder, char in caracteres_protegidos.items():
            texto = texto.replace(placeholder, char)
        
        return texto
    
    def _limpiar_caracteres(self, texto: str) -> str:
        """
        Elimina caracteres no deseados y puntuación
        """
        return re.sub(r'[^\w\sñü]', ' ', texto)
    
    def _filtrar_palabras(self, palabras: List[str]) -> List[str]:
        """
        Filtra stopwords y palabras cortas
        """
        return [
            palabra for palabra in palabras 
            if palabra not in self.stopwords and len(palabra) > 1
        ]
    
    def preprocesar_texto(self, texto: str) -> List[str]:
        """
        Realiza todo el preprocesamiento del texto
        """
        # Convertir a minúsculas y normalizar
        texto = texto.lower()
        texto = self._normalizar_acentos(texto)
        
        # Limpiar caracteres
        texto = self._limpiar_caracteres(texto)
        
        # Tokenizar y filtrar
        palabras = texto.split()
        palabras_filtradas = self._filtrar_palabras(palabras)
        
        return palabras_filtradas
    
    def _generar_estadisticas(self, texto_original: str, palabras_limpias: List[str]) -> Dict[str, int]:
        """
        Genera estadísticas del procesamiento
        """
        palabras_originales = texto_original.split()
        
        return {
            'total_palabras_original': len(palabras_originales),
            'total_palabras_limpias': len(palabras_limpias),
            'stopwords_eliminadas': len(palabras_originales) - len(palabras_limpias),
            'palabras_unicas': len(set(palabras_limpias))
        }
    
    def procesar(self, texto: str, top_n: int = 20) -> ProcesamientoResultado:
        """
        Procesa el texto y devuelve todos los resultados
        """
        # Preprocesamiento
        palabras_limpias = self.preprocesar_texto(texto)
        
        # Análisis de frecuencia
        contador = Counter(palabras_limpias)
        palabras_comunes = contador.most_common(top_n)
        
        # Estadísticas
        estadisticas = self._generar_estadisticas(texto, palabras_limpias)
        
        return ProcesamientoResultado(
            palabras_comunes=palabras_comunes,
            total_palabras=len(palabras_limpias),
            palabras_limpias=palabras_limpias,
            estadisticas=estadisticas,
            texto_procesado=' '.join(palabras_limpias)
        )

# Función de conveniencia para uso rápido
def procesar_texto(texto: str, top_n: int = 20) -> ProcesamientoResultado:
    """
    Función helper para procesamiento rápido sin instanciar la clase
    """
    procesador = ProcesadorTextoEspanol()
    return procesador.procesar(texto, top_n)

# Ejemplo de uso
if __name__ == "__main__":
    texto_ejemplo = "El rápido zorro marrón salta sobre el perro perezoso. ¡Qué día tan hermoso!"
    
    resultado = procesar_texto(texto_ejemplo)
    
    print("Palabras más comunes:", resultado.palabras_comunes)
    print("Total de palabras:", resultado.total_palabras)
    print("Estadísticas:", resultado.estadisticas)