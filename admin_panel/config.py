from environs import Env


env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")

POSTGRES_HOST: str = env.str("POSTGRES_HOST")
POSTGRES_PORT: str = env.str("POSTGRES_PORT")
POSTGRES_USER: str = env.str("POSTGRES_USER")
POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD")
POSTGRES_DB: str = env.str("POSTGRES_DB")