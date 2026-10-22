"""Editorial revisions to legacy stems; never creates independent approvals."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEMS = {
    'p1-d01-q01': 'Đặc điểm nào phân biệt Agentic AI với Generative AI?',
    'p1-d01-q02': 'Những thành phần nào thuộc agent harness? (Chọn tất cả đáp án đúng.)',
    'p1-d02-q01': 'Trước khi đề xuất một chatbot, câu hỏi nào giúp chẩn đoán đúng vấn đề cần giải quyết?',
    'p1-d02-q02': 'Chỉ cần thấy một công việc lặp lại là có thể đề xuất giải pháp ngay, dù chưa hiểu điểm đau của người dùng.',
    'p1-d05-q02': 'Mong muốn cảm thấy tự tin hơn và ít sợ sai hơn thuộc nhu cầu cảm xúc trong JTBD.',
    'p1-d05-q03': 'Những câu hỏi nào giúp làm rõ Jobs to Be Done? (Chọn tất cả đáp án đúng.)',
    'p1-d06-q03': 'Những điều kiện nào giúp xác định một support agent đã đáp ứng Definition of Done? (Chọn tất cả đáp án đúng.)',
    'p1-d07-q01': 'Một tài liệu có heading và section tốt; cần chia chunk trọn ý và giữ metadata section rõ ràng. Chiến lược chunking nào phù hợp nhất?',
    'p1-d07-q03': 'Những nhận định nào đúng về recursive chunking? (Chọn tất cả đáp án đúng.)',
    'p1-d08-q01': 'Trường hợp nào có lý do rõ ràng để dùng RAG?',
    'p1-d08-q02': 'Mọi câu hỏi kiến thức chung đều bắt buộc phải dùng RAG.',
    'p1-d08-q03': 'Những trường hợp nào chưa cần dùng RAG? (Chọn tất cả đáp án đúng.)',
    'p1-d09-q01': 'Hai subagent khám phá hai hướng độc lập, còn kết quả cuối là một sản phẩm chung. Cách tổ chức nào giúp tránh xung đột khi tích hợp?',
    'p1-d09-q02': 'Để tránh xung đột, nên cho nhiều subagent đồng thời ghi vào một sản phẩm chung mà không điều phối.',
    'p1-d10-q03': 'Những tín hiệu nào cần xét khi đánh giá một chunk được truy xuất? (Chọn tất cả đáp án đúng.)',
    'p1-d11-q01': 'Cặp kiểm soát nào giúp lọc nội dung và kiểm chứng căn cứ của đầu ra trong output guardrail pipeline?',
    'p1-d11-q03': 'Có thể chọn điểm chuyển xử lý cho con người chỉ từ confidence score của model, không cần xét rủi ro và khả năng hoàn tác.',
    'p1-d12-q03': 'Những mục nào cần kiểm tra trước khi triển khai ứng dụng AI? (Chọn tất cả đáp án đúng.)',
    'p1-d13-q02': 'Monitoring tập trung theo dõi các câu hỏi và failure mode đã biết trước.',
    'p1-d13-q03': 'Những loại telemetry nào hỗ trợ observability? (Chọn tất cả đáp án đúng.)',
    'p1-d14-q01': 'Vì sao accuracy đơn lẻ chưa đủ để đánh giá LLM hoặc agent?',
    'p1-d14-q02': 'Những nguyên tắc nào giúp thiết kế evaluation có ích cho hệ thống AI? (Chọn tất cả đáp án đúng.)',
    'p1-d15-q01': 'Một nhóm có GPU server và ưu tiên inference throughput cao. Công cụ serving nào phù hợp?',
    'p1-d15-q02': 'Ollama phù hợp cho phát triển, demo và triển khai ở edge nhờ thiết lập đơn giản.',
    'p2-t1-d01-q01': 'Sau khi phát hành sản phẩm AI, chu trình nào cần tiếp tục để duy trì chất lượng?',
    'p2-t1-d01-q02': 'Một sản phẩm AI sẽ chạy đúng thiết kế mãi mãi sau lần phát hành đầu tiên.',
    'p2-t1-d01-q03': 'Những hoạt động nào cần tiếp tục trong vòng lặp cải tiến sau khi phát hành sản phẩm AI? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d02-q01': 'Một ứng dụng gọi xe gửi push notification khi tài xế đến điểm đón. Push notification này là output hay outcome của sản phẩm?',
    'p2-t1-d02-q02': 'Tạo được push notification đồng nghĩa đã đo được kết quả tài xế chờ ít hơn.',
    'p2-t1-d03-q02': 'Đưa cả nhắc AI, thanh tiến độ và huy hiệu vào cùng một biến thể thử nghiệm sẽ cho biết chính xác tác động riêng của từng thành phần.',
    'p2-t1-d04-q01': 'Một sản phẩm AI đã có lưu lượng sử dụng thực tế và phản hồi của người dùng. Khi bắt đầu evaluation để tìm lỗi, dữ liệu nên lấy từ đâu?',
    'p2-t1-d04-q02': 'Khi con người gán nhãn các trường hợp thất bại để cải thiện AI, nên ưu tiên chất lượng nhãn hơn số lượng.',
    'p2-t1-d04-q03': 'Những việc nào thuộc vòng lặp evaluation và cải tiến chất lượng AI? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d07-q02': 'Một mô hình định giá hybrid có thể gồm phí gói cơ bản và khoản trả thêm khi vượt mức sử dụng cho phép.',
    'p2-t1-d07-q03': 'Định giá hybrid kết hợp phí gói và phí vượt mức sử dụng nhằm những mục tiêu nào? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d08-q01': 'Chỉ số Cost/Job dùng để đo điều gì?',
    'p2-t1-d08-q03': 'Những khoản nào cần tính khi xác định Cost/Job của ứng dụng AI? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d09-q01': 'Quy tắc phản ứng với chỉ số nào đủ cụ thể để đội vận hành thực thi?',
    'p2-t1-d11-q03': 'Những ghép nối nào đúng với mô hình ADKAR? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d01-q02': 'Trong mô hình trách nhiệm chia sẻ khi triển khai AI trên cloud, những việc nào thuộc đội triển khai? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d01-q01': 'Một nhóm muốn làm prototype nhanh với cách tính phí theo token và không quản trị hạ tầng. Nên chọn lớp dịch vụ cloud nào?',
    'p2-t2-d01-q03': 'Một hệ thống có thể kết hợp training bằng IaaS, serving bằng PaaS và làm prototype bằng AI-aaS.',
    'p2-t2-d03-q01': 'Một use case được chấm đa số tiêu chí Agentic Fit chỉ ở mức 1–2/5. Nên bắt đầu triển khai thế nào?',
    'p2-t2-d03-q02': 'Những tình huống nào là dấu hiệu chưa nên sử dụng agent loop? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d03-q03': 'Trước khi chọn agent loop, nên benchmark các giải pháp rule, workflow hoặc chatbot đơn giản hơn.',
    'p2-t2-d04-q01': 'Phát biểu nào mô tả đúng FAISS?',
    'p2-t2-d04-q02': 'Những ghép nối giữa loại vector index và đặc tính nào là đúng? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d04-q03': 'Lựa chọn vector index nào đáng đánh giá đầu tiên cho hệ thống này và vì sao?',
    'p2-t2-d05-q02': 'Những mô tả nào đúng về speculative decoding và batching? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d07-q01': 'Những thành phần nào cần quản lý trong prompt artifact và context bundle? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d08-q02': 'Những điều kiện nào phù hợp để chọn kiến trúc active-passive? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d10-q01': 'Một proxy đưa method hoặc tool name vào HTTP header. Thiết kế này giúp gateway thực hiện việc gì?',
    'p2-t2-d10-q02': 'Lớp gateway MCP có thể cung cấp những năng lực vận hành nào? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d11-q03': 'Khi so sánh chi phí training giữa các cấu hình, nên dùng chi phí mỗi job thay vì chỉ nhìn chi phí mỗi GPU-hour.',
    'p2-t2-d12-q02': 'Những ghép nối nào đúng khi so sánh rules với anomaly detection trong kiểm tra chất lượng dữ liệu? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d01-q02': 'Những nội dung nào nên lưu trong reflection memory? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d02-q01': 'Agent cần truy xuất tri thức domain qua embeddings và vector database. Loại memory nào phù hợp?',
    'p2-t3-d02-q02': 'Một agent quản lý memory với giới hạn token và chỉ ghi dữ liệu dài hạn sau khi task hoàn tất. Những bước nào phù hợp với quy trình này? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d02-q03': 'Khi thông tin dài hạn mâu thuẫn với thông tin ngắn hạn mới hơn, có thể ưu tiên tính mới và đánh dấu xung đột để review.',
    'p2-t3-d03-q02': 'Những mô tả nào đúng về late chunking? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d03-q01': 'Hierarchical retrieval giải quyết sự đánh đổi giữa chunk nhỏ và chunk lớn như thế nào?',
    'p2-t3-d04-q02': 'Những mô tả nào đúng khi so sánh property graph với RDF? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d05-q01': 'Routing có thể tiết kiệm chi phí, nhưng sai sót nào trong routing dễ làm giảm chất lượng kết quả?',
    'p2-t3-d05-q03': 'Trong kiến trúc supervisor dạng graph, mỗi worker có thể được tổ chức thành một node với bộ tools riêng.',
    'p2-t3-d06-q02': 'Những mô tả nào đúng về cơ chế LoRA? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d09-q02': 'Những bước nào dùng để tính Faithfulness dựa trên các factual claim và context? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d09-q03': 'Tính Faithfulness bằng tỷ lệ factual claim được context hỗ trợ và giải thích giới hạn của kết luận.',
    'p2-t3-d10-q02': 'Những kiểm soát nào cần cho semantic response cache? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d11-q03': 'Trong MCP, Prompt là template tái sử dụng do người dùng chọn, khác Tool là function mà LLM quyết định gọi.',
    'p2-t3-d13-q01': 'Những chiều nào cần xét khi đánh giá toàn diện một hệ thống agent? (Chọn tất cả đáp án đúng.)',
    'p2-t4-d01-q03': 'Kỹ thuật nào phù hợp để xử lý gradient bùng nổ?',
    'p2-t4-d01-q04': 'Trong AdamW, weight decay được tách khỏi bước cập nhật theo gradient, thay vì cộng hạng L2 vào gradient.',
    'p2-t4-d02-q03': 'Chọn các mô tả đúng về multi-head attention.',
    'p2-t4-d03-q03': 'IoU có những vai trò nào trong phát hiện đối tượng? Chọn tất cả đáp án đúng.',
    'p2-t4-d03-q04': 'Trong kiến trúc YOLO26, head one-to-one có thể suy luận không cần NMS.',
    'p2-t4-d05-q04': 'Khi hàm cong mạnh hoặc độ bất định lớn, xấp xỉ của EKF có thể lệch cả trung bình lẫn độ rộng phân phối.',
    'p2-t4-d08-q02': 'Chọn mô tả phù hợp với nhánh top-down sử dụng query attention để tạo đặc trưng BEV.',
    'p2-t4-d08-q03': 'Với tọa độ ảnh (u,v), depth z và ma trận nội tại K, công thức khôi phục tọa độ camera là gì?',
    'p2-t4-d08-q04': 'Có thể coi việc so sánh NDS giữa các model camera và LiDAR là một bảng xếp hạng công bằng tuyệt đối, dù backbone và dữ liệu bổ sung khác nhau.',
    'p2-t4-d10-q01': 'Đầu ra đặc trưng của mô hình VLA dành cho robot là gì?',
    'p2-t4-d10-q02': 'Trong giai đoạn alignment của Qwen3-VL khi ViT và LLM được đóng băng, thành phần nào được cập nhật?',
    'p2-t4-d10-q03': 'Những yếu tố nào quyết định số token ảnh khi mã hóa đầu vào cho mô hình thị giác–ngôn ngữ?',
    'p2-t4-d10-q04': 'CLIP học tương phản trên các cặp ảnh–văn bản.',
    'p2-t4-d11-q01': 'Những nhóm sai khác nào có thể gây ra sim2real gap?',
    'p2-t4-d11-q02': 'Nhận xét nào đúng về phạm vi của domain randomization?',
    'p2-t4-d12-q03': 'Khoảng cách tới vật cản là 12 m và tốc độ tiến gần không đổi là 5 m/s. Time to Collision (TTC) bằng bao nhiêu?',
    'p2-t4-d12-q01': 'Cần lưu những thông tin nào để tái tạo một lần chạy log replay?',
}
STEMS.update({
    'p1-d04-q03': 'Trong mô hình bốn lớp của hệ thống agent, những nội dung nào thuộc harness engineering? (Chọn tất cả đáp án đúng.)',
    'p1-d11-q02': 'Để kiểm chứng guardrails và cơ chế chuyển xử lý cho con người, cần chuẩn bị những bằng chứng nào? (Chọn tất cả đáp án đúng.)',
    'p1-d14-q03': 'Offline evaluation dùng batch test trên golden dataset, phù hợp khi phát hành phiên bản hoặc thay đổi prompt.',
    'p2-t4-d05-q01': 'Hai bước lặp của Kalman filter được thực hiện theo thứ tự nào?',
    'p2-t4-d07-q02': 'Trong ByteTrack, box score thấp được dùng để tạo track mới ngay lập tức.',
    'p2-t4-d11-q03': 'Một quy trình tạo ảnh có điều kiện dùng IoU để kiểm tra vật sinh có nằm đúng vị trí yêu cầu. Hai box nào cần được đối chiếu?',
    'p2-t1-d10-q02': 'Trong ma trận ảnh hưởng–quan tâm, Champions có ảnh hưởng cao và quan tâm cao.',
    'p2-t1-d10-q03': 'Những câu hỏi nào giúp phân loại stakeholder theo hai trục ảnh hưởng và quan tâm? (Chọn tất cả đáp án đúng.)',
    'p2-t2-d12-q01': 'Nguồn dữ liệu cập nhật trễ so với SLA nhưng schema vẫn đúng. Trụ cột nào trực tiếp phát hiện vấn đề này?',
    'p2-t2-d13-q01': 'Những thông tin nào cần ghi trong audit trail của request để truy vết phiên bản mô hình và chi phí? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d04-q01': 'Một triple trong knowledge graph có cấu trúc nào?',
    'p2-t3-d04-q03': 'Trong hệ thống RAG dùng knowledge graph, retrieval có thể duyệt entities và relations thay vì chỉ tìm chunk văn bản.',
    'p2-t3-d07-q01': 'DPO không cần huấn luyện riêng thành phần nào vốn được dùng để chấm reward trong pipeline RLHF truyền thống?',
    'p2-t3-d07-q02': 'Những ghép nối nào đúng giữa nguồn tín hiệu đánh giá tốt/xấu và phương pháp alignment? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d07-q03': 'Single-stage alignment có thể kết hợp việc học từ demonstration và preference trong một giai đoạn, thay cho một bước SFT riêng biệt.',
    'p2-t3-d08-q02': 'Những nguyên tắc nào giúp node function an toàn khi retry và cập nhật state? (Chọn tất cả đáp án đúng.)',
    'p2-t3-d11-q01': 'Primitive MCP nào cung cấp dữ liệu chỉ đọc theo URI để ứng dụng dùng làm context?',
    'p2-t1-d02-q03': 'Một dịch vụ gọi xe muốn cải thiện việc tài xế và hành khách tìm thấy nhau tại điểm đón. Những kết quả nào thể hiện outcome mong muốn? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d05-q01': 'Responsible AI chuyển các giá trị đạo đức thành những yếu tố vận hành nào?',
    'p2-t1-d05-q02': 'AI Safety Evaluation xem xét các dạng thất bại, tác hại và ngưỡng chặn triển khai.',
    'p2-t1-d05-q03': 'Những giá trị nào thuộc AI Ethics? (Chọn tất cả đáp án đúng.)',
    'p2-t1-d10-q01': 'Trong mô hình phân nhóm stakeholder Champions–Blockers–Supporters–Bystanders theo ảnh hưởng và quan tâm, stakeholder có ảnh hưởng cao nhưng quan tâm thấp thuộc nhóm nào?',
    'p2-t3-d01-q03': 'Reflexion dùng text feedback để cải thiện vòng thử, không cập nhật gradient của model trong mỗi vòng.',
    'p2-t3-d06-q01': 'Few-shot prompt chưa đạt ngưỡng vì thiếu tri thức riêng, không phải thiếu hành vi. Nên đánh giá hướng xử lý nào trước?',
    'p2-t3-d06-q03': 'Với ma trận trọng số kích thước d × k, LoRA rank r dùng hai ma trận adapter có tổng r(d+k) tham số trainable, thay vì cập nhật toàn bộ dk tham số gốc.',
    'p2-t3-d10-q01': 'Circuit breaker ở trạng thái OPEN xử lý lời gọi đến dependency như thế nào?',
    'p2-t2-d10-q03': 'Với API phi trạng thái có xác thực, mỗi request cần mang thông tin xác thực để hệ thống kiểm tra danh tính cho từng lời gọi.',
})

def main():
    changes = []
    for path in sorted((ROOT / 'data/questions/drafts').glob('*.json')):
        bank = json.loads(path.read_text(encoding='utf-8'))
        dirty = False
        for question in bank['questions']:
            replacement = STEMS.get(question['id'])
            if replacement and question['question'] != replacement:
                changes.append({'id': question['id'], 'previous_revision': question['revision'],
                    'revision': question['revision'] + 1, 'before': question['question'], 'after': replacement,
                    'draft_path': path.relative_to(ROOT).as_posix(), 'source_reference': question['source_reference']})
                question['question'] = replacement
                question['revision'] += 1
                question['status'] = 'pending_review'
                question.pop('review', None)
                question.setdefault('review_notes', []).append('Root editorial revision: standalone knowledge question; independent re-review required.')
                dirty = True
        if dirty:
            path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if changes:
        target = ROOT / 'reports/expansion/wording-change-set.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        previous = json.loads(target.read_text(encoding='utf-8')).get('changes', []) if target.exists() else []
        latest = {change['id']: change for change in previous + changes}
        target.write_text(json.dumps({'editor': 'root-content', 'changes': sorted(latest.values(), key=lambda c: c['id'])}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Editorial revisions requiring independent review:', len(changes))

if __name__ == '__main__':
    main()
