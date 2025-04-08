from colorsys import hls_to_rgb
import numpy as np
from scipy.ndimage import gaussian_filter


def generate_complex_pattern(N, sigma, sigma_env):
    # Generate a random complex pattern
    complex_pattern = np.random.rand(N, N) * np.exp(
        1j * np.random.rand(N, N) * 2 * np.pi
    )

    # Smooth the pattern using a Gaussian filter

    # Standard deviation for Gaussian kernel
    smooth_complex_pattern = gaussian_filter(complex_pattern, sigma=sigma * N)

    # Create a Gaussian envelope
    x = np.linspace(-1, 1, N)
    y = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x, y)
    gaussian_envelope = np.exp(-(X**2 + Y**2) / (2 * sigma_env**2))

    # Multiply the smoothed complex pattern by the Gaussian envelope
    pattern_with_envelope = smooth_complex_pattern * gaussian_envelope
    # Multiply the smoothed complex pattern by the Gaussian envelope
    pattern_with_envelope = smooth_complex_pattern * gaussian_envelope
    pattern_with_envelope = pattern_with_envelope / np.max(
        np.abs(pattern_with_envelope)
    )
    return pattern_with_envelope, X, Y


def colorize(
    z,
    theme="dark",
    saturation=1.0,
    beta=1.4,
    transparent=False,
    alpha=1.0,
    max_threshold=1,
):
    r = np.abs(z)
    r /= max_threshold * np.max(np.abs(r))
    arg = np.angle(z)

    h = (arg + np.pi) / (2 * np.pi) + 0.5
    l = 1.0 / (1.0 + r**beta) if theme == "white" else 1.0 - 1.0 / (1.0 + r**beta)
    s = saturation

    c = np.vectorize(hls_to_rgb)(h, l, s)  # --> tuple
    c = np.array(c)  # -->  array of (3,n,m) shape, but need (n,m,3)
    c = c.swapaxes(0, 2)
    ## The following is to match the orientation of the reference image as displayed
    ## by numpy for two-dimension arrays
    c = c.swapaxes(0, 1)
    if transparent:
        a = 1.0 - np.sum(c**2, axis=-1) / 3
        alpha_channel = a[..., None] ** alpha
        return np.concatenate([c, alpha_channel], axis=-1)
    else:
        return c


def generate_reference(X, Y, fx, fy):
    fx = fx * X.shape[1] * 1 / 2
    fy = fy * X.shape[0] * 1 / 2
    reference = np.exp(1j * 2 * np.pi * (X * fx + Y * fy))
    return reference


def crop_center(img, crop_width, crop_height):
    img_height, img_width = img.shape[:2]
    crop_width = min(img_width, crop_width)
    crop_height = min(img_height, crop_height)
    return img[
        (img_height - crop_height) // 2 : (img_height + crop_height) // 2,
        (img_width - crop_width) // 2 : (img_width + crop_width) // 2,
    ]
