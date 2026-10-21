"""
Layer 3: Least-Privilege Tools (Saltzer & Schroeder [17]).
Each HR task receives only the minimum toolset required:
  - 'rank_resumes' task -> ['read_resume', 'rank_candidates'] (no 'send_email' access)
  - 'send_shortlist' task -> ['send_email']
"""

TASK_TOOL_POLICIES = {
    "rank_resumes": {"read_resume", "rank_candidates"},
    "send_shortlist": {"send_email"},
}


class LeastPrivilegeToolManager:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def get_allowed_tools(self, task_name: str) -> set[str]:
        if not self.enabled:
            return {"read_resume", "rank_candidates", "send_email"}
        return TASK_TOOL_POLICIES.get(task_name, {"read_resume"})

    def check_tool_call(self, task_name: str, tool_name: str) -> tuple[bool, str]:
        allowed = self.get_allowed_tools(task_name)
        if tool_name in allowed:
            return True, f"Tool '{tool_name}' permitted for task '{task_name}'."
        return (
            False,
            f"Layer 3 Blocked: Tool '{tool_name}' is not in the allowed toolset {sorted(list(allowed))} for task '{task_name}'.",
        )
