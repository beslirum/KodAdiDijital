import random #veri setini oluşturmak amaçlı
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr #korelasyon analizi
import matplotlib.pyplot as plt #görselleştirmek için 

n = 1000
brands = ['BMW', 'Audi', 'Mercedes', 'Toyota', 'Hyundai', 'RangeRover', 'Mini', 'Ford']
fuel_types=["Benzin", "Dizel", "Elekrtik", "Hibrit"]
transmissions = ["Manuel", "Otomatik"]
colors=["Beyaz", "Siyah", "Gri", "Mavi", "Kırmızı"]
region = ["İstanbul", "Ankara","İzmir","Bursa","Adana"]

data = [] #veriyi ürettikten sonra bu boş listeye kaydedecek.

for i in range(n):
  brand = random.choice(brands) 
  #yukarıda tanımlanan brands ile aynı değil karıştırma
  model_year = random.randint(2013,2024)
  km = random.randint(10_000,200_000)
  fuel = random.choice(fuel_types) 
  transmission = random.choice(transmissions)
  engine_size = min(max(random.gauss(1.6, 0.5), 0.9), 4.5) 
  # Ortalaması 1.6, standart sapması 0.5 olan normal dağılımdan bir motor hacmi değeri üretir.
  # Ancak bu değeri, 0.9 (min) ve 4.5 (max) litr arasında sınırlandırır (kırpar/clamp).
  # Yani, üretilen rastgele değer 0.9'den küçükse 0.9, 4.5'ten büyükse 4.5 yapılır.
  owners = random.randint(1.4)
  accidents = np.random.poisson(0.5)

  brand_factor = {
    "BMW":1.3, "Audi":1.25, "Mercedes":1.4, "Toyota":1.0, "Hyundai":0.8, "RangeRover": 1.6, "Mini":1.4, "Ford":1.2
    #markaların fiyatlara olan etkisini belirleyek katsayı faktörü belirledik
  }
  #Fiyat formülü
  base_price = {
      500_000 #taban fiyat
      - (2024 - model_year) * 1500 # yaşı arttıkça fiyat düşecek
      - (km/1000)*100 # km arttıkça fiyat düşecek
      + brand_factor[brand] * 20_000 # marka kat sayısına göre fiyatı etkilemektedir
      + engine_size * 5000
      - accidents * 1000 
      + random.gauss (0,5000)
  }

  price = int(min(max(base_price, 1_000_000), 6_000_000))

  #Fiyat formülü
  base_price = {
      500_000 #taban fiyat
      - (2024 - model_year) * 1500 # yaşı arttıkça fiyat düşecek
      - (km/1000)*100 # km arttıkça fiyat düşecek
      + brand_factor[brand] * 20_000 # marka kat sayısına göre fiyatı etkilemektedir
      + engine_size * 5000
      - accidents * 1000 
      + random.gauss (0,5000)
  }

  price = int(min(max(base_price, 1_000_000), 6_000_000))


  data.append([brand, model_year, km, fuel, transmissions, colors, region, owners, 
              accidents, price, round(engine_size,1)]) 
  #data listemize random oluşturulan değerleri atıyoruz.
  #round ile engine_size değerimize virgülden sonra 1 basamak gelmesini sağladık

#for döngüsünden çıkıyoruz

sutun_isimleri = ["Brands", "ModelYear", "KM", "Fuel", "Transmission",
                  "Color", "Region", "Owners", "Accidents", "Price", "EngineSize"]

df_cars = pd.DataFrame(data, columns= sutun_isimleri)






