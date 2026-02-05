# THU THẬP YÊU CẦU

[Functional Requirements]()

[Non-Functional Requirements]()

# Functional Requirements

### **1\. Xử lý Video Tự động** 

* **Tự động xử lý Video dài (Youtube/Raw):**  
  * **Auto-cut (Cắt đoạn thừa):** Tự động phát hiện khoảng lặng (silence detection) và cắt bỏ các đoạn "dead air".  
  * **Auto-insert B-roll:** Phân tích kịch bản (transcript) để tìm và chèn video/ảnh minh họa từ kho API (Pexels, Storyblocks...).  
  * **Auto-insert Elements:** Chèn Intro, Outro, Lower-third, Transition theo Brand Identity.  
  * **Auto-insert SFX:** Phân tích ngữ cảnh để chèn hiệu ứng âm thanh (vỗ tay, cười...).  
  * **Tạo phụ đề (Speech-to-Text):** Sử dụng Whisper để tạo file sub (.srt/.vtt) có timestamp chuẩn.  
  * **Xuất Video (Rendering):** Render tổ hợp các layer thành file .mp4 hoàn chỉnh (HD/4K).  
* **Tự động tạo Video ngắn (Shorts/TikTok):**  
  * **Phát hiện Viral Hooks:** Tự động phát hiện các đoạn hấp dẫn trong video dài để cắt thành clip ngắn.  
  * **Auto-crop (Face Detection):** Chuyển khung hình từ ngang (16:9) sang dọc (9:16) và giữ chủ thể ở giữa.  
  * **Tạo phụ đề Karaoke:** Render video ngắn kèm phụ đề hiệu ứng nhảy chữ.

  ### **2\. Tạo Nội dung & Marketing** 

* **Tạo Kịch bản & Caption:** Sử dụng LLM để tóm tắt nội dung video, viết tiêu đề, mô tả hoặc kịch bản quay lại.  
* **Tạo bài viết Social:** Tạo nội dung text cho bài đăng dựa trên phụ đề video.  
* **Tạo hình ảnh/Infographic:** Tạo ảnh minh họa khớp với Brandkit sử dụng AI.  
* **Quản lý đăng bài đa nền tảng:**  
  * Kết nối tài khoản (OAuth 2.0) với Facebook, LinkedIn, Instagram.  
  * Tự động đăng video, ảnh, caption lên các nền tảng theo lịch hoặc tức thì.

  ### **3\. Quản lý & Giao diện Người dùng (Web App)**

* **Upload & Quản lý File:**  
  * Giao diện upload video gốc (hỗ trợ file lớn, resume upload).  
  * Kho lưu trữ video (Giao diện quản lý file Input/Output).  
* **Theo dõi tiến trình:**  
  * Hiển thị trạng thái xử lý video (Processing status).  
  * Giao diện xem trước (Preview) và tải xuống thành phẩm.  
* **Quản lý tài khoản & License:**  
  * Xác thực License Key (Chống dùng lậu, check hạn bản quyền).  
  * Cơ chế khóa tính năng hoặc chuyển về Read-only khi hết hạn.

  ### **4\. Hệ thống & Vận hành**  

* **Thông báo lỗi (Error Handling):** Gửi cảnh báo qua Webhook (Telegram/Slack) khi render thất bại hoặc lỗi API.  
* **Tự động dọn dẹp:** Script xóa file tạm/video gốc cũ để giải phóng dung lượng server.  
* **Giám sát:** Dashboard giám sát tài nguyên server cho khách hàng.

# Non-Functional Requirements

### **A. Quy mô và Hiệu năng**

* **Số lượng người dùng:**

  * **DAU (Daily Active Users) dự kiến tối đa:** **\~50 users** (Dựa trên công suất Server hiện tại được cấu hình cho mức Tối đa).  
  * **Peak concurrent users (Người dùng render cùng lúc):** **2 users**. (Cấu hình Nginx/Queue giới hạn max 2 video xử lý đồng thời để tránh sập server).  
* **Khối lượng dữ liệu:**

  * **Requests per second (RPS):** Thấp (Dự kiến \< 10 RPS cho các thao tác Web UI). Hệ thống chủ yếu chịu tải ở tác vụ nền (background job).  
  * **Tổng dung lượng data hiện tại:** **500GB \- 1TB**. (Dựa trên cấu hình S3 Storage dự kiến).  
  * **Tốc độ tăng trưởng data:** Phụ thuộc vào [chính sách xóa file tạm (Temp file)]() cũ hơn X ngày.  
* **Latency yêu cầu:**

  * **API response time mong đợi (Web UI):** **\< 500ms** cho các thao tác CRUD cơ bản.  
  * **Video Processing Time (Render):** Chấp nhận độ trễ cao. Cấu hình timeout lên tới **600s (10 phút)** để tránh ngắt kết nối khi xử lý video nặng. Người dùng chỉ cần chờ video được upload (5-10p) và có thể tắt trình duyệt khi bắt đầu xử lý trong nền.  
  * **Page load time chấp nhận được:** **\< 2 giây**.  
* **Throughput:**

  * **Số requests hệ thống cần xử lý mỗi giây:** Thấp.  
  * **Bandwidth yêu cầu:** Cần băng thông lớn cho Upload/Download. Cấu hình Nginx cho phép upload file lên tới **1GB \- 5GB**.

### **B. Tính Khả dụng và Độ tin cậy**

* **Availability target:**

  * **SLA mong muốn:** **99.99%** (Tương ứng với cam kết của AWS S3).  
* **Consistency requirements:**

  * **Strong Consistency:** Cho dữ liệu người dùng, License Key, thanh toán.  
  * **Eventual Consistency:** Cho trạng thái xử lý Video (Video đang render \-\> Render xong).  
  * **Độ trễ đồng bộ dữ liệu chấp nhận được:** Thấp, sử dụng Redis Queue để đảm bảo thứ tự xử lý.  
* **Data durability:**

  * **RPO (Recovery Point Objective):** \< 24 giờ ([Backup dữ liệu hàng ngày]()).  
  * **Cơ chế bảo vệ:** Dữ liệu Video gốc và Final lưu trên S3 (Object Storage) để đảm bảo không mất dữ liệu khi xóa container,.

### **C. Bảo mật**

* **Authentication & Authorization:**

  * **Phương thức xác thực:**  
    * **License Key:** Kiểm tra bản quyền khi khởi động app.  
    * **OAuth 2.0:** Kết nối với Facebook, LinkedIn, Instagram để đăng bài.  
* **Data protection:**

  * **Dữ liệu cần mã hóa:**  
    * **At rest:** Mật khẩu DB, API Key bên thứ 3 (OpenAI, OpusClip) lưu trong file .env,.  
    * **In transit:** Bắt buộc HTTPS.  
  * **Compliance requirements:** Tuân thủ chính sách của các nền tảng Social (TikTok/FB API policies).  
* **API security:**

  * **Rate limiting yêu cầu:** Cấu hình Queue giới hạn số lượng video render đồng thời.  
  * **API authentication method:** API Key/Token cho giao tiếp nội bộ và License Key cho Client.  
  * **Network Security:** Cấu hình tường lửa chỉ mở port 80/443 và SSH, chặn port Database từ bên ngoài.

### **D. Khả năng mở rộng**

* **Scalability requirements:**  
  * **Hệ thống cần scale theo chiều ngang hay chiều dọc?**  
    * Dọc  
  * **Có cần auto-scaling không?** Hiện tại chưa cần.  
  * **Dự kiến tăng trưởng:** Từ 1 tài khoản lên \~50 **users** trên hạ tầng hiện tại.

### **E. Vận hành** 

* **Monitoring & Observability:**

  * **Metrics cần theo dõi:** CPU/RAM usage (tránh OOM Kill khi render), Disk space (tránh full ổ cứng do file tạm), Queue size (số lượng video đang chờ).  
  * **Alerting thresholds:** Cảnh báo khi render thất bại hoặc API lỗi qua Webhook (Telegram/Slack/Discord).  
* **Maintenance window:**

  * **Cơ chế dọn dẹp:** Script tự động xóa file tạm/video gốc cũ hơn X ngày.

# Chính sách xóa file

#### **Giai đoạn 1: Hết hạn License \- "Chế độ Read-only"**

