import asyncio
import json
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    if hasattr(sys.stdout, "reconfigure"):
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
except Exception:
    pass


from sqlmodel import select
from app.core.database import async_session_factory, init_db
from app.models import (
    Award,
    BotSetting,
    ContactSubmission,
    Project,
    TeamMember,
    TeamQuote,
)


async def seed_data():
    await init_db()

    async with async_session_factory() as session:
        # 1. Seed Bot Settings if empty
        existing_settings = (await session.exec(select(BotSetting))).first()
        if not existing_settings:
            print("🚀 Seeding default team settings...")
            settings_to_seed = [
                BotSetting(key="team_name", value="DevUpward", description="Official team name"),
                BotSetting(key="team_motto", value="Building the future, one hackathon at a time 🚀", description="Team slogan"),
                BotSetting(key="team_about", value="We are DevUpward, an elite hackathon team specialized in AI, autonomous agents, and high-impact full-stack products. We build production-ready prototypes in 48 hours.", description="Team bio"),
                BotSetting(key="brand_color", value="#5865F2", description="Primary hex brand color"),
                BotSetting(key="presence_status", value="🏆 Preparing for Next Hackathon", description="Current Discord bot status"),
                BotSetting(key="presence_activity_type", value="watching", description="playing, watching, listening, competing"),
                BotSetting(key="website_url", value="https://devupward.tech", description="Official team website"),
                BotSetting(key="github_org_url", value="https://github.com/DevUpward", description="Team GitHub Org"),
                BotSetting(key="linkedin_org_url", value="https://linkedin.com/company/devupward", description="Team LinkedIn"),
                BotSetting(key="devpost_url", value="https://devpost.com/teams/devupward", description="Team Devpost"),
                BotSetting(key="coffee_cups_consumed", value="420", description="Fun stat: Coffee cups"),
            ]
            session.add_all(settings_to_seed)

        # 2. Seed Team Members if empty
        existing_members = (await session.exec(select(TeamMember))).first()
        if not existing_members:
            print("👥 Seeding default team members...")
            members = [
                TeamMember(
                    name="Marwan",
                    role="Team Lead & AI Architect",
                    bio="Specialized in Multi-Agent systems, LLM orchestration, and scalable cloud architectures. 5x Hackathon Finalist.",
                    avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80",
                    skills=json.dumps(["Python", "FastAPI", "Gemini API", "LangGraph", "Docker", "PyTorch"]),
                    github_url="https://github.com/MarwanFo",
                    linkedin_url="https://linkedin.com/in/marwan",
                    portfolio_url="https://marwan.dev",
                    display_order=1,
                ),
                TeamMember(
                    name="Alex Vance",
                    role="Full-Stack Engineer",
                    bio="Building blazingly fast frontends with React & Next.js and robust backend microservices. Obsessed with clean UI/UX.",
                    avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&auto=format&fit=crop&q=80",
                    skills=json.dumps(["React", "TypeScript", "Next.js", "Tailwind CSS", "Node.js", "GraphQL"]),
                    github_url="https://github.com",
                    linkedin_url="https://linkedin.com",
                    portfolio_url="https://alexvance.io",
                    display_order=2,
                ),
                TeamMember(
                    name="Elena Rostova",
                    role="Product & UI/UX Designer",
                    bio="Translating complex hackathon concepts into sleek, intuitive interfaces and pitch-winning slide decks.",
                    avatar_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&auto=format&fit=crop&q=80",
                    skills=json.dumps(["Figma", "Design Systems", "Prototyping", "Pitch Strategy", "User Research"]),
                    github_url="https://github.com",
                    linkedin_url="https://linkedin.com",
                    portfolio_url="https://elena.design",
                    display_order=3,
                ),
                TeamMember(
                    name="David Chen",
                    role="Backend & Distributed Systems",
                    bio="Data pipeline optimization, Redis caching, and real-time WebSockets. Ensuring demos never crash on stage.",
                    avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&auto=format&fit=crop&q=80",
                    skills=json.dumps(["Go", "Rust", "PostgreSQL", "Kafka", "WebSockets", "Kubernetes"]),
                    github_url="https://github.com",
                    linkedin_url="https://linkedin.com",
                    portfolio_url="https://davidchen.tech",
                    display_order=4,
                ),
            ]
            session.add_all(members)

        # 3. Seed Projects & Awards if empty
        existing_projects = (await session.exec(select(Project))).first()
        if not existing_projects:
            print("💡 Seeding default showcase projects & awards...")
            projects = [
                Project(
                    title="OmniAgent Flow",
                    slug="omniagent-flow",
                    tagline="Autonomous multi-modal agent workspace for real-time document analysis and code generation.",
                    description="Built during HackGlobal 2026. OmniAgent Flow coordinates specialized autonomous subagents to ingest multi-gigabyte datasets, generate validated API specifications, and benchmark execution in parallel.",
                    category="AI",
                    hackathon_name="HackGlobal 2026",
                    hackathon_year=2026,
                    awards_won="🥇 1st Place Overall & Best AI Agent",
                    demo_url="https://demo.omniagent.dev",
                    repo_url="https://github.com/DevUpward/omniagent-flow",
                    devpost_url="https://devpost.com/software/omniagent-flow",
                    banner_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80",
                    is_featured=True,
                    display_order=1,
                ),
                Project(
                    title="PulseGuard DeFi",
                    slug="pulseguard-defi",
                    tagline="Real-time smart contract exploit prevention and automated liquidity circuit breaker.",
                    description="Built at ETHDenver 2025. PulseGuard monitors mempools for malicious flash-loan patterns and automatically triggers protective pause hooks before transactions land on-chain.",
                    category="Web3",
                    hackathon_name="ETHDenver 2025",
                    hackathon_year=2025,
                    awards_won="🥈 2nd Place Security Track",
                    demo_url="https://pulseguard.defi",
                    repo_url="https://github.com/DevUpward/pulseguard-defi",
                    devpost_url="https://devpost.com/software/pulseguard-defi",
                    banner_url="https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&auto=format&fit=crop&q=80",
                    is_featured=True,
                    display_order=2,
                ),
                Project(
                    title="CodeSynth Live",
                    slug="codesynth-live",
                    tagline="Interactive collaborative browser IDE with instant AI pair programming and live sandboxes.",
                    description="Built at Junction Hackathon. Zero-setup WebAssembly development environments with real-time audio sync and contextual AI code generation.",
                    category="DevTools",
                    hackathon_name="Junction Hackathon",
                    hackathon_year=2025,
                    awards_won="🏆 Best Developer Experience Award",
                    demo_url="https://codesynth.live",
                    repo_url="https://github.com/DevUpward/codesynth-live",
                    devpost_url="https://devpost.com/software/codesynth-live",
                    banner_url="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80",
                    is_featured=False,
                    display_order=3,
                ),
            ]
            session.add_all(projects)
            await session.flush()

            existing_awards = (await session.exec(select(Award))).first()
            if not existing_awards:
                awards = [
                    Award(
                        hackathon_name="HackGlobal 2026",
                        award_title="1st Place Grand Champion",
                        placement=1,
                        category="Overall",
                        prize_description="$15,000 + Venture Investor Demo",
                        year=2026,
                        project_id=projects[0].id,
                        icon="🥇",
                    ),
                    Award(
                        hackathon_name="HackGlobal 2026",
                        award_title="Best Autonomous Agent Implementation",
                        placement=0,
                        category="AI Track",
                        prize_description="$5,000 Cloud Credits",
                        year=2026,
                        project_id=projects[0].id,
                        icon="🌟",
                    ),
                    Award(
                        hackathon_name="ETHDenver 2025",
                        award_title="2nd Place DeFi Security",
                        placement=2,
                        category="Security & Infrastructure",
                        prize_description="$8,000 Bounty",
                        year=2025,
                        project_id=projects[1].id,
                        icon="🥈",
                    ),
                    Award(
                        hackathon_name="Junction Hackathon 2025",
                        award_title="Best Developer Experience",
                        placement=0,
                        category="Developer Tools",
                        prize_description="$3,000 API Credits",
                        year=2025,
                        project_id=projects[2].id,
                        icon="🏆",
                    ),
                ]
                session.add_all(awards)

        # 4. Seed Quotes if empty
        existing_quotes = (await session.exec(select(TeamQuote))).first()
        if not existing_quotes:
            print("💬 Seeding default team quotes...")
            quotes = [
                TeamQuote(
                    quote="It worked on my localhost 5 minutes ago, I swear.",
                    author="David",
                    context="3:45 AM during HackGlobal Demo Freeze",
                ),
                TeamQuote(
                    quote="Sleep is a depreciating asset during a 48-hour hackathon.",
                    author="Marwan",
                    context="Sunday 6:00 AM presentation rehearsal",
                ),
                TeamQuote(
                    quote="Don't worry about the edge cases, the judges will only click the shiny green button.",
                    author="Alex",
                    context="20 minutes before submission deadline",
                ),
            ]
            session.add_all(quotes)

        # 5. Seed sample inbox if empty
        existing_inbox = (await session.exec(select(ContactSubmission))).first()
        if not existing_inbox:
            sample_inbox = ContactSubmission(
                sender_name="Sarah Jenkins",
                email="sarah.jenkins@techventures.vc",
                organization="TechVentures Accelerator",
                discord_tag="sarah_j#1001",
                message="Hey DevUpward team! Loved your OmniAgent Flow demo at HackGlobal. We'd love to chat with you about our summer cohort.",
                status="unread",
            )
            session.add(sample_inbox)

        await session.commit()
        print("✅ Database successfully verified and populated with showcase data!")


if __name__ == "__main__":
    asyncio.run(seed_data())
