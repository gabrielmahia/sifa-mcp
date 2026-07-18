# ⭐ sifa-mcp — Portable Reputation & Skills Passport MCP Server
<!-- mcp-name: io.github.gabrielmahia/sifa-mcp -->

[![sifa-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/sifa-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/sifa-mcp)
[![smithery badge](https://smithery.ai/badge/@gabrielmahia/sifa-mcp)](https://smithery.ai/server/@gabrielmahia/sifa-mcp)


---
**Compatible with `claude-sonnet-5`** (released 2026-06-30) — Anthropic's most agentic
Sonnet yet. Runs multi-step tool chains end-to-end without stopping short.
Install: `pip install sifa-mcp` · Use with any MCP client.

---


*Sifa* = reputation/praise in Swahili.

Informal-sector workers build reputation with one buyer, one platform, one neighborhood at a time — and lose it the moment they switch. Nothing makes that reputation portable or agent-queryable.

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

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
Connect it to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) —
the coordination event bus that routes signals between domains automatically.

```bash
pip install africa-coord-bus
```

All 32 servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)
Live demo: [coord-cascade-demo](https://github.com/gabrielmahia/coord-cascade-demo)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — 33 MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
