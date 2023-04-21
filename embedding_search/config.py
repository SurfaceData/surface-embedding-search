from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_PATH: str
    DEVICE: str = "cpu"
    MODEL_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        use_enum_value = True


settings = Settings()
