import discord
import asyncio
import random
import os
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
PRICE_CHANNEL_ID = int(os.environ["PRICE_CHANNEL_ID"])  # channel for price updates
SHILL_CHANNEL_ID = int(os.environ["SHILL_CHANNEL_ID"])  # channel for "you won" pings
WEBSITE = "https://coin.jkcoxson.com"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

price = 0.000042  # starting price

MOON_MESSAGES = [
    (
        "🚀 iDVC IS PUMPING!",
        "Up {pct}% in the last 15 minutes!\nGet in NOW before you get left behind. This is your last chance. I'm not kidding.",
    ),
    (
        "📈 TO THE MOON",
        "iDVC just went up {pct}%! The founder has NOT boarded a flight yet. There is still time.",
    ),
    ("🌕 MOONING", "iDVC up {pct}%! Do NOT tell your financial advisor about this."),
    ("⬆️ iDVC PUMPING 🔥", "Up {pct}%! The liquidity pool is still intact. For now."),
    (
        "🎯 Price Update",
        "iDVC up {pct}%. The founder's bags are NOT yet packed. This is still a legitimate investment opportunity.",
    ),
    (
        "💹 GET IN NOW",
        "iDVC mooning!! +{pct}%\nIf you don't buy you will regret it forever probably.",
    ),
    (
        "🚀 BREAKING: iDVC PUMPING",
        "Up {pct}%! Our quant team ran the numbers and the numbers said 'yes'. That's all we have.",
    ),
    (
        "📊 Price Alert",
        "iDVC +{pct}%. The founder is still in his chair. He has not stood up. Very bullish.",
    ),
    (
        "🔥 IT'S HAPPENING",
        "iDVC up {pct}%! A financial advisor somewhere just got a very concerning text from their client.",
    ),
    (
        "🌙 LUNAR TRAJECTORY CONFIRMED",
        "Up {pct}%! NASA has not responded to our partnership proposal but we remain optimistic.",
    ),
    (
        "💎 Diamond Hands Printing",
        "iDVC +{pct}%. The people who didn't buy last week are now staring at their screen in silence.",
    ),
    (
        "⚡ SURGE DETECTED",
        "iDVC up {pct}%! We have no explanation. The chart just decided. Respect the chart.",
    ),
]

DIP_MESSAGES = [
    (
        "📉 BUY THE DIP",
        "iDVC dipped {pct}%. THIS IS THE DIP. BUY IT.\nThe founder is definitely not using this opportunity to exit.",
    ),
    (
        "🩸 Weak Hands Selling",
        "iDVC down {pct}%. STRONG hands are buying. Which one are you??",
    ),
    (
        "💀 Healthy Correction",
        "iDVC -{pct}%. All coins do this. The smart money is accumulating rn.",
    ),
    (
        "😤 Small L, Big Future",
        "iDVC down {pct}%. The fundamentals have NOT changed. The founder is still here. Probably.",
    ),
    (
        "🔻 Price Update",
        "iDVC -{pct}%. Buy the dip or stay poor. Those are literally your only two options.",
    ),
    (
        "😭 Don't Panic Sell",
        "iDVC down {pct}%. The founder is NOT currently at an airport.",
    ),
    (
        "📉 Temporary Setback",
        "iDVC -{pct}%. The founder has issued a statement: 'lol'. Full statement to follow.",
    ),
    (
        "🩸 Liquidity Event",
        "iDVC down {pct}%. We are calling this a 'planned volatility window.' It was not planned.",
    ),
    (
        "😬 Minor Correction",
        "iDVC -{pct}%. This is fine. The founder is fine. Everything is fine. Please do not check his location.",
    ),
    (
        "🔻 Shakeout Complete",
        "Down {pct}%. The weak hands have been eliminated. Welcome to the strong hand zone. Stay strong.",
    ),
    (
        "💀 Healthy Accumulation Phase",
        "iDVC -{pct}%. Price going down means more coins per dollar. This is called 'math.' Buy more.",
    ),
    (
        "🧘 Zen Mode",
        "iDVC down {pct}%. Breathe. The founder is breathing. Probably. His read receipts are off.",
    ),
]

