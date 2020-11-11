print("------------------------")
label = {-1:'Sin sentimiento', 0:'Neutro', 1:'Positivo',2: 'Negativo'}
y = -1
proba = 0.5
print(label[y])

print("------------------------")
prediction='Neutro'
print("hola mundo")
inv_label = {'Sin sentimiento':-1, 'Neutro':0, 'Positivo':1,'Negativo':2}
print(inv_label)
y = inv_label[prediction]
if feedback != 'Aprobado':
    y = prediction

print(y)

47.48