* **Thời điểm:** Ngay khi hết hạn gói (Day 0).  
* **Hạ tầng:** VPS vẫn chạy, S3 vẫn chạy.  
* **Hành động (Dựa trên module Licensing):**  
  * Hệ thống kiểm tra License Key Trả về Expired.  
  * Giao diện Web khóa nút **"Render/Create New"** (tác vụ tốn CPU).  
  * Giao diện Web vẫn cho phép **Xem/Tải xuống** video cũ.  
* **Mục tiêu:** Nhắc nhở khách gia hạn mà không gây khó chịu, giảm tải cho Server vì không có render nặng.

#### **Giai đoạn 2: Thời gian ân hạn  \- "Chỉ còn kho lạnh"**

* **Thời điểm:** Sau khi hết hạn X ngày (ví dụ: Day 7).  
* **Hành động Kỹ thuật (Quan trọng):**  
  * **Trigger Script "Takeout":** Hệ thống tự động quét tất cả Video Final trong S3 của khách.  
  * **Generate Presigned URLs:** Tạo danh sách link tải trực tiếp từ S3 (có hạn dùng 30 ngày) cho các video này.  
  * **Gửi Email:** Gửi danh sách link này vào email khách hàng với thông điệp: *"Server của bạn sẽ bị hủy trong 24h tới. Đây là link tải dự phòng, có hiệu lực trong 30 ngày."*  
  * **Hủy VPS:** Gọi API lên Cloud Provider (AWS/Hetzner) để **Terminate (Xóa)** VPS của khách hàng đó.  
* **Kết quả:**  
  * **Chi phí:** Bạn cắt được ngay khoản $60 tiền VPS. Chỉ tốn vài đồng lẻ cho S3 lưu trữ trong 30 ngày tiếp theo.  
  * **Trải nghiệm:** Khách hàng vẫn tải được video (qua email) dù không còn vào được Web App.

#### **Giai đoạn 3: Dọn dẹp hoàn toàn**  

* **Thời điểm:** Sau 30 ngày kể từ khi hủy VPS.  
* **Hành động:**  
  * Cấu hình **S3 Lifecycle Rule**: Tự động xóa toàn bộ object trong Bucket của khách hàng đó.  
  * Xóa Bucket S3 và các tài nguyên liên quan (IP tĩnh, DNS record).  
* **Kết quả:** Dữ liệu bị xóa vĩnh viễn, chi phí về 0\.

# Chiến lược backup

### **1.Critical Data \- Bắt buộc Backup**

* **A. Cơ sở dữ liệu (PostgreSQL)**

  * **Tại sao:** Tài liệu WBS mô tả Database là "Sổ cái kế toán & Danh sách khách hàng", chứa thông tin user, lịch sử thanh toán, metadata của video. Nếu mất cái này, khách hàng sẽ mất toàn bộ thông tin về các video đã làm.  
  * **Chiến lược:**  
    * Thực hiện **Automated Backups** (Sao lưu tự động) định kỳ (ví dụ: hàng ngày) bằng script pg\_dump.  
    * Trong module "Kiểm thử triển khai" của WBS có yêu cầu test việc "Thử xóa database... và thực hiện khôi phục lại từ file backup" để đảm bảo tính toàn vẹn.  
* **B. File Cấu hình Môi trường (.env)**

  * **Tại sao:** File .env chứa các biến môi trường cực kỳ nhạy cảm như: DB\_PASSWORD, LICENSE\_KEY, S3\_ACCESS\_KEY, OPENAI\_API\_KEY,.  
  * **Rủi ro:** Nếu mất file này, hệ thống Docker container sẽ không thể khởi động lại được, và không thể kết nối tới kho video trên S3.  
  * **Chiến lược:** Cần hướng dẫn khách hàng lưu trữ file này ở một nơi an toàn ngoài server (ví dụ: máy tính cá nhân) ngay sau khi cài đặt xong.

### **2\. Media Assets \- Backup dựa trên Kiến trúc**

* **A. Video Gốc & Thành phẩm (Lưu trên S3)**

  * **Tại sao:** Tài liệu hạ tầng định nghĩa S3 là "Kho lạnh", nơi chứa nguyên liệu và món ăn đã nấu xong.  
  * **Chiến lược:** **Không cần backup thủ công**. Các dịch vụ Object Storage (AWS S3/Cloudflare R2) đã có độ bền dữ liệu cực cao (99.999999999%),. Bạn chỉ cần đảm bảo không xóa nhầm bucket.

# ƯỚC LƯỢNG VÀ TÍNH TOÁN QUY MÔ

[Capacity]()  
[Xác định Bottlenecks tiềm ẩn]()

# Capacity

#### **A. Ước lượng Traffic**  

* **Dữ liệu đầu vào:**

  * Max users (Hệ thống hiện tại): **\~50 users** .  
  * Hành vi người dùng: Upload video, config và render.  
  * Giới hạn hệ thống: Cấu hình Queue giới hạn **Max 2 video** được render cùng lúc để tránh sập server.  
* **Tính toán:**

  * **Average Traffic:** Rất thấp (chủ yếu là thao tác UI).  
  * **Critical Metric:** Số lượng Job Render đồng thời.  
  * **Peak Concurrency:** **2 Jobs**. Nếu user thứ 3 bấm "Render", hệ thống sẽ đẩy vào hàng đợi (Redis Queue).  
  * **Kết luận:** Server không lo về số lượng request API (RPS), mà lo về CPU/RAM khi Render.

#### **B. Ước lượng Storage** 

* **Giả sử (Dựa trên WBS):**

  * Số lượng user: **50 users** .  
  * Kích thước file upload tối đa: **1GB \- 3GB/video** (Cấu hình Nginx cho phép max body size lớn).  
  * Tần suất: Giả sử mỗi user active làm 1 video/ngày (mức cao điểm).  
  * Dung lượng trung bình: Input (2GB) \+ Output (1GB) \= **3GB/transaction**.  
* **Tính toán:**

  * Storage/ngày (nếu full 50 user hoạt động): 50 x 3GB \= 150GB/ngày.  
  * Chính sách dọn dẹp (Retention Policy): WBS có task viết script xóa file tạm cũ hơn X ngày. Giả sử giữ file trong **7 ngày**.  
  * Tổng Storage cần thiết duy trì: 150GB x 7 xấp xỉ 1,050GB \= 1TB$.  
* **Đối chiếu hạ tầng:**

  * Tài liệu "Chi phí hàng tháng" đã phân bổ gói S3 Storage: **500GB \- 1TB**.  
  * **Kết luận:** Dung lượng 1TB là vừa đủ cho quy mô 50 accounts với chính sách dọn dẹp định kỳ 7 ngày.

#### **C. Ước lượng Bandwidth**  

* **Tính toán:**

  * Upload Traffic (đỉnh điểm): Giả sử 5 user cùng upload file 2GB trong cùng 1 giờ.  
  * 5 x 2GB \= 10GB.  
  * Tốc độ trung bình cần thiết: 10GB / 3600s \= 2.8 MB/s \= 23 Mbps.  
* **Đối chiếu hạ tầng:**

  * Các gói VPS thường có port speed **1Gbps \- 10Gbps**.  
  * **Kết luận:** Băng thông mạng không phải là vấn đề. Tuy nhiên, cần cấu hình Nginx client\_max\_body\_size và proxy\_read\_timeout lên 600s để tránh ngắt kết nối khi mạng user yếu.

#### **D. Ước lượng Memory (RAM) & Cache**

Khác với ứng dụng thông thường cache dữ liệu đọc, Crownmercado cần RAM chủ yếu để "nuôi" tiến trình Render (FFmpeg/Remotion).

* **Dữ liệu đầu vào:**

  * Server RAM: **16GB**.  
  * Web UI (Container): Giới hạn max **1GB RAM**.  
  * Redis (Cache/Queue): Dùng để lưu hàng đợi số thứ tự xử lý video.  
* **Tính toán:**

  * Redis Cache Size: Metadata của Queue rất nhẹ (Text), chỉ tốn \< **100MB RAM**.  
  * Render Memory: 16GB Tổng \- 1GB Web \- 1GB System/Redis \= **14GB Free**.  
  * Nếu chạy 2 Concurrent Jobs: Mỗi Job có thể dùng tối đa **7GB RAM**.

### 

