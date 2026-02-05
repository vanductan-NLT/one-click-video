1. ### **Adapter**

| Adapter | Port | Tech stack | Mô tả | Phase |
| ----- | ----- | ----- | ----- | ----- |
| PostgresVideoRepository | IVideoRepository | PostgreSQL (AWS RDS) | CRUD VideoJob, update status atomic, transaction support | 1 |
| S3StorageAdapter | IAssetStoragePort | AWS S3 | Upload video/assets, presigned URL (expire 1h), bucket input/output/assets, ACL private | 1 |
| WhisperXTranscriptionAdapter | ITranscriptionPort | WhisperX (local GPU/CPU) | Load audio, run model, parse word-level timestamps \+ confidence, fallback nếu GPU thiếu | 1 |
| PexelsBrollAdapter | IBrollProviderPort | Pexels API | Search keyword → download clip ngắn (3–8s), lưu temp path, fallback nếu API fail | 1 |
| FFmpegRenderAdapter | IRenderEnginePort | FFmpeg | Build command concat/overlay/drawtext/audio mix, progress pipe, timeout & error handling | 1 |
| CeleryRedisQueueAdapter | IQueuePort | Redis \+ Celery | Enqueue task (video-processing), limit concurrent (worker concurrency=2), job timeout | 1 |
| CryptoLicenseAdapter | ILicenseValidatorPort | cryptography (Fernet) \+ JWT | Offline: decrypt & check expiry/quota; Online: HTTP fallback nếu có mạng | 1 |
| GeminiContentAdapter | IGenerativeContentPort | google-generativeai / OpenAI SDK | Prompt Gemini/OpenAI tạo caption/kịch bản/social copy từ transcript | 2 |
| SocialOAuthAdapter | ISocialPublisherPort | requests-oauthlib \+ platform SDK (TikTok/FB/IG) | OAuth flow, post clip, schedule (cron-like), handle token refresh | 2 |
| PgDumpBackupAdapter | IBackupPort | pg\_dump  | Dump DB schema/data | 3 |
| StripeWebhookAdapter | IPaymentProviderPort | stripe-python SDK | Verify webhook signature, create checkout session, trigger license creation & email | 3 |
| StructlogMonitoringAdapter | (optional IMonitoringPort) | structlog (JSON log) | Structured log, error code table, container health (Prometheus exporter nếu cần) | 1.3+ |
| RemotionRenderAdapter  | IRenderEnginePort / IPreviewPort | Remotion (Node.js \+ React) | Render motion text/animation/transition (karaoke sub, zoom/pop), preview trong web hoặc xuất MP4 | 1.2+ |

2. ### **Dependency Inject**

| Module | Port  | Adapter | Provider | Dependencies  | Note | Phase |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| M2 (Video Engine) | IVideoRepository | PostgresVideoRepository | providers.Factory(PostgresVideoRepository, session=db\_session) | AsyncSession (từ engine) | Repository cho VideoJob metadata, status, transcript JSON | 1 |
| M2 (Video Engine) | ITranscriptionPort | WhisperXTranscriptionAdapter | providers.Factory(WhisperXTranscriptionAdapter) |  | ASR local (WhisperX) – không cần config ngoài | 1 |
| M2 (Video Engine) | IBrollProviderPort | PexelsBrollAdapter | providers.Factory(PexelsBrollAdapter, api\_key=providers.Configuration("pexels.api\_key")) | PEXELS\_API\_KEY (từ config) | B-roll từ Pexels API, cần API key | 1 |
| M2 (Video Engine) | IRenderEnginePort | FFmpegRenderAdapter | providers.Factory(FFmpegRenderAdapter) |  | Render FFmpeg – dùng subprocess, không cần inject ngoài | 1 |
| M2 (Video Engine) | IRenderEnginePort / IPreviewPort | RemotionRenderAdapter | providers.Factory(RemotionRenderAdapter, remotion\_path=providers.Configuration("remotion.path")) | REMOTION\_PATH (từ config) | Render motion text/animation (karaoke sub, zoom/pop) – cần Node runtime | 1.2+ |
| M9 Storage | IAssetStoragePort | MinIOStorageAdapter | providers.Factory(S3StorageAdapter, aws\_access\_key\_id=..., aws\_secret\_access\_key=..., region\_name=..., endpoint\_url=...) | AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY, AWS\_REGION, S3\_ENDPOINT (từ .env) | Upload video/assets vào AWS S3, presigned URL (expire 1h), bucket input/output/assets, ACL private | 1 |
| M8 Queue | IQueuePort | CeleryRedisQueueAdapter | providers.Factory(CeleryRedisQueueAdapter, redis\_url=providers.Configuration("redis.url")) | REDIS\_URL (từ config) | Queue job processing, limit concurrent – cần Redis connection | 1 |
| **auth\_license** (M7 License) | ILicenseValidatorPort | CryptoLicenseAdapter | providers.Factory(CryptoLicenseAdapter, fernet\_key=providers.Configuration("license.fernet\_key")) | FERNET\_KEY (từ config/secrets) | Offline crypto validation \+ online fallback – cần key bí mật | 1 |
| M12 – phase 3 | IPaymentProviderPort | StripeWebhookAdapter | providers.Factory(StripeWebhookAdapter, stripe\_secret=providers.Configuration("stripe.secret")) | STRIPE\_SECRET\_KEY | Xử lý webhook Stripe → trigger license | 3 |
| M11 – phase 3 | IBackupPort | PgDumpBackupAdapter | providers.Factory(PgDumpBackupAdapter, pg\_dump\_path=...) | PG\_DUMP\_PATH | Backup DB  | 3 |

