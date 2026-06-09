#!/usr/bin/env python3
# sifa-mcp — Portable Reputation & Skills Passport MCP Server
# © 2026 Gabriel Mahia / AI Kung Fu LLC — MIT License
#
# Sifa = reputation/praise in Swahili
#
# The structural problem: Trust in East Africa is tribal/family-based.
# A skilled mechanic in Mombasa cannot take her reputation to Nairobi.
# A qualified mason cannot prove his work history to a new contractor.
# Economic mobility is throttled by reputation portability.
#
# Western parallel: Yelp, Uber ratings, LinkedIn endorsements, Angie's List,
#   Better Business Bureau, professional license registries.
# Research: IFC "The Value of Reputation" (2020), ILO Skills Recognition (2023)
#           "Mobile-Based Reputation Systems" (World Bank, 2021)
#
# TRUST INTEGRITY: All profiles are DEMO/synthetic. No real identity verification.
# A production implementation requires integration with Huduma Number, NIIMS,
# or other Kenya DPI (Digital Public Infrastructure) identity systems.
# =============================================================================

from __future__ import annotations
import json
import datetime
import hashlib
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP(
    name="sifa-mcp",
    instructions="""Portable reputation and skills passport MCP server for East Africa.
    Provides tools to create worker profiles, record service history, generate
    references, and calculate trust scores — enabling economic mobility for
    informal workers.
    
    IMPORTANT: All profiles are DEMO/synthetic. No real identity verification.
    A production deployment requires integration with Kenya's Huduma Number
    or NIIMS identity infrastructure.
    """,
)

# In-memory profile store (demo — production uses persistent DB)
_PROFILES: dict[str, dict] = {}

SKILL_CATEGORIES = {
    "construction": ["masonry", "plumbing", "electrical", "carpentry", "painting",
                     "roofing", "tiling", "welding", "concrete_work"],
    "transport":    ["boda_boda_riding", "tuk_tuk_driving", "truck_driving",
                     "taxi_driving", "logistics_coordination"],
    "domestic":     ["house_cleaning", "childcare", "cooking", "laundry",
                     "elder_care", "gardening"],
    "tech":         ["phone_repair", "computer_repair", "solar_installation",
                     "appliance_repair", "cctv_installation"],
    "agriculture":  ["crop_farming", "animal_husbandry", "irrigation",
                     "pest_control", "greenhouse_management"],
    "food":         ["catering", "baking", "butchery", "food_processing",
                     "market_vending"],
    "health":       ["community_health_worker", "pharmacy_assistant",
                     "lab_technician", "first_aid"],
    "education":    ["primary_tutoring", "secondary_tutoring", "vocational_training",
                     "adult_literacy"],
    "business":     ["bookkeeping", "inventory_management", "sales",
                     "customer_service", "procurement"],
}

def _profile_id(name: str, phone: str) -> str:
    """Generate a deterministic, non-reversible profile ID."""
    raw = f"{name.lower().strip()}:{phone.strip()}"
    return "SFA-" + hashlib.sha256(raw.encode()).hexdigest()[:12].upper()

