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
  owners = random.randint(1,4)
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


  #Fiyat formülü
  base_price = (
      500_000 #taban fiyat
      - (2024 - model_year) * 1500 # yaşı arttıkça fiyat düşecek
      - (km/1000)*100 # km arttıkça fiyat düşecek
      + brand_factor[brand] * 20_000 # marka kat sayısına göre fiyatı etkilemektedir
      + engine_size * 5000
      - accidents * 1000 
      + random.gauss (0,5000)
  )

  price = int(min(max(base_price, 1_000_000), 6_000_000))


  data.append([brand, model_year, km, fuel, transmissions, colors, region, owners, 
              accidents, price, round(engine_size,1)]) 
  #data listemize random oluşturulan değerleri atıyoruz.
  #round ile engine_size değerimize virgülden sonra 1 basamak gelmesini sağladık

#for döngüsünden çıkıyoruz

sutun_isimleri = ["Brands", "ModelYear", "KM", "Fuel", "Transmission",
                  "Color", "Region", "Owners", "Accidents", "Price", "EngineSize"]

df_cars = pd.DataFrame(data, columns= sutun_isimleri)


#KORELASYON ANALİZİ

#km nin fiyata olan etkisindeki korelasyon

km_val = df_cars["KM"]
price_val = df_cars["Price"]

#Kütüphanede yazdığımız pearson lineer ilişkiye, spear ise sıralama ilişkisine bakacak. Bu aşamada bunu kullanacağız.

#PEARSON İLİŞKİ = +1 ile -1 aralığında bir değer üretilir. 
#pearson_corr = df_num.corr(method="pearson")       #ekstra örnek 


pearson_corr, p_val_pearson = pearsonr(km_val, price_val)
pearson_matrix = df_cars.select_dtypes(include=[np.number]).corr(method="pearson")#revize edildi 
#İkinci Yöntem
pearson_corr = df_cars["KM"].corr(df_cars["Price"], method="pearson")

#formül yazımı
x = df_cars["KM"]
y = df_cars["Price"]

x_mean = x.mean()
y_mean = y.mean()

cov_xy = ((x-x_mean)*(y-y_mean)).sum() / (len(x) - 1)

std_x = np.sqrt(((x-x_mean) ** 2).sum() / (len(x) - 1))
std_y = np.sqrt(((y-y_mean) ** 2).sum() / (len(x) - 1))

pearson_manuel = cov_xy / (std_x * std_y)

print("Pearson formülü ile : ", pearson_manuel)

#Spearman Korelasyonu (Sıralama İlişkisi) İki değişken arasındaki
#ilişkinin var olup olmadığına bakar. Lineer olup olmamasıyla ilgilenmez.

spearman_corr, p_val_spearman = spearmanr(km_val, price_val)

print("Spearman correlation ile : ", spearman_corr, "p-değeri : ", p_val_spearman)

#Görselleştirme

plt.figure(figsize = (8,5))
plt.scatter(km_val, price_val, alpha = 0.4)
plt.xlabel("KM")
plt.ylabel("Price")
plt.title("Fiyat-KM İlişkisi")
plt.show()

#Z Score ( Outlier Tespiti) 

#z = ((x - X') / s)

z_scores = (df_cars["Price"] - df_cars["Price"].mean()) / df_cars["Price"].std()

outliers = df_cars[np.abs(z_scores) >3]

#Regresyon Çizgisi (Lineer Trend)

import seaborn as sns

sns.regplot(x="KM", y="Price", data=df_cars, line_kws={"color":"red"})

