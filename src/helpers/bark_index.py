import numpy as np


class BarkIndex:
    def __init__(self, sample_rate=16000, n_fft=512):
        """
        Initializes the psychoacoustic coordinator.

        :param sample_rate: Audio sampling rate (e.g., 16000 Hz)
        :param n_fft: FFT window size used to compute the frame spectrum
        """
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        # Precalculate physical frequency frequencies mapping to STFT bin indices
        self.fft_freqs = np.fft.rfftfreq(n_fft, d=1 / sample_rate)

    def to_bark(self, frequency_hz):
        """
        Converts critical frequency in Hz to the Bark scale position (z).
        Supports both scalars and NumPy arrays.
        """
        freqs = np.atleast_1d(frequency_hz)

        # Traunmüller analytical formula
        bark = (26.81 * freqs) / (1960.0 + freqs) - 0.53

        # Post-processing clean up for sub-zero edge cases near 0Hz
        bark = np.where(bark < 0, 0.0, bark)

        return bark if bark.ndim > 0 else bark[0]

    def get_quiet_threshold(self, frequency_hz):
        """
        Calculates Terhardt's absolute threshold in quiet: Quiet(nu) in dB SPL.
        """
        # Convert Hz to kHz and clamp to avoid division by zero errors at 0 Hz
        f_khz = np.clip(np.atleast_1d(frequency_hz) / 1000.0, 1e-5, None)

        # Terhardt's equation
        quiet_db = (3.64 * (f_khz ** -0.8)
                    - 6.5 * np.exp(-0.6 * (f_khz - 3.3) ** 2)
                    + 0.001 * (f_khz ** 4))

        return quiet_db if quiet_db.ndim > 0 else quiet_db[0]

    def find_maskers(self, frame_spectrum, peak_threshold_db=-30):
        """
        Locates acoustic maskers inside a frame's power/magnitude spectrum.
        Uses a local maxima detection filter.

        :param frame_spectrum: 1D NumPy array representing the magnitudes/power of the STFT frame
        :param peak_threshold_db: Dynamic range ceiling floor to filter out irrelevant floor noise
        :return: List of masker frequencies in Hz
        """
        masker_frequencies = []

        # Simple, robust peak picking loop across frequency bin ranges
        for i in range(1, len(frame_spectrum) - 1):
            # Check if index is a local maximum
            if frame_spectrum[i] > frame_spectrum[i - 1] and frame_spectrum[i] > frame_spectrum[i + 1]:
                # Convert magnitude to log decibel representation for filtering
                magnitude_db = 20 * np.log10(frame_spectrum[i] + 1e-8)
                if magnitude_db > peak_threshold_db:
                    masker_frequencies.append(self.fft_freqs[i])

        return masker_frequencies

    def spreading_function(self, b_nu, b_i):
        """
        Calculates the spreading effect T[b_nu, b_i] in dB using Schroeder's model.

        :param b_nu: Target critical band value (maskee) in Barks
        :param b_i: Source critical band value (masker) in Barks
        """
        delta_z = b_nu - b_i

        # Schroeder's prototype base equation
        sf_db = 15.81 + 7.5 * (delta_z + 0.474) - 17.5 * np.sqrt(1.0 + (delta_z + 0.474) ** 2)

        return sf_db