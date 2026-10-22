# Kiểm kê nguồn slide (Discovery)

Phạm vi: chỉ khảo sát nguồn; chưa ingest toàn văn, chưa tạo câu hỏi hay sửa mã ứng dụng. Số trang bên dưới là **trang vật lý PDF, bắt đầu từ 1**.

Tổng: **63 PDF**, **407,168,913 bytes**, **3.589 trang**. Đã tính SHA-256 từng file và thử trích xuất chữ trên mọi trang bằng pypdf. Không file mã hóa; không lỗi đọc/trích xuất. Các mục `errors` trong JSON sau bổ sung chỉ là xung đột phân loại, không phải lỗi mở PDF.

| Thư mục | File | Trang | Trang không có text | Day trong tên file |
|---|---:|---:|---:|---|
| `phase1` | 15 | 1128 | 1128 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 |
| `track1 k3` | 11 | 417 | 417 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| `track2 k3` | 12 | 564 | 564 | 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13 |
| `track3 k3` | 13 | 685 | 685 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| `track4` | 12 | 795 | 348 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |

## Bằng chứng và khoảng trống

- Đã render và nhìn trang bìa của cả 63 PDF; contact sheet nằm trong `tmp/discovery/a1/covers-*.png`. Các tiêu đề trong bảng là đọc trực tiếp bìa trang 1, không suy ra từ tên file.
- 3.142/3.589 trang không trích xuất được chữ (87,55%). Toàn bộ Phase1 và Track1–3 là 2.794 trang không có text. Track4 có 447 trang có text; một phần text chứa glyph private-use/hỏng dấu, ví dụ `slide/track4/Day11.pdf`, trang 1. Cần OCR + kiểm tra hình/công thức trước khi tạo câu hỏi; số ký tự chỉ là phép đo kỹ thuật.
- Không tìm thấy file Day9 trong `track2 k3`; chưa có bằng chứng đó là thiếu bài hay đánh số khác. Không tự tạo Day9.
- Phase1 là nhãn thư mục. `phase1/day 2 ai product.pdf`, trang 1, lại ghi `AI IN ACTION – DAY 02 – TRACK 1`; giữ xung đột để chủ nguồn xác nhận.
- `track2 k3/day 3 tu chatbot den agentic agent.pdf`, trang 1, ghi `AICB-P1 · Ngày 3` và `Phase 1`; không tự xếp thành Phase2 dù nằm thư mục Track2.
- Phase2/Track2 và Phase2/Track3 có bằng chứng bìa ở phần lớn file (ví dụ Track2 Day1 và Track3 Day1, trang 1). Phase2 của toàn bộ Track1/Track4 chưa được xác minh; không gán mặc định. Tên lĩnh vực Track1 AI Product & Business, Track4 Computer Vision & Robotics có trên một số bìa, nhưng chưa coi là taxonomy chuẩn toàn bộ chương trình.
- Day trong tên file khác Day trên slide ở nhiều file: Track1 Day1→16, Day4→20–21, Day7→18, Day9→26 (đều trang 1); Track3 Day8/Day10 lại in 08/10. Không áp dụng công thức cộng 15. JSON giữ riêng `day_in_filename` và `day_in_source`; null là chưa xác minh, không phải không có.
- `k3` chỉ là token thư mục; chưa xác nhận nghĩa cohort. Không đổi thành nhãn khóa học chính thức.
- Section title/learning objectives bên trong chưa được đọc đầy đủ vì 87,55% trang không có text. JSON chỉ lưu một số dòng mở đầu/ứng viên section và số ký tự từng trang, không lưu corpus toàn văn. Không tuyên bố discovery đã hiểu mọi nội dung.

## Danh mục theo bìa

Mỗi dòng dẫn **đúng file và trang vật lý 1**. SHA-256, bytes, thống kê từng trang và bằng chứng text có trong `source-inventory.json`.

