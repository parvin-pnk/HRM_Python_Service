from pydantic import BaseModel
from typing import Optional

class EmployeeInput(BaseModel):
    employee_id: int
    attendance_issues: int
    overtime_load: float
    performance_history: float
    leave_patterns: float
    salary_gap: float
    manager_rating: Optional[str] = "A"
    department: str = "Sales"