def _trust_score(profile: dict) -> dict:
    """Calculate trust score from profile signals."""
    jobs = profile.get("service_records", [])
    verified = sum(1 for j in jobs if j.get("verified"))
    avg_rating = (sum(j.get("rating", 0) for j in jobs) / len(jobs)) if jobs else 0
    tenure_months = profile.get("tenure_months", 0)

    # Score components (0-100)
    volume_score  = min(30, len(jobs) * 3)          # Up to 30 pts for job count
    quality_score = int(avg_rating / 5 * 35)        # Up to 35 pts for avg rating
    verified_score = min(20, verified * 5)           # Up to 20 pts for verified jobs
    tenure_score  = min(15, tenure_months // 3)      # Up to 15 pts for tenure

    total = volume_score + quality_score + verified_score + tenure_score

    tier = ("TRUSTED" if total >= 70 else
            "ESTABLISHED" if total >= 45 else
            "BUILDING" if total >= 20 else "NEW")

    return {
        "total_score": total,
        "tier": tier,
        "breakdown": {
            "job_volume": volume_score,
            "average_quality": quality_score,
            "verified_records": verified_score,
            "tenure": tenure_score,
        },
        "tier_description": {
            "TRUSTED":     "Strong, verifiable history. High confidence for new engagements.",
            "ESTABLISHED": "Good track record. Suitable for most engagements.",
            "BUILDING":    "Growing history. Recommend starting with small jobs.",
            "NEW":         "Limited history. Ask for references and start with a trial job.",
        }[tier],
    }


@mcp.tool(
    description=(
        "Create a portable worker reputation profile. "
        "Western parallel: LinkedIn profile creation, Angie's List contractor profile. "
        "This is the 'economic passport' that travels with the worker. "
        "DEMO — no real identity verification in this prototype."
    ),
    annotations={"readOnlyHint": False, "destructiveHint": False},
)
def create_worker_profile(
    full_name: Annotated[str, "Worker's full name"],
    phone: Annotated[str, "M-PESA phone number (used as identity anchor, not stored in plain text)"],
    primary_skill: Annotated[str, "Primary skill category (see skill_categories tool)"],
    sub_skills: Annotated[str, "Comma-separated list of specific skills (e.g., 'masonry,tiling,plastering')"],
    location: Annotated[str, "Current base location (town or county)"],
    years_experience: Annotated[int, "Years of experience in primary skill (0-40)"],
    languages: Annotated[str, "Languages spoken (e.g., 'Swahili,English,Kikuyu')"] = "Swahili",
) -> dict:
    profile_id = _profile_id(full_name, phone)

    profile = {
        "profile_id": profile_id,
        "name": full_name,
        "phone_masked": phone[-4:].rjust(len(phone), "*"),
        "primary_skill": primary_skill.lower(),
        "sub_skills": [s.strip() for s in sub_skills.split(",")],
        "location": location,
        "years_experience": years_experience,
        "languages": [l.strip() for l in languages.split(",")],
        "created": datetime.date.today().isoformat(),
        "service_records": [],
        "tenure_months": max(0, years_experience * 12),
    }

    _PROFILES[profile_id] = profile

    return {
        "status": "OK",
        "profile_id": profile_id,
        "profile_summary": {
            "name": full_name,
            "primary_skill": primary_skill,
            "location": location,
            "experience_years": years_experience,
            "trust_score": _trust_score(profile),
        },
        "next_steps": [
            "Add service records with add_service_record to build trust score",
            "Share your profile_id with clients so they can verify your history",
            "After 5+ verified records, generate a reference with generate_reference",
        ],
        "share_text": (
            f"My Sifa Profile: {profile_id} · {primary_skill} · {years_experience}yr exp · {location}"
        ),
        "note": "DEMO — No real identity verification. Production requires Huduma Number integration.",
        "source": "sifa-mcp. Reference: IFC 'The Value of Reputation' (2020).",
    }


@mcp.tool(
    description=(
        "Add a completed service record to a worker's profile. "
        "Western parallel: Uber trip completion, Angie's List job review, "
        "Upwork completed contract. Each record builds the reputation score. "
        "DEMO — client verification is simulated."
    ),
    annotations={"readOnlyHint": False, "destructiveHint": False},
)
def add_service_record(
    profile_id: Annotated[str, "Worker profile ID (SFA-XXXXXXXXXXXX format)"],
    client_name: Annotated[str, "Client name (or business name)"],
    client_phone: Annotated[str, "Client M-PESA number (for verification anchor)"],
    service_type: Annotated[str, "Type of service performed"],
    duration_days: Annotated[int, "Duration of the job in days"],
    payment_kes: Annotated[int, "Amount paid in KES (0 if unpaid/pro bono)"],
    client_rating: Annotated[int, "Client rating 1-5 stars"],
    notes: Annotated[str, "Brief description of work done"] = "",
) -> dict:
    if profile_id not in _PROFILES:
        return {"status": "NOT_FOUND",
                "message": f"Profile {profile_id} not found. Create it first with create_worker_profile."}

    if not 1 <= client_rating <= 5:
        return {"status": "ERROR", "message": "Rating must be 1-5"}

    record = {
        "record_id": f"REC-{datetime.date.today().isoformat()}-{len(_PROFILES[profile_id]['service_records'])+1:03d}",
        "date": datetime.date.today().isoformat(),
        "service": service_type,
        "client": client_name,
        "client_phone_masked": client_phone[-4:].rjust(len(client_phone), "*"),
        "duration_days": duration_days,
        "payment_kes": payment_kes,
        "rating": client_rating,
        "notes": notes,
        "verified": True,  # In demo, all client-submitted records are marked verified
                           # Production: requires OTP confirmation from client phone
    }

    _PROFILES[profile_id]["service_records"].append(record)
    new_score = _trust_score(_PROFILES[profile_id])

    return {
        "status": "OK",
        "record_id": record["record_id"],
        "profile_id": profile_id,
        "new_trust_score": new_score,
        "total_records": len(_PROFILES[profile_id]["service_records"]),
        "verification_note": (
            "DEMO: Record marked verified. In production, client receives an OTP "
            "to confirm the job completion — prevents workers from fabricating history."
        ),
        "source": "sifa-mcp.",
    }


@mcp.tool(
    description=(
        "Retrieve a worker's full reputation profile including trust score. "
        "Western parallel: Checking a contractor's BBB rating or Upwork JSS. "
        "DEMO data."
    ),
    annotations={"readOnlyHint": True},
)
def get_reputation_profile(
    profile_id: Annotated[str, "Worker profile ID to retrieve"],
    requester_context: Annotated[str, "Who is requesting (employer, SACCO, bank, NGO)"] = "employer",
) -> dict:
    if profile_id not in _PROFILES:
        return {"status": "NOT_FOUND",
                "message": "Profile not found. Worker may not have registered yet."}

    profile = _PROFILES[profile_id]
    score = _trust_score(profile)
    records = profile.get("service_records", [])

    return {
        "status": "OK",
        "profile": {
            "profile_id": profile_id,
            "name": profile["name"],
            "primary_skill": profile["primary_skill"],
            "skills": profile["sub_skills"],
            "location": profile["location"],
            "experience_years": profile["years_experience"],
            "languages": profile["languages"],
            "member_since": profile["created"],
        },
        "trust_score": score,
        "service_history": {
            "total_jobs": len(records),
            "verified_jobs": sum(1 for r in records if r.get("verified")),
            "average_rating": round(sum(r["rating"] for r in records) / len(records), 1) if records else 0,
            "total_earned_kes": sum(r.get("payment_kes", 0) for r in records),
            "recent_jobs": records[-3:] if records else [],
        },
        "recommendation_for_requester": {
            "employer": f"{'Recommended' if score['tier'] in ('TRUSTED','ESTABLISHED') else 'Start with a trial job'}",
            "SACCO":    f"{'Eligible for member loan' if score['tier'] == 'TRUSTED' else 'Insufficient history for loan'}",
            "bank":     f"{'Consider for microfinance product' if score['total_score'] >= 60 else 'Insufficient reputation history'}",
            "NGO":      f"{'Strong candidate for programme participation' if score['total_score'] >= 30 else 'Emerging candidate'}",
        }.get(requester_context, "Review profile and trust score manually."),
        "note": "DEMO — Synthetic profile. Production requires Huduma Number verification.",
        "source": "sifa-mcp.",
    }


@mcp.tool(
    description=(
        "Generate a structured professional reference letter for a worker. "
        "Western parallel: LinkedIn recommendation, employer reference letter. "
        "Outputs a formatted reference that can be printed, shared as PDF, "
        "or verified by QR code in production. DEMO."
    ),
    annotations={"readOnlyHint": True},
)
def generate_reference(
    profile_id: Annotated[str, "Worker profile ID"],
    reference_purpose: Annotated[str, "Purpose: job_application, loan_application, tenancy, SACCO_membership, NGO_programme"] = "job_application",
) -> dict:
    if profile_id not in _PROFILES:
        return {"status": "NOT_FOUND", "message": "Profile not found."}

    profile = _PROFILES[profile_id]
    score = _trust_score(profile)
    records = profile.get("service_records", [])
    today = datetime.date.today().strftime("%B %d, %Y")
    avg_rating = round(sum(r["rating"] for r in records) / len(records), 1) if records else 0
    total_earned = sum(r.get("payment_kes", 0) for r in records)

    reference_text = f"""SIFA REPUTATION REFERENCE
Issued: {today}
Profile ID: {profile_id}
Verification: sifa-mcp.africastack.io/{profile_id} [DEMO]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TO WHOM IT MAY CONCERN

This reference is issued on behalf of {profile["name"]}, whose portable
reputation profile ({profile_id}) has been verified by the Sifa network.

PROFESSIONAL SUMMARY
Name:           {profile["name"]}
Primary Skill:  {profile["primary_skill"].title()}
Skills:         {", ".join(profile["sub_skills"])}
Experience:     {profile["years_experience"]} years
Location:       {profile["location"]}
Languages:      {", ".join(profile["languages"])}

REPUTATION SUMMARY
Trust Tier:     {score["tier"]}
Trust Score:    {score["total_score"]}/100
Completed Jobs: {len(records)}
Verified Jobs:  {sum(1 for r in records if r.get("verified"))}
Average Rating: {avg_rating}/5.0 stars
Total Earned:   KES {total_earned:,}

ASSESSMENT
{profile["name"]} has demonstrated {score["tier_description"].lower()}

{"This reference is provided for: " + reference_purpose.replace("_", " ").title() + "."}

VERIFICATION
This profile can be independently verified at the QR code above or by
contacting the Sifa network at sifa-mcp.africastack.io [DEMO].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DEMO DOCUMENT — Synthetic for educational purposes.
Production version requires Huduma Number integration.
sifa-mcp · © 2026 Gabriel Mahia / AI Kung Fu LLC · MIT License
"""

    return {
        "status": "OK",
        "profile_id": profile_id,
        "reference_purpose": reference_purpose,
        "reference_text": reference_text,
        "trust_score": score,
        "note": "DEMO — Reference is illustrative only. Production version uses digital signatures and Huduma Number verification.",
        "source": "sifa-mcp. Reference: ILO Skills Recognition Framework (2023).",
    }


@mcp.tool(
    description=(
        "List all skill categories and subcategories available in the Sifa system. "
        "Use this to see valid skill values for create_worker_profile."
    ),
    annotations={"readOnlyHint": True},
)
def list_skill_categories() -> dict:
    return {
        "status": "OK",
        "categories": SKILL_CATEGORIES,
        "total_skills": sum(len(v) for v in SKILL_CATEGORIES.values()),
        "usage": "Pass the category name as primary_skill and specific skills as sub_skills in create_worker_profile",
        "source": "sifa-mcp. Categories aligned with Kenya NITA (National Industrial Training Authority) trade classifications.",
    }


@mcp.tool(
    description=(
        "Compare the reputation scores of multiple workers for a specific job. "
        "Western parallel: Contractor comparison on Thumbtack, Bark, or Houzz. "
        "DEMO data."
    ),
    annotations={"readOnlyHint": True},
)
def compare_workers(
    profile_ids: Annotated[str, "Comma-separated list of profile IDs to compare"],
    required_skill: Annotated[str, "Skill required for the job"] = "",
) -> dict:
    ids = [p.strip() for p in profile_ids.split(",")]
    results = []
    for pid in ids:
        if pid in _PROFILES:
            p = _PROFILES[pid]
            s = _trust_score(p)
            results.append({
                "profile_id": pid,
                "name": p["name"],
                "primary_skill": p["primary_skill"],
                "location": p["location"],
                "trust_score": s["total_score"],
                "trust_tier": s["tier"],
                "total_jobs": len(p.get("service_records", [])),
                "experience_years": p["years_experience"],
                "skill_match": not required_skill or required_skill.lower() in [
                    sk.lower() for sk in p.get("sub_skills", [])] or
                    required_skill.lower() == p["primary_skill"].lower(),
            })
        else:
            results.append({"profile_id": pid, "status": "NOT_FOUND"})

    results_sorted = sorted(
        [r for r in results if "trust_score" in r],
        key=lambda x: (x.get("skill_match", False), x.get("trust_score", 0)),
        reverse=True
    )

    return {
        "status": "OK",
        "required_skill": required_skill or "any",
        "ranked_workers": results_sorted,
        "recommendation": results_sorted[0] if results_sorted else None,
        "note": "DEMO — Ranking based on synthetic trust scores. Production uses verified job history.",
        "source": "sifa-mcp.",
    }


def main():
    mcp.run()

if __name__ == "__main__":
    main()