| Thông số | Giá trị Ước lượng | Ghi chú & Giải pháp |
| ----- | ----- | ----- |
| **Max Active Users** | 50 Accounts | Giới hạn bởi năng lực xử lý Server hiện tại. |
| **Concurrent Renders** | 2 Threads | Cấu hình trong Worker Queue. Vượt quá sẽ phải chờ. |
| **Daily Storage Growth** | \~150GB/ngày | Nếu full tải. Cần script tự động xóa file cũ sau 7 ngày. |
| **Total Storage Required** | 1TB | Khớp với gói chi phí hạ tầng đã duyệt (S3/R2). |
| **RAM Requirement** | 16GB  |  |

# Xác định Bottlenecks tiềm ẩn

#### **1\. Database có chịu được write/read load không?**

* **Đánh giá:** **CÓ**.  
* **Phân tích:**  
  * Hệ thống sử dụng **PostgreSQL** cho dữ liệu người dùng và **Redis** cho hàng đợi.  
  * Với quy mô \~50 users hoạt động, lượng request (RPS) vào database rất thấp (chủ yếu là metadata video, user profile). Database không phải là vấn đề về hiệu năng xử lý.  
* **Rủi ro tiềm ẩn:**  
  * **Connection Exhaustion:** Nếu không cấu hình Max Connections phù hợp với RAM của server, database có thể bị sập khi container Web tạo quá nhiều kết nối.  
  * **Giải pháp:** Cấu hình Connection Pool và giới hạn max connections trong file docker-compose hoặc config của DB.

#### **2\. Network bandwidth có đủ không?**

* **Đánh giá:** **CÓ**, nhưng **Timeout** là vấn đề lớn hơn Bandwidth.  
* **Điểm nghẽn (Bottleneck):**  
  * Kết nối giữa Client và Server có thể bị ngắt (Time-out) trước khi upload xong nếu mạng người dùng yếu.  
  * Nginx mặc định chặn file lớn (\>1MB).  
* **Giải pháp đã có trong WBS:**  
  * Tăng client\_max\_body\_size lên 1GB-3GB.  
  * Tăng proxy\_read\_timeout và keepalive\_timeout lên 600s (10 phút).

#### **3\. Single points of failure (SPOF) ở đâu?**

* **Hạ tầng (Critical SPOF):**  
  * **Single VPS:** Toàn bộ Web, DB, Worker, Redis chạy trên 1 VPS. Nếu VPS này sập (mất điện, lỗi phần cứng), toàn bộ hệ thống "Crownmercado" ngừng hoạt động.  
* **Phụ thuộc bên thứ 3 (Business SPOF):**  
  * **OpusClip/Klap API:** Nếu các bên này thay đổi chính sách giá hoặc đóng API, tính năng "Auto Viral" (cắt short video) sẽ tê liệt ngay lập tức.  
  * **OpenAI API:** Nếu OpenAI bị lỗi (downtime), tính năng viết kịch bản và sub sẽ không hoạt động.  
* **Dữ liệu (Data SPOF):**  
  * Nếu ổ cứng VPS bị hỏng và chưa kịp đồng bộ lên S3 hoặc chưa backup DB, dữ liệu sẽ mất vĩnh viễn.

#### **4\. Component nào có thể trở thành bottleneck khi scale?**

* **A. CPU & RAM (Render Workers) \- Bottleneck lớn nhất:**

  * **Vấn đề:** Quá trình render video (FFmpeg/Remotion) cực kỳ tốn RAM và CPU. Tài liệu ghi rõ: "Nếu 1000 khách cùng bấm Tạo Video... server sẽ sập ngay lập tức".  
  * **Giới hạn hiện tại:** Cấu hình hàng đợi (Queue) chỉ cho phép **Max 2 video** xử lý cùng lúc.  
  * **Tác động khi Scale:** Khi user thứ 3, 4, 5 bấm render, họ sẽ phải chờ rất lâu (xếp hàng).   
* **B. Disk Space (Dung lượng ổ cứng):**

  * **Vấn đề:** File video gốc và file tạm (temp) trong quá trình render sinh ra rất nhanh.  
  * **Rủi ro:** Nếu không có script dọn dẹp, ổ cứng server sẽ đầy sau khoảng 1 tuần, dẫn đến server bị treo, không thể ghi log hay database.  
  * **Giải pháp:** Bắt buộc có Cronjob xóa file temp cũ hơn X ngày.

### 

| Thành phần | Trạng thái | Điểm nghẽn tiềm năng | Giải pháp (Mitigation) |
| ----- | ----- | ----- | ----- |
| **Database** | Ổn định (Low Load) | Connection Limit | Cấu hình Pool Size phù hợp RAM. |
| **Network** | Ổn định (High Latency) | Upload Timeout | Tăng Nginx Timeout lên 600s. |
| **Storage (Disk)** | Tăng nhanh | Disk Full (Đầy ổ) | Script auto-clean file tạm \+ Mount S3. |
| **Dependency** | Rủi ro cao | 3rd Party API Down | Chấp nhận rủi ro (Phase 1), Code lỏng (Loose coupling). |

# THIẾT KẾ KIẾN TRÚC TỔNG QUAN

[High-Level Architecture]()  
[Database]()  
[Cache]()

# High-Level Architecture

### **A. Sơ đồ và Các thành phần chính**

#### **1\. Danh sách Components** 

* **Client:** Trình duyệt Web (Next.js).  
* **Reverse Proxy / Gateway:** **Nginx**. Đóng vai trò cổng vào duy nhất, xử lý SSL và điều hướng request vào container Web.  
* **Web Server (API Container):** Xử lý logic nghiệp vụ, xác thực (Auth), quản lý file, gọi API bên thứ 3 (OpenAI, Social).  
* **Worker Server (Engine Container):** Chứa FFmpeg/Remotion. Chuyên thực hiện tác vụ nặng: Cắt, ghép, render video. Tách biệt với Web Server để tránh làm treo giao diện,.  
* **Database:** **PostgreSQL**. Lưu trữ thông tin user, metadata video, lịch sử render.  
* **Message Queue:** **Redis**. Đóng vai trò hàng đợi để trung chuyển job từ Web sang Worker.  
* **File Storage:**  
  * **Local Volume (SSD):** Lưu file tạm (temp), cache trong quá trình render.  
  * **Object Storage (S3):** Lưu trữ dài hạn video gốc và video thành phẩm.  
* **External Services:** OpenAI (Whisper/GPT), OpusClip, Facebook/TikTok API.

#### **2\. Mô tả Luồng dữ liệu**  

**Luồng 1: Upload Video**  

1. **Client** gửi file qua HTTPS → **Nginx** (Cấu hình client\_max\_body\_size lớn).  
2. **Nginx** → **Web Container**.  
3. **Web Container** ghi file vào **Local Volume** (để xử lý nhanh) đồng thời upload bản backup lên **S3** (để lưu trữ an toàn).  
4. **Web Container** ghi metadata (tên file, path) vào **PostgreSQL**.

**Luồng 2: Xử lý & Render Video**  

1. **Client** bấm "Render" → **Web Container**.  
2. **Web Container** tạo một "Job" (chứa ID video, config) → Đẩy vào **Redis Queue**.  
3. **Web Container** trả về response "Processing" cho Client ngay lập tức (Non-blocking).  
4. **Worker Container** (đang lắng nghe Redis) →Lấy Job ra.  
5. **Worker** đọc file từ **Local Volume** → Gọi FFmpeg/AI để xử lý → Render ra file MP4 cuối cùng.  
6. **Worker** upload file MP4 lên **S3** → Cập nhật trạng thái "Done" vào **PostgreSQL**.  
7. **Worker** xóa file tạm ở Local (theo chính sách dọn dẹp).

### **B. Pattern phù hợp**

1. **Architecture Pattern:** **Module hóa**  
2. **Concurrency Pattern:** **Producer-Consumer (Event-driven)**  
   * *Thành phần:* Web Server (Producer) → Redis (Queue) → Worker (Consumer).  
   * *Lý do:* Render video là tác vụ rất nặng (CPU bound). Nếu xử lý trực tiếp (Synchronous), Web Server sẽ bị treo, timeout (Nginx lỗi 504). Cần dùng Queue để xử lý bất đồng bộ và giới hạn số lượng render đồng thời (Max 2 jobs).  
3. **Storage Pattern:** **Hybrid Storage**  
   * Sử dụng SSD cục bộ cho tốc độ xử lý (High I/O) và S3 cho lưu trữ lâu dài (Low cost/Scalability).

### **C. Communication Protocols**

1. **Client \- Server:** **HTTPS REST API**  
2. **Web Container \- Worker Container:** **HTTPS REST API**  
3. **App \- Database:** **HTTPS REST API**  
   * *Lưu ý:* Cấu hình Max Connections để tránh sập DB khi Worker chạy đa luồng.  
