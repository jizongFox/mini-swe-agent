"""Shared agent utilities for benchmark runners."""

from typing import Any

from minisweagent.agents.default import DefaultAgent
from minisweagent.run.benchmarks.utils.batch_progress import RunBatchProgressManager


class ProgressTrackingAgent(DefaultAgent):
    """Agent that reports per-step progress via :class:`RunBatchProgressManager`."""

    def __init__(
        self, *args: Any, progress_manager: RunBatchProgressManager, instance_id: str = "", **kwargs: Any
    ) -> None:
        """Forward agent arguments and attach the progress manager and instance identifier."""
        super().__init__(*args, **kwargs)
        self.progress_manager = progress_manager
        self.instance_id = instance_id

    def step(self) -> dict:
        """Update the displayed step and cost before returning the underlying step's observations."""
        self.progress_manager.update_instance_status(self.instance_id, f"Step {self.n_calls + 1:3d} (${self.cost:.2f})")
        return super().step()
