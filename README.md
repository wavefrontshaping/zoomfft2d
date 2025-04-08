# ZoomFFT2D

The `ZoomFFT2D` class provides a convenient way to perform a zoomed Fast Fourier Transform (FFT) on two-dimensional. It is particularly useful for analyzing a localized frequency band (centered around a specified frequency). This implementation leverages SciPy’s `ZoomFFT` based on Chirp Z-transforms.

For more details on the underlying concepts and advanced usage, see the [off-axis FFT](/zoomfft2d/offaxis.ipynb) and the corresponding [tutorial](https://www.wavefrontshaping.net/post/id/90).

---

## Overview

The `ZoomFFT2D` class:
- **Performs a 2D Zoom FFT:** Applies the transform independently on the two dimensions using two `ZoomFFT` objects.
- **Handles Frequency Parameters:** Accepts center frequency (`f_center`) and frequency range (`f_range`) parameters (as floats or tuples), which are doubled internally.
- **Phase Reference Correction:** Computes a phase reference based on a localized area around a defined center (`pos_center`) to correct the phase of the FFT output.
- **Supports Direction:** Can output either a “forward” FFT result or a “backward” FFT by reversing the result.

---

## Initialization Parameters

- **n (tuple):**  
  Dimensions of the input array as `(nx, ny)`.

- **m (tuple):**  
  Number of FFT interpolation points for each axis as `(mx, my)`.

- **f_center (float or tuple):**  
  The center frequency/frequencies around which the FFT is calculated. Internally, each value is multiplied by 2.

- **f_range (float or tuple):**  
  The span of frequencies considered for the FFT, also multiplied by 2 internally. Defines the width of the frequency band around `f_center`.

- **pos_center (tuple, optional):**  
  The center position used to compute the phase reference. If not provided, it defaults to the center of the input array.

- **direction (string):**  
  Determines the output orientation of the FFT. Must be either `"forward"` (default) or `"backward"`. When set to `"backward"`, the FFT result is reversed.

---

## How It Works

1. **Frequency Axis Definition:**  
   The frequency limits for each axis (`fnx` and `fny`) are computed based on the provided `f_center` and `f_range`.

2. **ZoomFFT Objects Setup:**  
   Two `ZoomFFT` objects (`f1` and `f2`) are initialized – one for each axis.

3. **Phase Reference Calculation:**  
   The `_get_phase_ref` method is called upon initialization. It creates a small focused region around `pos_center` (or the center of the input if not specified) and computes a reference phase. This phase is used in the final FFT result to remove any unwanted phase variations. 
   This allows compensating for the fact that ZommFFT does not know about negative positions and consider that the reference of your coordinate system is in the corner of your image.
   It plays a similar role as using `fftshift`.     

4. **FFT Application:**  
   The `__call__` method applies the zoom FFT sequentially along the two axes. If the transform is in `"backward"` mode, the FFT output is reversed, corresponding to an inverse FFT. Finally it applies the phase slope correction to the result.

---

## Usage Example

```python
import numpy as np
from scipy.signal import ZoomFFT

# Assuming ZoomFFT2D is defined in zoomfft2d.py or inline as provided.
# from zoomfft2d import ZoomFFT2D

# Define input parameters
n = (256, 256)             # Dimensions of the input array.
m = (256, 256)             # FFT interpolation points.
f_center = (0.5, 0.5)        # Center frequency (normalized); gets doubled internally.
f_range = (1.0, 1.0)         # Frequency range for the FFT.
pos_center = None          # Defaults to the center of the array.
direction = "forward"      # FFT direction.

# Initialize the ZoomFFT2D object
zoom_fft = ZoomFFT2D(n, m, f_center, f_range, pos_center, direction)

# Create an example input array (e.g., random or your experimental data)
A = np.random.rand(*n)

# Apply the Zoom FFT
result = zoom_fft(A)

# `result` now holds the transformed array, with phase correction applied if available.
```