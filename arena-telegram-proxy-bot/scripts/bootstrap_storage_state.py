import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


ARENA_URL = "https://arena.ai/"
STATE_PATH = Path("sessions/main_account/storage_state.json")


async def main() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(ARENA_URL, wait_until="domcontentloaded", timeout=60_000)

        print("Opened Arena.ai in a visible browser.")
        print("Complete cookies, Terms, and reCAPTCHA/security verification manually.")
        print("Send one short test prompt if Arena asks for it.")
        input("Press Enter here after Arena is usable, then storage_state will be saved...")

        try:
            await context.storage_state(path=str(STATE_PATH), indexed_db=True)
        except TypeError:
            await context.storage_state(path=str(STATE_PATH))
        print(f"Saved storage_state to {STATE_PATH.resolve()}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
