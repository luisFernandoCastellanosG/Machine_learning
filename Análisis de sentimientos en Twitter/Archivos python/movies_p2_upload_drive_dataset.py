from google.colab import drive
drive.mount('/content/gdrive')

import re
import pandas as pd
import nltk


df = pd.DataFrame()
df = pd.read_csv('/content/gdrive/My Drive/USTA-201902/USTA-201902_7°_DEEP_LEARNING/Documentos/libros_jupyter/PLN/DataSets/PLN_movie_data.csv', encoding='utf-8')

print("cargando archivo PLN_movie_data.csv desde google drive: USTA-201902/USTA-201902_7°_DEEP_LEARNING/Documentos/libros_jupyter/PLN/DataSets/")

# creamos una funcion llamada preprocessor
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
    text = (re.sub('[\W]+', ' ', text.lower()) +' '.join(emoticons).replace('-', ''))
    return text



#Aplicamos preprocessor al dataframe
print("Aplicando preprocessor para eliminar caracteres de HTML y emoticones")
df['review'] = df['review'].apply(preprocessor)
df.to_csv('movie_data_clean.csv', index=False, encoding='utf-8')
print("finaliza la creación del archivo movie_data_clean.csv")
