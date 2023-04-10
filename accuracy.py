import tensorflow as tf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

model = tf.keras.models.load_model('Model/keras-3_model.h5')
test_data = tf.keras.preprocessing.image.ImageDataGenerator().flow_from_directory(
        'dataset/test',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical')
predictions = model.predict(test_data)
loss, accuracy = model.evaluate(test_data)

print('Testing Accuracy: ', accuracy)
y_pred = model.predict(test_data)
y_pred = np.argmax(y_pred, axis=1)
y_true = test_data.classes

cm = confusion_matrix(y_true, y_pred)
cm

sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=True, yticklabels=True)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.show()
