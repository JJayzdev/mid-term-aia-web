# -*- coding: utf-8 -*-
exec(open('scripts/content/expand_a_peerfix2.py',encoding='utf-8').read().split("addpage(8,'p2-t1-d07-x02'")[0])
change(3,'p1-d07-x01','Đưa một tài liệu ngắn trực tiếp vào prompt theo cách in-context có bắt buộc embedding và database không?', ['Không; nội dung được cung cấp trực tiếp nhưng bị giới hạn bởi context window','Có; mọi văn bản vào prompt phải đi qua vector index trước','Có; cần huấn luyện lại weights để model nhìn được tài liệu trong prompt'],'In-context gửi thẳng nội dung, khác RAG có pipeline lưu và tìm; sự đơn giản đánh đổi giới hạn context.',6)
