"""Models for AIVenture."""

import enum
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlmodel import Column, Enum, Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig


class AIModelTypeEnum(str, enum.Enum):
    """AI model type enum."""

    AUDIO = "audio"
    CV = "cv"
    MULTI_MODAL = "multi_modal"
    NLP = "nlp"

    @property
    def item(self) -> "AIModelTypeBase":
        """Get the item."""
        return AI_MODEL_TYPE_MAPPING[self]


class LocationEnum(str, enum.Enum):
    """Location enum."""

    US = "us"
    EU = "eu"
    APAC = "apac"

    @property
    def item(self) -> "LocationBase":
        """Get the location."""
        return LOCATION_MAPPING[self.value]


class ModifierTypeEnum(str, enum.Enum):
    """Modifier type enum."""

    EMPLOYEE = "employee"
    LAB = "lab"
    LOCATION = "location"

    @property
    def item(self) -> "ModifierTypeBase":
        """Get the modifier type."""
        return MODIFIER_TYPE_MAPPING[self.value]


class ModifierEnum(str, enum.Enum):
    """Modifier enum."""

    # TODO: Add modifiers

    @property
    def item(self) -> "ModifierBase":
        """Get the modifier."""
        return MODIFIER_MAPPING[self.value]


class QualityEnum(str, enum.Enum):
    """Quality enum."""

    POOR = "poor"
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    STAR = "star"

    @property
    def item(self) -> "QualityBase":
        """Get the quality."""
        return QUALITY_MAPPING[self.value]


class RoleCategoryEnum(str, enum.Enum):
    """Role category enum."""

    RESEARCH = "research"
    ENGINEERING = "engineering"
    OPERATIONS = "operations"
    LEADERSHIP = "leadership"
    SALES = "sales"
    HR = "hr"

    @property
    def item(self) -> "RoleCategoryBase":
        """Get the category."""
        return ROLE_CATEGORY_MAPPING[self.value]


class RoleEnum(str, enum.Enum):
    """Role enum."""

    # Research
    RESEARCH_ENGINEER = "research_engineer"
    RESEARCH_SCIENTIST = "research_scientist"
    AI_SAFETY_RESEARCHER = "ai_safety_researcher"
    # Engineering
    ML_ENGINEER = "ml_engineer"
    SOFTWARE_ENGINEER = "software_engineer"
    DATA_ENGINEER = "data_engineer"
    SITE_RELIABILITY_ENGINEER = "site_reliability_engineer"
    INFRASTRUCTURE_ENGINEER = "infrastructure_engineer"
    SECURITY_ENGINEER = "security_engineer"
    # Operations
    PROJECT_MANAGER = "project_manager"
    DATA_OPERATIONS_MANAGER = "data_operations_manager"
    TECHNICAL_PROGRAM_MANAGER = "technical_program_manager"
    COMPUTE_OPERATIONS_MANAGER = "compute_operations_manager"
    # Leadership
    CHIEF_SCIENTIST = "chief_scientist"
    RESEARCH_DIRECTOR = "research_director"
    ENGINEERING_DIRECTOR = "engineering_director"
    CTO = "cto"
    # Sales
    AI_SOLUTIONS_ARCHITECT = "ai_solutions_architect"
    PARTNERSHIP_MANAGER = "partnership_manager"
    BUSINESS_DEVELOPMENT = "business_development"
    CUSTOMER_SUCCESS_MANAGER = "customer_success_manager"
    # HR
    TECHNICAL_RECRUITER = "technical_recruiter"
    LEARNING_DEVELOPMENT_MANAGER = "learning_development_manager"
    TALENT_OPERATIONS_MANAGER = "talent_operations_manager"
    DIVERSITY_INCLUSION_SPECIALIST = "diversity_inclusion_specialist"

    @property
    def item(self) -> "RoleBase":
        """Get the role object for this enum value."""
        return ROLE_MAPPING[self.value]


class UUIDModel(SQLModel):
    """Model with a UUID."""

    id: str = Field(
        # NOTE: This is a workaround to use UUIDs as primary keys in SQLite + aiosqlite and SQLModel/SQLAlchemy.
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True},
    )

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}})


