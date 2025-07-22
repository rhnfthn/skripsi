from tensorflow.keras.models import load_model

# Ganti dengan nama file model kamu
model = load_model('model_vgg16_pneumonia.h5')
# Simpan ulang tanpa optimizer
model.save('model_vgg16_pneumonia_small.h5', include_optimizer=False)
print("Model berhasil dikompres dan disimpan sebagai model_vgg16_pneumonia_small.h5")