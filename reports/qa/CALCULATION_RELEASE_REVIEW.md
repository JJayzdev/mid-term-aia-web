# Independent release metadata gate — 1284

**PASS** cho regex correction và metadata bank `2026.10.22-28fda6d871f4` hiện emit. Không có finding mở trong phạm vi kiểm này.

Đã đọc diff cả `validate_release.py` và `expansion_audit.py`: negative lookahead chỉ miễn cụm số học “theo phần trăm”, không bỏ nhóm “theo phần …” nói chung. Reviewer chạy 10 Python release fixtures: **10/10 pass**; probe riêng expansion regex xác nhận “theo phần trăm” được phép, còn “theo phần tổng kết”, “theo phần minh họa”, “theo tài liệu” vẫn bị phát hiện.

Reviewer tự chạy `python -X utf8 scripts/validate_release.py --verify-sources --min-per-document 20 --standalone-stems`: **errors=[]**. Kết quả 1284 câu, 63/63 tài liệu, minimum20; 51 tài liệu có20 câu và 12 tài liệu Track4 có22 câu. Có24 objective calculation Track4, đủ pool cho minimum2 của đề thi. Các gate schema, exact-revision independent approval, source-page coverage và SHA256 nguồn đều pass.

Đối chiếu metadata độc lập: approved bank và public bank giống byte; coverage ghi1284 và omitted=[]; digest từ questions khớp bank_version; report `expand-root-calculation.json` có24 approved và0 rejected. Gate này kiểm ràng buộc artifact và provenance; phần semantic/numerical của24 câu mới là review độc lập của Root, không tuyên bố reviewer này đọc lại24 câu hoặc toàn bộ1260 cũ.

Code-only gate trước ở `CALCULATION_CODE_REVIEW.md` giữ hiệu lực. Chưa tự chạy production build/browser/live1284 trong lần kiểm metadata này; báo cáo release đang ghi validation in progress đúng thực tế tại thời điểm đọc. Cần giữ bằng chứng browser/deployment riêng khi Root hoàn tất.
