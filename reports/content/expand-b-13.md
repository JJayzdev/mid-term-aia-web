# Kiểm định độc lập B13

**32 approved** exact revisions trong JSON (26 r1, 6 r2). Đã đọc toàn bộ stem/options/answers/explanations và xem 26 trang vật lý được trích dẫn của T4 Days5–6; ảnh ở `tmp/reviewer/expand-b-13/`. Hai SHA256 nguồn khớp catalog, schema kiểm lại thành công.

Finding factual/scope đã đóng: d05x08 r1 ngụ ý predict với process noise luôn làm covariance tăng. r2 nêu rõ mô hình một chiều hệ số 1 và noise độc lập Q>0 nên P_next=P+Q; đã đối chiếu công thức p19. Không mở rộng kết luận này sang F co hoặc mọi matrix transition.

Năm findings distractor đã đóng: d05x14 bỏ ID chẵn/lẻ; d06x02/x04/x08/x14 thay filler bằng nhầm lẫn về per-point timing, voxel resolution, box semantics và common fusion representation. Đã đọc đúng r2 và kiểm answer IDs sau rút còn 3 options.

Đã so với 8 legacy cùng PDF: gain/innovation/process-noise/UKF/PF/fusion errors khác predict-update order và EKF; preprocessing mismatch classification khác bài chẩn đoán frame/yaw tổng hợp. Gate chỉ nội dung B13, không kiểm thử app hay phê duyệt batch khác. Không sửa draft/bank.

## Bằng chứng từng câu

