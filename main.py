import os
from dotenv import load_dotenv
from bot_commands import *

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# Startup
@client.event
async def on_ready() -> None:
    await tree.sync()  # Sync bot commands
    print(f'{client.user} is now running!')


# Main
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
