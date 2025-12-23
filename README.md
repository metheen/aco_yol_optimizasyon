# 🗺️ Üniversite Kampüsü Ring Otobüsü Rota Optimizasyonu

Bu proje, bir üniversitenin kampüsü içinde ring seferi yapan otobüsün **Karınca Kolonisi Algoritması (ACO)** kullanarak en kısa ve verimli tur rotasını bulmayı hedefler. Proje, kampüs içindeki fakülteler, yurtlar ve spor kompleksi gibi 10 farklı durak arasındaki **gerçek sürüş mesafelerini** Google Maps API ile çekerek optimizasyon yapar.

## 📋 Proje Senaryosu

Bir üniversitenin kampüsü içinde ring seferi yapan otobüs, aşağıdaki 10 duraktan geçerek başlangıç noktasına geri dönmektedir:

1. Mühendislik Fakültesi
2. İktisadi ve İdari Bilimler Fakültesi
3. Fen-Edebiyat Fakültesi
4. Tıp Fakültesi
5. Merkezi Kütüphane
6. Öğrenci Yurdu A
7. Öğrenci Yurdu B
8. Spor Kompleksi
9. Teknokent
10. Rektörlük Binası

## 🏗️ Proje Yapısı

```
bursa_aco_projesi/
├── .env                      # API anahtarları (Google Maps ve/veya OpenRouteService)
├── .gitignore               # Git ignore dosyası
├── requirements.txt          # Python bağımlılıkları
├── README.md                # Bu dosya
├── main.py                  # Streamlit ana uygulama dosyası
├── data/
│   └── coordinates.py       # Okul koordinatları ve isimleri
└── core/
    ├── distance_manager.py  # Google Maps Distance Matrix API entegrasyonu
    └── ant_algorithm.py     # Karınca Kolonisi Optimizasyon algoritması
```

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.8 veya üzeri
- **Gerçek sürüş mesafeleri için:** Google Maps API anahtarı VEYA OpenRouteService API anahtarı (ücretsiz)

### 2. Projeyi İndirin ve Bağımlılıkları Yükleyin

```bash
# Proje dizinine gidin
cd bursa_aco_projesi

# Sanal ortam oluşturun (önerilir)
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. API Anahtarını Ayarlayın

#### Seçenek 1: OpenRouteService (Önerilen - Ücretsiz)

1. [OpenRouteService](https://openrouteservice.org/dev/#/signup) üzerinden ücretsiz hesap oluşturun
2. API anahtarınızı alın
3. `.env` dosyasına ekleyin:

```env
ORS_API_KEY=YOUR_ORS_API_KEY_HERE
```

**Avantajlar:**
- ✅ Tamamen ücretsiz (günde 2000 istek)
- ✅ Gerçek sürüş mesafeleri
- ✅ Billing gerektirmez

#### Seçenek 2: Google Maps API

1. `.env` dosyasını açın
2. `Maps_API_KEY=` satırına Google Maps API anahtarınızı ekleyin:

```env
Maps_API_KEY=YOUR_API_KEY_HERE
```

**Not:** Google Maps API anahtarı almak için:
- [Google Cloud Console](https://console.cloud.google.com/) üzerinden bir proje oluşturun
- "APIs & Services" > "Library" bölümünden "Distance Matrix API"yi etkinleştirin
- **ÖNEMLİ:** Billing hesabınızı aktifleştirmeniz gerekir (ücretsiz kredi ile başlayabilirsiniz)
- "Credentials" bölümünden bir API anahtarı oluşturun

#### API Öncelik Sırası

Uygulama şu sırayla API'leri dener:
1. Google Maps API (varsa)
2. OpenRouteService API (varsa)
3. Haversine formülü (yaklaşık mesafe - gerçek sürüş mesafesi değil)

## 🎯 Kullanım

### Uygulamayı Başlatın

```bash
streamlit run main.py
```

Tarayıcınızda otomatik olarak açılacak veya `http://localhost:8501` adresine gidin.

### Parametreleri Ayarlayın

Sol sidebar'dan algoritma parametrelerini ayarlayabilirsiniz:

- **Karınca Sayısı**: Her iterasyonda kaç karınca rota oluşturacak (5-50)
- **İterasyon Sayısı**: Algoritmanın kaç kez çalışacağı (10-200)
- **Alpha**: Feromon izlerinin seçim üzerindeki etkisi (0.1-3.0)
- **Beta**: Mesafenin seçim üzerindeki etkisi (1.0-10.0)
- **Buharlaşma Oranı**: Her iterasyonda feromonların ne kadarının buharlaşacağı (0.1-0.9)

### Optimizasyonu Çalıştırın

"🚀 Optimize Et" butonuna tıklayın. Uygulama:

1. Google Maps API'den gerçek sürüş mesafelerini çeker
2. ACO algoritmasını çalıştırarak en iyi rotayı bulur
3. Sonuçları harita üzerinde görselleştirir
4. İterasyon bazlı mesafe değişimini grafik olarak gösterir

## 📊 Özellikler

- ✅ **Gerçek Mesafe Hesaplama**: Google Maps Distance Matrix API ile gerçek sürüş mesafeleri
- ✅ **İnteraktif Harita**: PyDeck ile optimize edilmiş rotanın görselleştirilmesi
- ✅ **İterasyon Grafiği**: Algoritmanın her iterasyondaki performansını gösteren grafik
- ✅ **Parametre Kontrolü**: Kullanıcı dostu sidebar ile algoritma parametrelerini ayarlama
- ✅ **Detaylı Rota Bilgisi**: Her okulun sırası ve toplam mesafe bilgisi

## 🔧 Teknik Detaylar

### Karınca Kolonisi Algoritması (ACO)

ACO, doğadaki karıncaların yiyecek kaynağına en kısa yolu bulma davranışından esinlenen bir meta-sezgisel optimizasyon algoritmasıdır. Bu projede:

- **Feromon İzleri**: Karıncalar geçtikleri yollara feromon bırakır
- **Sezgisel Bilgi**: Kısa mesafeler daha cazip görünür
- **Buharlaşma**: Zamanla feromonlar buharlaşır, kötü yollar unutulur
- **Takviye**: İyi yollar daha fazla feromon alır

### Modüller

- **`data/coordinates.py`**: Okul isimleri ve koordinatlarını içeren sözlük
- **`core/distance_manager.py`**: Google Maps API entegrasyonu ve mesafe matrisi oluşturma
- **`core/ant_algorithm.py`**: ACO algoritmasının çekirdek implementasyonu
- **`main.py`**: Streamlit web arayüzü ve görselleştirme

## 📝 Lisans

Bu proje eğitim ve araştırma amaçlı geliştirilmiştir.

## 🤝 Katkıda Bulunma

Proje hakkında önerileriniz veya sorularınız için issue açabilirsiniz.

## 📧 İletişim

Bursa Belediyesi Geri Dönüşüm Rota Optimizasyonu Projesi

---

**Not**: Bu proje, Google Maps API kullanımı için ücretli bir API anahtarı gerektirir. API kullanım limitlerini kontrol etmeyi unutmayın.

