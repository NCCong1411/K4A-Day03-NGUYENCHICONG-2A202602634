# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Chí Công  
> **Mã Sinh Viên / Mã Học viên:** 2A202602634  
> **Chủ đề Lựa chọn:**  
> *Trợ lý Đơn hàng & Kho vận (Supply Chain Agent):* Tra cứu mã vận đơn, vị trí lưu kho và cập nhật trạng thái đơn hàng.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá           | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm (có bằng chứng)                                                                                                                                                                                                                                                                                                                           |
| --------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Multi-step Reasoning** | **4/ 5**       | Agent đã thể hiện rõ chuỗi suy luận Thought → Action → Observation. Bằng chứng nằm ở [docs/trace_waterfall.json](docs/trace_waterfall.json): với TC02, TC03, TC04 có các bước `TOOL_EXECUTION` rồi mới đến `FINAL_ANSWER`.                                                                                                                                                    |
| **2. Tool Interaction**     | **4 / 5**      | Hệ thống đã tương tác thành công với MCP Server và gọi đúng 3 tool chính: `track_order`, `get_warehouse_location`, `update_order_status`. Bằng chứng nằm trong [docs/trace_waterfall.json](docs/trace_waterfall.json), nơi `tool_name` xuất hiện đúng theo từng test case. Tuy nhiên, vì TC05 vẫn còn một phần chưa hoàn toàn khớp theo kỳ vọng ban đầu nên chưa chấm tối đa. |
| **3. Dynamic Decision**     | **4 / 5**      | Agent biết khi nào cần gọi tool và khi nào không. Bằng chứng: TC01 không gọi tool, còn TC02–TC04 đều gọi tool phù hợp. Logic này phù hợp với prompt trong [src/prompts.py](src/prompts.py) và mock routing trong [src/providers.py](src/providers.py).                                                                                                                        |
| **4. Long Horizon Goal**    | **4 / 5**      | Agent duy trì mục tiêu xuyên suốt test suite. Bằng chứng là [docs/trace_waterfall.json](docs/trace_waterfall.json) chứa nhiều step cho nhiều câu hỏi khác nhau trong cùng một phiên chạy, từ câu hỏi chung đến tra cứu đơn hàng, cập nhật trạng thái và vị trí kho.                                                                                                           |
| **TỔNG ĐIỂM AGENTIC FIT**   | **16 / 20**    | Tổng điểm đạt được là 16/20 vì hệ thống đã có khả năng suy luận, gọi tool, và duy trì luồng ReAct. Tuy nhiên thì chưa chắc đã là cách làm tốt nhất.                                                                                                                                                                                                                           |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

Ở đây, em dùng OpenAI

```json
    {
    "step": 1,
    "query": "Chào bạn, bạn có thể hỗ trợ tra cứu đơn hàng và kho vận không?",
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn! Tôi có thể giúp bạn tra cứu trạng thái đơn hàng và vị trí lưu kho. Bạn cần cung cấp mã vận đơn hoặc mã đơn hàng để tôi có thể hỗ trợ bạn tốt hơn.",
    "latency_ms": 4478.6
  }
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).

- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (TC02, TC03, TC04, TC05 đã gọi tool theo đúng luồng; TC01 không cần gọi tool).
- **Kết quả đẩy Repo nộp bài:** [V] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
