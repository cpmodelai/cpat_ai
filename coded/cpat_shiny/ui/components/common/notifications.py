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
        task: Callable[[], Awaitable[None]],
        notification: Callable[[], None],
        ) -> None:
    with ui.Progress(min=1, max=10) as p:
        p.set(message=message, detail="Please wait...")
        p.set(1)
        await task()
        p.set(10)
        notification()
