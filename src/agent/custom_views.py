# -*- coding: utf-8 -*-
# @Time    : 2025/1/2
# @Author  : wenshao
# @ProjectName: browser-use-webui
# @FileName: custom_views.py

from dataclasses import dataclass
from typing import Type
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model
from browser_use.controller.registry.views import ActionModel


@dataclass
class CustomAgentStepInfo:
    step_number: int
    max_steps: int
    memory: str



class CustomAgentBrain(BaseModel):
    """Current state of the agent"""

    prev_action_evaluation: str
    memory: str
    progress: str
    thought: str
    summary: str
    action: str


class CustomAgentOutput(BaseModel):
    """Output model for agent

    @dev note: this model is extended with custom actions in AgentService. You can also use some fields that are not in this model as provided by the linter, as long as they are registered in the DynamicActions model.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_state: CustomAgentBrain
    action: list[ActionModel]

    @staticmethod
    def type_with_custom_actions(custom_actions: Type[ActionModel]) -> Type['CustomAgentOutput']:
        """Extend actions with custom actions"""
        return create_model(
            'AgentOutput',
            __base__=CustomAgentOutput,
            action=(list[custom_actions], Field(...)),  # Properly annotated field with no default
            __module__=CustomAgentOutput.__module__,
        )