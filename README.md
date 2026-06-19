# ⭐ sifa-mcp — Portable Reputation & Skills Passport MCP Server

[![sifa-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/sifa-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/sifa-mcp)


*Sifa* = reputation/praise in Swahili.

**First portable reputation MCP server for East Africa.**

## The Structural Problem

In mature economies, reputation travels: Uber driver ratings, Yelp reviews, LinkedIn endorsements, contractor licence registries. A skilled plumber in Chicago can prove her track record to any homeowner in Los Angeles.

In Kenya, trust is tribal and local. A qualified mason in Mombasa cannot take her reputation to Nairobi. Economic mobility is throttled by the non-portability of professional identity.

**Reputation portability is a coordination technology.** Without it, hiring defaults to personal networks, which excludes the most talented people outside existing networks.

## Tools

| Tool | What it does |
|------|-------------|
| `create_worker_profile` | Create a portable reputation profile with skills, location, experience |
| `add_service_record` | Log a completed job with client details and rating |
| `get_reputation_profile` | Retrieve full profile with trust score for any requester type |
| `generate_reference` | Generate a formatted professional reference letter |
| `list_skill_categories` | Browse all NITA-aligned skill categories |
| `compare_workers` | Rank multiple workers by trust score and skill match |

## Trust Score

Scored 0–100 across four signals:
- **Job volume** (up to 30 pts) — number of completed jobs
- **Average quality** (up to 35 pts) — client star ratings
- **Verified records** (up to 20 pts) — client-OTP-confirmed completions
- **Tenure** (up to 15 pts) — years of documented history

Tiers: `NEW` → `BUILDING` → `ESTABLISHED` → `TRUSTED`

## Quick Start

```bash
pip install sifa-mcp       # coming soon to PyPI
sifa-mcp                   # starts on stdio
```

## Example

```python
# Create a mason's portable profile
create_worker_profile(
    full_name="James Mwangi",
    phone="0712345678",
    primary_skill="construction",
    sub_skills="masonry,tiling,plastering",
    location="Nairobi",
    years_experience=8
)
# → SFA-A3F2B19C4E1D

# Log a completed job
add_service_record(
    profile_id="SFA-A3F2B19C4E1D",
    client_name="ABC Contractors",
    client_phone="0722000000",
    service_type="Kitchen tiling",
    duration_days=5,
    payment_kes=15000,
    client_rating=5
)

# Generate a reference for a new job application
generate_reference(profile_id="SFA-A3F2B19C4E1D", reference_purpose="job_application")
```

## Research Basis

- IFC "The Value of Reputation" (2020)
- ILO Skills Recognition Framework (2023)
- World Bank "Mobile-Based Reputation Systems" (2021)
- Kenya NITA (National Industrial Training Authority) trade classifications

⚠️ DEMO — Production requires Huduma Number / NIIMS integration for identity verification.

---
*© 2026 Gabriel Mahia / AI Kung Fu LLC · MIT License*
