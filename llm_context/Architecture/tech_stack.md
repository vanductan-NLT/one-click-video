

| \# | Module / Layer / Component | Công nghệ chính  | Mô tả ngắn gọn & Vai trò | Phase  |
| ----- | ----- | ----- | ----- | ----- |
| 1 | **Frontend** (M1 – Web App / UI) | Next.js \+ React \+ Tailwind CSS \+ TypeScript | Dashboard upload, progress real-time, preview, config brand/insertion, YouTube-style UI | 1 |
| 2 | **Backend API** (Core backend, orchestration) | FastAPI (Python 3.11+) | REST API chính, WebSocket progress, dependency injection, error handling, rate limiting | 1  |
| 3 | **Runtime Environment** | Node.js \+ Python (cho FastAPI \+ worker) | Chạy Remotion (React-based render) \+ Python processing | 1.2+  |
| 4 | **Database** (M4 – Metadata) | AWS RDS PostgreSQL | Lưu VideoJob metadata, status, transcript JSON, user config, license | 1  |
| 5 | **Storage** (M9 – Storage & Asset Mgmt) | AWS S3 | Lưu input/output video, asset library (elements/SFX/music), presigned URL | 1  |
| 6 | **Queue & Resource Mgmt** (M8) | AWS SQS \+ Celery (Python) | Queue job render, limit concurrent (max 2–3), resource limit | 1  |
| 7 | **Video Processing** (M2 Core Engine) | FFmpeg \+ WhisperX (local GPU/CPU) \+ Remotion (Node.js) | Silence removal, ASR word-level, B-roll insert, text overlay, render MP4/HD | 1–2 |
| 8 | **Generative AI** (M5 – phase 2\) | Google Gemini API / OpenAI API  | Tạo caption, kịch bản, social post từ transcript | 2 |
| 9 | **License & Activation** (M7) | cryptography \+ JWT | Offline crypto validation \+ online fallback (HTTP API nhỏ) | 1 |
| 10 | **Social Integration** (M6 – phase 2\) | requests-oauthlib \+ platform SDK (TikTok/FB/IG API) | OAuth connect, auto-publish shorts, schedule post | 2 |
| 11 | **Payment & Monetization** (M12 – phase 3\) | Stripe SDK (stripe-python) \+ webhook | Payment gateway, trigger license/email credential | 3 |
| 12 | **Monitoring & Logging** (M10) | structlog (JSON)  | Structured log, error code, container health | 1.3+ |
| 13 | **Backup & Persistence** (M11 – phase 3\) | pg\_dump  | Auto backup DB \+ S3 bucket | 3 |
| 14 | **Deployment & Infra** | Docker Compose (self-hosted) \+ AWS ECS  |  | 1 |
| 15 | **Testing** | pytest  | Unit test domain/application, integration test adapters | 1 |
| 16 | **Automation Trigger** | AWS Lambda \+ Step | Hỗ trợ trợ tự động gửi mail về cho user khi đăng ký thành công.  Tự động set up server cho user đó. |  |

