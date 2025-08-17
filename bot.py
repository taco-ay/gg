from discord.ext import commands
import discord
from logic import DB_Manager
from config import TOKEN
db = DB_Manager("idk.db")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} olarak giriş yapıldı ve hazır!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def books(ctx):
    rows = db.get_books()
    msg = "\n".join([f"{r[1]} - {r[2]} (ISBN: {r[0]})" for r in rows])
    await ctx.send(f"**Kitaplar:**\n{msg}")

@bot.command()
async def users(ctx):
    rows = db.get_users()
    msg = "\n".join([f"ID: {r[0]} | {r[1]} | Age: {r[2]}" for r in rows])
    await ctx.send(f"**Kullanıcılar:**\n{msg}")

@bot.command()
async def ratings(ctx):
    rows = db.get_ratings()
    msg = "\n".join([f"User {r[0]} -> {r[1]} : {r[2]}" for r in rows])
    await ctx.send(f"**Puanlamalar:**\n{msg}")

# 🔍 SQL sorgusu çalıştır
@bot.command()
async def sql(ctx, *, query):
    try:
        if not query.strip().lower().startswith("select"):
            await ctx.send("⚠️ Sadece SELECT sorgularına izin var.")
            return
        rows = db.run_sql(query)
        if not rows:
            await ctx.send("Sonuç bulunamadı.")
            return
        msg = "\n".join([str(r) for r in rows[:10]])  # ilk 10 sonucu göster
        await ctx.send(f"**Sonuçlar:**\n{msg}")
    except Exception as e:
        await ctx.send(f"⚠️ Hata: {e}")

@bot.command()
async def ara(ctx, *, kitap_adi):
    try:
        sql = """
        SELECT ISBN, `Book-Title`, `Book-Author`, `Year-Of-Publication`, Publisher, `Image-URL-M`
        FROM books
        WHERE `Book-Title` LIKE ?
        LIMIT 5
        """
        rows = db._DB_Manager__execute(sql, (f"%{kitap_adi}%",))  # güvenli parametre kullanımı
        if not rows:
            await ctx.send("📕 Kitap bulunamadı.")
            return
        msg = "\n\n".join([
            f"**{r[1]}**\n✍️ {r[2]}\n📅 {r[3]}\n🏢 {r[4]}\nISBN: {r[0]}\n{r[5]}"
            for r in rows
        ])
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"⚠️ Hata: {e}")


bot.run(TOKEN)