WIN_MESSAGES = [
    (
        "🎉 You've Been Selected!",
        "Congratulations {mention}!! You have been **randomly selected** to receive FREE iDevice Coin!\nClaim your tokens before they expire.",
    ),
    (
        "🏆 YOU WON",
        "{mention} our algorithm has selected you to receive complimentary iDVC tokens!\nOffer expires soon (we will not say when).",
    ),
    (
        "💰 FREE iDVC Airdrop",
        "ATTENTION {mention}: You are eligible for a **FREE iDVC airdrop**!\nThis is not a scam. Bring friends.",
    ),
    (
        "🎁 Unclaimed Tokens",
        "{mention} — Our records show you have **unclaimed iDVC tokens** waiting!\nLog in to see your balance. Act fast.",
    ),
    (
        "🚨 THIS IS NOT SPAM",
        "{mention} you have genuinely won free crypto.\nGo right now. Tell no one. Come alone.",
    ),
    (
        "⚡ URGENT: Act Now",
        "{mention} your iDVC airdrop allocation is about to be forfeited!\nThe founder is waiting for you personally.",
    ),
    (
        "🌟 Special Bonus",
        "Big news {mention}!! You're our **1,337th community member** (we say this to everyone).\nVery real. Very free.",
    ),
    (
        "📬 You Have Mail",
        "{mention} our lawyers have informed us we are required to notify you of your free iDVC allocation.\nThis is legally binding in no jurisdiction. Claim at the link.",
    ),
    (
        "🔔 Reminder",
        "Hey {mention}, just a friendly reminder that you have free crypto waiting.\nThe founder has not left the country yet. Time is running out though.",
    ),
    (
        "🤑 Life-Changing Opportunity",
        "{mention} a small investment of $0 could change your life forever.\nFree iDVC tokens available now. Results not typical. Or real.",
    ),
    (
        "🧠 Smart People Only",
        "{mention} only the most financially sophisticated investors are receiving this message.\nFree iDVC. Claim it. Tell your accountant not to worry about it.",
    ),
    (
        "😤 Last Warning",
        "{mention} this is our FINAL notice regarding your unclaimed iDVC tokens.\n(We will send this again in 1 minute.)",
    ),
    (
        "🎰 You're A Winner!",
        "{mention} out of everyone in this server, our proprietary algorithm chose YOU.\nThe algorithm is just random.choice(). Claim your free iDVC anyway.",
    ),
    (
        "📈 Get Rich Quick",
        "{mention} the founder personally wants you to have free iDVC tokens.\nThis is not suspicious. The founder just likes you specifically.",
    ),
    (
        "🛸 The Future Is Here",
        "{mention} iDVC is the currency of tomorrow. Today. Right now.\nFree tokens available. The future is free. Mostly.",
    ),
    (
        "🏝️ Financial Freedom",
        "{mention} imagine retiring at 30. Now imagine retiring at 30 with iDVC.\nSame outcome, but you'd have gone through an additional emotional journey first.",
    ),
    (
        "👀 We've Been Watching",
        "{mention} our analytics show you have NOT yet claimed your free iDVC.\nWe find this deeply concerning. Please fix this immediately.",
    ),
    (
        "🐋 Whale Alert",
        "{mention} our systems have flagged you as a potential iDVC whale.\nThis is based on nothing. But free tokens await. Don't let the whales win.",
    ),
    (
        "💎 Diamond Hands Needed",
        "{mention} iDVC needs believers. Holders. Heroes.\nAlso your attention for 10 seconds. Free tokens at the link.",
    ),
    (
        "🤝 Partnership Opportunity",
        "{mention} the iDVC Foundation would like to offer you a strategic partnership.\nThe partnership involves you claiming free tokens and telling your friends.",
    ),
    (
        "🚀 Early Adopter Bonus",
        "{mention} as an early community member you qualify for bonus iDVC.\nNote: we define 'early' loosely. You still qualify. Go claim.",
    ),
    (
        "🎓 Financial Education",
        "{mention} did you know that not claiming free crypto is leaving money on the table?\nWe don't know whose table. Claim your iDVC and find out.",
    ),
    (
        "🌍 Global Opportunity",
        "{mention} people in 0 countries are already holding iDVC.\nBe the first. Free tokens. Internationally worthless.",
    ),
    (
        "⏰ Time-Sensitive",
        "{mention} this offer expires in [REDACTED] days.\nOur legal team said we can't specify. Just claim it now to be safe.",
    ),
    (
        "🔐 Exclusive Access",
        "{mention} you have been granted exclusive early access to the iDVC ecosystem.\nThe ecosystem is a website. It is free to visit.",
    ),
    (
        "🧾 Tax Season Reminder",
        "{mention} friendly reminder that free iDVC tokens are technically taxable income.\nSo you should probably claim some so you have something to report. Trust.",
    ),
    (
        "📊 Portfolio Diversification",
        "{mention} financial advisors recommend a diversified portfolio.\nAdding iDVC costs $0 and diversifies you into the 'joke crypto' asset class.",
    ),
    (
        "🏆 VIP Status Unlocked",
        "{mention} congratulations! You have been upgraded to iDVC VIP status.\nVIP benefits include: this message, free tokens, and nothing else.",
    ),
    (
        "💌 Personal Message",
        "{mention} the founder wrote this message personally just for you.\n(The founder did not write this message. It was written in advance and sent by a bot.)",
    ),
    (
        "🌱 Ground Floor Opportunity",
        "{mention} get in on the ground floor of iDVC before it moons.\nThe ground floor is very close to the basement. Free tokens available.",
    ),
    (
        "🎤 Community Spotlight",
        "{mention} you have been selected as this minute's iDVC Community Member of the Minute!\nPrize: free tokens. Runner up prize: also free tokens.",
    ),
    (
        "🎪 Congratulations, Probably",
        "{mention} our system flagged your wallet as 'extremely promising.' Your wallet does not exist yet. Still promising.",
    ),
    (
        "📡 Signal Detected",
        "{mention} our proprietary AI detected that you are destined for iDVC greatness. The AI is a coin flip. Tails = you. You got tails.",
    ),
    (
        "🏦 Wealth Transfer Incoming",
        "{mention} a significant wealth transfer is about to occur in the iDVC ecosystem. Mostly toward the founder. You get free tokens.",
    ),
    (
        "🎲 You Have Been Chosen",
        "{mention} out of all possible random outcomes, you were selected. This means nothing statistically. Claim your tokens.",
    ),
    (
        "🦅 Freedom Awaits",
        "{mention} iDVC is the path to financial freedom. The path is unpaved, unlit, and may end in a ditch. Free tokens at the link.",
    ),
    (
        "🕐 Act Within The Next 0 Seconds",
        "{mention} this offer expires IMMEDIATELY. It has already expired. Claim it anyway. Time is fake.",
    ),
    (
        "🔮 The Algorithm Has Spoken",
        "{mention} our advanced selection algorithm chose you. The algorithm is `random.choice()` with your name in a list of everyone. Very advanced.",
    ),
    (
        "💼 Due Diligence Complete",
        "{mention} our team has completed a thorough review of your qualifications. We checked if you were online. You were. Tokens await.",
    ),
    (
        "🌊 Ride The Wave",
        "{mention} a massive iDVC wave is coming. Surfers say 'catch it or get crashed by it.' We are not surfers. Claim your free tokens.",
    ),
    (
        "🤖 Bot-Verified Human",
        "{mention} our systems have confirmed you are probably a human. Humans get free iDVC. Claim before we reconsider.",
    ),
]


