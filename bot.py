from discord import Intents, Activity, Status, __version__
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")

class Client(commands.Bot):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix="!") #dummy prefix cant be used

        self.cogslist = ["src.cogs.help", "src.cogs.ctftime"] # path for cogs
    # loading cogs
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            try:
                await self.load_extension(ext)
            except Exception as e:
                print(f"Failed to load extension '{ext}'. Error: {e}")

    # bot initialization
    async def on_ready(self) -> None:
#        clear_console()
        synced = str(len(await self.tree.sync()))
        await self.change_presence(activity=Activity(name="a random CTF", type=5), status=Status.do_not_disturb)
        print(f"{self.user} logged in successfully")
        print(f"Discord version: {__version__}")
        print(f"{synced} commands loaded")

client = Client()

if __name__ == "__main__":
    if TOKEN is not None:
        try:
            client.run(TOKEN)
        except Exception as e:
            print(f"Logging problem: {e}")
