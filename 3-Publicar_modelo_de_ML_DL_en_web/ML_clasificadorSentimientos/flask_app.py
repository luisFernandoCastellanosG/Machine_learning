from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
#CountVectorizer proporcionado por la biblioteca scikit-learn para vectorizar oraciones.
from sklearn.feature_extraction.text import CountVectorizer
#librerias para importar el modelo
import pickle
import os
import numpy as np
#librerias para base de datos
import sqlite3

app = Flask(__name__)

##----------carga de modelos para clasificacion-------
#cargando el modelo
cur_dir = os.path.dirname(__file__)
modeloPLNRegLogNew = pickle.load(open(os.path.join(cur_dir,'modeloIA', 'LogRegression_PLN_classSentimientos_model.sav'), 'rb'))
#cargando el vocabulario
vocabularyNew= pickle.load(open(os.path.join(cur_dir,'modeloIA','vocabulary.pkl'), 'rb'))
vectorizerNew = CountVectorizer(min_df=0, lowercase=True,vocabulary = vocabularyNew)  #creando un nuevo vectorizador con el vocabulario cargado


##----------clasificación del texto ingresado por el usuario usando el clasificador entrenado
db = os.path.join(cur_dir, 'DB_sentimientos_Esp.sqlite')
def f_clasificar(texto):
    label   = {0: 'Negativo',1:'Positivo'}
    oracion =[texto]
    x_bag   = vectorizerNew.transform(oracion)  #convertimos la oración al array del bagword
    predict =modeloPLNRegLogNew.predict(x_bag)[0]
    return label[predict]

#-------DML en sqllite--------
def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO sentimientos_db (texto, sentimento, fecha)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

def sqlite_select(path):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	c.execute("SELECT texto, sentimento, fecha FROM sentimientos_db")
	results = c.fetchall()
	return results

##---------DOOM/REQUEST entre HTMLS---------------
#clase que permite crear campos en formulario
class evaluarForm(Form):
    evaluarText = TextAreaField('',[validators.DataRequired(),
                                    validators.length(min=15)])

@app.route('/')
def index():
    form = evaluarForm(request.form)
    return render_template('index.html', form=form)

#esta funcion se ejecuta cuando en index.php en el action="/resultadoIA" llamando a la funcion
@app.route('/resultadoIA', methods=['POST'])
def resultadoIA():
    form = evaluarForm(request.form)
    if request.method == 'POST' and form.validate():
        texto = request.form['evaluarText']
        predict = f_clasificar(texto)
        return render_template('resultado.html',
                                content=texto,
                                prediction=predict)
    return render_template('index.html', form=form)

@app.route('/gracias', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    texto = request.form['texto']
    prediction = request.form['prediction']
    inv_label = {'Positivo':1,'Negativo':0}
    y = inv_label[prediction]
    sqlite_entry(db, texto, y)
    return render_template('gracias.html')

@app.route('/sqliteReport', methods=['POST'])
def sqliteReport():
	dataset =sqlite_select(db)
	return render_template('sqliteReport.html', dataset=dataset)

if __name__ == '__main__':
    app.run(debug=True)