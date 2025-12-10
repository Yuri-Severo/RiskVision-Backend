import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações centralizadas da aplicação"""

    # Configurações de banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "riskvision")

    # Configurações JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")

    # Configurações AWS
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "")

    # Configurações do coletor de dados de ações
    # Lista de tickers separados por vírgula (ex: AAPL,GOOGL,MSFT)
    STOCK_TICKERS: str = os.getenv("STOCK_TICKERS", "AAPL")

    # Intervalo de coleta em minutos (padrão: 5 minutos)
    STOCK_COLLECTION_INTERVAL_MINUTES: int = int(
        os.getenv("STOCK_COLLECTION_INTERVAL_MINUTES", "5")
    )

    # Período de dados a coletar (1d, 5d, 1mo, etc)
    STOCK_COLLECTION_PERIOD: str = os.getenv("STOCK_COLLECTION_PERIOD", "1d")

    # Intervalo dos dados coletados (1m, 5m, 15m, 1h, 1d, etc)
    STOCK_DATA_INTERVAL: str = os.getenv("STOCK_DATA_INTERVAL", "1m")

    # Habilitar/desabilitar o scheduler automático
    ENABLE_STOCK_SCHEDULER: bool = (
        os.getenv("ENABLE_STOCK_SCHEDULER", "false").lower() == "true"
    )

    # Número máximo de tentativas em caso de erro
    MAX_RETRY_ATTEMPTS: int = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))

    # Delay entre tentativas em segundos
    RETRY_DELAY_SECONDS: int = int(os.getenv("RETRY_DELAY_SECONDS", "5"))

    @classmethod
    def get_tickers_list(cls) -> list[str]:
        """Retorna a lista de tickers configurados"""
        return [
            ticker.strip().upper()
            for ticker in cls.STOCK_TICKERS.split(",")
            if ticker.strip()
        ]

    @classmethod
    def validate_settings(cls) -> dict[str, bool]:
        """Valida as configurações essenciais"""
        validations = {
            "database_configured": bool(cls.DATABASE_URL or cls.POSTGRES_HOST),
            "tickers_configured": bool(cls.get_tickers_list()),
            "collection_interval_valid": cls.STOCK_COLLECTION_INTERVAL_MINUTES > 0,
        }
        return validations


# Instância global de configurações
settings = Settings()
