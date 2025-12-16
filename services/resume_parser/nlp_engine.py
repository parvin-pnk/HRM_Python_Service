import re
from typing import List, Dict, Any

from services.resume_parser.constants import (
    SKILLS_DB,
    DEGREE_KEYWORDS,
    COMPANY_NOISE_WORDS,
    ROLE_PATTERNS,
)

import services.resume_parser.model_loader as model_loader



def split_sections(text: str) -> Dict[str, str]:
    sections = {
        "header": "",
        "summary": "",
        "experience": "",
        "education": "",
        "skills": "",
        "certification": "",
        "other": "",
    }

    pattern = r"(SUMMARY|EXPERIENCE|EDUCATION|SKILLS|CERTIFICATION|CERTIFICATIONS|KEY ACHIEVEMENTS)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    if not parts:
        sections["header"] = text
        return sections

    sections["header"] = parts[0]

    for i in range(1, len(parts), 2):
        heading = parts[i].strip().upper()
        content = parts[i + 1] if i + 1 < len(parts) else ""

        if heading == "SUMMARY":
            sections["summary"] += content
        elif heading == "EXPERIENCE":
            sections["experience"] += content
        elif heading == "EDUCATION":
            sections["education"] += content
        elif heading == "SKILLS":
            sections["skills"] += content
        elif heading in ("CERTIFICATION", "CERTIFICATIONS"):
            sections["certification"] += content
        else:
            sections["other"] += content

    return sections




def nlp_and_regex_parser(text: str) -> Dict[str, Any]:
    if model_loader.nlp is None:
        raise RuntimeError("SpaCy NLP model is not loaded")

    sections = split_sections(text)

    header_text = sections["header"]
    summary_text = sections["summary"]
    experience_text = sections["experience"]
    education_text = sections["education"]
    skills_text = sections["skills"]

    data: Dict[str, Any] = {}

   
    name = "N/A"

    if header_text.strip():
        header_doc = model_loader.nlp(header_text[:300])
        persons = [ent.text.strip() for ent in header_doc.ents if ent.label_ == "PERSON"]
        if persons:
            raw_name = persons[0]
            name = " ".join(
                p.upper() if len(p) == 1 else p.capitalize()
                for p in raw_name.split()
            )

    if name == "N/A":
        full_doc = model_loader.nlp(text[:600])
        persons = [ent.text.strip() for ent in full_doc.ents if ent.label_ == "PERSON"]
        if persons:
            raw_name = persons[0]
            name = " ".join(
                p.upper() if len(p) == 1 else p.capitalize()
                for p in raw_name.split()
            )

    data["name"] = name

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text
    )
    data["email"] = email_match.group(0) if email_match else "N/A"

    
    phone_match = re.search(r"(\+?\d[\d \-]{8,15}\d)", text)
    data["phone"] = phone_match.group(0).strip() if phone_match else "N/A"

    lower_text = (skills_text or text).lower()
    found_skills = {
        skill for skill in SKILLS_DB if skill.lower() in lower_text
    }
    data["skills"] = sorted(found_skills)

    
    companies: List[str] = []

    source_text = experience_text if experience_text.strip() else text
    doc = model_loader.nlp(source_text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            company = ent.text.strip()
            if not company:
                continue
            if any(noise in company.lower() for noise in COMPANY_NOISE_WORDS):
                continue
            companies.append(company)

    data["companies_worked"] = sorted(set(companies))

    
    job_titles: List[str] = []
    combined_text = (experience_text + " " + summary_text).lower()

    for role in ROLE_PATTERNS:
        if role in combined_text:
            job_titles.append(" ".join(w.capitalize() for w in role.split()))

    data["job_titles"] = sorted(set(job_titles))

   
    education_lines: List[str] = []

    if education_text.strip():
        for line in education_text.splitlines():
            clean_line = " ".join(line.split())
            if any(deg.lower() in clean_line.lower() for deg in DEGREE_KEYWORDS):
                if 0 < len(clean_line) < 220:
                    education_lines.append(clean_line)

    data["education"] = sorted(set(education_lines))

    
   
    experience_years = 0.0
    date_pattern = re.compile(
        r"(\d{2})/(\d{4})\s*[-–]\s*(\d{2})/(\d{4})"
    )

    for line in experience_text.splitlines():
        if re.search(r"intern(ship)?", line, re.IGNORECASE):
            continue

        for match in date_pattern.finditer(line):
            sm, sy, em, ey = match.groups()
            try:
                sy, ey = int(sy), int(ey)
                sm, em = int(sm), int(em)

                start = sy + (sm - 1) / 12.0
                end = ey + (em - 1) / 12.0
                experience_years += max(0.0, end - start)
            except ValueError:
                continue

    data["total_experience_years"] = round(experience_years, 2)

   
    summary_clean = " ".join(summary_text.split())
    if summary_clean:
        data["parsed_summary"] = summary_clean
    else:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        data["parsed_summary"] = " ".join(lines[:3]) if lines else ""

    return data
