from dataclasses import dataclass
from typing import List

@dataclass
class CheckResult:
    item_name: str
    passed: bool
    score_earned: int
    max_score: int
    feedback: str = ""

@dataclass
class SectionResult:
    section_name: str
    checks: List[CheckResult]
    
    @property
    def total_score(self):
        return sum(check.score_earned for check in self.checks)

    @property
    def max_score(self):
        return sum(check.max_score for check in self.checks)

@dataclass
class GradingReport:
    student_id: str
    student_name: str
    sections: List[SectionResult]
    
    @property
    def total_score(self):
        return sum(section.total_score for section in self.sections)
        
    @property
    def max_score(self):
        return sum(section.max_score for section in self.sections)
