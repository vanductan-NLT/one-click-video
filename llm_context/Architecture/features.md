### **1\. Tổng quan module**

| \# | Module | Mô tả   | Ưu tiên | Ghi chú |
| ----- | ----- | ----- | ----- | ----- |
| M0 | Architecture | Thiết lập nền tảng ban đầu cho hệ thống, bao gồm cấu hình môi trường, tích hợp bên thứ ba, deployment và hạ tầng kiểm thử để bảo đảm dự án vận hành ổn định | 1 |  |
| M1 | Quản lý & Giao diện Người dùng (Web App) | Upload, quản lý file, theo dõi tiến trình real-time, dashboard cơ bản, preview, error handler thân thiện (YouTube-style) | 1 | Cửa ngõ chính → user phải vào được hệ thống trước  |
| M2 | Xử lý Video Tự động (Core Engine) | Xử lý video dài → silence removal, ASR word-level timestamps, JSON structured output, B-roll insertion (Pexels API), text/keyword overlay, effects/SFX/music insertion, final render MP4 | 1 |  |
| M3 | Tạo Video Ngắn (Shorts/Reels) | Auto detect viral hook, crop 9:16/face tracking, tạo sub karaoke-style/animated captions, render shorts với virality score cơ bản | 2 |  |
| M4 | Cơ sở dữ liệu (Databas) | PostgreSQL schema cho video/job/user/license, status tracking, transcript/JSON structured, … | 1 |  |
| M5 | Tạo Nội dung & Marketing (Generative AI) | Tạo caption, kịch bản, bài social, infographic từ transcript/video, AI suggest keyword/hashtag | 2 |  |
| M6 | Đăng bài đa nền tảng (Social Integration) | Kết nối OAuth (FB/IG/TikTok/YouTube/LinkedIn), lên lịch/đăng, duyệt bài, report status (success/fail/views), … | 3 |  |
| M7 | Quản lý License & Activation | Check key khi khởi động/request, hết hạn → lock/read-only, chống crack (offline crypto \+ online fallback), cấp credential tự động sau payment | 1 |  |
| M8 | Hệ thống Queue & Resource Management | Giới hạn concurrent render (max 2), queue job (Redis), limit CPU/RAM per container, graceful shutdown | 1 | Ngăn server crash khi nhiều video nặng  |
| M9 | Storage & File Management | Input/output video, asset library (elements/SFX/music), S3, volume mapping an toàn, preview thumbnail | 1 |  |
| M10 | Monitoring, Logging & Error Handling | Structured log (JSON), error code table, basic dashboard tiến trình/job status, FAQ troubleshoot, container health check | 2 | Giúp debug & support khách  |
| M11 | Backup & Data Persistence | Auto backup DB \+ volume video (cron/snapshot), restore an toàn | 3 | Quan trọng dài hạn cho self-hosted |
| M12 | Thanh toán | Payment gateway (Stripe/PayPal) → trigger license/credential email, subscription recurring | 3 |  |

### **2\. Feature chi tiết** 

**Version 1.1 – Core MVP** 

| Feature | Module | Tên tính năng | Mô tả  | Ưu tiên |
| ----- | ----- | ----- | ----- | ----- |
| F1 | M7 | Set up License Key logic, validation | Offline crypto check \+ online fallback, cấp JWT session | 1 |
| F2 | M1 | Xử lý upload video lớn (resumable upload \+ presigned url) | Chunk upload, resume/retry, progress real-time | 1 |
| F3 | M9 | Quản lý input/output video | Docker volume mapping, list/preview thumbnail/download | 1 |
| F4 | M4 | Set up database | Cơ bản cho MVP | 1 |
| F5 | M8 | Job queue render | Enqueue job, limit concurrent 1–2 | 1 |
| F6 | M2 | Preprocessing: silence removal | Tự động cắt đoạn lặng | 1 |
| F7 | M2 | ASR: word-level timestamps | Audio → text \+ timestamps \[{word, start, end}\] (WhisperX/faster-whisper) | 1 |
| F8 | M2 | Generate JSON structured output |  | 1 |
| F9 | M2 | B-roll insertion (Pexels API) | Keyword → search Pexels video → chèn ngắn vào vị trí hợp lý | 2 |
| F10 | M2 | Text insertion (keyword overlay) | Zoom/pop text tại word position (Remotion) | 2 |
| F11 | M2 | Final render MP4 HD | Ghép layer → output MP4, progress tracking | 1 |
| F12 | M1 | Dashboard upload/progress/storage | YouTube-style UI, toast error thân thiện | 1 |

**Version 1.2 – Elements Library & Preview**  

| Feature | Module | Tên tính năng | Mô tả ngắn gọn | Ưu tiên |
| ----- | ----- | ----- | ----- | ----- |
| F13 | M9 | Thư viện elements (animation, transition, highlights, background, effects) | Lưu trữ \+ quản lý trên storage | 1 |
| F14 | M9 | Thư viện SFX \+ background music | Quản lý, symlink/manifest | 1 |
| F15 | M1 | Preview elements/SFX qua web | Remotion composition preview | 1 |
| F16 | M2 | Update Agent skills cho elements/SFX hiện có |  | 2 |

**Version 1.3 – Full Pipeline & Agent Skills Hoàn chỉnh** 

| Feature | Module | Tên tính năng | Mô tả ngắn gọn | Ưu tiên |
| ----- | ----- | ----- | ----- | ----- |
| F17 | M2 | Pipeline hoàn chỉnh | Silence \+ ASR \+ JSON \+ B-roll \+ Effects \+ SFX \+ Music insertion \+ Preview (Remotion) | 1 |
| F18 | M2 | Video render hiệu quả | Full layer composition, tối ưu thời gian | 1 |
| F19 | M9 | Lưu final video durable | Output hợp lý, backup strategy cơ bản | 2 |
| F20 | M1 | Xử lý pipeline UI | Progress chi tiết, thông báo user, error handler nâng cao | 1 |
| F21 | M7 | Update Agent skills/rules hoàn chỉnh | Bộ rules edit thông minh | 2 |

**Version 1.4 – Payment \+ Polish \+ Stress**

| Feature | Module | Tên tính năng | Mô tả ngắn gọn | Ưu tiên |
| ----- | ----- | ----- | ----- | ----- |
| F22 | M11 | Payment web → trigger license email | Test flow thanh toán → cấp credential tự động | 2 |
| F23 | M10 | Stress tests concurrent | Upload/render nhiều user cùng lúc | 2 |
| F24 | M1 | Tối ưu UI/UX | Config insertion user, credential trên web | 1 |

**Version 2**

**Version 3**