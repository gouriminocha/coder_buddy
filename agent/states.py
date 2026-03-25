from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# 📁 File structure
class File(BaseModel):
    path: str = Field(description="The path to the file")
    purpose: str = Field(description="Purpose of the file")


# 🧠 Planner output
class Plan(BaseModel):
    name: str
    description: str
    techstack: str
    features: list[str]
    files: list[File]


# 🧠 Architect output
class ImplementationTask(BaseModel):
    filepath: str
    task_description: str


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask]
    model_config = ConfigDict(extra="allow")


# 🧠 Coder state (FINAL VERSION ✅)
class CoderState(BaseModel):
    task_plan: TaskPlan
    current_step_idx: int = 0
    current_file_content: Optional[str] = None
    project_root: Optional[str] = None

    # 🔥 Logs added
    logs: list[str] = Field(default_factory=list)