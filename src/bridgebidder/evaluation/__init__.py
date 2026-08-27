from .registry import EvalContext, evaluate, get_evaluator, register_evaluator, REGISTRY
from . import evaluators  # noqa: F401  (populates the registry on import)

__all__ = ["EvalContext", "evaluate", "get_evaluator", "register_evaluator", "REGISTRY"]
