import math



theta_deg = 60
theta_rad = theta_deg * math.pi / 180


# Mikrofon Sayım
N = 4

# Mikrofonlar arası mesafe [m]
d_m = 0.1

# i'inci mikrofonun referans mikrofona göre uzaklığı [m] 
d_i_m = [(i - 1) * d_m for i in range(2, N + 1)]


# Sıcaklık Parametreleri
temp_c = 25
temp_k = temp_c + 273.15

# Ses Hızı [m/s]
c_m_s = 331.3 * math.sqrt((1 + temp_k) / 273)


print(f"{d_i_m[0]}")
print(f"{c_m_s}")

print(f"{math.cos(theta_rad)}")

print(f"{math.sqrt(4)}")
