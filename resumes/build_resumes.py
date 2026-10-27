"""Build every resume version from one source of truth.

  python3 build_resumes.py        # writes html/ then renders PDFs into UAE/, EU/ and India/ via render.js

Edit facts here once; every version picks them up. Bullets are plain text with **bold** allowed.
"""
import html
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

CONTACT_FILE = HERE / "contact.json"  # gitignored: ["City, Country", "+phone", "email", "linkedin.com/in/..."]
CONTACT = json.loads(CONTACT_FILE.read_text()) if CONTACT_FILE.exists() else [
    "Dubai, UAE", "email on request", "linkedin.com/in/mariyam-pangarkar", "github.com/mariyampangarkar19"]
STATUS = {
    "UAE": "Family-sponsored UAE residence visa · Available immediately",
    "EU": "Open to relocation · Available immediately",
    "India": "Relocating to India · Available immediately",
}
EDUCATION = ("Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT)",
             "B.Tech, Information and Communication Technology", "2023")  # third field: graduation year
PROJECTS = []  # e.g. [("Job-match agent", "github.com/...", "One line on what it does and the stack.")]

JOBS = {
    "sharematch": ("ShareMatch", "Technical Analyst", "Nov 2025 – Jul 2026"),
    "quicko": ("Quicko (by Zerodha)", "Full Stack Developer", "Oct 2024 – Aug 2025"),
    "rising": ("Rising Financials", "Software Developer", "May 2024 – Sep 2024"),
    "monocept": ("Monocept Consulting", "Software Developer", "Jan 2023 – Apr 2024"),
}

# Reusable bullets so the same achievement reads the same way everywhere.
B = {
    "migration": "Migrated **100K+ customer accounts, ledger balances and calendar records** from DynamoDB to OpenSearch with Python ETL pipelines, with **zero data loss**.",
    "llm_bot": "Built and deployed an **LLM support assistant** (Gemini, LangChain, AWS) that automated repetitive customer-support workflows.",
    "four_features": "Shipped **4 end-to-end features** for Quicko Pro, owning frontend, backend, integration and testing through to production.",
    "lambda": "Built Node.js services and REST APIs on **AWS Lambda, Step Functions and API Gateway** for production financial workflows.",
    "sql40": "Optimised SQL pipelines across financial datasets, improving data retrieval speed by **40%**.",
    "tableau7": "Built Tableau dashboards for P&L, churn and ROI and presented the findings to clients, contributing to a **7% increase in sales**.",
    "trade_pipes": "Built Python pipelines ingesting **real-time trade data** for market analysis, strategy testing and performance evaluation.",
    "eda": "Evaluated market trends with EDA, hypothesis testing and SQL to support data-driven decisions.",
    "nysa": "Built end-to-end insurance workflows for **ICICI's Nysa CV**, integrating policy retrieval, quotation and claims APIs.",
    "pytest": "Wrote pytest unit and integration suites with **85%+ coverage**, making production releases more reliable.",
    "agile": "Delivered production features in cross-functional Agile teams, from requirements to release.",
    "solana": "Architected backend workflows for **Solana wallets, token operations and on-chain settlement**, integrated with third-party payment providers.",
    "integrations": "Built event-driven integrations with REST APIs, webhooks, WebSockets and N8N for **payment processing and blockchain monitoring**.",
    "agents": "Shipped **agentic AI workflows** (LangChain, LangGraph, RAG, ChromaDB) for automated trade screening and compliance assistance.",
    "lead3": "**Led a team of 3 developers** as the primary stakeholder liaison, owning requirements, architecture decisions and delivery.",
    "hal": "Built **HAL-AI**, a sports intelligence engine, and upgraded the platform's production RAG chatbot with LangChain, LangGraph and ChromaDB.",
    "angular": "Led the **Angular 19 upgrade and Angular Material v2-to-v3 refactor** across customer-facing and back-office apps.",
}

