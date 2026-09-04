from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PenaltyStructure(BaseModel):
    first_offense_fine: str
    subsequent_offense: str
    imprisonment_term: Optional[str] = None
    compoundable: bool = True


class StatutoryThreshold(BaseModel):
    criterion: str
    applicability_limit: str
    enforcing_authority: str


class StatutorySection(BaseModel):
    code_id: str  # wages_2019, ir_2020, ss_2020, oshwc_2020
    code_name: str
    chapter_number: str
    chapter_title: str
    section_number: str
    title: str
    statutory_text: str
    keywords: List[str]
    thresholds: Optional[StatutoryThreshold] = None
    penalties: Optional[PenaltyStructure] = None
    mandatory_registers: List[str] = Field(default_factory=list)
    citation: str  # e.g., "Code on Wages, 2019, Sec. 14"


class LabourCodeSummary(BaseModel):
    code_id: str
    title: str
    act_number: str
    enactment_year: int
    total_chapters: int
    total_sections: int
    primary_objective: str
    enforcing_spheres: List[str]
    repealed_acts: List[str]
    mandatory_registers: List[str]


class KnowledgeQueryResult(BaseModel):
    query: str
    total_matches: int
    results: List[StatutorySection]
