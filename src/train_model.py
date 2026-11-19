import tensorflow as tf
from tensorflow.keras import layers

import pandas as pd
import numpy as np
# "Timestamp","Units","Variable","Sensor Name","Flagged as Suspect Reading","Value","Quality"


def load_data_test():
    #abalone_train = pd.read_csv(
    #    "https://storage.googleapis.com/download.tensorflow.org/data/abalone_train.csv",
    #    names=["Length", "Diameter", "Height", "Whole weight", "Shucked weight",
    #       "Viscera weight", "Shell weight", "Age"])
    pm25_train = pd.read_csv("PM2.5_labelled_data_pruned_2.csv", names=["Value","Quality"])
    pm25_train.head()

    pm25_features = pm25_train.copy()
    pm25_labels = pm25_features.pop('Quality')
    print(pm25_labels)

    pm25_features = np.array(pm25_features)
    pm25_features

    normalize = layers.Normalization()
    normalize.adapt(pm25_features)
    pm25_model = tf.keras.Sequential([
        normalize,
        layers.Dense(1, activation='relu'),
        layers.Dense(10, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])

    pm25_model.compile(loss = "sparse_categorical_crossentropy",
                        optimizer = tf.keras.optimizers.Adam(),
                        metrics=["Accuracy"])

    pm25_model.fit(pm25_features, pm25_labels, epochs=50)
    #pm25_model.summary()

    return pm25_model

def test(model):
    pm25_train = pd.read_csv("model_test_data.csv", names=["Value"])
    print(model.predict(pm25_train))

def representative_dataset():
    for _ in range(100):
        yield [np.random.rand(0,1).astype(np.float32)]

def main():
    m = load_data_test()
    test(m)

    m.save("model.keras")

    converter = tf.lite.TFLiteConverter.from_keras_model(m)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.float32
    converter.inference_output_type = tf.float32
    tflite_model = converter.convert()

    with open("output.tflite", "wb") as file:
        file.write(tflite_model)

if __name__ == "__main__":
    main()