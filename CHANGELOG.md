# CHANGELOG

## 2026-01-17 - Alert kalıcılığı
### Added
- Uygulama açılışında `logs/alerts.jsonl` yükleniyor (neden: restart sonrası /alerts boş görünmesin).

### How to test
- 5 kez başarısız `login_attempt` gönder, `alerts.jsonl` oluşsun.
- Sunucuyu kapat/aç, `/alerts` çağır; önceki alert listede görünmeli yani 5 adet hatalı denemeden sonra sunucu kapatılım açılsa bile kapatılmadan önceki alert listede görünmeli, bu şöyle bi sıkıntı oluşturabilir uygulamayı tekrar açınca, ram tekrar doldurulur alerts.jsonl dosyası okunarak bu küçük ve kontrollü olduğu için sıkıntı çıkarmaz ama sonuç olarak yükü arttırıyor bu yüzden ilerde limit koymayı düşünüyorum son 1k alert gibi.

## 2026-01-17 - .env güvenliği
### Added
- `.env` ve `.env.*` .gitignore'a eklendi (neden: anahtarlar yanlışlıkla git'e girmesin).

### How to test
- `git ls-files | rg '\.env'`

## 2026-01-17 - Alerts filtresi ve kural netliği
### Added
- `.gitignore` eklendi (neden: log ve cache dosyaları Git'e girmesin).
- GET `/alerts` filtreleri eklendi: user, ip, alert_type, severity (neden: alert listesinde daraltma için).

### Changed
- Brute force kuralı sabitleri netleştirildi (neden: kural değerleri tek yerde olsun).

### How to test
- Server: `py -m uvicorn app.main:app --reload`
- Docs: `http://127.0.0.1:8000/docs`
- 5 kez başarısız `login_attempt` gönder.
- `/alerts?user=alice&ip=1.2.3.4` çağır.

## 2026-01-17 - Brute force tespiti, alert logu ve /alerts
### Added
- Brute force kuralı eklendi (neden: kısa sürede çoklu başarısız denemeyi yakalamak için).
- Alert log dosyası eklendi: `logs/alerts.jsonl` (neden: şüpheli kayıtları ayrı tutmak için).
- GET `/alerts` endpoint’i eklendi (neden: RAM'deki alert listesini görmek için).

### Changed
- POST `/event` response'una `alert_created` alanı eklendi (neden: alert üretildi mi görmek için).

### How to test
- Server: `py -m uvicorn app.main:app --reload`
- Docs: `http://127.0.0.1:8000/docs`
- 5 kez başarısız `login_attempt` gönder.
- `type logs\events.jsonl`
- `type logs\alerts.jsonl`

## 2026-01-17 - Phase-1 başlangıç: API ayağa kalktı, event alıyor, JSONL log var
### Added
- FastAPI servis kuruldu ve çalıştırıldı (Uvicorn ile).
- GET `/health` endpoint’i eklendi (servis ayakta mı kontrolü).
- POST `/event` endpoint’i eklendi (JSON event alıp response dönüyor).
- `/docs` (Swagger UI) üzerinden test akışı kullanıldı.
- JSONL event logging eklendi: `logs/events.jsonl`
  - Her satır 1 JSON kayıt
  - `ts` (UTC ISO timestamp) alanı var.

### Changed
- Windows ortamında pip yerine `py -m pip ...` standardına geçildi (pip PATH problemi yüzünden).

### Fixed
- `uvicorn app.main:app` hatası (FastAPI app değişken adı) düzeltildi: `app = FastAPI(...)` olacak.

### How to test
- Server: `py -m uvicorn app.main:app --reload`
- Test health: `http://127.0.0.1:8000/health`
- Docs: `http://127.0.0.1:8000/docs`
- Event gönder (docs üzerinden) ve log kontrol et:
  - `type logs\events.jsonl`
