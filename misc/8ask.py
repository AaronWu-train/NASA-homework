import numpy as np
import matplotlib.pyplot as plt

def generate_8ask_passband(symbols, symbol_rate=1.0, samples_per_symbol=100, carrier_freq=5.0):
    """
    產生 8-ASK 經載波的波形與基帶包絡線
    - symbols: 符號序列 (每個值介於 0～7)
    - symbol_rate: 符號速率 (symbols/sec)
    - samples_per_symbol: 每符號取樣點數 (建議 ≤100)
    - carrier_freq: 載波頻率 (Hz)
    回傳:
      t: 時間軸 (s)
      baseband: 基帶包絡線振幅
      waveform: 經載波調製後的波形
    """
    M = 8
    fs = symbol_rate * samples_per_symbol
    levels = np.arange(1, M + 1, 1)  
    amplitudes = levels[symbols]
    
    num_samples = len(symbols) * samples_per_symbol
    t = np.arange(num_samples) / fs
    baseband = np.repeat(amplitudes, samples_per_symbol)
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    waveform = baseband * carrier
    return t, baseband, waveform

if __name__ == "__main__":
    symbols = np.arange(8)
    t, baseband, waveform = generate_8ask_passband(
        symbols,
        symbol_rate=1.0,
        samples_per_symbol=100,
        carrier_freq=5.0
    )

    plt.figure(figsize=(10, 6))
    plt.plot(t, waveform, label="Waveform")
    plt.plot(t, baseband, drawstyle='steps-post', label="Amplitude")
    plt.title("8-ASK Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("8-ask.png", dpi=300, bbox_inches="tight")