class EmployeeModifierLink(SQLModel, table=True):
    """Link table for employees and modifiers."""

    __tablename__ = "employee_modifier_link"

    employee_id: str | None = Field(default=None, foreign_key="employees.id", primary_key=True)
    modifier_id: str | None = Field(default=None, foreign_key="modifiers.id", primary_key=True)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "employee_id": "123e4567-e89b-12d3-a456-426614174000",
                "modifier_id": "123e4567-e89b-12d3-a456-426614174001",
            }
        }
    )


class PlayerLabInvestmentLink(SQLModel, table=True):
    """Link table for players and lab investments."""

    __tablename__ = "player_lab_investment_link"

    player_id: str | None = Field(default=None, foreign_key="players.id", primary_key=True)
    lab_id: str | None = Field(default=None, foreign_key="labs.id", primary_key=True)
    part: float = Field(default=1.0, ge=0.0, le=1.0, description="The part of the lab that the player owns.")

    player: "Player" = Relationship(back_populates="investments", sa_relationship_kwargs={"lazy": "selectin"})
    lab: "Lab" = Relationship(back_populates="investors", sa_relationship_kwargs={"lazy": "selectin"})

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "player_id": "123e4567-e89b-12d3-a456-426614174000",
                "lab_id": "123e4567-e89b-12d3-a456-426614174001",
                "part": 0.5,
            }
        }
    )


class AIModelTypeBase(SQLModel):
    """AI model type base model."""

    id: int = Field(primary_key=True)
    name: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "NLP"}})


class AIModelType(AIModelTypeBase, table=True):
    """AI model type model."""

    __tablename__ = "ai_model_types"


AI_MODEL_TYPE_MAPPING: dict[int, AIModelTypeBase] = {
    1: AIModelTypeBase(id=1, name="Audio"),
    2: AIModelTypeBase(id=2, name="CV"),
    3: AIModelTypeBase(id=3, name="NLP"),
    4: AIModelTypeBase(id=4, name="Multi Modal"),
}


class GlobalGameState(BaseModel):
    """Global game state."""

    n_connected_players: int


class Health(BaseModel):
    """Health model for the API."""

    status: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"status": "healthy"}},
    )


class PlayerBase(UUIDModel):
    """Player model."""

    name: str
    avatar: str
    funds: float = Field(default=100000.0)
    user_id: str = Field(foreign_key="users.id", sa_column_kwargs={"unique": True})

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "funds": 100000,
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
            }
        }
    )


class Player(PlayerBase, table=True):
    """Player model."""

    __tablename__ = "players"

    labs: list["Lab"] = Relationship(back_populates="player", sa_relationship_kwargs={"lazy": "selectin"})
    investments: list[PlayerLabInvestmentLink] = Relationship(
        back_populates="player",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class LabBase(UUIDModel):
    """Lab model."""

    name: str
    location: LocationEnum = Field(sa_column=Column(Enum(LocationEnum)))
    valuation: float
    income: float
    tech_tree_id: str
    player_id: str = Field(foreign_key="players.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Lab Zero",
                "location": "us",
                "valuation": 1000000,
                "income": 100000,
                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174001",
                "player_id": "123e4567-e89b-12d3-a456-426614174002",
            }
        }
    )


