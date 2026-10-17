# Gerekli kütüphaneleri içe aktar
import discord  # Discord API ile çalışmak için kullanılan kütüphane
from discord.ext import commands  # Komut tabanlı bot kontrolü için modül
import requests  # HTTP istekleri göndermek için kullanılan kütüphane
import pyttsx3  # Konuşma sentezi için kullanılan kütüphane

# Konuşma sentezleyiciyi başlat
engine = pyttsx3.init()  # Konuşma sentezi için bir nesne oluştur

# Bot nesnesini başlat
intents = discord.Intents.default()  # Bot için gerekli izinleri yapılandır
intents.message_content = True  # Mesaj içeriklerini okuyabilme iznini etkinleştir
bot = commands.Bot(command_prefix="!", intents=intents)  # Belirtilen komut ön ekiyle botu oluştur

# API üzerinden rastgele bir bilgi alan fonksiyon
def get_fact() -> str:
    """
    API üzerinden rastgele bir bilgi alır.

    Döndürür:
        str: Bilgi metni ya da bir hata mesajı
    """
    base_url = "https://uselessfacts.jsph.pl/random.json?language=en"  # Rastgele bilgi almak için kullanılan URL
    response = requests.get(base_url)  # API'ye GET isteği gönder

    if response.status_code == 200:  # Eğer istek başarılıysa (kod 200)
        data = response.json()  # Yanıtı JSON formatında ayrıştır
        return data.get("text", "Bilgi alınamadı.")  # Bilgi metnini döndür
    else:
        return "Veri alınamadı. Lütfen daha sonra tekrar deneyin."  # Hata mesajı döndür

# Konuşma sentezi yapan fonksiyon
def speak(text: str):
    """
    Verilen metni pyttsx3 kullanarak seslendirir.

    Parametreler:
        text (str): Seslendirilecek metin
    """
    engine.say(text)  # Metni konuşma sentezine gönder
    engine.runAndWait()  # Konuşmayı gerçekleştir ve bitmesini bekle

# İlginç bir bilgi getiren komut
@bot.command()
async def fact(ctx):
    """
    Rastgele bir bilgi alır ve seslendirir.

    Parametreler:
        ctx: Komut bağlamı (komutun çağrıldığı yerle ilgili bilgiler)
    """
    random_fact = get_fact()  # Rastgele bir bilgi al
    await ctx.send(f"İşte ilginç bir bilgi: {random_fact}")  # Bilgiyi Discord kanalına gönder
    speak(random_fact)  # Bilgiyi seslendir

# Botu çalıştır
bot.run("YOUR_BOT_TOKEN")  # Botu belirtilen token ile çalıştır
