import random
from time import sleep
import discord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()

mateuszID = 178094529008762880
przemekID = 190868516470128641
martynaID = 331364675222765580
mikolajID = 140237130549952513
wojtekID = 191185837818511360
zuziaID = 522857702225870869
kacperID = 385835713004044301

admin_ids = [178094529008762880, 123]
trusted_ids = [przemekID, martynaID, mateuszID, wojtekID, kacperID, zuziaID, mikolajID]

random.seed(a=None, version=2)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    async def has_permission(user_id, ranga):
        if ranga == 'admin':
            if user_id in admin_ids:
                return True
            else:
                await message.channel.send("Nie masz permisji aby użyć tej komendy")
                return False
        elif ranga == 'trusted':
            if user_id in trusted_ids:
                return True
            else:
                await message.channel.send("Nie masz permisji aby użyć tej komendy")
                return False
        else:
            await message.channel.send("Niespodziewane zachowanie z twojej strony")
            return False

    if message.author == client.user:
        return

    if message.content.lower().startswith('$ping'):
        await message.channel.send('pong')

    if message.content.lower().startswith('$pong'):
        await message.channel.send('ping')

    if message.content.lower().startswith('$say ') and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split(" ", 1)
        await message.delete()
        await message.channel.send(temp[1])

    if message.content.lower().startswith('$roll'):
        s = [int(s) for s in message.content.split() if s.isdigit()]
        await message.channel.send("*rolls*")
        sleep(1)
        await message.channel.send(random.randint(1, s[0]))

    if message.content.lower().startswith('$repeat'):
        await message.channel.send(message.content.replace("$repeat", "Napisal_s: "))

    if message.content.lower().startswith("$listnote") and await has_permission(message.author.id, 'trusted'):
        temp = "**Zanotowane tagi:** | "
        with open('note', 'r') as noteFile:
            for line in noteFile.readlines():
                temp += (line.split(" ", 1)[0]) + " | "
            await message.channel.send(temp)

    if message.content.lower().startswith("$viewnote") and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split()
        message.channel.send("Arg: " + temp[1])
        with open('note', 'r') as noteFile:
            for line in noteFile.readlines():
                if temp[1] == line.split(" ", 1)[0]:
                    await message.channel.send(f"**{temp[1]}:** " + line.split(" ", 1)[1])

    if message.content.lower().startswith('$note') and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split(" ", 2)
        with open('note', 'a') as noteFile:
            noteFile.writelines(temp[1] + " " + temp[2] + "\n")
            await message.channel.send('Zanotowal_s: *' + temp[2] + '*\npod tagiem **' + temp[1] + "**")

    if message.content.lower() == '$clickbait':
        with open('clickbaitprefix', 'r', encoding="UTF-8") as prefixList, \
                open('clickbaitperson', 'r', encoding="UTF-8") as personList, \
                open('clickbaitactivity', 'r', encoding="UTF-8") as activityList:
            prefix = random.choice(prefixList.read().splitlines())
            person = random.choice(personList.read().splitlines())
            activity = random.choice(activityList.read().splitlines())
            await message.channel.send(f"**{prefix.upper()}** {person.upper()} {activity.upper()}")

    if message.content.lower().startswith('$clickbait remove person') and await has_permission(message.author.id, 'admin'):
        toremove = message.content.split(" ", 3)
        with open('clickbaitperson', 'a+', encoding="UTF-8") as file:
            file.seek(0)
            file.writelines([line for line in file.read().splitlines() if line.lower() != toremove.lower()])
            await message.channel.send(f"Usunięto **{toremove}** z bazy osób")

    if message.content.lower().startswith('$clickbait add person') and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split(" ", 3)
        with open('clickbaitperson', 'r+', encoding="UTF-8") as personList:
            if temp[3].lower() not in personList.read().lower().splitlines():
                personList.writelines(temp[3] + "\n")
                await message.channel.send(f'Dodales do bazy osob: **{temp[3].upper()}**')
            else:
                await message.channel.send(f"**{temp[3]}** jest juz w bazie")

    if message.content.lower().startswith('$clickbait add prefix') and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split(" ", 3)
        with open('clickbaitprefix', 'r+', encoding="UTF-8") as prefixList:
            if temp[3].lower() not in prefixList.read().lower().splitlines():
                prefixList.writelines(temp[3] + "\n")
                await message.channel.send(f'Dodales do bazy prefixów: **{temp[3].upper()}**')
            else:
                await message.channel.send(f"**{temp[3]}** jest juz w bazie")

    if message.content.lower().startswith('$clickbait add activity') and await has_permission(message.author.id, 'trusted'):
        temp = message.content.split(" ", 3)
        with open('clickbaitactivity', 'r+', encoding="UTF-8") as activityList:
            if temp[3].lower() not in activityList.read().lower().splitlines():
                activityList.writelines(temp[3] + "\n")
                await message.channel.send(f'Dodales do bazy activity: **{temp[3].upper()}**')
            else:
                await message.channel.send(f"**{temp[3]}** jest juz w bazie")

    if message.content.lower() == "$exams":
        with open('plan', 'r') as file:
            await message.channel.send(file.read())

    if message.content.lower() == '$admin' and await has_permission(message.author.id, 'admin'):
        print("is admin indeed")
        await message.channel.send('admin')

    if message.content.lower() == '$trusted' and await has_permission(message.author.id, 'trusted'):
        await message.channel.send('trusted')

    if message.content.lower() == 'beep':
        await message.channel.send('BEEP BEEP')


with open('token', 'r') as token:
    client.run(token.readline())
