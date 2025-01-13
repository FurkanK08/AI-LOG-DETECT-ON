![image](https://github.com/user-attachments/assets/91518ada-0ef2-46b9-9738-e132805f8f88)
# Web Log Anomaly Detection with LSTM

Bu proje, web log verileri üzerinden anomali tespiti yapmak için bir **LSTM (Long Short-Term Memory)** modelini kullanır. Model, log dosyasındaki verileri işleyerek, anormal kullanıcı davranışlarını ve potansiyel siber saldırıları (örneğin, brute force saldırıları) tespit etmeyi amaçlar.

## Proje Açıklaması

Bu proje, web sunucusundan alınan log verilerini analiz etmek için bir derin öğrenme modelini kullanır. Model, IP adresleri ve diğer web istekleri üzerinden anomali tespiti yapar. Kullanıcı davranışları izlenir ve bu verilerden normal ve anormal aktiviteler ayrılır.

### Kullanılan Teknolojiler
- Python
- Keras (TensorFlow Backend)
- Pandas
- NumPy
- Scikit-learn
- Matplotlib (İsteğe bağlı olarak görselleştirme için)
- TensorFlow LSTM modeli

## Özellikler
- **Log Dosyası İşleme**: Apache veya Nginx gibi web sunucularının log dosyalarını okur, her bir istek için belirli özellikleri çıkarır.
- **Zaman Serisi Veri İşleme**: LSTM modeline uygun şekilde veriler zaman serisi formatında işlenir.
- **Etiketleme ve Dönüşüm**: Kategorik veriler (`client`, `request`) etiketlenir ve modelin tahminlerinde bu etiketler geri dönüştürülür.
- **Anomali Tespiti**: Eğitilen LSTM modeline dayanarak, log verilerinde anomali tespiti yapılır.
- **Veri Ölçeklendirme**: Modelin eğitiminde daha iyi performans elde etmek için veriler ölçeklendirilir.
- **Modelin Yüklenmesi ve Tahmin**: Önceden eğitilmiş bir model kullanılarak log verileri üzerinde tahmin yapılır.

## Kurulum

### Gereksinimler

- Python 3.x
- Keras
- TensorFlow
- Pandas
- NumPy
- Scikit-learn
- Matplotlib (opsiyonel, görselleştirme için)

### Gerekli Paketlerin Kurulumu

Projeyi çalıştırmadan önce, aşağıdaki bağımlılıkları yüklemeniz gerekebilir:
pip install -r requirements.txt

