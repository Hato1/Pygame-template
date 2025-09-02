"""Loads configuration settings from config.yaml in CWD."""

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

from pygame_me import logging

logger = logging.get_logger()

CONFIG_FILE = Path("config.yaml")


class Game(BaseModel):
    """App config class."""

    name: str


class Config(BaseSettings):
    """CLI config class."""

    log_level: int | logging.LogLevel = logging.LogLevel.INFO
    game: Game

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize the sources for loading settings.

        This method allows customization of how settings are loaded.
        It returns a tuple of settings sources, which are used
        to populate the settings object.
        """
        yaml_settings = YamlConfigSettingsSource(settings_cls, yaml_file=CONFIG_FILE)
        return init_settings, env_settings, yaml_settings, file_secret_settings


def load_config() -> Config:
    """Load the config."""
    if not CONFIG_FILE.is_file():
        raise FileNotFoundError(f"Could not find config file: '{CONFIG_FILE}'")

    return Config()  # type: ignore[reportCallissue]


if __name__ == "__main__":
    config = load_config()
    logger.info(config.model_dump())