4. **Server \- External (OpenAI/Social):** **HTTPS REST API**  
   * *Lưu ý:* Cần cơ chế Retry khi gọi API bên thứ 3 thất bại (Network glitch).

# Database

### **1\. Lựa chọn**

* **Database:** PostgreSQL (AWS RDS).

### **2\. Thiết kế Schema Chi tiết**  

#### **Nhóm 1: Quản lý Người dùng & Bản quyền**  

**users**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| email | VARCHAR(255) | UNIQUE, NOT NULL |  |
| pw\_hash | VARCHAR | NOT NULL | Bcrypt/Argon2 |
| role | VARCHAR(20) | DEFAULT 'user' | 'admin', 'user' |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**licenses** 

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| user\_id | INT | FK \-\> users.id |  |
| license\_key | VARCHAR(64) | UNIQUE, NOT NULL | Khóa bản quyền |
| status | VARCHAR(20) | DEFAULT 'active' | 'active', 'expired', 'banned' |
| expires\_at | TIMESTAMP | NOT NULL | Ngày hết hạn |

#### **Nhóm 2: Quản lý Tài sản** 

**projects**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| user\_id | INT | FK \-\> users.id |  |
| name | VARCHAR(255) | NOT NULL |  |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**videos (Input Files)**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| project\_id | INT | FK \-\> projects.id |  |
| original\_filename | VARCHAR(255) | NOT NULL | Tên file gốc |
| raw\_s3\_path | VARCHAR(500) | NOT NULL | Path trên S3 (Input) |
| duration\_sec | FLOAT |  | Độ dài video (giây) |
| resolution | VARCHAR(20) |  | '1080p', '4K' |
| file\_size\_bytes | BIGINT |  | Bổ sung để quản lý quota |
| uploaded\_at | TIMESTAMP | DEFAULT NOW() |  |

#### **Nhóm 3: Xử lý Video**  

**jobs**  

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, DEFAULT uuid\_v4() | Dùng UUID để tránh lộ ID tuần tự |
| video\_id | INT | FK \-\> videos.id |  |
| type | VARCHAR(50) | NOT NULL | 'auto-cut', 'viral-shorts', 'add-sub' |
| status | VARCHAR(20) | INDEX | 'pending', 'processing', 'completed', 'failed' |
| progress | INT | DEFAULT 0 | 0 \- 100% |
| config | JSONB |  | Lưu config render (màu sắc, font...) |
| error\_message | TEXT |  |  |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |
| completed\_at | TIMESTAMP |  |  |

**pipeline\_steps (Tracking chi tiết)**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | BIGSERIAL | PK |  |
| job\_id | UUID | FK \-\> jobs.id |  |
| step\_name | VARCHAR(50) | NOT NULL | 'transcribe', 'cut-silence', 'render' |
| status | VARCHAR(20) |  | 'pending', 'running', 'done', 'error' |
| started\_at | TIMESTAMP |  |  |
| finished\_at | TIMESTAMP |  |  |

**segments (Kết quả phân tích AI)**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | BIGSERIAL | PK |  |
| job\_id | UUID | FK \-\> jobs.id |  |
| start\_sec | FLOAT | NOT NULL |  |
| end\_sec | FLOAT | NOT NULL |  |
| type | VARCHAR(20) |  | 'silence', 'speech', 'viral\_hook' |
| text | TEXT |  | Nội dung speech (nếu có) |
| score | FLOAT |  | Điểm viral/energy |

**transcripts (Subtitle)**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| job\_id | UUID | FK \-\> jobs.id |  |
| language | VARCHAR(10) | DEFAULT 'vi' |  |
| s3\_json\_path | VARCHAR(500) |  | File JSON chi tiết từ Whisper |
| raw\_text | TEXT |  | Full text search nếu cần |

**renders (Output Files)**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| job\_id | UUID | FK \-\> jobs.id |  |
| s3\_video\_path | VARCHAR(500) | NOT NULL | Path trên S3 (Output) |
| duration\_sec | FLOAT |  |  |
| download\_url | TEXT |  | Presigned URL (tạm thời) |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

#### **Nhóm 4: Mạng Xã hội**  

**social\_connections**

| Column | Type | Constraints | Note |
| ----- | ----- | ----- | ----- |
| id | SERIAL | PK |  |
| user\_id | INT | FK \-\> users.id |  |
| platform | VARCHAR(20) | NOT NULL | 'facebook', 'tiktok', 'youtube' |
| access\_token | TEXT | NOT NULL | Mã hóa khi lưu |
| refresh\_token | TEXT |  |  |
| expires\_at | TIMESTAMP |  |  |

### **3\. Chiến lược Indexing** 

1. **Tìm việc cho Worker:**

   * CREATE INDEX idx\_jobs\_status\_created ON jobs(status, created\_at);  
   * *Mục đích:* Giúp Worker nhanh chóng tìm các job đang pending cũ nhất để xử lý (First In First Out).  
2. **User xem danh sách Video/Project:**

   * CREATE INDEX idx\_videos\_project ON videos(project\_id);  
   * CREATE INDEX idx\_projects\_user ON projects(user\_id);  
3. **Tra cứu Segments (Khi edit timeline):**

   * CREATE INDEX idx\_segments\_job ON segments(job\_id, start\_sec);  
   * *Mục đích:* Load nhanh các đoạn cắt khi user mở giao diện Editor.

# Cache

### **1\. Xác định Dữ liệu cần Cache**

| Loại Dữ liệu | Tần suất Đọc | Tần suất Ghi | Giải pháp Cache | Lý do |
| ----- | ----- | ----- | ----- | ----- |
| **Trạng thái Job Render** (% progress) | Rất cao (Client poll liên tục) | Cao (Worker update liên tục) | **Redis** | Tránh việc Client "spam" Database chỉ để xem video render được bao nhiêu %. |
| **Cấu hình/License** | Trung bình | Rất thấp | **Redis** | Tránh query DB/API License mỗi khi user chuyển trang. |
| **File Tĩnh (CSS/JS/Logo)** | Cao | Rất thấp | **Browser/Nginx** | Tăng tốc độ load trang Dashboard. |
| **Video Preview** | Trung bình | Thấp | **S3 \+ Browser** | Giảm băng thông tải lại video nhiều lần. |

### **2\. Các tầng Cache**

#### **Tầng 1: Client-Side Cache (Browser & Nginx)**

* **Công nghệ:** Cấu hình **Nginx**.  
* **Chiến lược:**  
  * **Lưu Static Assets (CSS, JS, Images)**.

#### **Tầng 2: Application Cache (Server-side)**

* **Công nghệ:** **Redis**.  
* **Dữ liệu Cache:**  
  1. **Job Progress (Quan trọng nhất):**  
     * Khi Worker render, nó cập nhật tiến độ vào Redis: SET job\_progress:{job\_id} 45 (TTL 1 giờ).  
     * API lấy tiến độ từ Redis trả về cho Client. Không query xuống PostgreSQL.  
  2. **User Session & License:**  
     * Lưu thông tin user và trạng thái License sau khi login.  
     * Key: session:{user\_id}, TTL: 24h.

#### **Tầng 3: Storage Cache (S3 Presigned URL)**

* **Công nghệ:** AWS S3.  
* **Chiến lược:**  
  * Link video (Input/Output) là các **Presigned URL** có hạn (ví dụ: 60 phút).  
  * Browser sẽ cache video dựa trên URL này.

### **3\. Chiến lược Cập nhật & Loại bỏ**  

#### **A. Chiến lược Cập nhật** 

* **Với Job Progress:** Sử dụng chiến lược **Write-Through** (biến thể):  
  * Worker tính toán % → Ghi vào Redis → Ghi vào DB khi hoàn thành (Status: Done).  
  * Lý do: Client cần thấy tiến độ realtime, đọc trực tiếp từ Redis là nhanh nhất.  
* **Với User/Config:** Sử dụng chiến lược **Cache-Aside (Lazy Loading)**:  
  * App cần thông tin user → Hỏi Redis.  
  * Redis Miss → Hỏi DB → Lưu vào Redis → Trả về.  
  * User update profile → Ghi DB → Xóa key trong Redis (Invalidate).

#### **B. Chính sách Loại bỏ**  

Áp dụng **TTL (Time-To-Live)** triệt để để giải phóng RAM cho Video Engine:

