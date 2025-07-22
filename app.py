print("=== MULAI IMPORT FLASK ===")
from flask import Flask, render_template, request
print("=== MULAI IMPORT TENSORFLOW ===")
from tensorflow.keras.models import load_model
print("=== MULAI IMPORT NUMPY ===")
import numpy as np
print("=== MULAI IMPORT CV2 ===")
import cv2
print("=== MULAI IMPORT OS ===")
import os

print("=== MULAI INISIALISASI FLASK ===")
app = Flask(__name__, template_folder="templates")
print("=== MULAI LOAD MODEL ===")
model = load_model('model_vgg16_pneumonia_small.h5')
print("=== MODEL BERHASIL DILOAD ===")
class_names = ['NORMAL', 'PNEUMONIA']

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def predict_image(img_path):
    print(f"[DEBUG] Membaca gambar dari: {img_path}")
    img = cv2.imread(img_path)
    if img is None:
        print("[ERROR] Gambar tidak valid!")
        return "Gambar tidak valid", 0.0
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    kelas = int(pred[0][0] > 0.5)
    print(f"[DEBUG] Hasil prediksi: {class_names[kelas]}, Probabilitas: {float(pred[0][0])}")
    return class_names[kelas], float(pred[0][0])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    probability = None
    filename = None
    error_message = None
    if request.method == 'POST':
        try:
            file = request.files.get('file')
            print(f"[DEBUG] File diterima: {file}")
            if file and file.filename:
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                print(f"[DEBUG] File disimpan di: {filepath}")
                pred_label, prob = predict_image(filepath)
                prediction = pred_label
                probability = prob
                filename = file.filename
            else:
                error_message = 'Tidak ada file yang diupload.'
                print("[ERROR] Tidak ada file yang diupload.")
        except Exception as e:
            error_message = str(e)
            print('[ERROR] Error saat prediksi:', error_message)
    return render_template('predict.html', prediction=prediction, probability=probability, filename=filename, error_message=error_message)

@app.route('/pneumonia-info')
def pneumonia_info():
    return render_template('pneumonia_info.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 