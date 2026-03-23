from app.models.schemas import DecisionAnalysis, Task


class DecisionEngine:
    def evaluate(self, mission: str, tasks: list[Task]) -> DecisionAnalysis:
        budget_sensitive = any("budget" in task.title.lower() for task in tasks)
        return DecisionAnalysis(
            recommendation=(
                "Start with a province-prioritized launch plan, then automate outreach and analytics in waves."
            ),
            pros=[
                "Fast alignment between campaign strategy, execution, and analytics.",
                "Reusable workflow templates for Nepal telecom operations.",
                "Lower coordination overhead through autonomous delegation.",
            ],
            cons=[
                "Requires approval workflow design for regulated or high-volume actions.",
                "Integration maintenance increases with each external business system.",
            ],
            roi_estimate=(
                "High ROI when used for repeatable campaigns, executive planning, and internal tooling."
                if budget_sensitive
                else "Strong ROI through labor savings, faster launches, and reduced context switching."
            ),
            risk_analysis=[
                "Need clear guardrails before sending telecom campaign communications.",
                "Market assumptions must be localized for Nepal provinces and channel economics.",
                "Automation failures should be retried with audit logs and alerting.",
            ],
        )
