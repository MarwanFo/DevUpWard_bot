# Functional Specification (Cahier des Charges)
**Project Title:** Hackathon Team Official Showcase Bot  
**Purpose:** Brand Identity, Portfolio Display, and Team Representation on Discord  

---

## 1. Project Overview & Vision
The objective of this project is to create an official Discord bot that acts as the digital storefront, interactive portfolio, and identity ambassador for our hackathon team. 

Rather than serving as a temporary project management tool during competitions, this bot is a permanent fixture in our Discord server. It is designed to impress guests, mentors, judges, potential sponsors, and fellow developers by presenting who we are, what we have built, and what we have achieved in a clean, interactive format.

---

## 2. Target Audience
* **Team Members:** A central hub to celebrate milestones, track collective achievements, and share official links.
* **Visitors & Guests:** Other developers, hackathon organizers, or friends visiting the server who want to learn about the team.
* **Mentors, Judges & Recruiters:** External stakeholders looking for a quick, structured overview of our members' skills, past projects, and awards.

---

## 3. Core Functional Modules

### 3.1. Team Identity & Branding
* **Team Overview (`/about`):** Displays the official team card containing our name, logo, motto/slogan, founding story, and primary areas of focus (e.g., AI, Web3, Full-Stack, FinTech).
* **Custom Presence & Status:** The bot continuously displays a customized status reflecting the team's current state (e.g., *" Preparing for [Upcoming Hackathon]"* or *"🏆 X Hackathons Won"*).
* **Official Links Hub (`/socials` or `/links`):** Provides instant access to the team's collective platforms, such as our website, GitHub organization, LinkedIn page, Devpost profile, and YouTube demo channel.

### 3.2. Interactive Team Roster
* **Full Roster Directory (`/team`):** Lists all core team members alongside their primary titles/roles within the squad.
* **Individual Member Profiles (`/member [name]`):** Generates a personalized profile card for a selected team member, featuring:
  * Role and specialty (e.g., UI/UX Designer, Backend Architect, Pitch Lead).
  * Short personal bio.
  * Key skills and areas of expertise.
  * Personal professional links (Portfolio, LinkedIn, GitHub).

### 3.3. Hackathon Hall of Fame (Track Record)
* **Achievements & Awards (`/awards` or `/palmares`):** A chronological showcase of all hackathons the team has participated in, highlighting podium finishes, special category prizes, and honorable mentions.
* **Team Statistics (`/stats`):** A high-level summary of the team's journey (e.g., Total Hackathons Attended, Total Projects Built, Awards Won, Cups of Coffee Consumed).

### 3.4. Project & Prototype Showroom
* **Project Catalog (`/projects`):** Displays an interactive menu of prototypes and products built by the team during past competitions.
* **Project Spotlight (`/project [name]`):** Displays a rich presentation card for a specific project, including:
  * The problem it solves and our solution.
  * The hackathon where it was created and any prizes won.
  * Visual previews (screenshots, banner, or logo).
  * Direct links to the live demo, video pitch, and source code.

### 3.5. Server Hospitality & Engagement
* **Automated VIP Onboarding:** Greets new guests joining the server with a branded welcome card, introducing the team and guiding them on how to explore our portfolio using the bot's commands.
* **Contact & Collaboration (`/contact`):** Provides clear instructions or an interactive form for external visitors who want to invite the team to an event, propose a collaboration, or get in touch.
* **Team Culture & Fun (`/mascot` or `/quote`):** Shares inside jokes, memorable hackathon moments, team photos, or famous quotes from late-night coding sessions to showcase the team's personality.

---

## 4. User Experience & Design Guidelines
* **Visual Consistency:** Every message sent by the bot must strictly follow the team's visual identity (consistent color palette, official logos, banners, and clean formatting).
* **Interactive Navigation:** Instead of requiring users to type long commands, the bot should utilize interactive buttons and dropdown menus so visitors can browse through members and projects effortlessly.
* **Concise Presentation:** Information should be scannable, impactful, and well-structured, reading like an executive summary or a sleek digital brochure.

---

## 5. Technical Architecture & Tech Stack
* **Discord Bot Engine:** Python (using `discord.py`).
* **API / Backend Layer:** Python (FastAPI / ASGI) to serve data and handle CRUD operations for the management dashboard.
* **Admin Management Interface:** React (Vite + Tailwind CSS / UI component library) to manage:
  * Team member profiles, bios, roles, and professional links.
  * Projects, showroom prototypes, demo links, and media previews.
  * Awards, hackathon placements, and team statistics.
  * Bot status/presence messages, hospitality settings, and welcome cards.
  * Incoming visitor contact messages and collaboration inquiries.
* **Data Storage:** Unified database (e.g., SQLite for lightweight setups or PostgreSQL) or structured data store accessible by both the bot and API service.
