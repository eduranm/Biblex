import google.generativeai as genai
import requests
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time


key = 'API_KEY'
genai.configure(api_key=key)
model = genai.GenerativeModel('models/gemini-2.0-flash')


def get_keywords(texto):
    safety_config = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

    config = genai.types.GenerationConfig(top_k=1, top_p=0, temperature=0.1, candidate_count=1)

    reglas = """
        Selecciona términos con el máximo grado de precisión. No uses conceptos generales si es posible usar otros más concretos. Ejemplo: Prefiere "política fiscal" sobre "economía".
        Incluye todos los descriptores necesarios que reflejen los distintos aspectos del contenido. Sin embargo, si hay demasiadas opciones, prioriza términos aglutinadores.
        Los términos deben representar exactamente el contenido del documento. No deben reflejar contenidos de otras secciones (editoriales, índice, resumen externo).
        Aplica las reglas de manera consistente. Usa siempre los mismos términos para los mismos conceptos. Maneja listas de encabezamientos y tesauros disponibles.
        Evita interpretaciones subjetivas. El documento es la máxima autoridad. No impongas juicios personales.
        Descarta información irrelevante sin sacrificar especificidad o fidelidad. Usa tu criterio para determinar lo que debe ser recuperable en una búsqueda.
        Usa minúsculas, excepto en nombres propios. Ej: América Latina, justicia penal
        Preferencia por el singular, excepto donde el uso común sea plural. Ej: Prefiere "mineral" sobre "minerales"
        No usar palabras vacías (como "de", "para", "con", "el", "la"). No usar siglas o abreviaturas no normalizadas.
        No repetir palabras que ya aparecen en el título del documento, salvo si aportan valor temático adicional.
        Consultar recursos normalizados para elegir términos consistentes: Tesauro de la UNESCO, Tesauro de LILACS, Glosarios de Redalyc y Scielo, Listas controladas internas del sistema.
    """

    prompt = (f"Dime máximo 10 palabras clave dentro de las más relevantes del siguiente texto\n"
              f"La respuesta la requiero en formato JSON, las palabras clave encontradas escríbelas en español con espacios y acentos\n"
              f"Ejemplo:\n"
              '{"palabras":["palabra clave 1 en español", "palabra clave 2 en español", "palabra clave 3 en español" ...]}\n'
              f"Para obtener las palabras además sigue las siguientes reglas:{reglas}\n"
              f"El texto es el siguiente:{texto}"
              )

    attemps = 10

    while attemps > 0:
        try:
            response = model.generate_content(contents=prompt, generation_config=config, safety_settings=safety_config)
            attemps = 0
        except:
            print("ERROR QUOTA")
            print('tamaño:' + str(len(prompt)) + '')
            time.sleep(10)
            attemps -= 1
            
    try:
        return f"{response.text}"
    except:
        return '{"palabras" : "Sin resultado"}'