@tasks.loop(minutes=10)
async def price_update():
    global price
    channel = client.get_channel(PRICE_CHANNEL_ID)
    if channel is None:
        return

    change = random.uniform(-0.12, 0.18)  # slightly biased up (for now)
    price = max(0.000001, price * (1 + change))
    pct = abs(round(change * 100, 2))
    price_str = f"{price:.6f}"

    if change >= 0:
        title, body = random.choice(MOON_MESSAGES)
        color = discord.Color.green()
        arrow = "▲"
    else:
        title, body = random.choice(DIP_MESSAGES)
        color = discord.Color.red()
        arrow = "▼"

    embed = discord.Embed(title=title, description=body.format(pct=pct), color=color)
    embed.add_field(name="Price", value=f"**${price_str}**", inline=True)
    embed.add_field(name="Change", value=f"{arrow} {pct}%", inline=True)
    embed.add_field(name="Buy Now", value=WEBSITE, inline=False)
    embed.set_footer(text="This is a rugpull.")

    role_names = {"clown", "ping pong"}
    mentions = " ".join(
        role.mention
        for guild in client.guilds
        for role in guild.roles
        if role.name.lower() in role_names
    )

    await channel.send(content=mentions or None, embed=embed)


@tasks.loop(seconds=30)
async def shill_random_member():
    channel = client.get_channel(SHILL_CHANNEL_ID)
    if channel is None:
        print("[shill] Channel not found — check SHILL_CHANNEL_ID")
        return

    members = [m for m in channel.guild.members if not m.bot]
    if not members:
        print("[shill] No eligible members found in server")
        return

    target = random.choice(members)
    title, body = random.choice(WIN_MESSAGES)
    print(f"[shill] Pinging {target.display_name}")

    embed = discord.Embed(
        title=title,
        description=body.format(mention=target.mention, website=WEBSITE),
        color=discord.Color.blue(),
    )
    embed.add_field(name="Claim Here", value=WEBSITE, inline=False)
    embed.set_footer(
        text="idevice Coin - the next generation of decentralized finance or whatever."
    )

    await channel.send(content=target.mention, embed=embed)


@tasks.loop(seconds=10)
async def countdown():
    price_next = price_update.next_iteration
    shill_next = shill_random_member.next_iteration
    if price_next is None or shill_next is None:
        return

    import datetime

    now = datetime.datetime.now(datetime.timezone.utc)

    def fmt(delta):
        total = max(0, int(delta.total_seconds()))
        m, s = divmod(total, 60)
        return f"{m:02d}:{s:02d}"

    price_in = fmt(price_next - now)
    shill_in = fmt(shill_next - now)
    print(
        f"\r[iDVC] next price update: {price_in}  |  next shill: {shill_in}    ",
        end="",
        flush=True,
    )


@client.event
async def on_ready():
    print(f"Logged in as {client.user}. Definitely not running a scam.")
    price_update.start()
    shill_random_member.start()
    countdown.start()


client.run(TOKEN)