class Lab(LabBase, table=True):
    """Table for labs."""

    __tablename__ = "labs"

    employees: list["Employee"] = Relationship(back_populates="lab", sa_relationship_kwargs={"lazy": "selectin"})
    models: list["AIModel"] = Relationship(back_populates="lab", sa_relationship_kwargs={"lazy": "selectin"})
    investors: list[PlayerLabInvestmentLink] = Relationship(
        back_populates="lab",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    player: Player = Relationship(back_populates="labs", sa_relationship_kwargs={"lazy": "selectin"})


class AIModelBase(UUIDModel):
    """AI model base model."""

    name: str
    ai_model_type_id: int = Field(foreign_key="ai_model_types.id")
    tech_tree_id: str
    lab_id: str = Field(foreign_key="labs.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "name": "GPT-2",
                "ai_model_type_id": 3,
                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174000",
                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class AIModel(AIModelBase, table=True):
    """AI model model."""

    __tablename__ = "ai_models"

    lab: Lab = Relationship(back_populates="models", sa_relationship_kwargs={"lazy": "selectin"})


class EmployeeBase(UUIDModel):
    """Employee model."""

    name: str
    salary: int
    image_url: str
    role_id: int = Field(foreign_key="roles.id")
    quality_id: int = Field(foreign_key="qualities.id")
    lab_id: str | None = Field(foreign_key="labs.id", default=None)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "bonuses": ["Free lunch", "Free gym"],
                "salary": 100000,
                "image_url": "https://avatar.iran.liara.run/public",
                "role_id": 1,
                "quality_id": 1,
                "modifier_id_1": 1,
                "modifier_id_2": 2,
                "modifier_id_3": 3,
                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class Employee(EmployeeBase, table=True):
    """Table for employees."""

    __tablename__ = "employees"

    # modifiers: list[Modifier] = Relationship(
    #     back_populates="employees",
    #     link_model=EmployeeModifierLink,
    #     sa_relationship_kwargs={"lazy": "selectin"},
    # )
    lab: Lab | None = Relationship(back_populates="employees", sa_relationship_kwargs={"lazy": "selectin"})


class LocationBase(SQLModel):
    """Location model."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    modifier_id: int = Field(foreign_key="modifiers.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "US",
                "description": "The United States of America",
                "modifier_id": 1,
            }
        }
    )


class Location(LocationBase, table=True):
    """Table for locations."""

    __tablename__ = "locations"


LOCATION_MAPPING: dict[str, LocationBase] = {
    "us": LocationBase(id=1, name="US", description="The United States of America", modifier_id=1),
    "eu": LocationBase(id=2, name="EU", description="The European Union", modifier_id=2),
    "apac": LocationBase(id=3, name="APAC", description="Asia Pacific", modifier_id=3),
}


class ModifierTypeBase(SQLModel):
    """Modifier type model."""

    id: int = Field(primary_key=True)
    name: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "lab"}})


class ModifierType(ModifierTypeBase, table=True):
    """Modifier type model."""

    __tablename__ = "modifier_types"


MODIFIER_TYPE_MAPPING: dict[str, ModifierTypeBase] = {
    "employee": ModifierTypeBase(id=1, name="employee"),
    "lab": ModifierTypeBase(id=2, name="lab"),
    "location": ModifierTypeBase(id=3, name="location"),
}


class ModifierBase(SQLModel):
    """Modifier base model."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    type_id: int = Field(foreign_key="modifier_types.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Boost model accuracy",
                "description": "Boost model accuracy by 10%",
                "type_id": 1,
            }
        }
    )


class Modifier(ModifierBase, table=True):
    """Modifier model."""

    __tablename__ = "modifiers"

    # employees: list[Employee] = Relationship(
    #     back_populates="modifiers",
    #     link_model=EmployeeModifierLink,
    #     sa_relationship_kwargs={"lazy": "selectin"},
    # )


MODIFIER_MAPPING: dict[str, ModifierBase] = {
    # TODO: Add modifiers
}


class QualityBase(SQLModel):
    """Quality model."""

    id: int = Field(primary_key=True)
    name: str
    hex_color: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "Poor", "hex_color": "#9d9d9d"}})


class Quality(QualityBase, table=True):
    """Quality model."""

    __tablename__ = "qualities"


QUALITY_MAPPING: dict[str, QualityBase] = {
    "poor": QualityBase(id=1, name="Poor", hex_color="#9d9d9d"),
    "common": QualityBase(id=2, name="Common", hex_color="#ffffff"),
    "uncommon": QualityBase(id=3, name="Uncommon", hex_color="#1eff00"),
    "rare": QualityBase(id=4, name="Rare", hex_color="#0070dd"),
    "epic": QualityBase(id=5, name="Epic", hex_color="#a335ee"),
    "legendary": QualityBase(id=6, name="Legendary", hex_color="#ff8000"),
    "star": QualityBase(id=7, name="Star", hex_color="#e6cc80"),
}


