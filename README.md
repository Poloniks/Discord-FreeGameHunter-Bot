# 🎮 FreeGame Hunter

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-Bot-red.svg)
![License](https://img.shields.io/badge/License-Open%20Source-green.svg)

This project is an advanced, plug-and-play Discord bot that automatically hunts for free games on Steam, Epic Games, GOG, and other platforms.

[🇹🇷 Türkçe açıklamalar için aşağıya kaydırın / Scroll down for Turkish]

### 🇬🇧 Features

* **Smart Web Scraper:** Automatically fetches high-quality cover images directly from store pages (Open Graph data).
* **Reliability (Fallback System):** If a store page is down or missing image metadata, the bot switches to a fallback mode to ensure you never miss a deal.
* **Dynamic Channel Routing:** Configure different channels for different platforms easily using slash commands.
* **Smart Memory:** Keeps track of posted deals locally. Safe to restart; it will never post the same game twice.
* **Zero Hardcoding:** No need to paste Channel IDs into code. Everything is managed via Discord UI.

### 🇬🇧 Usage

Once the bot is invited to your server, you don't need to edit any code. Simply go to the text channel where you want the games to be announced and type the corresponding slash command:
* `/set_steam` : Sets the current channel for free Steam games.
* `/set_epic` : Sets the current channel for free Epic Games.
* `/set_gog` : Sets the current channel for free GOG games.
* `/set_other` : Sets the current channel for other platforms (Itch.io, Ubisoft, IndieGala, etc.).
* `/status` : Forces the bot to immediately scan for new games without waiting for the 15-minute timer.

### 🇬🇧 Installation

* Clone the repository with the command: `git clone https://github.com/poloniks/FreeGameHunter.git`
* Install the required libraries with the command: `pip install -r requirements.txt`
* Create a `.env` file in the main folder and add your token: `DISCORD_TOKEN=your_token_here`
* Run the bot using the command: `python main.py`

---

### 🇹🇷 Özellikler

* **Akıllı Web Kazıyıcı:** Mağaza sayfalarından orijinal ve yüksek çözünürlüklü kapak fotoğraflarını (Open Graph) otomatik çeker.
* **Güvenilirlik (B Planı Sistemi):** Eğer mağaza sitesi çökerse veya görsel bulunamazsa bot hata verip kapanmaz; fırsatı kaçırmamanız için standart metin formatında gönderimi tamamlar.
* **Dinamik Kanal Yönlendirme:** Steam, Epic Games gibi farklı platformları kolayca farklı kanallara yönlendirin.
* **Akıllı Hafıza:** Gönderilen oyunları yerel hafızasına kaydeder. Bilgisayarı kapatsanız bile aynı oyunu asla ikinci kez atmaz.
* **Kodsuz Yönetim:** Kanal ID'lerini koda yapıştırmakla uğraşmayın. Her şey Discord komutlarıyla yönetilir.

### 🇹🇷 Nasıl Kullanılır?

Bot sunucunuza eklendikten sonra kodla uğraşmanıza gerek yoktur. Oyunların düşmesini istediğiniz metin kanalına gidin ve şu komutları kullanın:
* `/set_steam` : Bulunduğunuz kanalı bedava Steam oyunları için ayarlar.
* `/set_epic` : Bulunduğunuz kanalı bedava Epic Games oyunları için ayarlar.
* `/set_gog` : Bulunduğunuz kanalı bedava GOG oyunları için ayarlar.
* `/set_other` : Bulunduğunuz kanalı diğer platformlar (Itch.io, Ubisoft vb.) için ayarlar.
* `/status` : 15 dakikalık süreyi beklemeden, anında yeni bedava oyun taraması başlatır.

### 🇹🇷 Kurulum

* Projeyi bilgisayarınıza klonlayın: `git clone https://github.com/poloniks/FreeGameHunter.git`
* Gerekli kütüphaneleri şu komutla kurun: `pip install -r requirements.txt`
* Ana klasörde `.env` adında bir dosya oluşturun ve token'ınızı ekleyin: `DISCORD_TOKEN=sizin_tokeniniz_buraya`
* Botu şu komutla çalıştırın: `python main.py`

---
> Developed by **poloniks**