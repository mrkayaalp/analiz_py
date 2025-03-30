import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.io.wavfile as wav
import math

# Güncellenmiş GCC-PHAT ile TDOA Hesaplama
def gcc_phat(x1, x2, fs):
    N = max(len(x1), len(x2))
    X1 = np.fft.fft(x1, n=N)
    X2 = np.fft.fft(x2, n=N)
    R = X1 * np.conj(X2)
    R /= np.abs(R + 1e-10)  # Küçük değer ekleyerek sıfıra bölmeyi engelle
    
    r = np.fft.ifft(R).real
    r = np.fft.fftshift(r)  # Çapraz korelasyonu sıfır merkezli hale getir

    lags = np.arange(-N//2, N//2) / fs  # Gecikmelerin ölçeklenmesi
    max_idx = np.argmax(np.abs(r))
    print(max_idx)
    return lags[N-max_idx]

def calculate_sound_speed(temp_c):
    temp_k = temp_c + 273.15
    return 331.45 * math.sqrt((1 + temp_k) / 273)

def read_wav_file(file_path, sampling_rate):
    fs, data = wav.read(file_path)
    
    # Verilen örnekleme frekansına göre yeniden örnekleme yap
    if fs != sampling_rate:
        data = signal.resample(data, int(len(data) * sampling_rate / fs))
    
    # Stereo ise mono'ya çevir
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    return data.astype(np.float32) / np.max(np.abs(data))

def main():
    # Mikrofon Sayısı
    N = 4

    # Mikrofonlar arası mesafe [m]
    d_m = 0.15

    # Mikrofon konumları (referans mikrofona göre)
    d_i_m = np.array([(i - 1) * d_m for i in range(2, N + 1)])

    # Sıcaklık Parametreleri
    temp_c = 25

    # Ses Hızı [m/s]
    c_m_s = calculate_sound_speed(temp_c)

    # Açı Parametreleri (Gerçek geliş açısı)
    theta_deg = 45
    theta_rad = np.deg2rad(theta_deg)

    # Zaman Farkları (Mikrofonlara ulaşma gecikmesi)
    tau_i_s = d_i_m * np.cos(theta_rad) / c_m_s

    # WAV Dosyasını Okuma
    fs = 48000
    source_signal = read_wav_file('sample.wav', fs)
    t = np.linspace(0, len(source_signal) / fs, num=len(source_signal), endpoint=False)

    # Mikrofonlara Ulaşan Sinyaller
    mic_signals = np.zeros((N, len(source_signal)))
    mic_signals[0, :] = source_signal  # Referans mikrofon

    # Ses Gecikmesini Diğer Mikrofonlara Ekler
    for i in range(1, N):
        """
        Ayrik Zamanda Ne Kadar kaydirilmasi Gerektiği:
            kaydirilacak_örnekleme_sayisi = zaman_gecikmesi * ornekleme_frekansi
            
        NOT: round sayesinde ondalikli sayilar yuvarlanir

        """   
        delay_samples = int(round(tau_i_s[i - 1] * fs))


        """ 
        Verilen sinyali  istenilen örnekleme kadar sağa kaydirir

        NOT: Amaç gecikmeyi ayrik zamanda gerceklemek
        
        """
        mic_signals[i, :] = np.roll(source_signal, delay_samples)

    # Mikrofon Sinyalleri Görselleştirme
    plt.figure()
    for i in range(N):
        plt.plot(t, mic_signals[i, :], label=f'Mikrofon {i+1}')
    plt.xlabel('Zaman [s]')
    plt.ylabel('Genlik')
    plt.title('Mikrofonlara Ulaşan Sinyaller')
    plt.legend()
    plt.grid(True)
    plt.show()

    # TDOA Hesaplama (Yan yana mikrofon çiftleri için)
    time_delay_estimate = np.array([gcc_phat(mic_signals[i], mic_signals[i+1], fs) for i in range(N-1)])

    # DEBUG --------------------------------------------------------------------------------------
    print(f"Gerçek Zaman Farkları: {tau_i_s}")
    print(f"Tahmini Zaman Farkları: {time_delay_estimate}")

    # Açıyı Her Mikrofon Çifti İçin Tahmin Etme
    angle_estimates = np.arccos((time_delay_estimate * c_m_s) / d_m) * 180 / np.pi

    # Ortalama açı hesaplama
    average_angle = np.mean(angle_estimates)

    # Sonuçları Görselleştirme
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot([0, np.deg2rad(theta_deg)], [0, 1], '-b', linewidth=2, label='Gerçek Açı')
    ax.plot([0, np.deg2rad(average_angle)], [0, 1], '-k', linewidth=2, label='Ortalama Tahmini Açı')
    for angle in angle_estimates:
        ax.plot([0, np.deg2rad(angle)], [0, 1], '--r', linewidth=1)
    ax.legend()
    ax.set_title("TDOA ile Kaynak Açısı Tahmini")
    plt.show()

    # Sonuçları Yazdırma
    print(f"Gerçek Açı: {theta_deg} derece")
    print(f"Tahmin Edilen Açılar (Her Mikrofon Çifti İçin): {angle_estimates}")
    print(f"Ortalama Tahmini Açı: {average_angle:.2f} derece")

main()
