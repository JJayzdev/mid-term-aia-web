# Kiểm định độc lập B12

**32 approved** tại exact revisions trong JSON (25 r1, 7 r2). Đã đọc toàn bộ câu/options/đáp án/giải thích và xem 31 trang vật lý được trích dẫn của T4 Days3–4, cùng p17 bổ trợ chẩn đoán azimuth coverage vốn đã nằm trong tập trang. Ảnh ở `tmp/reviewer/expand-b-12/`; hai PDF hashes khớp catalog và schema kiểm lại thành công.

Sáu findings về distractor đã đóng: d03x04 và x14; d04x03/x04/x09/x10 thay phương án khác modality hoặc không liên quan bằng nhầm lẫn sampling/quantization, shape/semantics, IO/throughput, camera geometry và health metrics. Đã đọc đúng 6 revision2 và kiểm mapping answer IDs mới. d04x13 r2 target-based fleet calibration cũng được đối chiếu p23.

Đã so với 8 câu legacy hai tài liệu: NMS crowded-scene trade-off khác thứ tự greedy NMS; các câu health/calibration nhắm các failure khác với extrinsics sau tháo lắp. Không phê duyệt batch khác hoặc tuyên bố app tests. Không sửa draft/bank.

## Bằng chứng từng câu

- **p2-t4-d03-x01 r1 approved**: PDF p7: Instance segmentation tách từng cá thể bằng mask; a đúng. Semantic class map không phân biệt instance; box/classification không có mask. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x02 r1 approved**: PDF p13: Letterbox resize rồi pad, đảo bằng trừ pad/chia scale; d đúng. Hai thao tác đơn lẻ không trả tọa độ ảnh gốc. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x03 r1 approved**: PDF p15: Fast R-CNN chia sẻ một lần CNN toàn ảnh, lấy RoI feature; c đúng. Không chạy CNN riêng mọi proposal như R-CNN. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x04 r2 approved**: PDF p18: RoIAlign không lượng tử hóa tọa độ, lấy mẫu bằng bilinear interpolation; r2 c đúng. Distractors rounding/max pool và nearest integer cùng lớp cơ chế, đã thay class/NMS không liên quan. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x05 r1 approved**: PDF p29: NMS threshold thấp dễ suppress người thật chồng nhau; a đúng. Nguồn nêu trade-off crowded scene, không bảo đảm giữ mọi người. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x06 r1 approved**: PDF p31: Query DETR không được ghép học no-object; d đúng. One-to-one matching không tái ghép foreground trùng GT. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x07 r1 approved**: PDF p35: CLIP zero-shot so image embedding với text class descriptions; c đúng. Không đòi train classifier mới trên toàn nhãn đích. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x08 r1 approved**: PDF p42: GT chỉ ghép một prediction, duplicate dư là FP; b đúng, không tăng TP hay biến thành FN. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x09 r1 approved**: PDF p44: Cùng aggregate mAP có thể khác AP-small; a đúng. Confidence/parameter count không thay metric slice kích thước. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x10 r1 approved**: PDF p45: Ngưỡng deployment .5 cần P/R/F1 tại ngưỡng đó; d đúng. mAP ranking không bảo đảm mọi operating point. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x11 r1 approved**: PDF p51: U-Net concat feature encoder cùng resolution vào decoder để giữ chi tiết biên; c đúng. Không chỉ final class label. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x12 r1 approved**: PDF p54: Foreground ít làm all-background prediction vẫn accuracy cao; b đúng. Class-wise IoU/Dice giúp thấy imbalance. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x13 r1 approved**: PDF p57: YOLO-seg tổ hợp shared prototypes với coefficients từng detection rồi crop/upsample; a đúng. Không dùng mask chung hoặc box rasterization. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x14 r2 approved**: PDF p67: Thứ tự keypoint là contract data/model/decoder; r2 b đúng, shape vẫn hợp lệ nhưng nhầm khớp. Đã thay distractors màu/runtime bằng shape/semantics cùng lớp. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x15 r1 approved**: PDF p70: Top-down detect rồi chạy pose cho từng person crop, latency theo số người; c đúng. Không một crop cho mọi người. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d03-x16 r1 approved**: PDF p75: PCK khi biết person location bỏ detection miss/false person; b đúng. Nó vẫn kiểm sai số keypoint trong crop, unlike distractors. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x01 r1 approved**: PDF p6: Camera có semantic/color cho sign/light; d đúng. Range/Doppler đơn thuần không cung cấp màu/chữ tương đương. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x02 r1 approved**: PDF p7: Event camera có sparse asynchronous events/low latency cho motion nhanh; c đúng, không frame RGB đầy đủ cố định. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x03 r2 approved**: PDF p8: Data rate FPS×resolution×bit depth có thể vượt IO; r2 c đúng. Inference-only/buffer-only bỏ bottleneck throughput đầu vào. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x04 r2 approved**: PDF p8: Scanline khác thời điểm gây rolling-shutter skew khi quay; r2 b đúng. Lens distortion cố định và uniform motion blur là nhầm lẫn gần, không cùng cơ chế. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x05 r1 approved**: PDF p9: 2D LiDAR chỉ quét một mặt phẳng nên bỏ vật treo hoặc thấp ngoài plane; d đúng. Không đảm bảo coverage toàn 3D. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x06 r1 approved**: PDF p10: Packet loss làm scan thủng; packet count là chẩn đoán p10, azimuth coverage được nêu rõ thêm tại p17 đã xem. c đúng, không kết luận model miss từ dữ liệu thiếu. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x07 r1 approved**: PDF p11: Radar đo Doppler velocity bên cạnh range cho ACC; b đúng. Mask/color/text là khả năng khác modality. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x08 r1 approved**: PDF p12: Sonar lân cận có ultrasonic cross-talk; a đúng theo p12, không nhầm hiện tượng camera/LiDAR. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x09 r2 approved**: PDF p16: Glare/overexposure mất texture đi cùng saturated pixel ratio; r2 c đúng. Dropped/late-frame ratio đo transport, không trực tiếp đo bão hòa pixel. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x10 r2 approved**: PDF p17: Fog tạo false returns/range giảm; density theo distance và outlier ratio phản ánh degradation; r2 b đúng. Timestamp/packet-loss đơn lẻ không xác định chất lượng returns thời tiết. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x11 r1 approved**: PDF p18: Barrier multipath gây radar ghost, cần persistence/gating/fusion; b đúng. Không tin tuyệt đối một reading hoặc bỏ toàn radar. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x12 r1 approved**: PDF p20: Critical không còn tin sensor cần disable feature hoặc safe fallback; a đúng. Mild warning/smoothing không đủ cho mức này. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x13 r2 approved**: PDF p23: Target-based checkerboard/AprilTag chính xác lab nhưng cần bố trí target, khó scale fleet; d r2 đúng. Không phải chỉ timestamp hay luôn tự calibration không target. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x14 r1 approved**: PDF p24: Timestamp gốc và interpolate/deskew ego-motion về common time; c đúng. Callback time/frame index không chứng minh đồng thời. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x15 r1 approved**: PDF p25: Pseudo-label agreement phụ thuộc calibration/time sync; b đúng. Manual audit là biện pháp kiểm, không nguyên nhân đồng loạt sai. Đã kiểm stem/options/answer/explanation với trang gốc.
- **p2-t4-d04-x16 r1 approved**: PDF p26: Health logs + raw data cho mine slice night/glare/low-density và tái hiện lỗi; a đúng. Frame count hoặc frame đẹp không thay per-slice benchmark. Đã kiểm stem/options/answer/explanation với trang gốc.