1. **Job Progress Key:** TTL \= 3600s (1 giờ).  
   * Nếu Job treo hoặc xong lâu rồi, Redis tự xóa để dọn rác.  
2. **Session Key:** TTL \= 86400s (24 giờ).  
   * Bắt buộc user login lại mỗi ngày để check lại License Key (đề phòng hết hạn).  
3. **Redis Memory Policy:**  
   * Cấu hình maxmemory cho Redis (ví dụ: 512MB).  
   * Cấu hình maxmemory-policy: allkeys-lru: Khi đầy RAM, tự động xóa các key ít dùng nhất để nhường chỗ cho job mới.

# THIẾT KẾ CHI TIẾT CÁC THÀNH PHẦN

[API]()  
[Message Queue]()  
[Storage]()

# API

### **1\. Nguyên tắc chung** 

* **Architectural Style:** **REST API**.  
* **Protocol:** **HTTPS** (Bắt buộc để bảo vệ License Key và Token).  
* **Data Format:** **JSON** cho body request/response.  
* **Versioning:** URL Path Versioning (ví dụ: /api/v1/...).  
* **Authentication:** **JWT (JSON Web Token)**.

### **2\. Danh sách API Endpoints Quan trọng**

#### **A. Nhóm Xác thực & Bản quyền** 

* POST /api/v1/auth/login: Đăng nhập (email/password), trả về Access Token \+ Refresh Token.  
* POST /api/v1/auth/refresh: Lấy token mới khi hết hạn.  
* GET /api/v1/system/license: Kiểm tra trạng thái License Key (Active/Expired).  
  * *Logic:* Middleware sẽ chặn các API tạo video nếu License hết hạn (trả về lỗi 403 Payment Required).

#### **B. Nhóm Quản lý Dự án** 

* GET /api/v1/projects: Lấy danh sách dự án (có phân trang, lọc theo ngày).  
* POST /api/v1/projects: Tạo dự án mới.  
* GET /api/v1/projects/{id}: Lấy chi tiết dự án (bao gồm danh sách video input/output).  
* PUT /api/v1/projects/{id}/config: Cập nhật cấu hình render (JSONB) cho dự án (ví dụ: đổi màu sub, font chữ).

#### **C. Nhóm Upload Video** 

Do file video lớn (1GB-5GB), ta không upload trực tiếp qua API đơn thuần mà dùng cơ chế **Presigned URL** và **Chunk Upload**.

* POST /api/v1/uploads/presigned-url:  
  * *Request:* { "filename": "video.mp4", "file\_size": 2000000, "type": "input" }  
  * *Response:* Trả về URL upload trực tiếp lên S3 (Client PUT thẳng lên S3, không qua Server để giảm tải).  
* POST /api/v1/uploads/complete:  
  * *Request:* { "s3\_key": "path/to/video.mp4", "project\_id": "..." }  
  * *Logic:* Server ghi nhận file vào Database videos, bắt đầu quy trình phân tích background.

#### **D. Nhóm Xử lý Video** 

* POST /api/v1/jobs: Tạo yêu cầu Render.  
  * *Request:* { "project\_id": "...", "type": "auto-cut", "config": {...} }  
  * *Logic:* Đẩy job vào Redis Queue, trả về job\_id ngay lập tức (Async).  
* GET /api/v1/jobs/{id}: Kiểm tra trạng thái Job (Polling).  
  * *Response:* { "status": "processing", "progress": 45, "step": "transcribing" }.  
* POST /api/v1/jobs/{id}/cancel: Hủy job đang chạy (Worker sẽ check flag này để dừng FFmpeg).

#### **E. Nhóm Mạng xã hội**  

* GET /api/v1/social/connect/{platform}: Lấy URL redirect để OAuth với Facebook/TikTok.  
* POST /api/v1/social/posts: Lên lịch đăng bài.  
  * *Request:* { "render\_id": "...", "platforms": \["facebook", "tiktok"\], "scheduled\_at": "2023-10-20T10:00:00Z", "caption": "..." }

### **3\. Quy chuẩn Request & Response**

**Thành công (HTTP 200/201):**

{  
  "status": "success",  
  "data": {  
    "id": "job\_123",  
    "progress": 100,  
    "url": "https://s3..."  
  }  
}

**Thất bại (HTTP 4xx/5xx):**

{  
  "status": "error",  
  "error": {  
    "code": "LICENSE\_EXPIRED",  
    "message": "Gói bản quyền của bạn đã hết hạn. Vui lòng gia hạn để render.",  
    "details": null  
  }  
}

### **4\. Các mã lỗi HTTP** 

* **200 OK:** Thành công (GET, PUT).  
* **201 Created:** Tạo mới thành công (POST job, project).  
* **202 Accepted:** Đã nhận yêu cầu xử lý video (trả về khi đẩy vào Queue).  
* **400 Bad Request:** Dữ liệu đầu vào sai (Validate file type, thiếu params).  
* **401 Unauthorized:** Chưa đăng nhập hoặc Token sai.  
* **402 Payment Required:** **Quan trọng cho Self-host** \- Trả về khi License Key hết hạn hoặc không hợp lệ.  
* **403 Forbidden:** Không có quyền truy cập tài nguyên này.  
* **429 Too Many Requests:** Spam API hoặc vượt quá giới hạn render đồng thời.

### **5\. Cơ chế Bảo mật API**

* **Rate Limiting:** Cấu hình ở Nginx/Middleware (ví dụ: 100 req/phút) để chống DDoS.  
* **Input Validation:** Sử dụng thư viện (như Zod hoặc Joi) để kiểm tra kỹ dữ liệu đầu vào, đặc biệt là các đường dẫn file để tránh lỗi bảo mật.  
* **CORS:** Chỉ cho phép domain của Web App gọi API.

# Message Queue

### **1\. Công nghệ & Mô hình** 

* **Công nghệ:** **Redis**.  
* **Mô hình:** **Producer-Consumer** kết hợp **Work Queue**.  
  * **Producer:** Web API Container (nhận request từ user).  
  * **Queue:** Redis.  
  * **Consumer:** Worker Container (chạy FFmpeg/AI).  
* **Thư viện hỗ trợ:**  
  * Backend là Python: **Celery**.  
  * *Lợi ích:* Các thư viện này tự động xử lý việc retry, priority và delayed jobs tốt hơn tự viết code Redis thuần.

### **2\. Kiến trúc Hàng đợi**

#### **A. render\_queue (Hàng đợi ưu tiên cao & Tốn tài nguyên)**

* **Mục đích:** Xử lý các tác vụ nặng như Auto-cut, Render video, Burn subtitle.  
* **Concurrency Limit:** **Max 2**. (Worker chỉ lấy tối đa 2 job cùng lúc để tránh OOM Kill như đã phân tích ở Phase 2).  
* **Cơ chế:** FIFO (Vào trước ra trước).

#### **B. light\_queue (Hàng đợi tác vụ nhẹ)**

* **Mục đích:** Gửi email, thông báo Slack/Telegram, đăng bài lên Facebook/TikTok, tạo thumbnail ảnh.  
* **Concurrency Limit:** **Max 5-10**. (Các tác vụ này chủ yếu chờ I/O mạng, ít tốn CPU nên có thể chạy nhiều).

### **3\. Thiết kế Cấu trúc Message** 

Dữ liệu đẩy vào Redis (Payload) cần chứa đủ thông tin để Worker tự chạy mà không cần hỏi lại user.

**Ví dụ Payload cho render\_queue (JSON):**

{  
  "job\_id": "uuid-v4-xxxx",  
  "project\_id": "proj\_123",  
  "user\_id": "user\_456",  
  "type": "RENDER\_VIDEO",  
  "payload": {  
    "input\_path": "/data/uploads/video\_raw.mp4",  
    "output\_path": "/data/renders/video\_final.mp4",  
    "config": {  
      "resolution": "1080p",  
      "codec": "h264",  
      "add\_subtitles": true,  
      "cut\_silence\_threshold": \-30  
    }  
  },  
  "created\_at": 1697000000,  
  "retry\_count": 0  
}

### **4\. Chiến lược Xử lý lỗi & Độ tin cậy** 

* **Time-out (Visibility Timeout):**  
  * Render video rất lâu. Cần cấu hình timeout cho Worker là **30 phút**.  
  * Nếu sau 30 phút Worker không báo "Xong", hệ thống coi như Worker bị treo và đẩy job lại vào hàng đợi (hoặc đánh dấu lỗi).  