# Two engineering resumes (AI Engineer, Software Engineer) plus one analyst fallback, per 2026-10-27 decision.
# Retired versions (FDE, Data Engineer, Data Analyst, Full Stack, Python) are in archive/.
VERSIONS = {
    "AI Engineer": dict(
        file="AI_Engineer",
        headline="AI Engineer · LLM Agents & RAG · Python · AWS · Fintech",
        summary="AI engineer with 3.5 years of production software experience, building LLM features in regulated fintech since 2024. Shipped **LangGraph agents for trade screening and compliance**, a production RAG chatbot, and an **LLM support assistant at Zerodha's Quicko**, on solid Python, PostgreSQL and AWS foundations. Led a team of 3 developers.",
        skills=[("GenAI", "LLM agents (LangGraph, LangChain), RAG, vector search (ChromaDB, OpenSearch), prompt engineering, LLM APIs (Gemini), Hugging Face"),
                ("Languages", "Python, TypeScript, SQL, Java"),
                ("Backend & cloud", "Node.js, REST APIs, Webhooks, WebSockets, PostgreSQL, Supabase, AWS (Lambda, Step Functions, API Gateway), GCP, Docker, GitHub Actions"),
                ("ML & data", "TensorFlow, Pandas, NumPy, ETL pipelines, pytest")],
        titles={"sharematch": "Technical Analyst (AI & Engineering Lead)"},
        jobs={"sharematch": ["Shipped **LangGraph agents for automated trade screening and compliance assistance** on a regulated fintech platform, connected to live trading, KYC, payment and wallet systems.",
                             "Built **HAL-AI**, a sports intelligence engine, and upgraded the platform's **production RAG chatbot** (LangChain, LangGraph, ChromaDB).",
                             "**Led a team of 3 developers**, turning business and Shariah-compliance requirements into AI architecture, specifications and delivery.",
                             B["integrations"]],
              "quicko": [B["llm_bot"], B["migration"],
                         "Built Node.js services on **AWS Lambda** for production financial workflows and shipped **4 end-to-end features**."],
              "rising": [B["trade_pipes"], B["sql40"]],
              "monocept": ["Worked on a **CUDA-accelerated TensorFlow diffusion-model pipeline**.", B["nysa"], B["pytest"]]},
    ),
    "Software Engineer": dict(
        file="Software_Engineer",
        headline="Software Engineer · Backend & Full Stack · Python · TypeScript · AWS",
        summary="Software engineer with 3.5 years shipping production systems in fintech, payments and insurance: a **zero-loss migration of 100K+ accounts at Zerodha's Quicko**, payment, wallet and settlement flows on a Solana platform, and real-time trade pipelines. Works across Python and Node.js backends, React/Next.js frontends and AWS, and led a team of 3 developers.",
        skills=[("Languages", "Python, TypeScript, JavaScript, SQL, Java"),
                ("Backend", "Node.js, Django, REST APIs, GraphQL, Webhooks, WebSockets"),
                ("Frontend", "React, Next.js, Angular, Flutter, Tailwind CSS"),
                ("Data & cloud", "PostgreSQL, DynamoDB, OpenSearch, Supabase, AWS (Lambda, Step Functions, API Gateway, IAM), Docker, GitHub Actions, CI/CD"),
                ("AI", "LangChain, LangGraph, RAG")],
        titles={"sharematch": "Technical Analyst (Engineering Lead)"},
        jobs={"sharematch": ["**Led a team of 3 developers** building web and mobile apps on React/Next.js, Flutter and Supabase/PostgreSQL, owning requirements, architecture and delivery.",
                             B["solana"], B["integrations"],
                             "Shipped **LangGraph/RAG agents** for automated trade screening and compliance assistance."],
              "quicko": [B["migration"], B["lambda"], B["four_features"], B["angular"]],
              "rising": [B["trade_pipes"], B["sql40"]],
              "monocept": [B["nysa"], B["pytest"]]},
    ),
    "Technical Analyst": dict(
        file="Technical_Analyst",
        headline="Technical Analyst · Requirements · Fintech · AI Automation",
        summary="Technical analyst with 3.5 years bridging business and engineering in fintech and e-commerce. Writes the requirements, leads the team that builds them, and has shipped production code as a full-stack engineer.",
        skills=[("Analysis", "Requirements gathering, process analysis, stakeholder management, UAT, technical documentation, Agile"),
                ("Data", "SQL, Python, Tableau, Power BI"),
                ("Technology", "React/Next.js, Node.js, PostgreSQL, AWS, REST APIs, Solana, payment integrations"),
                ("AI & automation", "LangChain, LangGraph, RAG, N8N, Claude Code")],
        jobs={"sharematch": ["Translated business and **Shariah-compliance requirements** into specifications, workflows and roadmaps for a fintech platform.",
                             "Led requirements sessions and documented functional requirements and architecture decisions; **managed a team of 3 developers**.",
                             "Analysed **trading, KYC, payment, wallet and blockchain** flows to find system and process improvements.",
                             "Coordinated product, engineering, compliance and external partners; delivered **AI automation** (LangChain, RAG) for compliance."],
              "quicko": ["Delivered **4 end-to-end product features** from requirements through development, testing and deployment.",
                         B["migration"], "Coordinated the **Angular 19 upgrade** across customer-facing and back-office apps.", B["llm_bot"]],
              "rising": ["Presented market and business analysis to clients, contributing to a **7% increase in sales**.",
                         "Built Tableau dashboards for P&L, churn and ROI tracking.", B["sql40"]],
              "monocept": [B["nysa"], B["agile"]]},
    ),
}


