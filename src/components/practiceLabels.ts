import type { FocusTopic, PracticeKind } from '../domain/types';

export const focusLabels: Record<FocusTopic, string> = {
  react: 'ReAct và agent', generation: 'Tham số sinh văn bản', kalman: 'Kalman và hợp nhất xác suất',
  sensors: 'Camera, radar, LiDAR và fusion', 'closed-loop': 'Open-loop và closed-loop',
  activations: 'Hàm kích hoạt', normalization: 'BatchNorm và LayerNorm',
};
export const kindLabels: Record<PracticeKind, string> = {
  matching: 'Ghép cặp', ordering: 'Sắp xếp pipeline', calculation: 'Chỉ câu tính toán', concept: 'Phân biệt khái niệm', scenario: 'Tình huống vận dụng',
};
