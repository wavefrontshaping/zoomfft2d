from scipy.signal import ZoomFFT
import numpy as np


class ZoomFFT2D:
    def __init__(self, n, m, f_center, f_range, pos_center=None, direction="forward"):
        nx, ny = n
        mx, my = m
        self.n = n
        self.m = m
        self.norm = np.sqrt(np.prod(self.n))
        self.direction = direction

        if direction not in ["forward", "backward"]:
            raise ValueError("direction must be 'forward' or 'backward'")
        if isinstance(f_center, tuple) or isinstance(f_center, list):
            self.f_center = [2 * f for f in f_center]
        elif isinstance(f_center, float) or isinstance(f_center, int):
            self.f_center = (2 * f_center, 2 * f_center)
        else:
            raise ValueError("f_center must be a tuple or a float")

        if isinstance(f_range, tuple) or isinstance(f_range, list):
            self.f_range = [f for f in f_range]
        elif isinstance(f_range, float) or isinstance(f_range, int):
            self.f_range = (f_range, f_range)
        else:
            raise ValueError("f_range must be a tuple or a float")

        print(self.f_center, self.f_range)

        if pos_center is None:
            self.pos_center = ((self.n[0] - 1) / 2, (self.n[1] - 1) / 2)
        elif isinstance(pos_center, tuple) or isinstance(pos_center, list):
            self.pos_center = pos_center
        else:
            raise ValueError("pos_center must be a tuple")

        self.fnx = [
            self.f_center[0] - self.f_range[0] / 2,
            self.f_center[0] + self.f_range[0] / 2,
        ]
        self.fny = [
            self.f_center[1] - self.f_range[1] / 2,
            self.f_center[1] + self.f_range[1] / 2,
        ]
        self.f1 = ZoomFFT(nx, m=mx, fn=self.fnx)
        self.f2 = ZoomFFT(ny, m=my, fn=self.fny)
        self.ref = None
        self._get_phase_ref()

    def _get_phase_ref(self):
        foc = np.zeros(self.n)

        if 2 * self.pos_center[0] % 1 == 0:
            start_x = int(self.pos_center[0]) + 1
            end_x = int(self.pos_center[0]) + 2
        else:
            start_x = int(self.pos_center[0])
            end_x = int(self.pos_center[0]) + 2

        if 2 * self.pos_center[1] % 1 == 0:
            start_y = int(self.pos_center[1]) + 1
            end_y = int(self.pos_center[1]) + 2
        else:
            start_y = int(self.pos_center[1])
            end_y = int(self.pos_center[1]) + 2

        foc[start_x:end_x, start_y:end_y] = 1

        ref = self(foc)
        self.ref = np.exp(-1j * np.angle(ref))

    def __call__(self, A):
        FFT = self.f1(A, axis=-2)
        FFT = self.f2(FFT, axis=-1)
        FFT = FFT / self.norm
        if self.direction == "backward":
            FFT = FFT[..., ::-1, ::-1]
        if self.ref is not None:
            return FFT * self.ref
        else:
            return FFT
