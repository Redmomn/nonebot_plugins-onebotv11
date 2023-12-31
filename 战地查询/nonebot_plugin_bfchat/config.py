from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    bfchat_prefix: str = '/'
    bfchat_dir: str = './data/bfchat_data/'
    class Config:
        extra = "ignore"