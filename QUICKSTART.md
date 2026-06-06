# QUICK START GUIDE / HIZLI BAŞLANGIÇ KILAVUZU

## English

### Prerequisites
- Python 3.9+
- Binance account with API keys
- 2FA enabled on Binance account

### Step 1: Install
```bash
# Clone repository
git clone https://github.com/baruthane/yapay-zeka-botum.git
cd yapay-zeka-botum

# Run setup script
chmod +x setup.sh
./setup.sh

# On Windows:
# setup.bat
```

### Step 2: Configure
Edit `.env` file with your Binance API credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=True  # Start with testnet!
```

### Step 3: Run
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run bot once (analysis)
python main.py --mode once

# Run bot in continuous loop (300s intervals)
python main.py --mode loop --interval 300

# Run webhook server (optional)
python webhook_server.py
```

### Step 4: Monitor
- Check `logs/bot.log` for detailed information
- Monitor positions on Binance
- Review risk reports in console output

---

## Türkçe

### Gereksinimler
- Python 3.9+
- Binance hesabı ve API anahtarları
- Binance hesabında 2FA aktif

### Adım 1: Kurulum
```bash
# Repository'yi klonlayın
git clone https://github.com/baruthane/yapay-zeka-botum.git
cd yapay-zeka-botum

# Setup script'ini çalıştırın
chmod +x setup.sh
./setup.sh

# Windows'ta:
# setup.bat
```

### Adım 2: Yapılandırma
`.env` dosyasını Binance API bilgileriniz ile düzenleyin:
```env
BINANCE_API_KEY=api_anahtarınız
BINANCE_API_SECRET=api_sırrınız
BINANCE_TESTNET=True  # Başlangıçta testnet'te çalıştırın!
```

### Adım 3: Çalıştırma
```bash
# Virtual environment'i aktif et
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bot'u bir kez çalıştır (analiz)
python main.py --mode once

# Bot'u sürekli loop'ta çalıştır (300s aralık)
python main.py --mode loop --interval 300

# Webhook server başlat (opsiyonel)
python webhook_server.py
```

### Adım 4: Izleme
- `logs/bot.log` dosyasını detaylı bilgi için kontrol edin
- Binance'de pozisyonları izleyin
- Konsol çıktısında risk raporlarını gözden geçirin

---

## Önemli Uyarılar / Important Warnings

⚠️ **DİKKAT - ATTENTION:**

1. **Testnet'te başlayın** - Start with testnet
2. **Küçük pozisyon boyutlarıyla test edin** - Test with small positions
3. **Kod değişiklikleri yaparsanız, kapsamlı backtest edin** - Backtest thoroughly if you modify code
4. **Maddi kayıp riski vardır** - There is a risk of financial loss
5. **Otomatik trading saatinde bota göz kulak olun** - Monitor the bot while it's trading
6. **Risk yönetimi kurallarını asla görmezden gelmeyin** - Never ignore risk management rules

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### "BinanceAPIException"
- Check API keys in `.env`
- Verify 2FA is enabled
- Check IP whitelist in Binance account
- Ensure testnet is set to `True`

### "No data fetched"
- Check internet connection
- Verify Binance API status
- Check trading pair symbols (should be uppercase, e.g., BTCUSDT)

### Bot not executing trades
- Check risk limits in `config.py`
- Verify account has sufficient balance
- Check position limits
- Review `logs/bot.log` for errors

---

## Common Commands

```bash
# View help
python main.py --help

# Run with custom interval (500 seconds)
python main.py --mode loop --interval 500

# View logs in real-time
tail -f logs/bot.log  # Linux/Mac
type logs/bot.log  # Windows

# Kill the bot
Ctrl+C

# Deactivate virtual environment
deactivate
```

---

## Next Steps

1. ✅ Complete setup and test on testnet
2. 📊 Analyze multiple trading pairs
3. 📈 Review performance metrics
4. 💾 Enable database logging (advanced)
5. 🔔 Setup Telegram notifications (advanced)
6. 🤖 Train ML models with your data (advanced)

---

## Support

- Documentation: See README.md
- Roadmap: See ROADMAP.md
- Issues: GitHub Issues
- Examples: See examples.py

Happy trading! 🚀

---

**Disclaimer:** This bot is provided as-is for educational purposes. Use at your own risk. The author is not responsible for any financial losses.
