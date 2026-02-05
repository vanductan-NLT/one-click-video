### **1\. Entities** 

| Entity | Module | Mô tả & Invariants | Attributes  | Domain Events  | Phase |
| ----- | ----- | ----- | ----- | ----- | ----- |
| VideoJob | M2 (Core Engine) | Đại diện 1 job xử lý video (upload → process → render).  Rules: status không thể skip, total duration phải hợp lệ, license valid trước render. | id (UUID), userId, inputFilePath (string), status (Enum: Uploaded, Queued, Processing, Completed, Failed), transcript (Transcript VO), renderConfig (RenderConfig VO), outputFilePaths (list\<string\>), createdAt, updatedAt | VideoJobCreated, VideoJobProcessed, VideoJobFailed | 1 |
| Transcript | M2 | Value Object chứa toàn bộ transcript từ ASR (word-level timestamps).  | fullText (string), words (list\<WordSegment VO\>), sentences (list\<Sentence VO\>), keywords (list\<Keyword VO\>) | TranscriptGenerated | 1 |
| ShortClip | M3 (Shorts/Reels) |  | id, parentVideoJobId, startTime, endTime, hookScore (float), subStyle (Enum: Karaoke, Animated), outputPath | ShortClipRendered | 2 |
| LicenseKey | M7 (License & Activation) | Rules: expiryDate \> now, usageQuota không vượt, không duplicate key. | key (string), userId, status (Active/Expired/Locked), expiryDate, quota (int: số video/tháng), featuresEnabled (list\<string\>) | LicenseActivated, LicenseExpired | 1 |
| AssetPackage | M9 (Storage) | Library assets (elements/SFX/music).  | id, name, type (Enum: Element/SFX/Music), files (list\<AssetFile VO\>), manifest (JSON) | AssetPackageUpdated | 1 |
| PaymentTransaction | M12 (Payment) | Rules: amount \> 0, status không skip. | id, userId, amount (Money VO), status (Pending/Paid/Failed), licenseKeyGenerated | PaymentCompleted | 3 |
| BackupSnapshot | M11 (Backup) |  | id, timestamp, dbDumpPath, volumeSnapshotPath, retentionDays | BackupCreated | 3 |

### **2\. Value Objects** 

| VO | Module | Mô tả | Attributes |
| ----- | ----- | ----- | ----- |
| TimestampRange | M2 | Khoảng thời gian (start – end) cho word/silence/hook.  Rules: start \< end, duration \> 0\. | start (float seconds), end (float) |
| WordSegment | M2 | Từ đơn trong transcript với timestamp. Rules: confidence 0–1. | word (string), start, end, confidence (float) |
| Sentence | M2 | Câu từ words.  Rules: words liên tục. | text (string), start, end, words (list\<WordSegment\>), score |
| Keyword | M2/M5 | Từ khóa extract từ transcript.  Rules: score \> 0\. | text (string), score (float), positions (list\<TimestampRange\>) |
| RenderLayer | M2 | Một layer trong render (video base, text overlay, B-roll, SFX).  Rules: z-index hợp lệ. | type (Enum: Base/Text/Broll/SFX/Music), path (string), startTime, duration, zIndex (int) |
| RenderConfig | M2 | Config render (resolution, format, watermark).  Invariant: resolution chuẩn (HD/4K). | resolution (string e.g. "1920x1080"), format ("mp4") |
| HookSegment | M3 | Đoạn hook viral (phase 2).  Rules: score cao nhất trong video. | start, end, hookScore (float), reason (string) |
| ViralScore | M3 | Điểm viral cho short clip (phase 2).  Rules: 0–100. | score (float), factors (map\<string, float\>) |
| Money | Shared | Giá trị tiền (cho quota/payment).  Rules: amount \>= 0\. | amount (decimal), currency (string e.g. "USD") |

### **3\. Domain Services**

| Domain Service | Module | Mô tả | Input/Output  |
| ----- | ----- | ----- | ----- |
| KeywordExtractorService | M2/M5 | Extract top keywords từ transcript (frequency \+ relevance). | Input: Transcript VO → Output: list\<Keyword VO\> |
| SilenceRule | M2 | Quy tắc detect silence (\>1.5s lặng → cắt). | Input: audio energy levels → Output: list\<TimestampRange\> cần cắt |
| HookDetectionRule | M3 | Detect đoạn hấp dẫn (audio peak \+ sentiment \+ transcript hook words). | Input: Transcript \+ audio metadata → Output: list\<HookSegment\> |
| InsertionRuleEngine | M2/M1 | Quy tắc chèn layer (text tại keyword position, B-roll tại silence gap). | Input: Transcript, RenderConfig → Output: list\<RenderLayer\> |
| LicenseValidationService | M7 | Validate key: expiry, quota, features (pure crypto \+ logic). | Input: LicenseKey, currentUsage → Output: bool valid \+ reason |
| ViralityScorer | M3 | Tính viral score cho short (hook strength \+ duration \+ caption quality). | Input: ShortClip → Output: ViralScore VO |

### **4\. Ports / Interfaces**

| Port/Interface | Layer | Module | Mô tả  | Phase |
| ----- | ----- | ----- | ----- | ----- |
| IVideoRepository | Domain | M2/M4 | save/load/delete VideoJob, findByStatus/UserId | 1 |
| ITranscriptionPort | Domain | M2 | transcribe audio → Transcript VO | 1 |
| IBrollProviderPort | Domain | M2 | search keyword → list\<video clip URL/path\> | 1 |
| IRenderEnginePort | Domain | M2 | render layers → output file path | 1 |
| IAssetStoragePort | Domain | M9 | upload/download asset, get presigned URL, list library | 1 |
| IQueuePort | Application | M8 | enqueue job, get status, limit concurrent | 1 |
| ILicenseValidatorPort | Domain | M7 | validate key offline/online | 1 |
| IGenerativeContentPort | Domain | M5 | generate caption/kịch bản từ transcript | 2 |
| ISocialPublisherPort | Domain | M6 | post clip to platform, schedule | 2 |
| IBackupPort | Application | M11 | create/restore snapshot | 3 |
| IPaymentProviderPort | Application | M12 | process payment, webhook handler | 3 |

