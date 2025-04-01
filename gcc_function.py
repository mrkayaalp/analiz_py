import numpy as np

# Ağırlık Fonksiyonları

# ------------------------------------------------------------------------------
# PHAT: Faz bilgisine dayali agirliklandirma
# Genlik bilgisi yok sayilir. Gecikme tahmininde yaygin olarak kullanilir.
# Gurultuye karsi dayaniklidir.
def phat_weight(X1, X2):
    """
    PHAT (Phase Transform) agirlik fonksiyonu.

    Faz bilgisine dayali olarak agirliklandirma yapar.
    Genellikle GCC-PHAT algoritmasinda kullanilir.

    Args:
        X1: Birinci sinyalin FFT sonucu
        X2: Ikinci sinyalin FFT sonucu

    Returns:
        Normalize edilmis PHAT agirlikli spektrum
    """
    eps = 1e-10
    return 1 / (np.abs(X1 * np.conj(X2)) + eps)


# ------------------------------------------------------------------------------
# Roth: Birinci sinyalin gucune gore normalize eder
# Duyarlilik azaltilarak gurultulu ortamlarda daha stabil olabilir.
def roth_weight(X1):
    """
    Roth agirlik fonksiyonu.

    Birinci sinyalin gucu kullanilarak normalize edilir.

    Args:
        X1: Birinci sinyalin FFT sonucu

    Returns:
        Roth agirlikli spektrum
    """
    eps = 1e-10
    return 1 / (np.abs(X1 * np.conj(X1)) + eps)




# ------------------------------------------------------------------------------
# SCOT: Iki sinyalin guc spektrumlarinin geometrik ortalamasi kullanilir
# Faz ve genlik bilgileri birlikte degerlendirilir.
def scot_weight(X1, X2):
    """
    SCOT (Smoothed Coherence Transform) agirlik fonksiyonu.

    Iki sinyalin guclerinin geometrik ortalamasi ile normalize eder.

    Args:
        X1: Birinci sinyalin FFT sonucu
        X2: Ikinci sinyalin FFT sonucu

    Returns:
        SCOT agirlikli spektrum
    """
    eps = 1e-10
    return 1 / (np.sqrt(np.abs(X1 * np.conj(X1) * X2 * np.conj(X2))) + eps)


# ------------------------------------------------------------------------------
# MLE: Maksimum Benzerlik Tahmini
# Coherence (benzerlik) fonksiyonu kullanilarak istatistiksel agirliklandirma yapar.
def wiener_hopf_filter(X1, X2):
    """
    Koherens (benzerlik) fonksiyonu hesaplar.

    Args:
        X1: Birinci sinyalin FFT sonucu
        X2: Ikinci sinyalin FFT sonucu

    Returns:
        gamma(w) - Koherens fonksiyonu
    """
    return ((X1 * np.conj(X2)) / np.sqrt(X1 * np.conj(X1) * X2 * np.conj(X2))) 

def mle_weight(X1, X2):
    """
    MLE (Maximum Likelihood Estimation) agirlik fonksiyonu.

    Koherens fonksiyonuna dayali olarak istatistiksel olarak guclu bir normalize islemi yapar.

    Args:
        X1: Birinci sinyalin FFT sonucu
        X2: Ikinci sinyalin FFT sonucu

    Returns:
        MLE agirlikli spektrum
    """

    gamma = wiener_hopf_filter(X1, X2)
    S = X1 * np.conj(X2)         # Cross power spectrum
    return (np.abs(gamma**2) / (np.abs(S) * np.abs(1 - np.abs(gamma**2))))

# none
def none_weight():
    return 1


# Agirlik fonksiyonları sözlügü
WEIGHT_FUNCTIONS = {
    'phat' : phat_weight,
    'roth' : roth_weight,
    'scot' : scot_weight,
    'mle'  : mle_weight,
    'none' : none_weight
}


def gcc_weighted(x1, x2, fs, weighting='phat'):
    """
    Genel GCC algoritması. Belirli bir ağırlık fonksiyonu ile zaman gecikmesi tahmini yapar.

    Args:
        x1: Birinci sinyal
        x2: İkinci sinyal
        fs: Örnekleme frekansı
        weighting: 'phat', 'roth', 'scot', 'none' seçeneklerinden biri

    Returns:
        tdoa: Tahmin edilen zaman farkı (saniye cinsinden)
    """    
    N = max(len(x1), len(x2))
    
    # Sinyaller Frekans Alanına Geciriliyor
    X1 = np.fft.fft(x1, n=N)
    X2 = np.fft.fft(x2, n=N)

    # GCC 
    R = X1 * np.conj(X2)

    # Kullanıcı Tarafindan Secilen Agirlik Fonksiyonu Sozlukte Yoksa Hata Cıkar
    if weighting not in WEIGHT_FUNCTIONS:
        raise ValueError(f"Unknown weighting: {weighting}. Choose from {list(WEIGHT_FUNCTIONS.keys())}")

    # Agirlik Fonk. Secimi
    if weighting == 'rhot':
        weight_func = WEIGHT_FUNCTIONS[weighting](X1)
    elif weighting == 'none':
        weight_func = WEIGHT_FUNCTIONS[weighting]()
    else:
        weight_func = WEIGHT_FUNCTIONS[weighting](X1, X2)

    # GCC ve Ağırlık Fonksiyonu Çarpımı
    R_weigthed = R * weight_func

    # Burda ters FFT alıyoruz real kısmını almazsak ne olur?
    r = np.fft.ifft(R_weigthed).real
    r = np.fft.fftshift(r)  # Çapraz korelasyonu sıfır merkezli hale getir


    # TODO: Burayi daha iyi anla
    lags = np.arange(-N//2, N//2) / fs  # Gecikmelerin ölçeklenmesi (saniye cinsinden)
    max_idx = np.argmax(np.abs(r))
    print(max_idx)
    tdoa = lags[N-max_idx]
    return tdoa, r, lags
