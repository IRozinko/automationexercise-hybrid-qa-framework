from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://automationexercise.com")
    headless: bool = _as_bool(os.getenv("HEADLESS"), True)
    slow_mo_ms: int = int(os.getenv("SLOW_MO_MS", "0"))
    default_timeout_ms: int = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
    artifacts_dir: str = os.getenv("ARTIFACTS_DIR", "artifacts")


settings = Settings()
