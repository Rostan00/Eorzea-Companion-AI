"""Configurações centralizadas do projeto."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente ou valores padrão."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Aplicação
    app_name: str = "Eorzea Companion AI"
    app_version: str = "0.2.0"
    debug: bool = True

    # Servidor
    host: str = "0.0.0.0"
    port: int = 8000

    # LLM
    llm_provider: str = "mock"  # mock | openai | anthropic | ollama (futuro)
    llm_model: str = "mock-model"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024

    # Personagem
    default_character: str = "lauda"

    # Memória
    memory_db_path: str = "data/memories.db"
    memory_retrieval_limit: int = 5
    memory_auto_extract: bool = True


settings = Settings()
