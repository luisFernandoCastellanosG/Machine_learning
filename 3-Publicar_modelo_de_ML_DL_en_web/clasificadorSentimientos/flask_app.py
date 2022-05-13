from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)
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
        y=1
        proba=1
        #y, proba = classify(texto)
        return render_template('resultado.html',
                                content=texto,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)