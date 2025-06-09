from .orchestrator import OrchestratorAgent, orchestrator
from .substitute_agent import SubstituteAgent, substitute_agent
from .combine_agent import CombineAgent, combine_agent
from .adapt_agent import AdaptAgent, adapt_agent
from .modify_agent import ModifyAgent, modify_agent
from .other_uses_agent import OtherUsesAgent, other_uses_agent
from .eliminate_agent import EliminateAgent, eliminate_agent
from .reverse_agent import ReverseAgent, reverse_agent

__all__ = [
    "OrchestratorAgent", "orchestrator",
    "SubstituteAgent", "substitute_agent",
    "CombineAgent", "combine_agent", 
    "AdaptAgent", "adapt_agent",
    "ModifyAgent", "modify_agent",
    "OtherUsesAgent", "other_uses_agent",
    "EliminateAgent", "eliminate_agent",
    "ReverseAgent", "reverse_agent"
]