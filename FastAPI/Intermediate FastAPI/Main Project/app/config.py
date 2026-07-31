from pydantic_settings import BaseSettings, SettingsConfigDict


_base_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

class DatabaseSetting(BaseSettings):
    DATABASE_URL: str

    # This configures how the settings are loaded
    model_config = _base_config


class SecuritySettings(BaseSettings):

    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = _base_config

db_setting = DatabaseSetting()
security_settings = SecuritySettings()