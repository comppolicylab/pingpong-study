import base64
import logging
import os
import tomllib
from functools import cached_property
from pathlib import Path
from typing import Literal, Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from pingpong.log_filters import IgnoreHealthEndpoint
from .email import AzureEmailSender, GmailEmailSender, MockEmailSender, SmtpEmailSender

logger = logging.getLogger(__name__)


class MockEmailSettings(BaseSettings):
    type: Literal["mock"]

    @cached_property
    def sender(self) -> MockEmailSender:
        return MockEmailSender()


class AzureEmailSettings(BaseSettings):
    type: Literal["azure"]
    from_address: str
    endpoint: str
    access_key: str

    @property
    def sender(self) -> AzureEmailSender:
        return AzureEmailSender(self.from_address, self.connection_string)

    @property
    def connection_string(self) -> str:
        return f"endpoint={self.endpoint};accessKey={self.access_key}"


class GmailEmailSettings(BaseSettings):
    type: Literal["gmail"]
    from_address: str
    password: str

    @property
    def sender(self) -> GmailEmailSender:
        return GmailEmailSender(self.from_address, self.password)


class SmtpEmailSettings(BaseSettings):
    type: Literal["smtp"]
    from_address: str
    host: str
    port: int = Field(587)
    username: str | None = Field(None)
    password: str | None = Field(None)
    use_tls: bool = Field(True)
    start_tls: bool = Field(False)
    use_ssl: bool = Field(False)

    @property
    def sender(self) -> SmtpEmailSender:
        return SmtpEmailSender(
            self.from_address,
            host=self.host,
            port=self.port,
            user=self.username,
            pw=self.password,
            use_tls=self.use_tls,
            start_tls=self.start_tls,
            use_ssl=self.use_ssl,
        )


EmailSettings = Union[
    AzureEmailSettings, GmailEmailSettings, SmtpEmailSettings, MockEmailSettings
]


class SentrySettings(BaseSettings):
    """Sentry settings."""

    dsn: str = Field("")


class MetricsSettings(BaseSettings):
    """Metrics settings."""

    connection_string: str = Field("")


class SecretKey(BaseSettings):
    """Secret key."""

    key: str
    algorithm: str = Field("HS256")


class AuthSettings(BaseSettings):
    """Authentication and related configuration."""

    secret_keys: list[SecretKey]


class StudySettings(BaseSettings):
    """Settings for the study."""

    airtable_api_key: str
    airtable_base_id: str
    airtable_class_table_id: str
    airtable_instructor_table_id: str
    airtable_admin_table_id: str
    airtable_preassessment_submission_table_id: str
    airtable_postassessment_submission_table_id: str
    airtable_user_class_association_table_id: str


class Config(BaseSettings):
    """Stats Chat Bot config."""

    model_config = SettingsConfigDict(case_sensitive=False)

    log_level: str = Field("INFO")
    reload: int = Field(0)
    study_public_url: str | None = Field(None)
    development: bool = Field(False)
    auth: AuthSettings
    email: EmailSettings
    study: StudySettings | None = Field(None)
    sentry: SentrySettings = Field(SentrySettings())
    metrics: MetricsSettings = Field(MetricsSettings())

    def study_url(self, path: str | None) -> str:
        """Return a URL relative to the study public URL."""
        if not self.study_public_url:
            raise ValueError("Study public URL is not configured")
        if not path:
            return self.study_public_url
        return f"{self.study_public_url.rstrip('/')}/{path.lstrip('/')}"


def _load_config() -> Config:
    """Load the config either from a file or an environment variable.

    Can read the config as a base64-encoded string from the CONFIG env variable,
    or from the file specified in the CONFIG_PATH variable.

    The CONFIG variable takes precedence over the CONFIG_PATH variable.

    Returns:
        Config: The loaded config.
    """
    _direct_cfg = os.environ.get("CONFIG", None)
    _cfg_path = os.environ.get("CONFIG_PATH", "config.toml")

    _raw_cfg: None | str = None

    if _direct_cfg:
        # If the config is provided directly, use it.
        # It should be encoded as Base64.
        _raw_cfg = base64.b64decode(_direct_cfg).decode("utf-8")
    else:
        # Otherwise read the config from the specified file.
        _raw_cfg = Path(_cfg_path).read_text()

    if not _raw_cfg:
        raise ValueError("No config provided")

    try:
        return Config.model_validate(tomllib.loads(_raw_cfg))
    except Exception as e:
        logger.exception(f"Error loading config: {e}")
        raise


# Globally available config object.
config = _load_config()


# Configure logging, shutting up some noisy libraries
logging.basicConfig(level=config.log_level)
# Shut up some noisy libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").addFilter(IgnoreHealthEndpoint())