- **p2-t4-d05-x01 r1 approved**: PDF p3: GPS mất vẫn prediction/dead reckoning bằng motion sensors, GPS trở lại update drift; c đúng. Không tái dùng last GPS như measurement mới. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x02 r1 approved**: PDF p5: Gyro mượt ngắn hạn nhưng drift, accelerometer gravity reference giúp dài hạn; b đúng. Không nói cả hai noise-free hoặc đảo tính chất. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x03 r1 approved**: PDF p7: EnKF dùng spread của ensemble để ước lượng P lớn; a đúng. Một trajectory hoặc P=0 không biểu diễn uncertainty. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x04 r1 approved**: PDF p14: Gaussian một chiều sigma lớn biểu diễn belief rộng/kém chắc chắn; d đúng. Không buộc mean hoặc bias đổi. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x05 r1 approved**: PDF p15: Fusion hai Gaussian độc lập dùng inverse variance, mean nghiêng nguồn variance nhỏ; c đúng. Stem giữ điều kiện độc lập. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x06 r1 approved**: PDF p17: Innovation là measurement trừ predicted measurement; b đúng với scalar H=1 minh họa. Không phải Q+R hay covariance difference. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x07 r1 approved**: PDF p17: K gần 1 kéo estimate mạnh về measurement; a đúng theo x_new=x_pred+K(z-x_pred). Không reset hoặc đảo residual. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x08 r2 approved**: PDF p19: r2 nêu x_next=x+u+w, w độc lập variance Q>0; d đúng vì P_next=P+Q. Đã đóng overgeneralization: không khẳng định P luôn tăng với mọi F. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x09 r1 approved**: PDF p23: Giữ prediction uncertainty, tăng R làm gain giảm và tin measurement ít hơn; c đúng. Không bỏ motion model hoặc coi R lớn là sensor mạnh. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x10 r1 approved**: PDF p25: State position/velocity, dynamics và covariance coupling cho ước lượng vận tốc từ chuỗi vị trí; b đúng. Không cần đổi nhãn hoặc cố định velocity. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x11 r1 approved**: PDF p27: Off-diagonal covariance mô tả liên hệ sai số các thành phần state; a đúng. Diagonal là variance từng biến, không mean/count. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x12 r1 approved**: PDF p32: UKF truyền sigma points qua hàm phi tuyến rồi weighted mean/covariance; d đúng. Khác Jacobian EKF hoặc một sample bỏ spread. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x13 r1 approved**: PDF p33: Particle filter weighted samples giữ đa giả thuyết vị trí; c đúng. Gaussian đơn không biểu diễn ba mode tách biệt. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x14 r2 approved**: PDF p33: Resampling nhân high-weight và bỏ low-weight particles; r2 c đúng. Distractors cùng pha motion/weighting thay filler chẵn/lẻ. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x15 r1 approved**: PDF p37: Trackers chung nguồn có correlated errors, không tự coi độc lập; a đúng. Double counting gây overconfidence. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d05-x16 r1 approved**: PDF p38: Gating so innovation với uncertainty kỳ vọng; d đúng. Absolute value/name/arrival order không là kiểm residual consistency. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x01 r1 approved**: PDF p4: Deskew train/inference khác nhau là preprocessing mismatch; b đúng. Không quy ngay score threshold hoặc class imbalance. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x02 r2 approved**: PDF p5: Point time offset kết hợp motion/pose để deskew scan; r2 b đúng. Timestamp toàn scan không thay thời điểm từng point. Nguồn p5 liệt kê attribute, p4 đã xem nêu deskew trong preprocessing. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x03 r1 approved**: PDF p8: Vanilla PointNet yếu local neighborhood và khó scale scene lớn; d đúng. Vẫn dùng làm building block/refinement, không bắt buộc voxel input. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x04 r2 approved**: PDF p9: Voxel size đổi chi tiết hình học và quality/memory/latency; r2 c đúng. Voxel nhỏ không luôn giảm memory, voxel lớn không giữ nguyên mọi vật nhỏ. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x05 r1 approved**: PDF p9: Range crop loại points ngoài vùng trước detector, mất coverage/recall; b đúng. Model không suy chính xác dữ liệu đã bỏ theo mặc định. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x06 r1 approved**: PDF p9: Benchmark giữ voxel size/range/max points/max voxels; a đúng. Model name/checkpoint/seed không thay preprocessing contract. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x07 r1 approved**: PDF p10: Pillar nén chiều cao sớm nên có thể mất chi tiết z cho vật chồng lớp; d đúng. Không khẳng định mọi z luôn được giữ. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x08 r2 approved**: PDF p11: Box conventions w/l/h, center, axis/yaw phải khớp; r2 b đúng. Cùng tensor shape hoặc đổi units đơn lẻ chưa đủ. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x09 r1 approved**: PDF p12: Center-based head regress size/orientation/possibly velocity sau center; b đúng. Không chỉ anchor ID, class hoặc GT IoU. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x10 r1 approved**: PDF p13: Near-ego false positives tác động planner khác vùng xa; a đúng. Aggregate mAP không bao hàm safety theo slice. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x11 r1 approved**: PDF p19: Feature fusion học feature riêng từng modality rồi ghép; d đúng. Raw input là early, outputs/tracks là late. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x12 r1 approved**: PDF p20: Frustum PointNets dùng 2D box tạo frustum lấy points để ước lượng box 3D; c đúng. Không bỏ point cloud hoặc gán depth cố định. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x13 r1 approved**: PDF p20: PointPainting gắn pixel semantic scores vào LiDAR point; b đúng. Không chỉ đổi viewer color hay thay xyz/ground truth yaw. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x14 r2 approved**: PDF p20: BEVFusion đưa hai feature streams về unified BEV; r2 b đúng. Final boxes là late fusion, nối index ở hệ riêng không align representation. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x15 r1 approved**: PDF p21: Box đúng trong cloud nhưng overlay ảnh sai gợi projection/calibration; d đúng. Đổi head/anchor/loss không chẩn đoán geometry này. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
- **p2-t4-d06-x16 r1 approved**: PDF p23: Drone motion 6-DoF/quay mạnh và power/compute constraints; c đúng. Không mặc định planar hoặc ít rung như xe. Đã kiểm stem/options/answer/explanation với ảnh nguồn.
