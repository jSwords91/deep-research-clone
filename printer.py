from typing import Any
from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

class Printer:
    def __init__(self, console: Console):
        self.live = Live(console=console)
        self.items: dict[str, tuple[str, bool]] = {}
        self.hide_done_ids: set[str] = set()
        self.live.start()

    def end(self) -> None:
        self.live.stop()

    def hide_done_checkmark(self, item_id: str) -> None:
        self.hide_done_ids.add(item_id)

    def update_item(
        self, item_id: str, content: str, is_done: bool = False, hide_checkmark: bool = False
    ) -> None:
        self.items[item_id] = (content, is_done)
        if hide_checkmark:
            self.hide_done_ids.add(item_id)
        self.flush()

    def mark_item_done(self, item_id: str) -> None:
        self.items[item_id] = (self.items[item_id][0], True)
        self.flush()

    def flush(self) -> None:
        item_renderables: list[Any] = []
        last_index = len(self.items) - 1

        for idx, (item_id, (content, is_done)) in enumerate(self.items.items()):
            if is_done:
                prefix = "✅ " if item_id not in self.hide_done_ids else ""
                item_renderables.append(Text(prefix + content))
            else:
                item_renderables.append(Spinner("dots", text=content))

            if idx != last_index:
                item_renderables.append(Rule(style="dim"))

        group = Group(*item_renderables) if item_renderables else Text("")
        panel = Panel(group, border_style="cyan", padding=(0, 1))
        self.live.update(panel)
