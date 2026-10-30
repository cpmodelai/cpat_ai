from typing import Callable, Awaitable
from shiny import ui

def success_notification(
        label: str
        ) -> None:
    ui.notification_show(
        label,
        type="message",
        duration=3,
        close_button=True,
    )

def error_notification(
        label: str
        ) -> None:
    ui.notification_show(
        label,
        type="error",
        duration=3,
        close_button=True,
    )

async def progress_bar(
        message: str,
        task: Callable[[], Awaitable[bool]],
        notification: Callable[[], None],
        ) -> None:
    """Run `task` under a progress bar; `notification` follows if the task returns True (it succeeded)."""
    with ui.Progress(min=1, max=10) as p:
        p.set(message=message, detail="Please wait...")
        p.set(1)
        succeeded = await task()
        p.set(10)
        if succeeded:
            notification()
