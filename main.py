import asyncio
from manager import ResearchManager
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()


async def main() -> None:
    console = Console()
    query = console.input("[bold cyan]What would you like to research?[/bold cyan] ")
    await ResearchManager().run(query)

if __name__ == "__main__":
    asyncio.run(main())
