import os            #  trabajar sobre el sistema operativo
import sys           #  manipular archivos (cortar, copiar, borrar, crear)
import tarfile       #  Manipular archivos comprimidos (comprimir, descomprimir)
import time          #  calcular tiempo (en este caso tiempo de descarga de archivo)

import pyprind       #visualizar el progreso de ejecución una tarea en background
import pandas as pd
import numpy as np

print("Iniciando proceso de descarga del DATASET desde http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz")

#p0 : descargar el dataset
source = 'http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'
target = 'aclImdb_v1.tar.gz'

# funcion para descargar arcchivos y ver su avance
def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = progress_size / (1024.**2 * duration)
    percent = count * block_size * 100. / total_size
    sys.stdout.write("\r%d%% | %d MB | %.2f MB/s | %d segundos transcurrido" %
                    (percent, progress_size / (1024.**2), speed, duration))
    sys.stdout.flush()


if not os.path.isdir('aclImdb') and not os.path.isfile('aclImdb_v1.tar.gz'):
    
    if (sys.version_info < (3, 0)):
        import urllib
        urllib.urlretrieve(source, target, reporthook)
    
    else:
        import urllib.request
        urllib.request.urlretrieve(source, target, reporthook)

#P1 descomprir el dataset en una carpeta llamada a aclImdb
print("descomprimiendo el dataset en una carpeta llamada a aclImdb")
if not os.path.isdir('aclImdb'):

    with tarfile.open(target, 'r:gz') as tar:
        tar.extractall()

basepath = 'aclImdb'

#p2: preprocesar el DATASET 
print("preprocesar el DATASET: convirtiendo todos los documentos en un solo DataFrame")
labels = {'pos': 1, 'neg': 0}
pbar = pyprind.ProgBar(50000)

df = pd.DataFrame()

for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = os.path.join(basepath, s, l)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 
                      'r', encoding='utf-8') as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]], 
                           ignore_index=True)
            pbar.update()

df.columns = ['review', 'sentiment']

#p2.1 permutamos el dataset (randomizamos)
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
#p2.2 guardamos el dataframe en un CSV para uso futuro
df.to_csv('movie_data.csv', index=False, encoding='utf-8')
print("se termino de exportar DataFrame al archivo movie_data.csv que permitira facilidad en su procesamiento")
