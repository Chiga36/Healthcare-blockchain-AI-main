import tensorflow as tf
import numpy as np
import pandas as pd

class AnomalyDetector:
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
        else:
            self.model = self._build_model()
            self._train_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation="relu", input_shape=(5,)),  # Example: 5 features
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        return model

    def _train_model(self):
        # Load sample data
        data = pd.read_csv("data/sample_data.csv")  # Columns: vitals, lab results, anomaly_label
        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        self.model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)
        self.model.save("ai/model.h5")

    def predict(self, patient_data):
        # Placeholder for federated learning
        # Future enhancement: Train across decentralized datasets using TensorFlow Federated
        data = np.array(patient_data).reshape(1, -1)
        return float(self.model.predict(data)[0])

    # Placeholder for public health analytics
    # Future enhancement: Extend to predict outbreaks by analyzing aggregated blockchain data