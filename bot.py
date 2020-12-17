import discord
from discord.ext import commands
import requests
from discord.utils import get
import json
import os
import youtube_dl

client = commands.Bot(command_prefix='+')
client.remove_command('help')


@client.event
async def on_ready():
    print('BOT connected')


# Clear message

@client.command(pass_context=True)
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)
    print('stop')


# Hello

@client.command(pass_context=True)
async def hello(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

    author = ctx.message.author
    await ctx.send(f'{author.mention}, чё надо?')


# Help

@client.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам')

    emb.add_field(name='{}clear'.format('+'), value='Очистка чата')
    emb.add_field(name='{}hello'.format('+'), value='Здрасте, ёпта')
    emb.add_field(name='{}fox'.format('+'), value='Лиса нахуй')
    emb.add_field(name='{}dog'.format('+'), value='Собака нахуй')
    emb.add_field(name='{}mem'.format('+'), value='Мем нахуй')
    emb.add_field(name='{}gif'.format('+'), value='Гифка нахуй')

    await ctx.send(embed=emb)


# Fox

@client.command(pass_context=True)
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')  # Get-запрос
    print(response.text)
    json_data = response.json()  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Лиса нахуй')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


# Dog

@client.command(pass_context=True)
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')  # Get-запрос
    print(response.text)
    json_data = response.json()  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Собака нахуй')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


# Mem

@client.command(pass_context=True)
async def mem(ctx):
    response = requests.get('https://some-random-api.ml/meme')  # Get-запрос
    print(response.text)
    json_data = response.json()  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Мем нахуй')  # Создание Embed'a
    embed.set_image(url=json_data['image'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


# Gif

@client.command(pass_context=True)
async def gif(ctx):
    response = requests.get('https://some-random-api.ml/animu/hug')  # Get-запрос
    print(response.text)
    json_data = response.json()  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Гифка нахуй')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


# Join

@client.command(pass_context=True)
async def j(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')

    await ctx.send(f'Влетел в {channel}')


# Disconnect

@client.command(pass_context=True)
async def l(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Бот вышел из {channel}')
        await ctx.send(f'Съебал из {channel}')
    else:
        print('Bot was told to leave voice channel, but was not in one')
        await ctx.send('Я не в канале, ебалаи...')


# Play

@client.command(pass_context=True)
async def p(ctx, url: str, loudless=1):
    try:
        song_there = os.path.isfile('song.mp3')
        if song_there:
            os.remove('song.mp3')
            print('Перемещён старый файл музыки')
    except PermissionError:
        print('Пытаюсь удалить файл музыки, но пиздец')
        await ctx.send('Пизда, не получилось сыграть')
        return

    await ctx.send('Заряжаю...')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Ждите...\n')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Переименовал файл: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{name} закончил проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = loudless

    nname = name.rsplit('-', 2)
    await ctx.send(f'Ебашу {nname}')
    print('Играю\n')


# Connect


token = ''

client.run(token)
