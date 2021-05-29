
import re
import pandas as pd

print("tomando como nuevo DataFrame el archivo movie_data_clean.csv")
df = pd.DataFrame()
df = pd.read_csv('movie_data_clean.csv', encoding='utf-8')

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline                         # permite implementar métodos de ajuste y transformación
from sklearn.linear_model import LogisticRegression           # modelo de regresión logistica
from sklearn.feature_extraction.text import TfidfVectorizer   #conversor de texto a vector
from sklearn.model_selection import GridSearchCV              #búsqueda de cuadrícula con validación cruzada (para usar con regresión logistica)



#funciones para tokenizar (clasico y metodo porter)
def tokenizer(text):
    return text.split()

porter = PorterStemmer()

def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]

# separamos los datos de entrenamiento y de pruebas
X_train = df.loc[:25000, 'review'].values
y_train = df.loc[:25000, 'sentiment'].values
X_test = df.loc[25000:, 'review'].values
y_test = df.loc[25000:, 'sentiment'].values

#propiedades de la conversor de texto a vectores
print("configurando propiedades: idioma ingles, vectorizando el DataFrame, creando pipeline y GridSearchCV")
tfidf = TfidfVectorizer(strip_accents=None,
                        lowercase=False,
                        preprocessor=None)


stop = stopwords.words('english')

param_grid = [{'vect__ngram_range': [(1, 1)],
               'vect__stop_words': [stop, None],
               'vect__tokenizer': [tokenizer],
               'clf__penalty': ['l1', 'l2'],
               'clf__C': [1.0, 10.0]},]

#mezclamos regresión lineal y vectores de textos en un solo proceso
lr_tfidf = Pipeline([('vect', tfidf),
                     ('clf', LogisticRegression(random_state=0))])

gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid,
                           scoring='accuracy',
                           cv=5,
                           verbose=1,
                           n_jobs=1)
#entrenamos el modelo
print ("Entrenando el modelo, este proceso puede demorar varios minutos")
gs_lr_tfidf.fit(X_train, y_train)
#Mostramos los resultados
print('Mejores set de parametros: %s ' % gs_lr_tfidf.best_params_)
print('CV exactitud: %.3f' % gs_lr_tfidf.best_score_)
      
clf = gs_lr_tfidf.best_estimator_
print('Test exactitud: %.3f' % clf.score(X_test, y_test))