* **Retry Strategy (Thử lại):**  
  * **Max Retries:** **3 lần**.  
  * **Backoff:** Exponential (Thử lại sau 10s, 30s, 1m).  
* **Dead Letter Queue (DLQ):**  
  * Nếu thử lại 3 lần vẫn thất bại → Chuyển job sang hàng đợi failed\_jobs.  
  * **Hành động:** Gửi thông báo lỗi cho User qua Webhook (Telegram/Email) để kiểm tra thủ công (như mô tả trong module Xử lý lỗi của WBS).

### **5\. Cập nhật Tiến độ**  

Vì render mất nhiều thời gian, Client cần biết tiến độ % để hiển thị thanh loading. Redis Queue mặc định không hỗ trợ cái này tốt, nên ta dùng cơ chế **Cache Update**:

1. **Worker:** Trong lúc render (FFmpeg callback), cứ mỗi 5% lại chạy lệnh: SET job\_progress:{job\_id} 45 (Redis Cache).  
2. **API Server:** Khi Client hỏi GET /jobs/{id}, API đọc giá trị từ Redis trả về ngay lập tức.

# Storage

### **1\. Kiến trúc Lưu trữ**  

#### **A. Tầng Xử lý Nóng (Hot Storage \- Local VPS)**

* **Vị trí:** Ổ cứng của VPS.  
* **Công nghệ:** Docker Volume (Map thư mục host vào container).  
* **Cấu trúc thư mục (Trên Host):**  
  * /data/uploads/: Chứa video gốc vừa upload lên.  
  * /data/temp/: Chứa file rác khi render (chunks, file audio tách rời).  
  * /data/renders/: Chứa video thành phẩm trước khi upload lên S3.

#### **B. Tầng Lưu trữ Lạnh/Ấm (Cold/Warm Storage \- Cloud S3)**

* **Vị trí:** AWS S3.  
* **Cấu trúc Key (S3 Object Key):**  
  * users/{user\_id}/projects/{project\_id}/source/video.mp4  
  * users/{user\_id}/projects/{project\_id}/render/final\_v1.mp4

### **2\. Luồng dữ liệu Upload & Xử lý**  

1. **Bước 1: Upload (Client → VPS):**

   * User upload file 2GB qua trình duyệt.  
   * **Nginx** (đã cấu hình client\_max\_body\_size 5GB và timeout 600s) nhận stream dữ liệu.  
   * **Web Container** ghi trực tiếp luồng dữ liệu vào /data/uploads/ (Sử dụng stream để không ngốn RAM).  
   * *Lưu ý:* Không upload lên S3 ở bước này để tiết kiệm thời gian và băng thông.  
2. **Bước 2: Xử lý (VPS Internal):**

   * **Worker** đọc file từ /data/uploads/ → Cắt/Ghép → Ghi file kết quả vào /data/renders/.  
3. **Bước 3: Đồng bộ & Dọn dẹp (VPS → S3):**

   * Sau khi render xong, Worker upload file thành phẩm từ /data/renders/ lên **S3**.  
   * (Tùy chọn) Upload file gốc lên S3 để backup (nếu gói cước cho phép lưu trữ source).  
   * **Quan trọng:** Xóa file trong /data/uploads và /data/renders ngay lập tức hoặc theo Cronjob để giải phóng SSD VPS.  
4. **Bước 4: Tải xuống (S3 → Client):**

   * Khi user bấm "Download", hệ thống tạo **Presigned URL** từ S3 và trả về cho client. User tải trực tiếp từ S3, không đi qua băng thông của VPS.

### **3\. Các quy định và Giới hạn** 

* **File Size Limit:** **5GB** (Cấu hình cứng ở Nginx và Application Layer).  
* **Allowed Types:** Chỉ chấp nhận .mp4, .mov, .avi, .mkv.  
  * *Bảo mật:* Validate "Magic Bytes" (Header của file) để đảm bảo user không đổi tên file .exe thành .mp4 để upload mã độc.  
* **Naming Convention:**  
  * Không dùng tên file gốc của user để lưu trên đĩa (tránh lỗi ký tự đặc biệt/tiếng Việt).  
  * Đổi tên thành UUID: a1b2-c3d4-e5f6.mp4.

# BẢO MẬT

[Security Architecture]()  
[API Security]()  
[Compliance]()

# Security Architecture

### **A. Network Security** 

1. **Firewall:**  
   * **Công cụ:** Sử dụng **UFW (Uncomplicated Firewall)** trên Linux Host.  
   * **Chính sách:**   
     * ALLOW Port 80 (HTTP) & 443 (HTTPS) → Dành cho Web Traffic.  
     * ALLOW Port SSH (Khuyên đổi từ 22 sang port Custom, ví dụ 2022\) → Dành cho Admin quản trị.  
     * DENY Port 5432 (PostgreSQL) & 6379 (Redis) → Tuyệt đối không public ra Internet, chỉ cho phép truy cập nội bộ qua Docker Network.  
2. **Reverse Proxy:**  
   * **Công cụ:** **Nginx**.  
   * **Vai trò:** Đứng chắn trước Application Container. Ẩn thông tin về công nghệ backend (Node.js/Python) để hacker khó khai thác lỗ hổng đặc thù.  
3. **Transport Security:**  
   * **HTTPS Enforced:** Bắt buộc 100% traffic qua HTTPS.  
   * **HSTS:** Cấu hình header Strict-Transport-Security để chặn tấn công hạ cấp giao thức (Protocol Downgrade).

### **B. Application & API Security** 

1. **Secure File Upload:**  
   * **Validate Magic Bytes:** Kiểm tra chữ ký Hex (Header) của file để đảm bảo file tải lên thực sự là Video (.mp4, .mov), tránh trường hợp hacker đổi tên file .exe thành .mp4 để upload mã độc.  
   * **Path Traversal Prevention:** Tự động đổi tên file upload thành **UUID** (ví dụ: a1b2-c3d4.mp4) để ngăn chặn các tên file chứa ký tự độc hại như ../../etc/passwd.  
   * **Size Limit:** Cấu hình Nginx client\_max\_body\_size 5GB để ngăn chặn tấn công DoS bằng cách upload file khổng lồ làm tràn ổ cứng.  
2. **API Protection:**  
   * **Rate Limiting:** Giới hạn mỗi IP chỉ được gửi 60 requests/phút đến các API tạo job render. Trả về mã lỗi 429 Too Many Requests nếu vượt quá.  
   * **CORS (Cross-Origin Resource Sharing):** Cấu hình Whitelist chỉ cho phép domain của Dashboard gọi API.  
3. **Container Security:**  
   * **Resource Limits:** Cấu hình docker-compose giới hạn RAM/CPU cho từng container (VD: Web UI max 1GB RAM) để tránh một module bị lỗi làm treo cả VPS.

### **C. Authentication & Authorization** 

1. **Authentication:**  
   * **Web Dashboard:** Sử dụng **JWT (JSON Web Token)** lưu trong **HttpOnly Cookie** để chống tấn công XSS.  
   * **Service-to-Service:** Các container nội bộ giao tiếp qua Docker Network, không cần xác thực phức tạp để tối ưu hiệu năng.  
2. **Licensing Guard:**  
   * **Middleware:** Mỗi khi khởi động hoặc thực hiện render, hệ thống kiểm tra LICENSE\_KEY.  
   * **Logic:** Nếu Key hết hạn → Chuyển ứng dụng sang chế độ **Read-only** (Xem được video cũ nhưng không render được video mới).

### **D. Data Protection & Secrets** 

1. **Secrets Management:**  
   * **File .env:** Chứa DB\_PASSWORD, OPENAI\_API\_KEY, AWS\_SECRET\_KEY.  
   * **Permission:** Thiết lập quyền chmod 600 .env trên VPS (Chỉ chủ sở hữu server mới đọc được, user khác không xem được).  
   * **Docker History:** Sử dụng .dockerignore để đảm bảo không bao giờ build file .env vào trong Docker Image.  
2. **Encryption at Rest:**  
   * **Social Tokens:** Mã hóa các Access Token của Facebook/TikTok/YouTube trong Database.  
   * **Passwords:** Băm mật khẩu.  
3. **Data Backup & Integrity:**  
   * **Docker Volumes:** Map dữ liệu ra host để đảm bảo không mất video khi xóa container.  
   * **Automated Backup:** Cronjob chạy pg\_dump database hàng ngày và upload lên S3 riêng biệt.

