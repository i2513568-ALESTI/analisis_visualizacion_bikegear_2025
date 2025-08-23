import numpy as np

# Conversión de tipos numpy a Python nativo
def to_python_type(val):
    if isinstance(val, (np.int64, np.int32)):
        return int(val)
    elif isinstance(val, (np.float64, np.float32)):
        return float(val)
    return val
