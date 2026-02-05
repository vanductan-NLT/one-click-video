### 

| \# | Module | Use Case  | Mô tả  | Input DTO | Output  | Phase  | Ports |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1 | M1 (Web App / UI) | UploadVideoUseCase | Nhận upload request, validate, tạo VideoJob, enqueue job processing | UploadVideoInput (fileChunk, metadata) | UploadVideoOutput (jobId, status, progressUrl) | 1 | IVideoRepository, IQueuePort |
| 2 | M1 | GetJobStatusUseCase | Lấy tiến trình job real-time cho dashboard | GetJobStatusInput (jobId) | JobStatusOutput (status, progress, error?) | 1 | IVideoRepository |
| 3 | M2 (Core Engine) | ProcessVideoJobUseCase | Orchestrate toàn bộ pipeline: silence → ASR → JSON → B-roll → text → render (main orchestrator) | ProcessJobInput (jobId) | ProcessJobOutput (finalPaths, transcript) | 1 | IVideoRepository, ITranscriptionPort, IBrollProviderPort, IRenderEnginePort, IAssetStoragePort |
| 4 | M2 | SilenceRemovalUseCase | Detect & cắt silence, cập nhật VideoJob transcript | SilenceRemovalInput (audioPath) | SilenceRemovalOutput (cutRanges, updatedTranscript) | 1 | SilenceRule (Domain Service) |
| 5 | M2 | TranscribeVideoUseCase | Gọi ASR → tạo Transcript VO → extract keywords | TranscribeInput (audioPath) | TranscribeOutput (Transcript VO) | 1 | ITranscriptionPort |
| 6 | M2 | GenerateBrollUseCase | Extract keywords → gọi port lấy B-roll clips → chọn vị trí chèn | GenerateBrollInput (keywords, transcript) | BrollOutput (list\<RenderLayer\>) | 1 | IBrollProviderPort, KeywordExtractorService |
| 7 | M2 | ApplyTextOverlayUseCase | Chèn text/keyword overlay vào timeline | TextOverlayInput (transcript, config) | TextOverlayOutput (list\<RenderLayer\>) | 1 | InsertionRuleEngine (Domain Service) |
| 8 | M2 | RenderFinalVideoUseCase | Ghép tất cả layers → gọi render port → lưu output | RenderInput (jobId, layers) | RenderOutput (outputPath, duration) | 1 | IRenderEnginePort, IVideoRepository |
| 9 | M3 (Shorts/Reels) | CreateShortClipsUseCase | Detect hook → crop 9:16 → apply sub style → render shorts \+ viral score (phase 2\) | CreateShortsInput (videoJobId) | ShortsOutput (list\<ShortClip\>, scores) | 2 | HookDetectionRule, IRenderEnginePort |
| 10 | M5 (Generative AI) | GenerateMarketingContentUseCase | Tạo caption, kịch bản, social post từ transcript (phase 2\) | GenerateContentInput (transcript) | ContentOutput (caption, script, hashtags) | 2 | IGenerativeContentPort |
| 11 | M6 (Social) | PublishToSocialUseCase | Lên lịch/đăng clip lên platform (phase 2+) | PublishInput (clipId, platforms, schedule) | PublishOutput (status per platform) | 2 | ISocialPublisherPort |
| 12 | M7 (License) | ValidateAndConsumeLicenseUseCase | Check license valid \+ trừ quota trước render | ValidateLicenseInput (userId, jobType) | LicenseValidationOutput (valid, remainingQuota) | 1 | ILicenseValidatorPort, IVideoRepository |
| 13 | M8 (Queue) | EnqueueProcessingJobUseCase | Đẩy job vào queue với priority/resource check | EnqueueInput (jobId, priority) | EnqueueOutput (queuePosition) | 1 | IQueuePort |
| 14 | M9 (Storage) | UploadAssetUseCase | Upload element/SFX/music vào library (phase 1.2+) | UploadAssetInput (file, type) | AssetOutput (id, url) | 1.2 | IAssetStoragePort |
| 15 | M11 (Backup) | CreateBackupUseCase | Tạo snapshot DB \+ volume (phase 3\) | BackupInput (retentionDays) | BackupOutput (snapshotId) | 3 | IBackupPort |
| 16 | M12 (Payment) | ProcessPaymentUseCase | Xử lý payment → tạo license \+ gửi credential (phase 3\) | PaymentInput (amount, userId) | PaymentOutput (transactionId, licenseKey) |  |  |

