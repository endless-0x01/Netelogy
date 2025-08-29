import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

current_dir: Path = Path(__file__).parent

load_dotenv(current_dir / ".env")

TOKEN_TG: Optional[str] = os.getenv("TOKEN_TG")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///default.db")

if not TOKEN_TG:
    raise ValueError("TOKEN_TG не найден в переменных окружения!")
