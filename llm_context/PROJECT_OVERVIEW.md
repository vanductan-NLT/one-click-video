# Overview

**PROJECT OVERVIEW**

1. **WBS (Work Breakdown Structure) and Timeline for Project:**   
   **Purpose:** To establish scope, assumptions, constraints, resource allocation, and timelines as the baseline for project planning and execution.  
   **Output:** An agreed WBS defining total project scope, total timeline, and Version 1 delivery milestones, including team roles and effort allocation.  
   → [**LINK**](https://docs.google.com/spreadsheets/d/1QlUg48mv4lp0xcXBqq-25XzHjEEqne1j1pdiA3zs9ng/edit?gid=1252245706#gid=1252245706)

2. **System Component & Tooling:**  
   **Purpose:** To identify the tools, platforms, and services used to build and operate the product, and to clarify their impact on cost, output quality, and operational risk.  
   **Output:** A structured list of system components and tools used in product development and operation, including key dependencies and related assumptions.  
   → [**LINK**]()

3. **Cost for Project:**  
   \- One-Time Cost: [**LINK**]()  
   \- Monthly Cost: **[LINK]()**

# System Component & Tooling

**SYSTEM COMPONENT & TOOLING**

1. **Infrastructure Layer**  
   Used to provide servers, storage, and bandwidth for stable system operation.

| Component | Purpose / Impact |
| ----- | ----- |
| **Servers (Cloud VPS)** | Main fixed monthly cost. Server capacity directly affects video processing and export speed. |
| **Video Storage (S3)** | Used to store video files with flexible capacity. Pay-as-you-go pricing helps control storage costs as usage grows. |
| **Bandwidth** | Determines upload speed and video playback quality. Insufficient bandwidth may cause delays or interruptions. |

2. **Middleware Layer**  
   Used to manage processing flow, store data, and prevent system overload.

| Component | Purpose / Impact |
| ----- | ----- |
| **System Deployment (Docker)** | Helps deploy and operate the system consistently, reducing setup and update issues. |
| **Data Storage (PostgreSQL)** | Stores all user and system data. Regular backups are required to prevent data loss. |
| **Processing Queue (Redis)** | Ensures tasks are processed in order and prevents system overload during peak usage. |

   

   

3. **Core Processing Engine**  
   Used to process video and content, creating the core value of the product.

| Component | Purpose / Impact |
| ----- | ----- |
| **Video Processing Tools (FFmpeg / Remotion)** | Determine video output quality, smoothness, and processing time. |
| **AI Content Services (OpenAI / Gemini)** | Used to analyze and process content. Costs increase based on actual usage. |
| **Automatic Subtitles (Whisper)** | Converts audio to subtitles. Accuracy directly affects user experience. |

4. **Third-Party Services**  
   Used to rely on external services the system does not build in-house and to connect with social platforms.

| Component | Risk / Note |
| ----- | ----- |
| **Auto-clipping Services (OpusClip / Klap)** | Dependency on third-party providers. Price changes or service shutdowns may impact features. |
| **Social Media Platforms** | Posting rules may change without notice, requiring ongoing updates and monitoring. |

# One \- Time Cost

**ONE-TIME COST**

**Version 1: Editing long videos and the platforms used.**  
**Price: 4,500 SGD**

-  **Automatic video editing feature**  
  → The system automatically removes unnecessary parts and silent gaps, and adds effects, sound effects, transitions, and text based on the original video content.  
- **Video uploading and hosting platform**  
  → A platform system for uploading raw videos and storing edited videos.  
  Footage video: [Link](https://drive.google.com/file/d/10Lkv5piw9MNv-AuShsc3miECg_LeJrOD/view?usp=drive_link)  
  Demo video: [Link](https://drive.google.com/file/d/1OShVqCkaCfHtNDgJJ0e83VHPhsOhKshw/view?usp=drive_link)   
  Process video: [Link](https://drive.google.com/file/d/1S8MYYaz-VEohsxEsLnXXLvhhWdFO_fxI/view?usp=drive_link)

	**Detail Version 1:** [Link](https://docs.google.com/spreadsheets/d/1QlUg48mv4lp0xcXBqq-25XzHjEEqne1j1pdiA3zs9ng/edit?gid=1252245706#gid=1252245706)  
**Estimate Timeline:** 17 days  
	

**Version 2: Short-form video editing & Social media posting**  
**Price: 4,500 SGD**

- **Short video editing**  
  → Creates short videos from unedited source videos, optimized for social media platforms (Reels, Shorts).  
-  **Short video storage**  
   → Stores and manages generated short videos.  
  Footage video: [Link](https://drive.google.com/file/d/10Lkv5piw9MNv-AuShsc3miECg_LeJrOD/view?usp=drive_link)  
  Demo video: [Link](https://drive.google.com/file/d/1Ae-xm8JbDGxo4U2LxwyfpY-rllE45rZU/view?usp=drive_link)  
  Process video: [Link](https://drive.google.com/file/d/1zb9HBBpo6Agi5dZcOCqD8nPScsMjw_Au/view?usp=drive_link)  
-  **Social media posting**  
  → Allows videos to be published directly from the system to social media platforms (Facebook, Instagram, LinkedIn).  
- **Post management via Google Sheet**  
  → Allows post scheduling and status tracking through Google Sheets without using a complex management interface.

  Concept Demo: [Link](https://drive.google.com/file/d/1msPCSF2LxfLSvjxr4JCVu5kwZf4kiDti/view?usp=drive_link)

**Detail Version 2:** Update later  
**Estimate Timeline:** Update later

**Version 3: Post management and publishing automation**  
**Price: 4,500 SGD**

- **Post scheduling**  
  → Automatically publishes posts based on a predefined schedule.  
-  **Publishing management interface**  
  → Allows users to track, edit, and manage all published and scheduled content within the system.  
- **Reporting system**  
   → Sends post status and publishing reports via WhatsApp or Telegram.  
- **Pre-publish approval**  
  → Allows content to be reviewed and approved before being published to social media platforms.

  Concept Demo: [Link](https://drive.google.com/file/d/1msPCSF2LxfLSvjxr4JCVu5kwZf4kiDti/view?usp=drive_link)

  **Detail Version 3:** Update later

	**Timeline:** Update later

# Monthly Cost

**MONTHLY COST**

***Exchange rate:** 1 USD ≈ 1.3 SGD*

1. **Fixed Infrastructure Cost (Group A)**  
   Paid monthly to keep the system running 24/7.

| Item | Solution | Min (USD) | Max (USD) | Notes |
| ----- | ----- | ----- | ----- | ----- |
| **Server (VPS)** | 8 vCPU / 16GB RAM | $40 | $60 | Hetzner or DigitalOcean |
| **Storage (S3)** | 500GB – 1TB | $10 | $30 | AWS S3 / Cloudflare R2 |
| **Domain & SSL** | Domain \+ DNS | $2 | $2 | Fixed monthly cost |
| **Total Fixed (A)** |  | **$52** | **$92** |  |

2. **Variable Cost – API Usage (Group B)**  
   Depends on actual customer usage.

| Item | Solution | Min (USD) | Max (USD) | Notes |
| ----- | ----- | ----- | ----- | ----- |
| **AI Text (LLM)** | GPT-4o mini | $5 | $15 | Script and keyword analysis |
| **AI Video (Viral)** | OpusClip / Klap | $15 | $30 | Short-video processing API fees |
| **Total Variable (B)** |  | **$20** | **$45** |  |

3. **Total Operating Cost (OpEx \= A \+ B)**

| Usage Level | Total (USD) | Actual Processing Volume |
| ----- | ----- | ----- |
| **MINIMUM** | **$72** | 4–6 videos per month Original video length: ≤ 20 minutes per video Total processing time: \~80–120 minutes Storage usage: \~40–60 GB Concurrent users: 4–5 users |
| **MAXIMUM** | **$137** | 30–40 videos per month Original video length: ≤ 20–30 minutes per video Total processing time: \~600–800 minutes Storage usage: \~300–500 GB Concurrent users: 20–30 users |

