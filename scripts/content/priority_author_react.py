from priority_author_common import *
D='p1-d03'
match(D,'react-stages',[34,37],'Ghép một-một thành phần ReAct với vai trò của nó.',[
 ('Thought','Xác định còn thiếu gì và bước tiếp theo','Thought chọn bước tiếp theo từ mục tiêu và quan sát hiện có.'),
 ('Action','Yêu cầu thực hiện công cụ cùng tham số','Action mô tả công cụ và dữ liệu đầu vào; ứng dụng thực thi lời gọi.'),
 ('Observation','Kết quả do công cụ hoặc môi trường trả về','Observation bổ sung bằng chứng để vòng tiếp theo quyết định.'),
 ('Final Answer','Câu trả lời khi đã đủ thông tin hoặc kết thúc có giải thích','Final Answer phải phản ánh bằng chứng đã thu được, không tự giả kết quả tool.')],
 'ReAct là Reasoning + Acting. Các thành phần liên kết thành vòng lặp; đây là pattern agent, khác React là thư viện giao diện.',focus='react')
order(D,'react-loop',[34,37],'Agent đang thiếu một dữ kiện cần tra cứu. Sắp xếp một vòng ReAct rồi kiểm tra có thể kết thúc hay phải lặp lại.',[
 'Thought: xác định dữ kiện cần tìm và công cụ phù hợp','Action: gửi yêu cầu công cụ với tham số','Observation: nhận kết quả thực thi','Đánh giá đủ thông tin để trả lời; nếu chưa đủ thì quay lại Thought'],
 'Action phải dựa trên quyết định ở Thought; Observation chỉ có sau thực thi. Kiểm tra kết quả quyết định lặp lại hay Final Answer, không luôn gọi tool vô hạn.',focus='react')
mc(D,'react-tool-error',[34,37,38],'Sau observation báo không tìm thấy chuyến bay, bước tiếp theo nào phù hợp nhất?','Phân tích kết quả, điều chỉnh truy vấn nếu hợp lý hoặc trả lời rằng chưa tìm thấy','Tự tạo một chuyến bay rồi trình bày như kết quả công cụ','Coi lời gọi search_flights là bằng chứng đặt vé thành công',
 'Observation là bằng chứng thực thi. Kết quả rỗng yêu cầu xem lại giả định hoặc báo giới hạn; Action mới chỉ là yêu cầu, không phải xác nhận giao dịch.',focus='react',context='Agent đã gọi search_flights với ngày và điểm đi/đến, công cụ trả về danh sách rỗng.')
match(D,'react-native',[34,46,47,48],'Ghép một-một cách tổ chức/cơ chế với mô tả chính xác.',[
 ('ReAct','Xen kẽ suy luận, hành động và quan sát','ReAct quy định vòng giải quyết nhiệm vụ dựa vào quan sát.'),
 ('Function Calling','Model tạo yêu cầu gọi hàm có cấu trúc','Function Calling là cơ chế biểu diễn lời gọi, có thể nằm trong vòng ReAct.'),
 ('Hybrid ReAct + native Function Calling','Giữ vòng suy luận–quan sát và dùng lời gọi hàm có cấu trúc','Hybrid kết hợp pattern điều khiển với cơ chế giao tiếp tool, không phải hai lựa chọn loại trừ.')],
 'Không đồng nhất pattern ReAct với kiểu output JSON. Ứng dụng vẫn phải thực thi tool và trả kết quả cho agent.',focus='react')
order(D,'react-dependent-tools',[40],'Trong quy trình đã quy định: xác nhận hàng và giá trước, kiểm mã giảm giá sau, rồi mới tính tổng có phí giao hàng. Sắp xếp các bước.',[
 'Kiểm tra tồn kho và đơn giá','Nhận kết quả tồn kho, sau đó kiểm mã giảm giá','Dùng giá và mức giảm đã xác minh để tính tiền hàng, lấy phí giao hàng','Tổng hợp tổng thanh toán từ các kết quả đã nhận'],
 'Đề đã chỉ rõ phụ thuộc của quy trình. Không suy ra rằng mọi tool trong mọi agent đều phải chạy nối tiếp; các yêu cầu độc lập có thể chạy song song.',focus='react')
mc(D,'react-stop',[34,39],'Điều kiện nào cho phép agent tạo Final Answer có căn cứ?','Đã có đủ kết quả liên quan để đáp ứng yêu cầu, hoặc phải dừng và nói rõ phần chưa giải quyết','Chỉ cần đã gọi ít nhất một tool, dù kết quả không liên quan','Chỉ cần model sinh câu trả lời dài hơn observation',
 'Vòng ReAct dùng observation để đánh giá đủ thông tin; dừng do giới hạn không cho phép che giấu phần chưa hoàn thành. Số tool call và độ dài không chứng minh nhiệm vụ đã xong.',focus='react',context='Người dùng yêu cầu gợi ý chuyến bay và trang phục theo thời tiết. Agent đã nhận cả kết quả tìm chuyến và dự báo liên quan.')
essay(D,'react-explain',[34,37,46,48],'Giải thích ngắn vì sao một agent dùng native Function Calling vẫn có thể là ReAct.',
 'ReAct mô tả vòng suy luận → hành động → quan sát. Native Function Calling biểu diễn hành động dưới dạng tên hàm/tham số có cấu trúc; ứng dụng chạy hàm và đưa kết quả trở lại vòng, nên hai khái niệm kết hợp được.',
 'Một khái niệm là pattern điều khiển, khái niệm kia là cơ chế gọi công cụ. Chỉ có JSON tool call chưa chứng minh agent đã dùng observation để quyết định vòng tiếp theo.',[
 ('Phân biệt pattern với cơ chế','Nêu ReAct là vòng điều khiển và Function Calling là cơ chế gọi hàm','Chỉ mô tả đúng một trong hai','Đồng nhất hai khái niệm hoặc coi chúng loại trừ nhau'),
 ('Nối kết quả tool vào vòng','Nêu ứng dụng thực thi và kết quả quay lại thành observation','Có nhắc kết quả tool nhưng thiếu vòng quyết định tiếp theo','Cho rằng model tự thực thi hàm hoặc không cần kết quả')],focus='react')
mc('p2-t3-d01','plan-react',[34,35],'Điểm khác biệt chính của quy trình Plan–Act–Verify so với vòng ReAct cơ bản là gì?','Tách rõ bước lập kế hoạch và xác minh, có thể lập lại kế hoạch khi kiểm tra thất bại','Cấm sử dụng công cụ trong bước Act','Luôn trả Final Answer ngay sau lập kế hoạch, không cần kiểm tra',
 'Plan–Act–Verify tách ba pha để kiểm soát tác vụ dài; ReAct xen kẽ suy luận và hành động theo observation. Đây không phải khẳng định một pattern luôn thắng mọi bài toán.',focus='react')
save('react')
