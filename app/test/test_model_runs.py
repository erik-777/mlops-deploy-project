import numpy as np
import onnxruntime as ort


def test_model_runs():
    """
    Prueba 1: El modelo responde a una entrada definida.
    """
    session = ort.InferenceSession("model.onnx")
    input_name = session.get_inputs()[0].name

    # Input aleatorio con shape [1, 1, 28, 28]
    x = np.random.rand(1, 1, 28, 28).astype("float32")

    outputs = session.run(None, {input_name: x})
    assert outputs[0].shape == (1, 10)
