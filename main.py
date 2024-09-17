import os
from bot_commands import *

# Load token
TOKEN = os.getenv("DISCORD_TOKEN")


# Startup
@client.event
async def on_ready() -> None:
    await tree.sync(guild=discord.Object(id=1263604022745501829))  # Sync bot commands
    print(f'{client.user} is now running!')


# Main
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
