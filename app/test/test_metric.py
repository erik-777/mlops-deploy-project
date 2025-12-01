import numpy as np
import onnxruntime as ort

METRIC_THRESHOLD = 0.85  # mínimo aceptable


def test_model_metric_above_threshold():
    """
    Prueba 2: La métrica (accuracy) está por encima de un umbral definido.
    """
    data = np.load("test_data.npz")
    X = data["X"]   # shape [N, 1, 28, 28]
    y = data["y"]   # shape [N]

    session = ort.InferenceSession("model.onnx")
    input_name = session.get_inputs()[0].name

    preds = []
    n_samples = 300  # subset para mantener el CI rápido
    for i in range(n_samples):
        x = X[i:i+1].astype("float32")
        output = session.run(None, {input_name: x})[0]  # [1, 10]
        pred_digit = int(output.argmax())
        preds.append(pred_digit)

    preds = np.array(preds)
    acc = (preds == y[:n_samples]).mean()

    assert acc >= METRIC_THRESHOLD, f"Accuracy {acc:.3f} < threshold {METRIC_THRESHOLD}"
