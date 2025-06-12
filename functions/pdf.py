import io
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import fitz


def read_pdf(pdf_path, margin=10):
    pdf_stream = io.BytesIO(pdf_path)
    pdf = extract_text(pdf_stream, laparams=LAParams(char_margin=10.0, word_margin=0.5))
    lines_total = []
    for l in pdf.split('\n'):
        if l not in lines_total:
            espacios = l.strip().split(' ')
            #Sólo es una palabra, no se agrega
            if len(espacios) > 1:
                lines_total.append(l)
    cleaned_text = '\n'.join(lines_total)
    return cleaned_text
    

def get_pdf(url, response=None):
    pdf_url = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        if response:
            pass
        else:
            response = requests.get(pdf_url, headers=headers, stream=True, verify=False)
    except:
        return ''

    if response.status_code == 200:

        #visor de pdf, buscaa la url real al pdf
        if 'view' in pdf_url:
            soup = BeautifulSoup(str(response.text), features="html.parser")
            #Todas las etiquetas a
            tags_a = soup.find_all('a')
            for tag_a in tags_a:
                if str(tag_a).find('href') != -1:
                    tmp_url = tag_a.get('href')
                    #busca la url de descarga
                    if 'download' in tmp_url:
                        pdf_url = tmp_url
                        if 'http' not in pdf_url:
                            pdf_url = 'http:' + pdf_url
                        break

            response = requests.get(pdf_url, headers=headers, stream=True, verify=False)

            if response.status_code != 200:
                return 'fallo'

        nombre_archivo = response.content

    else:
        return 'ERROR'

    try:
        texto_pdf = read_pdf(nombre_archivo)
    except:
        try:
            pdf_stream = io.BytesIO(nombre_archivo)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except:
            return 'ERROR'

    return texto_pdf