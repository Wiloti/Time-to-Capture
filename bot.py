#!/usr/bin/python3

import discord
import os
import requests
from dotenv import load_dotenv
from discord import app_commands
from typing import Optional
from datetime import datetime as dt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('TEST_GUILD')
IMG = os.getenv('IMG')
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=GUILD))
            self.synced = True
        print(f'{self.user.name} has connected to Discord!')
        print("-------------------")
        await client.change_presence(activity=discord.Game(name="CTF"))


client = Bot()
tree = app_commands.CommandTree(client)


@tree.command(name='team', description='Top team in leaderboard', guild=discord.Object(id=GUILD))
async def self(interaction: discord.Interaction, year: Optional[int] = dt.now().year):
    try:
        if year >= 2011 and year <= dt.now().year:
            r = requests.get(
                f'https://ctftime.org/api/v1/top/{year}/', headers=headers)
            team_data = r.json()
            embed = discord.Embed(
                title=f'Top team in {year}', timestamp=dt.now(), color=0xE3000B)
            embed.set_thumbnail(url=IMG)
            embed.add_field(
                name='\N{Crown} ' + team_data[str(year)][0]['team_name'], value=f'`points` {round(team_data[str(year)][0]["points"], 2)}', inline=False)
            embed.add_field(
                name='2 ' + team_data[str(year)][1]['team_name'], value=f'`points` {round(team_data[str(year)][1]["points"], 2)}', inline=False)
            embed.add_field(
                name='3 ' + team_data[str(year)][2]['team_name'], value=f'`points` {round(team_data[str(year)][2]["points"], 2)}', inline=False)
            embed.add_field(
                name='4 ' + team_data[str(year)][3]['team_name'], value=f'`points` {round(team_data[str(year)][3]["points"], 2)}', inline=False)
            embed.add_field(
                name='5 ' + team_data[str(year)][4]['team_name'], value=f'`points` {round(team_data[str(year)][4]["points"], 2)}', inline=False)
            embed.add_field(
                name='6 ' + team_data[str(year)][5]['team_name'], value=f'`points` {round(team_data[str(year)][5]["points"], 2)}', inline=False)
            embed.add_field(
                name='7 ' + team_data[str(year)][6]['team_name'], value=f'`points` {round(team_data[str(year)][6]["points"], 2)}', inline=False)
            embed.add_field(
                name='8 ' + team_data[str(year)][7]['team_name'], value=f'`points` {round(team_data[str(year)][7]["points"], 2)}', inline=False)
            embed.add_field(
                name='9 ' + team_data[str(year)][8]['team_name'], value=f'`points` {round(team_data[str(year)][8]["points"], 2)}', inline=False)
            embed.add_field(
                name='10 ' + team_data[str(year)][9]['team_name'], value=f'`points` {round(team_data[str(year)][9]["points"], 2)}', inline=False)
            embed.set_footer(
                text=f'Provide by CTFtime.org and {client.user.name}', icon_url=client.user.avatar)
            print(f'team command called with year {year}')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                'You traveled too far my dude!')
    except Exception as e:
        print(e)
        await interaction.response.send_message(
            'Something went wrong!')


@tree.command(name='event', description='5 next Upcoming events', guild=discord.Object(id=GUILD))
async def self(interaction: discord.Interaction):
    try:
        print('event command called')
        r = requests.get(
            'https://ctftime.org/api/v1/events/', headers=headers, params={'limit': 5, 'start': round(dt.now().timestamp())})
        event_data = r.json()
        for event in range(len(event_data)):
            embed = discord.Embed(title=f'Upcoming event : {event_data[event]["title"]}', description=event_data[event]['description'],
                                  timestamp=dt.now(), color=0xE3000B, url=event_data[event]['url'])
            embed.set_thumbnail(
                url=event_data[event]['logo'])
            embed.add_field(
                name='Organizers', value=event_data[event]['organizers'][0]['name'], inline=False)
            embed.add_field(
                name="Format", value=event_data[event]['format'], inline=True)
            embed.add_field(
                name='weight', value=event_data[event]['weight'], inline=True)
            embed.add_field(
                name='Restriction', value=event_data[event]['restrictions'], inline=True)
            embed.add_field(
                name='Duration', value=f'{event_data[event]["duration"]["days"]} Day(s) {event_data[event]["duration"]["hours"]} Hour(s)', inline=False)
            embed.add_field(
                name='Event start', value=f'{event_data[event]["start"].replace("T", " ").split("+", 1)[0]} UTC', inline=True)
            embed.add_field(
                name='Event End', value=f'{event_data[event]["finish"].replace("T", " ").split("+", 1)[0]} UTC', inline=True)
            embed.set_footer(
                text=f'Provided by CTFtime.org and {client.user.name}', icon_url=client.user.avatar)
            await interaction.channel.send(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message(
            'Something went wrong!')
try:
    client.run(TOKEN)
except:
    print(f'Error when logging in: {e}')
