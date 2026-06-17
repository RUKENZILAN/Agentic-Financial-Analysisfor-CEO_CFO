** What's New?** 
The major update that transforms our application into a completely standalone, smarter, and dynamic ecosystem is now live! With this release, we have streamlined the architecture and fully automated the data analysis workflows from end to end.

 1. Fully Standalone Single-File Architecture
What Changed?: index.html is now completely self-sufficient.

The Details: External dependencies like dashboard_data.js and app.js have been removed. All scripts and styles are now bundled inside a single HTML file. Simply double-clicking the file to open it in any browser is now enough to run the entire app!

 2. Advanced Dynamic "Upload Zone"
Broad Format Support: You can now drag-and-drop or click to upload .xlsx, .xls, and .csv files directly.

Smart Labeling: Regardless of the original filename, the uploaded file is automatically processed as financial_data.xlsx under the hood and displayed as a visual "pill" badge in the UI.

History Tracking: The last 5 uploads are tracked and displayed at the top as a mini-history timeline.

 3. 4-Step Visual Progress Bar
Data loading and processing steps are now completely transparent. The workflow can be tracked in real-time via a color-coded progress bar across 4 distinct steps:

Reading file 2.  Parsing data 3.  AI generating analysis 4.  Updating dashboard

 4. Embedded "Tabula Rasa" Analysis Engine
To prevent legacy data from polluting new insights, we have integrated an intelligent reset mechanism for every new upload:

The moment a new file is uploaded, dashboardData is wiped clean (null).

Both existing charts are entirely wiped from memory (destroy()).

The upload counter (uploadCount) increments, triggering a prompt to the Claude API: "Upload #N — TABULA RASA: ground zero analysis" to initiate a fresh, clean-slate evaluation.

Offline Resilience: If there is no API connection, an "Offline Fallback" mechanism seamlessly kicks in to ensure uninterrupted operation.

 5. All Core Dashboard Features Preserved!
The new dynamic upload architecture seamlessly feeds into the app's existing robust feature set. The following features now run flawlessly, powered directly by your newly uploaded live data:

Left Panel: AI Analysis, McKinsey 3 Horizons Model, and the Eisenhower Matrix.

Visual Components: KPI rings, Cash Flow charts, and Financial Ratios.

Financial Tools: DuPont Analysis and Historical Comparison tables.

Actionable Insights: Risk, Opportunity, and Action flags.

Utility Features: TR/EN language toggle, Black & White (B&W) theme support, and the PDF export button.


**TR**
**Neler Yeni? (What's New)**
Uygulamamızı tamamen bağımsız, daha akıllı ve dinamik bir yapıya kavuşturan büyük güncelleme yayında! Bu sürümle birlikte hem altyapıyı sadeleştirdik hem de veri analiz süreçlerini baştan sona otomatikleştirdik.

 1. Tam Bağımsız Tek Dosya Mimarisi (Standalone)
Ne Değişti?: index.html artık tamamen kendi kendine yeten bağımsız bir yapıya sahip.

Detay: dashboard_data.js ve app.js gibi dış dosyalar bağımlılık olmaktan çıkarıldı. Tüm scriptler ve stiller tek bir HTML dosyasında birleştirildi. Dosyayı çift tıklayıp tarayıcıda açmanız artık tüm uygulamayı çalıştırmak için yeterli!

 2. Gelişmiş Dinamik "Upload Zone"
Geniş Format Desteği: Sürükle-bırak veya tıklama yöntemiyle .xlsx, .xls ve .csv formatındaki dosyalar doğrudan yüklenebiliyor.

Akıllı Etiketleme: Yüklenen dosyanın adı ne olursa olsun arka planda otomatik olarak financial_data.xlsx etiketiyle işleniyor ve bir görsel "pill" (hap buton) olarak arayüzde gösteriliyor.

Geçmiş Takibi: Son yapılan 5 yükleme, üst panelde mini bir tarih şeridi (timeline) olarak listeleniyor.

 3. 4 Adımlı Görsel İlerleme Süreci (Progress Bar)
Veri yükleme ve işleme adımları artık tamamen şeffaf. Süreç şu 4 adımda, renk kodlu bir ilerleme çubuğuyla canlı olarak takip edilebiliyor:

Dosya okunuyor 2.  Veri ayrıştırılıyor 3.  AI analiz üretiyor 4.  Dashboard güncelleniyor

 4. "Tabula Rasa" Analiz Motoru
Her yeni veri yüklemesinde eski verilerin analizi kirletmesini önleyen akıllı bir sıfırlama mekanizması entegre edildi:

Yeni dosya yüklendiği an dashboardData sıfırlanıyor (null).

Mevcut iki grafik de tamamen bellekten uçuruluyor (destroy()).

Yükleme sayacı (uploadCount) tetikleniyor ve Claude API'ye "Yükleme #N — TABULA RASA: sıfır nokta analizi" prompt'u gönderilerek temiz bir analiz başlatılıyor.

Çevrimdışı Güvence: API bağlantısı olmadığı senaryolarda "Offline Fallback" (çevrimdışı yedek mekanizma) devreye girerek kesintisiz çalışma sağlıyor.

 5. Mevcut Güçlü Altyapı Aynen Korundu!
Yeni dinamik yükleme mimarisi, uygulamanın sevilen hiçbir özelliğine zarar vermedi. Artık yüklediğiniz canlı verilerle şu özelliklerin tamamı kusursuz çalışıyor:

Sol Panel: Yapay Zeka Analizi, McKinsey 3 Horizons Modeli ve Eisenhower Matrisi.

Görsel Bileşenler: KPI halkaları (Ring Charts), Nakit Akışı grafiği ve Rasyolar.

Finansal Araçlar: DuPont Analizi ve Tarihsel Karşılaştırma tabloları.

Yönlendirmeler: Risk, Fırsat ve Aksiyon bayrakları (flags).

Genel Araçlar: TR/EN dil geçişi, Black & White (Siyah/Beyaz) tema desteği ve PDF indirme butonu.
