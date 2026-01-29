from datetime import datetime
from enum import Enum, StrEnum, auto
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class GenericStatus(BaseModel):
    status: str


class AuthToken(BaseModel):
    """Auth Token - minimal token used to log in."""

    sub: str
    exp: int
    iat: int


class MagicLoginRequest(BaseModel):
    email: str
    forward: str = "/"


class LoginAsRequest(BaseModel):
    instructor_email: str
    admin_email: str
    forward: str = "/"


class SessionToken(BaseModel):
    """Session Token - stores information about user for a session."""

    sub: str
    exp: int
    iat: int


class SessionStatus(StrEnum):
    VALID = auto()
    ANONYMOUS = auto()
    MISSING = auto()
    INVALID = auto()
    ERROR = auto()


class Institution(BaseModel):
    id: int
    name: str
    description: str | None
    logo: str | None
    default_api_key_id: int | None = None
    created: datetime
    updated: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class Institutions(BaseModel):
    institutions: list[Institution]

    model_config = ConfigDict(
        from_attributes=True,
    )


class EmailValidationResult(BaseModel):
    email: str
    valid: bool
    isUser: bool = False
    name: str | None
    error: str | None = None


class EmailValidationResults(BaseModel):
    results: list[EmailValidationResult]


class InstructorResponse(BaseModel):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    academic_email: str | None = None
    personal_email: str | None = None
    honorarium_status: Literal["Yes", "No", "Unsure/Other"] | None = None
    mailing_address: str | None = None
    institution: str | None = None


class CreateInstitution(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)


class InteractionMode(StrEnum):
    CHAT = "chat"
    VOICE = "voice"


class Assistant(BaseModel):
    id: int
    name: str
    version: int | None = None
    instructions: str
    description: str | None
    notes: str | None = None
    interaction_mode: InteractionMode
    tools: str
    model: str
    temperature: float | None
    verbosity: int | None
    reasoning_effort: int | None
    class_id: int
    creator_id: int
    locked: bool = False
    assistant_should_message_first: bool | None = None
    should_record_user_information: bool | None = None
    allow_user_file_uploads: bool | None = None
    allow_user_image_uploads: bool | None = None
    hide_reasoning_summaries: bool | None = None
    hide_file_search_result_quotes: bool | None = None
    hide_file_search_document_names: bool | None = None
    hide_file_search_queries: bool | None = None
    hide_web_search_sources: bool | None = None
    hide_web_search_actions: bool | None = None
    hide_mcp_server_call_details: bool | None = None
    use_latex: bool | None
    use_image_descriptions: bool | None
    hide_prompt: bool | None
    published: datetime | None
    endorsed: bool | None = None
    created: datetime
    updated: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class Class(BaseModel):
    id: int
    name: str
    term: str
    institution_id: int
    institution: Institution | None = None
    created: datetime
    updated: datetime | None
    private: bool | None = None
    any_can_create_assistant: bool | None = None
    any_can_publish_assistant: bool | None = None
    any_can_share_assistant: bool | None = None
    any_can_publish_thread: bool | None = None
    any_can_upload_class_file: bool | None = None
    download_link_expiration: str | None = None
    last_rate_limited_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateClass(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    term: str = Field(..., min_length=1, max_length=100)
    api_key_id: int | None = None
    private: bool = False
    any_can_create_assistant: bool = False
    any_can_publish_assistant: bool = False
    any_can_share_assistant: bool = False
    any_can_publish_thread: bool = False
    any_can_upload_class_file: bool = False


class CreateUserResult(BaseModel):
    email: str
    display_name: str | None = None
    error: str | None = None


class CreateUserResults(BaseModel):
    results: list[CreateUserResult]


class ClassUserRoles(BaseModel):
    admin: bool
    teacher: bool
    student: bool

    def string(self) -> str:
        return f"admin={self.admin},teacher={self.teacher},student={self.student}"


class CreateUserClassRole(BaseModel):
    email: str = Field(..., min_length=3, max_length=100)
    display_name: str | None = None
    sso_id: str | None = None
    last_active: datetime | None = None
    roles: ClassUserRoles


class CreateUserClassRoles(BaseModel):
    roles: list[CreateUserClassRole]
    silent: bool = False
    lms_tenant: str | None = None
    lti_class_id: int | None = None
    is_lti_launch: bool = False
    sso_tenant: str | None = None


class UserNameMixin:
    email: str | None
    first_name: str | None
    last_name: str | None
    display_name: str | None

    @computed_field  # type: ignore
    @property
    def name(self) -> str | None:
        """Return some kind of name for the user."""
        if self.display_name:
            return self.display_name
        parts = [name for name in [self.first_name, self.last_name] if name]
        if not parts:
            return self.email
        return " ".join(parts)

    @computed_field  # type: ignore
    @property
    def has_real_name(self) -> bool:
        """Return whether we have a name to display for a user."""
        return bool(self.display_name or self.first_name or self.last_name)


class UserState(Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    BANNED = "banned"


class User(BaseModel, UserNameMixin):
    id: int
    state: UserState
    created: datetime
    updated: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class StudyFeatureFlags(BaseModel):
    """Feature flags and one-time notices for Study.

    Keys use dotted, versioned names. Example:
    - notice.profile_moved.v1
    - banner.maintenance_2025_09.v1
    - feature.some_toggle.v2
    """

    flags: dict[str, bool] = Field(default_factory=dict)


class StudyCourse(BaseModel):
    id: str
    name: str | None = None
    status: Literal["in_review", "accepted", "rejected", "withdrawn"] | None = None
    randomization: Literal["control", "treatment"] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    enrollment_count: int | None = None
    completion_rate_target: float | None = None
    preassessment_url: str | None
    postassessment_url: str | None = None
    pingpong_group_url: str | None
    preassessment_student_count: int | None = None
    postassessment_student_count: int | None = None


class StudySessionState(BaseModel):
    status: SessionStatus
    error: str | None = None
    instructor: InstructorResponse | None = None
    token: SessionToken | None = None
    feature_flags: StudyFeatureFlags | None = None


class StudyNoticeSeenRequest(BaseModel):
    key: str