| File | Trang | Tiêu đề bìa | Day file / Day nguồn |
|---|---:|---|---|
| `slide/phase1/day 1 AI & LLM.pdf` | 52 | AI & LLM Foundation (tr. 1) | 1 / 1 |
| `slide/phase1/day 11 Guardralis,HITL&Responsible AI.pdf` | 116 | Guardrails, HITL & Responsible AI (tr. 1) | 11 / 11 |
| `slide/phase1/day 14 AI Evaluation & Benchmarking.pdf` | 81 | AI Evaluation & Benchmarking (tr. 1) | 14 / 14 |
| `slide/phase1/day 2 ai product.pdf` | 50 | Xác định bài toán cho AI (tr. 1) | 2 / 2 |
| `slide/phase1/day 4 context,loop,harness.pdf` | 83 | Context · Loop · Harness Engineering (tr. 1) | 4 / 4 |
| `slide/phase1/day10 data pipeline & data observabitity.pdf` | 138 | Data Pipeline & Data Observability (tr. 1) | 10 / 10 |
| `slide/phase1/day12 Deployment.pdf` | 104 | Deployment — Đưa Agent Lên Cloud (tr. 1) | 12 / 12 |
| `slide/phase1/day13 Monitoring,logging & Observability.pdf` | 85 | Monitoring, Logging & Observability (tr. 1) | 13 / 13 |
| `slide/phase1/day15 dinh huong.pdf` | 55 | Triển Khai Thực Tế, Chi Phí Vận Hành & Định Hướng Chuyên Sâu (tr. 1) | 15 / 15 |
| `slide/phase1/day3 chat bot & agentic agent.pdf` | 94 | Từ Chatbot Đến Agentic Agent (tr. 1) | 3 / 3 |
| `slide/phase1/day5 AI product & requirements.pdf` | 51 | AI Product Thinking & Requirements (tr. 1) | 5 / 5 |
| `slide/phase1/day6 AI product & project management.pdf` | 37 | AI Product & Project Management (tr. 1) | 6 / 6 |
| `slide/phase1/day7 data foundations.pdf` | 58 | Data Foundations (tr. 1) | 7 / 7 |
| `slide/phase1/day8 RAG PIPELINE.pdf` | 66 | RAG Pipeline (tr. 1) | 8 / 8 |
| `slide/phase1/day9 mcp-a2a.pdf` | 58 | Multi-Agent & Kết Nối Hệ Thống (tr. 1) | 9 / 9 |
| `slide/track1 k3/day 11 AI Adoption & Change Management.pdf` | 37 | AI Adoption & Change Management (tr. 1) | 11 / chưa xác minh |
| `slide/track1 k3/day 5 AI Ethic.pdf` | 31 | AI Ethic, Responsible AI và AI Compliance (tr. 1) | 5 / chưa xác minh |
| `slide/track1 k3/day 6 Retention.pdf` | 49 | Retention, Engagement & Habit Loop (tr. 1) | 6 / 23 |
| `slide/track1 k3/day 7 AI Financial.pdf` | 35 | AI Financial Modeling & ROI (tr. 1) | 7 / 18 |
| `slide/track1 k3/day 8 từ sp chạy được đến sp bán được.pdf` | 29 | Từ sản phẩm chạy được đến sản phẩm bán được (tr. 1) | 8 / 26 |
| `slide/track1 k3/day02 product discovery.pdf` | 28 | Product Discovery (tr. 1) | 2 / 17 |
| `slide/track1 k3/Day1.pdf` | 45 | AI Product Manager (tr. 1) | 1 / 16 |
| `slide/track1 k3/day10 con người trong dự án AI.pdf` | 37 | Con Người Trong Dự Án AI — Từ Stakeholder Đến AI Team Performance (tr. 1) | 10 / chưa xác minh |
| `slide/track1 k3/day3 design the experiment.pdf` | 23 | Design the Experiment (tr. 1) | 3 / 18 |
| `slide/track1 k3/Day4 Ai Evaluation.pdf` | 66 | AI Evaluation (tr. 1) | 4 / 20–21 |
| `slide/track1 k3/day9.pdf` | 37 | Đèn nào bật trước? (tr. 1) | 9 / 26 |
| `slide/track2 k3/day 10 MCP a2a.pdf` | 60 | MCP/A2A Infrastructure & Agentic Routing (tr. 1) | 10 / 26 |
| `slide/track2 k3/day 12 data Observability.pdf` | 40 | Data Observability & Lineage cho hệ thống Data/AI (tr. 1) | 12 / chưa xác minh |
| `slide/track2 k3/day 13 platform Engineeering.pdf` | 22 | Platform Engineering & Documentation (tr. 1) | 13 / 28 |
| `slide/track2 k3/day 2 data pipeline engineering.pdf` | 42 | Data Pipeline Engineering (tr. 1) | 2 / 17 |
| `slide/track2 k3/day 3 tu chatbot den agentic agent.pdf` | 46 | Từ Chatbot Đến Agentic Agent (tr. 1) | 3 / 3 |
| `slide/track2 k3/day 4 vector store & feature store.pdf` | 61 | Vector Store & Feature Store (tr. 1) | 4 / 19 |
| `slide/track2 k3/day 6 CI_CD for AI Systems.pdf` | 40 | CI/CD for AI Systems (tr. 1) | 6 / 21 |
| `slide/track2 k3/day1 Cloud infrastructure for AI.pdf` | 40 | Cloud Infrastructure for AI (tr. 1) | 1 / 16 |
| `slide/track2 k3/day11 GPU Finops.pdf` | 50 | GPU FinOps & Cost Optimization (tr. 1) | 11 / 25 |
| `slide/track2 k3/day5 model serving & in-ference Optimization.pdf` | 46 | Model Serving & Inference Optimization (tr. 1) | 5 / 20 |
| `slide/track2 k3/day7 LLMops & Prompt versioning.pdf` | 75 | LLMOps & Prompt Versioning (tr. 1) | 7 / 22 |
| `slide/track2 k3/day8 disaster recovery.pdf` | 42 | Disaster Recovery & High Availability cho AI Infrastructure (tr. 1) | 8 / 23 |
| `slide/track3 k3/day 10 Circuit Breakers.pdf` | 34 | Circuit Breakers, Caching & Reliability for Production Agents (tr. 1) | 10 / 10 |
| `slide/track3 k3/day 13 full production agent system.pdf` | 30 | Workshop Tổng Hợp — Full Production Agent System (tr. 1) | 13 / 28 |
| `slide/track3 k3/day 3 production RAG.pdf` | 56 | Production RAG (tr. 1) | 3 / 18 |
| `slide/track3 k3/day 4 graphRAG& Knowledge graphs.pdf` | 65 | GraphRAG & Knowledge Graphs (tr. 1) | 4 / 19 |
| `slide/track3 k3/day 7 DPO,ORPO alignment.pdf` | 64 | DPO, ORPO & Alignment — Từ SFT đến Preference Learning (tr. 1) | 7 / 22 |
| `slide/track3 k3/day 9 RAGAS LLM-as-Judge and Guardrails.pdf` | 74 | RAGAS, LLM-as-Judge & Guardrails (tr. 1) | 9 / 24 |
| `slide/track3 k3/day1 advenced - agent- architecture.pdf` | 77 | Advanced Agent Architectures (tr. 1) | 1 / 16 |
| `slide/track3 k3/day11 MCP Tool Integration.pdf` | 39 | Model Context Protocol (MCP) (tr. 1) | 11 / 26 |
| `slide/track3 k3/day12 HITL,UX khi nao agent can xin phep.pdf` | 78 | Human-in-the-Loop UX — Khi Nào Agent Cần Xin Phép? (tr. 1) | 12 / 27 |
| `slide/track3 k3/day2  memory systems for agent.pdf` | 42 | Memory Systems for Agents (tr. 1) | 2 / 17 |
| `slide/track3 k3/day5 multi agent systems.pdf` | 39 | Multi-Agent Systems (tr. 1) | 5 / 20 |
| `slide/track3 k3/day6 fine tuning llm.pdf` | 51 | Fine-tuning LLMs — Từ Full Fine-tune đến LoRA/QLoRA (tr. 1) | 6 / 21 |
| `slide/track3 k3/day8 LangGrap and Agentic Orchestration.pdf` | 36 | LangGraph & Agentic Orchestration (tr. 1) | 8 / 08 |
| `slide/track4/Day01.pdf` | 96 | Mạng Nơ-ron và Huấn Luyện (tr. 1) | 1 / 1 |
| `slide/track4/Day02.pdf` | 93 | Kiến Trúc Mạng Cho Thị Giác Máy Tính (tr. 1) | 2 / 2 |
| `slide/track4/Day03.pdf` | 99 | 2D Perception: Detection · Segmentation · Keypoints (tr. 1) | 3 / chưa xác minh |
| `slide/track4/Day04.pdf` | 36 | Ngày 4 · Cảm biến và chuỗi khung hình - thời gian (tr. 1) | 4 / 4 |
| `slide/track4/Day05.pdf` | 43 | Bộ lọc Kalman & Hợp nhất xác suất (tr. 1) | 5 / chưa xác minh |
| `slide/track4/Day06.pdf` | 28 | 3D from Point Clouds and Where LiDAR Meets the Camera (tr. 1) | 6 / 6 |
| `slide/track4/Day07.pdf` | 47 | Tracking (tr. 1) | 7 / chưa xác minh |
| `slide/track4/Day08.pdf` | 47 | 3D từ Camera, BEV & Sensor Fusion (tr. 1) | 8 / chưa xác minh |
| `slide/track4/Day09.pdf` | 67 | Data và annotation pipeline cho Computer Vision và Robotics (tr. 1) | 9 / 09 |
| `slide/track4/Day10.pdf` | 59 | Vision–Language Model và VLA (tr. 1) | 10 / chưa xác minh |
| `slide/track4/Day11.pdf` | 95 | Synthetic, Simulated & Trajectory Data (tr. 1) | 11 / 11 |
| `slide/track4/Day12.pdf` | 85 | Phát lại nhật ký và kiểm thử vòng kín (tr. 1) | 12 / 12 |

## Điều kiện cho bước ingest tiếp theo

Cần chốt Day chuẩn (local/global/range), quan hệ Phase–Track, trường hợp bìa sai thư mục và phạm vi Day thiếu. Sau đó OCR có bảo toàn trang nguồn, kiểm tra bảng/công thức/diagram và xây section map trước khi sinh câu hỏi. Chưa cài OCR hay xử lý toàn bộ ảnh trong lượt discovery này.
