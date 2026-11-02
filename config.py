from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    #Атрибуты класса
    DB:str 
    DRIVER:str 
    USER:str 
    PASSWORD:str 
    HOST:str 
    PORT:int
    NAME:str 

    MINIO_BUCKET:str
    MINIO_ENDPOINT:str 
    MINIO_ACCESS_KEY:str 
    MINIO_SECRET_KEY:str

    SECRET_KEY:str 
    ALGORITHM:str 
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    #Метод под видом объекта для получения URL_BD
    @property
    def DATABASE_URL(self)->str: 
        return f"{self.DB}+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
    
    #Чтение данных из файла env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()