### **E. Vulnerability Prevention** 

1. **Input Validation:** Sử dụng thư viện để kiểm tra chặt chẽ mọi dữ liệu đầu vào tại tầng API.  
2. **XSS Protection:** Encode dữ liệu đầu ra khi hiển thị trên Frontend. Cấu hình Security Headers (X-XSS-Protection, Content-Security-Policy) tại Nginx.

# API Security

### **1\. HTTPS & Transport Security** 

* **Yêu cầu:** **HTTPS Only**.  
* **Triển khai:**  
  * Sử dụng **Nginx** làm Reverse Proxy.

### **2\. Authentication & Authorization**  

* **Cơ chế xác thực**   
  * Sử dụng **JWT (JSON Web Token)** cho các phiên đăng nhập của User trên Web Dashboard.  
  * **License Middleware:** Trước khi xử lý bất kỳ request nào đến API /api/v1/render, hệ thống phải chạy qua middleware kiểm tra trạng thái License Key (Active/Expired). Nếu hết hạn, trả về lỗi 402 Payment Required và chặn request.

### **3\. Input Validation & File Security**  

* **Validate File Upload:**  
  * **Không tin tưởng đuôi file:** Hacker có thể đổi tên malware.exe thành video.mp4.  
  * **Giải pháp:** API phải đọc **Magic Bytes** (Header hex signature) của file để xác nhận đó thực sự là video (MP4, MOV, AVI) trước khi lưu.  
* **Path Traversal Prevention:**  
  * **Rủi ro:** User đặt tên file là ../../etc/passwd để ghi đè file hệ thống.  
  * **Giải pháp:** API **luôn đổi tên file** thành UUID ngẫu nhiên (ví dụ: a1b2-c3d4.mp4) ngay khi nhận, bỏ qua tên file gốc.  
* **Sanitize Inputs:**  
  * Lọc bỏ các ký tự đặc biệt trong các trường text (như tên dự án, caption) để chống lỗi **XSS** khi hiển thị lại trên Dashboard.

### **4\. Rate Limiting & Resource Quota**  

* **Nginx Level:** Cấu hình limit\_req\_zone để giới hạn số lượng request API từ một địa chỉ IP (ví dụ: 60 requests/phút).  
* **Application Level (Queue):**  
  * API Render không xử lý ngay mà đẩy vào **Redis Queue**.  
  * Giới hạn **Concurrency \= 2** (chỉ 2 video được render cùng lúc). Các request thứ 3, 4 sẽ nằm chờ trong hàng đợi. 

### **5\. CORS & Security Headers**

* **CORS (Cross-Origin Resource Sharing):**  
  * Cấu hình Nginx hoặc Application Middleware để chỉ cho phép các domain tin cậy (Whitelisted Domains) được gọi API.

### **6\. Error Handling**  

* **Nguyên tắc:** Không bao giờ để lộ **Stack Trace** (chi tiết lỗi code) ra ngoài API Response.  
* **Thực hiện:**  
  * Nếu code bị crash, API chỉ trả về thông báo chung chung: { "code": 500, "message": "Internal Server Error" }.  
  * Log chi tiết lỗi vào file log nội bộ (Docker logs) để dev kiểm tra sau.

# Compliance

### **Tuân thủ Chính sách Nền tảng**  

* **Facebook/Instagram & TikTok API:**  
  * **Yêu cầu:** Các nền tảng này yêu cầu ứng dụng phải có tính năng **"Data Deletion Callback"**. Khi người dùng gỡ ứng dụng của bạn khỏi Facebook/TikTok, nền tảng sẽ gửi một request đến server của bạn yêu cầu xóa dữ liệu của người dùng đó.  
  * **Thiết kế:** Cần xây dựng một Webhook endpoint (ví dụ: POST /api/webhooks/facebook/delete-data) để tiếp nhận yêu cầu này và kích hoạt quy trình xóa dữ liệu user tương ứng trong Database.  
* **OpenAI / OpusClip API:**  
  * **Yêu cầu:** Không được lưu trữ các thông tin nhạy cảm hoặc log các prompt vi phạm chính sách nội dung.  
  * **Thiết kế:** Cần có cơ chế **Data Sanitization** (làm sạch dữ liệu) trước khi gửi prompt lên AI, và không log api\_key của khách hàng vào file log server.

# MONITORING & OBSERVABILITY

[Logging]()  
[Metrics and Monitoring]()  
[Alerting Strategy]()

# Logging

### **1\. Xác định nội dung cần Log** 

* **Application Logs (App & Worker):**  
  * Trạng thái Job: Job Created, Rendering Started, Rendering Failed, Job Completed.  
  * **Quan trọng:** Với lỗi Render, phải log được **FFmpeg output** (chi tiết lỗi từ engine xử lý video) để biết tại sao video không xuất ra được.  
* **Access Logs (Nginx):**  
  * Ghi lại mọi request HTTP đến server: IP nguồn, URL truy cập, Mã phản hồi (200, 404, 500), Thời gian phản hồi.  
* **Audit Logs (Hành vi người dùng):**  
  * Ghi lại các hành động nhạy cảm: User A deleted video B, Admin changed config, Login failed.  
  * Giúp khách hàng truy vết nếu dữ liệu bị mất.  
* **System Logs (Docker/Systemd):**

### **2\. Định dạng Log**

* **Cấu trúc:** Sử dụng định dạng **JSON**.  
  * *Lý do:* Máy dễ đọc, dễ dàng tích hợp vào các tool phân tích sau này nếu khách hàng muốn mở rộng.

**Các trường bắt buộc:**  
 {  
  "timestamp": "2023-10-25T14:30:00+07:00", // Timezone UTC+7 theo WBS  
  "level": "ERROR",  
  "service": "worker-engine",  
  "job\_id": "uuid-1234", // Rất quan trọng để trace theo từng video  
  "user\_id": "user\_5678",  
  "message": "FFmpeg process exited with code 1",  
  "error\_stack": "..."  
}

* **Timezone:** Cấu hình đồng bộ múi giờ (UTC+7) cho toàn bộ Container và Host để log khớp với thời gian thực tế của khách hàng.

### **3\. Chiến lược lưu trữ**

* **Cơ chế:** Sử dụng **Docker json-file logging driver**.  
* **Cấu hình giới hạn (Trong docker-compose.yml):**  
  * max-size: "100m" (Mỗi file log tối đa 100MB).  
  * max-file: "3" (Chỉ giữ 3 file log gần nhất).  
  * *Tổng cộng:* Mỗi container chỉ tốn tối đa 300MB ổ cứng cho log. Khi đầy, Docker tự động xóa log cũ nhất.

### **4\. Bảo mật Log** 

Tuân thủ nguyên tắc **"Không log dữ liệu nhạy cảm"**:

* **Redaction (Che dấu):**  
  * Tuyệt đối không log: Password, Social Access Token, OpenAI API Key.  
  * Nếu cần log request body, hãy mask các trường này: api\_key: "sk-\*\*\*\*a1b2".  
* **Access Control:**  
  * File log trên host chỉ được đọc bởi user root hoặc user docker.

# Metrics & Monitoring

#### **A. Infrastructure Metrics** 

1. **CPU Usage:**  
   * *Ngưỡng:* Cảnh báo nếu \> 90% trong 5 phút.  
   * *Ý nghĩa:* Nếu CPU cao liên tục, có thể FFmpeg đang bị treo hoặc cần nâng cấp VPS (Scale-up).  
2. **Memory (RAM) & Swap:**  
   * *Ngưỡng:* Cảnh báo nếu RAM thật \> 85% và Swap \> 50%.  
   * *Ý nghĩa:* Dự báo nguy cơ Container sắp bị OS giết (OOM Kill).  
3. **Disk Usage:**  
   * *Ngưỡng:* Cảnh báo khi ổ cứng đầy \> 80%.  
   * *Ý nghĩa:* Video chưa kịp xóa hoặc log quá nhiều. Nếu đầy 100%, database sẽ lỗi, hệ thống sập toàn diện.

#### **B. Application Metrics** 

1. **Queue Depth:**  
   * *Chỉ số:* Số lượng job đang chờ (waiting) và đang chạy (active).  
   * *Ý nghĩa:* Nếu hàng đợi luôn \> 10 job, nghĩa là Worker xử lý không kịp → Cần thêm Worker hoặc nâng VPS.  