class RoleCategoryBase(SQLModel):
    """Role category model."""

    id: int = Field(primary_key=True)
    name: str
    hex_color: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "Research", "hex_color": "#90dbf4"}})


class RoleCategory(RoleCategoryBase, table=True):
    """Role category model."""

    __tablename__ = "role_categories"


ROLE_CATEGORY_MAPPING: dict[str, RoleCategoryBase] = {
    "research": RoleCategoryBase(id=1, name="Research", hex_color="#90dbf4"),
    "engineering": RoleCategoryBase(id=2, name="Engineering", hex_color="#f1c0e8"),
    "operations": RoleCategoryBase(id=3, name="Operations", hex_color="#ffcfd2"),
    "leadership": RoleCategoryBase(id=4, name="Leadership", hex_color="#b9fbc0"),
    "sales": RoleCategoryBase(id=5, name="Sales", hex_color="#fbf8cc"),
    "hr": RoleCategoryBase(id=6, name="HR", hex_color="#8eecf5"),
}


class RoleBase(SQLModel):
    """Role model."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    category_id: int = Field(foreign_key="role_categories.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Research Engineer",
                "description": "Research and development of new products and technologies.",
                "category_id": 1,
            }
        }
    )


class Role(RoleBase, table=True):
    """Role model."""

    __tablename__ = "roles"


ROLE_MAPPING: dict[str, RoleBase] = {
    # Research
    "research_engineer": RoleBase(
        id=1,
        name="Research Engineer",
        description="Engineer who works on research and development of new products and technologies.",
        category_id=1,
    ),
    "research_scientist": RoleBase(
        id=2,
        name="Research Scientist",
        description="Scientist who works on research and development of new products and technologies.",
        category_id=1,
    ),
    "ai_safety_researcher": RoleBase(
        id=3,
        name="AI Safety Researcher",
        description="Researcher who works on AI safety and ethical considerations.",
        category_id=1,
    ),
    # Engineering
    "ml_engineer": RoleBase(
        id=4,
        name="ML Engineer",
        description="Engineer who works on machine learning and artificial intelligence.",
        category_id=2,
    ),
    "software_engineer": RoleBase(
        id=5,
        name="Software Engineer",
        description="Engineer who works on software development.",
        category_id=2,
    ),
    "data_engineer": RoleBase(
        id=6,
        name="Data Engineer",
        description="Engineer who works on data engineering.",
        category_id=2,
    ),
    "site_reliability_engineer": RoleBase(
        id=7,
        name="Site Reliability Engineer",
        description="Engineer who works on site reliability and performance.",
        category_id=2,
    ),
    "infrastructure_engineer": RoleBase(
        id=8,
        name="Infrastructure Engineer",
        description="Engineer who works on infrastructure.",
        category_id=2,
    ),
    "security_engineer": RoleBase(
        id=9,
        name="Security Engineer",
        description="Engineer who works on security.",
        category_id=2,
    ),
    # Operations
    "project_manager": RoleBase(
        id=10,
        name="Project Manager",
        description="Coordinates research projects and team resources",
        category_id=3,
    ),
    "data_operations_manager": RoleBase(
        id=11,
        name="Data Operations Manager",
        description="Oversees data collection and annotation processes",
        category_id=3,
    ),
    "technical_program_manager": RoleBase(
        id=12,
        name="Technical Program Manager",
        description="Manages complex technical programs across teams",
        category_id=3,
    ),
    "compute_operations_manager": RoleBase(
        id=13,
        name="Compute Operations Manager",
        description="Manages computing resources and infrastructure operations",
        category_id=3,
    ),
    # Leadership
    "chief_scientist": RoleBase(
        id=14,
        name="Chief Scientist",
        description="Sets overall research direction and scientific strategy",
        category_id=4,
    ),
    "research_director": RoleBase(
        id=15,
        name="Research Director",
        description="Leads research teams and coordinates research efforts",
        category_id=4,
    ),
    "engineering_director": RoleBase(
        id=16,
        name="Engineering Director",
        description="Oversees engineering teams and technical infrastructure",
        category_id=4,
    ),
    "cto": RoleBase(
        id=17,
        name="Chief Technology Officer",
        description="Leads technical strategy and innovation",
        category_id=4,
    ),
    # Sales
    "ai_solutions_architect": RoleBase(
        id=18,
        name="AI Solutions Architect",
        description="Designs AI solutions for client needs",
        category_id=5,
    ),
    "partnership_manager": RoleBase(
        id=19,
        name="Partnership Manager",
        description="Develops and maintains strategic partnerships",
        category_id=5,
    ),
    "business_development": RoleBase(
        id=20,
        name="Business Development Manager",
        description="Identifies new business opportunities and markets",
        category_id=5,
    ),
    "customer_success_manager": RoleBase(
        id=21,
        name="Customer Success Manager",
        description="Ensures client satisfaction and adoption of AI solutions",
        category_id=5,
    ),
    # HR
    "technical_recruiter": RoleBase(
        id=22,
        name="Technical Recruiter",
        description="Recruits top AI and engineering talent",
        category_id=6,
    ),
    "learning_development_manager": RoleBase(
        id=23,
        name="Learning & Development Manager",
        description="Develops training programs for AI researchers and engineers",
        category_id=6,
    ),
    "talent_operations_manager": RoleBase(
        id=24,
        name="Talent Operations Manager",
        description="Manages employee experience and HR operations",
        category_id=6,
    ),
    "diversity_inclusion_specialist": RoleBase(
        id=25,
        name="Diversity & Inclusion Specialist",
        description="Promotes diverse and inclusive workplace culture",
        category_id=6,
    ),
}


class StatusMessage(BaseModel):
    """Status message model for the API."""

    status: bool
    message: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"status": True, "message": "Success"}},
    )


class UserBase(SQLModel):
    """Users table"""

    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_admin: bool = Field(default=False)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "password": "password",
                "is_admin": False,
            }
        }
    )


class User(UserBase, UUIDModel, table=True):
    """User model"""

    __tablename__ = "users"


class UserRead(UUIDModel):
    """User read model"""

    email: str
    is_admin: bool

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "test@example.com",
                "is_admin": False,
            }
        }
    )


class UserCreate(UserBase):
    """User create model"""

    email: str
    password: str

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "password": "password",
            }
        }
    )


class UserPatch(BaseModel):
    """User patch model"""

    email: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
            }
        }
    )


class UserAdminPatch(BaseModel):
    """User admin patch model"""

    email: str
    is_admin: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "is_admin": True,
            }
        }
    )


class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        }
    )


class TokenData(BaseModel):
    """TokenData model"""

    username: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "test@example.com",
            }
        }
    )


class Version(BaseModel):
    """Version model for the API."""

    version: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"version": "0.1.0"}},
    )


class Investor(BaseModel):
    """Investor model"""

    player: Player
    part: float


class Investment(BaseModel):
    """Investment model"""

    lab: Lab
    part: float


class PlayerDataResponse(BaseModel):
    """Response model for retrieve-player-data"""

    id: str
    name: str
    avatar: str
    funds: float
    labs: list[Lab]
    investments: list[Investment]


class LabDataResponse(BaseModel):
    """Response model for retrieve-lab-data"""

    id: str
    name: str
    location: LocationEnum
    valuation: float
    income: float
    tech_tree_id: str
    player_id: str
    employees: list[Employee]
    models: list[AIModel]
    investors: list[Investor]
    player: Player | None


class AIModelDataResponse(BaseModel):
    """Response model for create-model"""

    id: str
    name: str
    ai_model_type_id: int
    tech_tree_id: str
    lab_id: str


class FundsUpdate(BaseModel):
    """Funds update model"""

    funds: float
    update_type: Literal["increment", "decrement"]
