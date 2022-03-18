from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
import os
from werkzeug.utils import secure_filename

def img(path, size, model_path):
    
    model = keras.models.load_model(model_path)
    size = size
    
    for d, sd, a in os.walk(path):
        list_names = a

    for name in list_names:
        img = Image.open(path + '\\' + name)
        img = img.resize(size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        pred = (model.predict(x) > 0.5).astype('int32')[0][0]
        if pred > 0.5:
            result = 'SIM, sua planta está doente!'
            color = '#FF0000'
            text_info = '''A doença causada por Hemileia Vastatrix (ferrugem) provoca queda precoce das folhas e seca dos ramos, afetando a produção de frutos do ano seguinte. É um patógeno que provoca prejuízos durante os anos de alta produção da cultura.'''
            danos = '''Danos: Em média, as perdas ficam em 35% quando as condições climáticas são favoráveis ao desenvolvimento da doença, mas, quando coincidem períodos de estiagem prolongada com alta incidência do fungo, os prejuízos podem ultrapassar 50%.'''
            controle = '''Fungicidas protetores: Cúpricos – Oxicloreto de cobre, hidróxido de cobre; Fungicidas sistêmicos: Solo (fungicida + inseticida) – Foliar (triazol, estrobilurina).'''
            real_value = 'A predição foi de: {}'.format(model.predict(x))
            return result, color, text_info, danos, controle, real_value
        else: 
            result = 'NÃO, sua planta está saudável!'
            color = '#008000'
            text_info = '''O algoritmo não detectou nenhum traço de ferrugem em sua planta. Caso a planta realmente esteja doente e a resposta não tenha sido precisa, tente cortar a imagem com foco na ferrugem.'''
            danos = "" 
            controle = ""
            real_value = 'A predição foi de: {}'.format(model.predict(x)) 
            return result, color, text_info, danos, controle, real_value

path = 'C:\\Users\\isacc\\Desktop\\CNN\\page\\cache_img'
size = (128, 128)
model_path = 'C:\\Users\\isacc\\Desktop\\CNN\\model1.keras'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/isacc/Desktop/CNN/page/cache_img/'

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')
	
@app.route('/response.html', methods=['POST'])
def response():
    for d, sd, arquivos in os.walk(path):
        lista = arquivos
    for name in lista:
        os.remove(os.path.join(path + '\\', name))

    response = request.files['file']
    name = secure_filename(response.filename)
    response.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
    result, color, text_info, danos, controle, real_value = img(path, size, model_path)
    return render_template('response.html', result=result, color=color, text_info=text_info, danos=danos, controle=controle, real_value=real_value)

if __name__ == '__main__':
	app.run(debug=True)