2. **Job Duration:**  
   * *Chỉ số:* Trung bình bao nhiêu phút để render xong 1 phút video.  
   * *Ý nghĩa:* Phát hiện bất thường (VD: Bình thường mất 2 phút, nay mất 20 phút → Có thể do lỗi mạng hoặc code).

#### **C. Business Metrics** 

1. **API Cost Tracking:** Đếm số token OpenAI và số phút OpusClip đã dùng trong ngày.  
2. **Success/Failure Rate:** Tỷ lệ render thành công/thất bại.

# Alerting Strategy

### **1\. Tại sao cần Alerting cho hệ thống này?**

* **Tránh "Im lặng chết chóc":** Video render thất bại do lỗi file nguồn hoặc thiếu RAM, nếu hệ thống không báo gì, khách hàng sẽ chờ mãi và sau đó khiếu nại gay gắt.  
* **Rủi ro Hạ tầng:** Xử lý video ngốn rất nhiều ổ cứng. Nếu đầy ổ cứng (Disk Full) mà không cảnh báo để dọn dẹp, toàn bộ database và docker sẽ sập, có thể gây lỗi dữ liệu.  
* **Quản lý chi phí API:** Nếu tài khoản OpenAI hoặc OpusClip hết tiền (Credit), tính năng sẽ dừng hoạt động. Cần báo ngay để Admin nạp tiền.

### **2\. Kênh cảnh báo**  

* **Telegram/Slack/Discord Webhook:** Gửi tin nhắn tức thì vào nhóm chat của Admin hoặc gửi trực tiếp cho User.

# DISASTER RECOVERY & HIGH AVAILABILITY

[Backup]()  
[Availability Design]()

# Backup

### **A. Backup Requirements**  

1. **RPO (Recovery Point Objective \- Chấp nhận mất bao nhiêu dữ liệu?):**  
   * **Mục tiêu:** **24 giờ**.  
   * *Lý do:* Dữ liệu quan trọng nhất là cấu hình User, License và lịch sử bài đăng. Các dữ liệu này không thay đổi quá nhanh. Việc backup thời gian thực (Real-time replication) là quá phức tạp và tốn kém cho mô hình 1 VPS,.  
2. **RTO (Recovery Time Objective \- Mất bao lâu để khôi phục?):**  
   * **Mục tiêu:** **\< 4 giờ**.  
   * *Quy trình:* Khách hàng cần thời gian để tạo VPS mới $\\rightarrow$ Chạy script install.sh → Import file backup database.  
3. **Tài sản cần bảo vệ:**  
   * **Cốt lõi (Critical):** Database (PostgreSQL) chứa thông tin User, Token mạng xã hội, Project metadata.  
   * **Cấu hình:** File .env chứa các biến môi trường và Key bảo mật.  
   * **Media:** File video gốc và file thành phẩm.

### **B. Backup Types** 

1. **Full Backup (Sao lưu toàn phần) \- Dành cho Database & Config:**  
   * **Tần suất:** Hàng ngày (Daily) vào giờ thấp điểm (ví dụ: 03:00 AM).  
   * **Cơ chế:** Sao chép toàn bộ dữ liệu tại thời điểm đó.  
2. **Off-site Backup \- Bắt buộc:**  
   * **Vị trí:** **AWS S3**.

### **D. Database Backup** 

**Công cụ:** Sử dụng **pg\_dump**.

# Availability Design

### **1\. Tự động Khởi động lại**

* **Cấu hình:** Trong file `docker-compose.yml`, thêm dòng `restart: always` hoặc `restart: unless-stopped` cho tất cả các service (Web, Worker, DB, Redis).  
* **Cơ chế hoạt động:**  
  * Nếu code bị lỗi (Uncaught Exception) → App crash → Docker phát hiện PID chết → Docker tự động start lại container mới.

### **2\. Kiểm tra Sức khỏe Ứng dụng**

Đôi khi ứng dụng không "chết hẳn" (Process vẫn chạy) nhưng bị treo (Deadlock) hoặc không phản hồi. `restart: always` không phát hiện được lỗi này. Ta cần cơ chế chủ động kiểm tra.

* **Thiết kế:**  
  * **API Endpoint:** Viết một API siêu nhẹ `/api/health` trả về status 200 OK nếu DB và Redis vẫn kết nối tốt.  
  * **Docker Healthcheck:** Cấu hình Docker định kỳ gọi API này. Nếu API lỗi 3 lần liên tiếp, Docker sẽ coi container là "Unhealthy" và restart nó.

### **3\. Phòng chống sập do hết RAM**

* **Resource Limits (Giới hạn cứng):**  
  * Cấu hình giới hạn RAM cho từng container để nếu có lỗi memory leak, chỉ container đó chết, không kéo theo cả Server chết.  
  * Ví dụ: Web App max 1GB, Worker max 4GB.

### **4\. Database Resilience**

* **Vấn đề:** Khi traffic tăng đột biến hoặc code bị lỗi mở quá nhiều kết nối, Database sẽ từ chối phục vụ (Error: `Too many connections`).  
* **Giải pháp:**  
  * Giới hạn `max_connections` trong PostgreSQL config phù hợp với lượng RAM của VPS (ví dụ: 100 connections cho 8GB RAM).

# DEPLOYMENT

[Auto Update]()

# Auto Update

### **1\. Nguyên lý hoạt động**

Hệ thống không tải từng file code về máy khách (như cách copy-paste ngày xưa). Thay vào đó:

1. **Server của bạn (Dev):** Đóng gói code mới \+ môi trường vào một **Docker Image** và đẩy lên kho chứa bí mật (Private Registry).  
2. **Máy của khách (Client):** Chỉ cần **tải Image mới này về** và thay thế Container cũ.

### **2\. Thiết kế luồng "1-Click Update"**

#### **A. Kho chứa phiên bản (Private Registry)**

* Bạn cần cấu hình **Docker Hub Private** hoặc **AWS ECR**.  
* Khi dev code xong tính năng mới, CI/CD pipeline sẽ tự động build và đẩy image lên với tag mới (ví dụ: `crownmercado:v1.2.0`) và cập nhật tag `crownmercado:latest`.

#### **B. Cơ chế thông báo (Update Notification)**

Trong Web Dashboard của khách hàng, bạn cần một tính năng nhỏ:

* Frontend gọi về API trung tâm của bạn (ví dụ: `https://api.crownmercado.com/version`).  
* So sánh version hiện tại của khách với version mới nhất.  
* Nếu có bản mới → Hiện thông báo: **"Đã có phiên bản mới v1.2.0. Bấm để cập nhật"**.

#### **C. Kịch bản cập nhật (The `update.sh` Script)**

Nội dung file `update.sh` sẽ thực hiện các bước sau một cách tự động:

\#\!/bin/bash

\# 1\. Kéo Image mới nhất từ kho về (yêu cầu login sẵn)  
docker-compose pull

\# 2\. Tắt container cũ, bật container mới (Recreate Strategy)  
\# Docker thông minh sẽ chỉ thay thế container nào có image thay đổi  
docker-compose up \-d \--remove-orphans

\# 3\. Dọn dẹp image rác (cũ) để đỡ tốn ổ cứng khách  
docker image prune \-f

echo "Cập nhật hoàn tất\! Hệ thống đang chạy phiên bản mới nhất."

### **3\. Cách khách hàng thực hiện**

#### **Update qua giao diện (Advanced \- Giống n8n nhất)**

* **Cách làm:** Web App (Node.js) cần có quyền gọi lệnh hệ thống (hoặc kết nối tới Docker Socket \- *lưu ý bảo mật*). Khi khách bấm nút "Update" trên web, Node.js sẽ kích hoạt file `update.sh` ở dưới nền.  
* **Ưu điểm:** Khách không cần biết gì về dòng lệnh.  
* **Nhược điểm:** Cấu hình Docker Socket mount vào container có rủi ro bảo mật nếu code bị hack.

### **4\. Vấn đề quan trọng: Database Migration**

Khi code mới về, cấu trúc Database (PostgreSQL) có thể thay đổi (thêm cột, thêm bảng).

* Bạn phải cấu hình trong `docker-compose.yml` hoặc `entrypoint.sh` của Image: **Mỗi khi container khởi động, nó tự động chạy lệnh migrate DB trước khi chạy App**.  
* Điều này đảm bảo khách bấm update xong là DB cũng tự khớp, không bị lỗi dữ liệu.