import os
import discord
from discord.ext import commands
import requests

TOKEN = os.environ.get("TOKEN")
FASTAPI_URL = "http://85.203.4.103:6262/api/lookup"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name="true")
async def true_lookup(ctx, phone: str):
    msg = await ctx.reply(f"🔎 กำลังดึงข้อมูลเบอร์ `{phone}`")

    try:
        # เรียกไปยัง Backend FastAPI
        response = requests.get(f"{FASTAPI_URL}?phone={phone}", timeout=15).json()

        if response.get("status") == "error":
            return await msg.edit(content=f"❌ {response.get('message')}")

        # สร้าง Embed แสดงผล
        embed = discord.Embed(title="🔍 ผลการตรวจสอบข้อมูลลูกค้า", color=0xed1c24)
        embed.add_field(name="👤 ชื่อ-นามสกุล", value=response.get("name"), inline=True)
        embed.add_field(name="🆔 เลขบัตรประชาชน", value=f"||{response.get('id_card')}||", inline=True)
        
        # แสดงรายการเบอร์โทร
        phones = "\n".join([f"• {n}" for n in response.get("all_phones", [])])
        embed.add_field(name="📞 เบอร์ทั้งหมดที่จดทะเบียน", value=f"```\n{phones}\n```", inline=False)
        
        # แสดงที่อยู่
        embed.add_field(name="🏠 ที่อยู่ลงทะเบียน", value=response.get("address"), inline=False)
        
        embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await msg.edit(content=None, embed=embed)

    except Exception as e:
        await msg.edit(content=f"⚠️ ไม่สามารถเชื่อมต่อกับ Backend Server ได้: `{e}`")

bot.run(TOKEN)