from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSetting(BaseSettings):
    DATABASE_URL: str

    # This configures how the settings are loaded
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

setting = DatabaseSetting()