def rich(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text))


def render_html(v, market):
    contact = " · ".join(html.escape(c) for c in CONTACT)
    skills = "".join(f"<div class='skill'><span class='k'>{html.escape(k)}:</span> {html.escape(val)}</div>"
                     for k, val in v["skills"])
    jobs = ""
    for key, bullets in v["jobs"].items():
        company, title, dates = JOBS[key]
        title = v.get("titles", {}).get(key, title)
        items = "".join(f"<li>{rich(b)}</li>" for b in bullets)
        jobs += (f"<div class='job'><div class='row'><span class='co'>{html.escape(company)}</span>"
                 f"<span class='dt'>{html.escape(dates)}</span></div><div class='ti'>{html.escape(title)}</div>"
                 f"<ul>{items}</ul></div>")
    projects = ""
    if PROJECTS:
        rows = "".join(f"<li><strong>{html.escape(n)}</strong> ({html.escape(u)}): {rich(d)}</li>" for n, u, d in PROJECTS)
        projects = f"<h2>Projects</h2><ul>{rows}</ul>"
    school, degree, year = EDUCATION
    edu = (f"<div class='row'><span class='co'>{html.escape(school)}</span><span class='dt'>{html.escape(year)}</span></div>"
           f"<div class='ti'>{html.escape(degree)}</div>")
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Mariyam Pangarkar - {html.escape(v['headline'].split(' · ')[0])}</title>
<style>
@page {{ size: A4; margin: 11mm 13mm; }}
:root {{ --fs: 10.4pt; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Caladea', 'Liberation Serif', Georgia, serif; font-size: var(--fs); line-height: 1.28; color: #111; }}
h1 {{ font-size: calc(var(--fs) * 2.05); margin: 0; letter-spacing: 0.3px; text-align: center; }}
.headline {{ text-align: center; font-size: calc(var(--fs) * 1.08); color: #1f3a5f; font-weight: bold; margin-top: 2px; }}
.contact, .status {{ text-align: center; font-size: calc(var(--fs) * 0.86); margin-top: 3px; }}
.status {{ color: #444; font-style: italic; margin-top: 1px; }}
h2 {{ font-size: calc(var(--fs) * 1.08); text-transform: uppercase; letter-spacing: 0.8px; color: #1f3a5f;
      border-bottom: 1px solid #1f3a5f; margin: 9px 0 4px; padding-bottom: 1px; }}
p.summary {{ margin: 0; }}
.skill {{ margin: 1px 0; }}
.k {{ font-weight: bold; }}
.job {{ margin-bottom: 5px; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; }}
.co {{ font-weight: bold; }}
.dt {{ white-space: nowrap; }}
.ti {{ font-style: italic; }}
ul {{ margin: 1px 0 0; padding-left: 15px; }}
li {{ margin: 1px 0; }}
strong {{ font-weight: bold; }}
</style></head><body>
<h1>Mariyam Pangarkar</h1>
<div class='headline'>{html.escape(v['headline'])}</div>
<div class='contact'>{contact}</div>
<div class='status'>{html.escape(STATUS[market])}</div>
<h2>Summary</h2><p class='summary'>{rich(v['summary'])}</p>
<h2>Skills</h2>{skills}
<h2>Experience</h2>{jobs}
{projects}
<h2>Education</h2>{edu}
</body></html>"""


def main():
    out = HERE / "html"
    out.mkdir(exist_ok=True)
    jobs = []
    for label, v in VERSIONS.items():
        for market in STATUS:
            src = out / f"{market}_{v['file']}.html"
            src.write_text(render_html(v, market))
            dst = HERE / market / f"Mariyam_Pangarkar_{v['file']}.pdf"
            dst.parent.mkdir(exist_ok=True)
            jobs.append({"src": str(src), "dst": str(dst)})
    (out / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(HERE / "render.js"), str(out / "jobs.json")], check=True)


if __name__ == "__main__":
    main()
