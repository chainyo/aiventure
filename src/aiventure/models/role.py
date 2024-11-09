"""Role model."""

from enum import Enum

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


class RoleCategoryBase(SQLModel):
    """Role category model."""

    id: int = Field(primary_key=True)
    name: str
    hex_color: str

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {"id": 1, "name": "Research", "hex_color": "#90dbf4"}
        }
    )


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


class RoleCategoryEnum(str, Enum):
    """Role category enum."""

    RESEARCH = "research"
    ENGINEERING = "engineering"
    OPERATIONS = "operations"
    LEADERSHIP = "leadership"
    SALES = "sales"
    HR = "hr"

    @property
    def item(self) -> RoleCategoryBase:
        """Get the category."""
        return ROLE_CATEGORY_MAPPING[self.value]


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


class RoleEnum(str, Enum):
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
    def item(self) -> RoleBase:
        """Get the role object for this enum value."""
        return ROLE_MAPPING[self.value]
