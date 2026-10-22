# Audit độc lập Root Track4

**47 approved, 1 rejected** theo revisions JSON. Reviewer khác tác giả Root. Hash12PDF khớp catalog; render90DPI và xem41trang vật lý ở `tmp/reviewer/track4/`. Tính lại gradient,quadratic cost,IoU,TTC; xem gốc công thức inverseK và hìnhfeedback.

## Finding và retest

Bốn câu d01q02,d03q03,d05q03,d06q01 revision1 có distractor cơ chế vô nghĩa/lệch topic; đã báo Root và đọc lại revision2, nay approved. D08q02 explanation nói hai mô tả đầu đúng trong khi options a,b đầu là false và shuffle=true; major, phải thay bằng tên model/IDs không tham chiếu vị trí.

## Từng câu

- **p2-t4-d01-q01 r1 approved**: p56: gradient p−y=(-.341,.242,.099), c đúng; d đảo dấu, a,b không trừ nhãn.
- **p2-t4-d01-q02 r2 approved**: p66: Gradient chỉ local, LR đặt bước; b đúng. Retest rev2 loại phương án cơ chế vô nghĩa, các lựa chọn mới nhầm bước/hướng/phạm vi local.
- **p2-t4-d01-q03 r1 approved**: p45: Exploding dùng clipping; a đúng; sigmoid/skip confusion và không kiểm norm không giải quyết theo slide.
- **p2-t4-d01-q04 r1 approved**: p81: Summary AdamW decoupled vs Adam L2 theo PyTorch ví dụ; true được nguồn nêu, không suy rộng mọi API phiên bản.
- **p2-t4-d02-q01 r1 approved**: p15: F=H−x, b đúng; phép cộng đường tắt ởoutput F+x.
- **p2-t4-d02-q02 r1 approved**: p36: O(n²d), n×2→4, a đúng, tính đại số độc lập.
- **p2-t4-d02-q03 r1 approved**: p32: Mỗi head chiếu QKV riêng, concat+project, a,d đúng; shared/all-sequential sai.
- **p2-t4-d02-q04 r1 approved**: p15: train error cao hơn là degradation không đủ overfitting, false đúng.
- **p2-t4-d03-q01 r1 approved**: p14: IoU=intersection/union=4/10=.4, a đúng, các phương án đảo/tách sai.
- **p2-t4-d03-q02 r1 approved**: p28: Confidence filter→sortdesc→highest→suppressIoU, d đúng.
- **p2-t4-d03-q03 r2 approved**: p14: Vai trò assignment/NMS/TPFP ghi cuối trang, a,c,d đúng. Retest rev2 b class-logits probability nhầm với hình học, sai hợp lý.
- **p2-t4-d03-q04 r1 approved**: p24: Sơ đồ one-to-one khôngNMS, true đúng theo ví dụ YOLO26 nguồn.
- **p2-t4-d04-q01 r1 approved**: p22: Intrinsics focal/principal/distortion; a,d đúng; transform=extrinsic,timestamp=temporal.
- **p2-t4-d04-q02 r1 approved**: p22: Lệch theo tốc độ gợi ý time sync, c đúng; đề hỏi ưu tiên chẩn đoán không khẳng định nguyên nhân duy nhất.
- **p2-t4-d04-q03 r1 approved**: p23: Online robust với dynamic objects ghi rõ, true đúng.
- **p2-t4-d04-q04 r1 approved**: p22/23: Fixed drift sau tháo lắp→extrinsic, đo reprojection+mAP/association. Rubric chẩn đoán+đo trước/sau rõ mức, trọng số1; đáp án giả định vận dụng đúng.
- **p2-t4-d05-q01 r1 approved**: p18: Predict rồi update mới, c đúng, các distractor bỏmột vế/NNtraining không phải chu trình.
- **p2-t4-d05-q02 r1 approved**: p18: Nhớ x/P, b đúng, các cặp ma trận khác không thay trạng thái/bất định.
- **p2-t4-d05-q03 r2 approved**: p31: Jacobian tại estimate current, a đúng. Retest rev2 global linear/fixedorigin/measurementaveraging đều khác local linearization nguồn.
- **p2-t4-d05-q04 r1 approved**: p31: cong mạnh/σlớn khiến lệch mean/width, true đúng theo hình.
- **p2-t4-d06-q01 r2 approved**: p9: Sparse conv chỉ nonempty,b đúng. Retest rev2 distractor dense/all-empty sai lầm adjacent,supported contrast.
- **p2-t4-d06-q02 r2 approved**: p7: Point direct,pillar vertical,range angle,a/b/c đúng; voxel continuous sai vì discretize3D.
- **p2-t4-d06-q03 r1 approved**: p5: Density giảm distance,vật xa ítpoint; true đúng.
- **p2-t4-d06-q04 r1 approved**: p4: Frame/yaw,deskew,metadata lỗi pipeline, c đúng; đổiNMS/backbone không xử lý geometry trước.
- **p2-t4-d07-q01 r1 approved**: p20: Hungarian min totalcost, a đúng;greedy b local,ID/boxcount không cost objective.
- **p2-t4-d07-q02 r1 approved**: p27: Low-score vòng2 cứu track, không tạo mới,false đúng.
- **p2-t4-d07-q03 r1 approved**: p26: ReID appearance thêmSORTmotion/geometry,c đúng;NMS/IoUonly/confidence không thêmappearance.
- **p2-t4-d07-q04 r1 approved**: p26: Tracklostlong Kalman kém tin cậy, b đúng; các distractor sai về embedding/lifecycle.
- **p2-t4-d08-q01 r1 approved**: p16: Bottomup depthpixel→BEV,d đúng;NMS/pixel-metre bỏgeometry không phải lift.
- **p2-t4-d08-q02 r2 rejected**: p16: BEVFormer projection3Dquery+temporal và DETR3Dquery3D, c,d đúng; a/b tuyệt đối sai. Lỗi explanation tham chiếu vị trí cần sửa trước approve.
- **p2-t4-d08-q03 r1 approved**: p9: Backprojection zK^-1[u,v,1],b đúng, checked geometry and displayed formula.
- **p2-t4-d08-q04 r1 approved**: p19: Đọc NDS xu hướng vì backbone/data khác,false đúng; không khẳng định ranking tuyệt đối.
- **p2-t4-d09-q01 r1 approved**: p33: Scenewise split ngăn frame near-duplicate leakage,c đúng;rename/randomframe không ngăn.
- **p2-t4-d09-q02 r1 approved**: p16: Eventtime+latewait,b đúng;ingestion/process/parquetwrite không measurementtime.
- **p2-t4-d09-q03 r1 approved**: p51: Prelabel người sửa/duyệt mớiGT,false đúng.
- **p2-t4-d09-q04 r1 approved**: p30: Data commit+splitlist+code,manifest seed; rubric2criteria định danh/split rõ0/.5/1,sum1; đáp án đúng không chỉ v3/tỷlệ.
- **p2-t4-d10-q01 r1 approved**: p39: VLA output dx/dy/dz/rotate/grip,b đúng;caption/box/depth chỉ perception khôngaction.
- **p2-t4-d10-q02 r1 approved**: p19: Qwen3VL projector-mergeronly frozenViT/LLM,a đúng; scopevídụ rõ.
- **p2-t4-d10-q03 r1 approved**: p8: Resolution/tiles/merge,a/b/d đúng;temperature outputsampling không imagebudget.
- **p2-t4-d10-q04 r1 approved**: p7: CLIP contrastive image-text,true đúng.
- **p2-t4-d11-q01 r1 approved**: p15: Appearance/contentbehavior/sensor,a/b/c đúng;epochonly không mô tả domain gap.
- **p2-t4-d11-q02 r1 approved**: p23: DR hẹp thiếucoverage/rộng phímẫu,d đúng;seedonly/appearanceonly sai.
- **p2-t4-d11-q03 r1 approved**: p36: IoU conditionbox vs redetectbox,c đúng; nguồn đề xuấtlab không chuẩnpublic,question bảo toàn qualifier.
- **p2-t4-d11-q04 r1 approved**: p38: Same steps/batch/arch để quydata effect,true đúng; không hỏi số gain minh họa.
- **p2-t4-d12-q01 r1 approved**: p17: Run card log/code/model/calibration/seed/config,a/b/d đúng;onlyweights thiếu.
- **p2-t4-d12-q02 r1 approved**: p21: Compare tolerance không everybit,true đúng trong source scope.
- **p2-t4-d12-q03 r1 approved**: p43: TTC distance÷closingvelocity=12/5=2.4,b đúng; independently viewed÷symbol and arithmetic;7subtract/60multiply/.417inverse sai.
- **p2-t4-d12-q04 r1 approved**: p26/27: Openloop resetlog,closed feedback/accumulate leadingcollision; rubric feedback+mechanism precise and weights1, đáp án không khẳng định mọiclosedloop va chạm.

## Phạm vi

Chỉ câu và trang dẫn, không chứng nhận toàn795trang Track4. Không khẳng định benchmark/phiên bảnmodel ví dụ còn mới ngoài tài liệu; các stem giới hạn theo slide khi cần. Ba rubric source-supported, thresholds cụ thể. Chưa test sản phẩm.

## Retest hai explanation revision2

Đã đọc d08q02 dùng rõ BEVFormer/DETR3D và d06q02 dùng claim voxel continuous; không tham chiếu vị trí options. Approved revision2. Tổng hiện hành48 approved:6rev2+42rev1; lịch sử finding giữ trên.
