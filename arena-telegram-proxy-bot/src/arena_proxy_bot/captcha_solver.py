class CaptchaSolvingUnavailable(RuntimeError):
    """Raised when code asks for automated CAPTCHA solving."""


class AsyncCaptchaSolver:
    """Compatibility shim for CAPTCHA-related imports.

    Arena verification is intentionally handled by the manual /verify browser
    flow. Automated third-party CAPTCHA solving is not wired into this project.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def solve_image(self, image_path: str) -> dict:
        raise self._unavailable()

    async def solve_recaptcha_v2(
        self,
        sitekey: str,
        url: str,
        invisible: bool = False,
    ) -> dict:
        raise self._unavailable()

    async def solve_recaptcha_v3(
        self,
        sitekey: str,
        url: str,
        action: str = "verify",
        min_score: float = 0.7,
    ) -> dict:
        raise self._unavailable()

    async def solve_hcaptcha(self, sitekey: str, url: str) -> dict:
        raise self._unavailable()

    async def solve_turnstile(self, sitekey: str, url: str) -> dict:
        raise self._unavailable()

    async def solve_funcaptcha(
        self,
        public_key: str,
        url: str,
        service_url: str | None = None,
    ) -> dict:
        raise self._unavailable()

    async def get_balance(self) -> float:
        return 0.0

    async def report(self, task_id: str, correct: bool) -> dict:
        raise self._unavailable()

    @staticmethod
    def _unavailable() -> CaptchaSolvingUnavailable:
        return CaptchaSolvingUnavailable(
            "Automated CAPTCHA solving is not available. Use /verify to complete "
            "Arena verification manually, then /verify_done to save the browser session."
        )
