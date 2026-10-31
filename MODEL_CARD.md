# Model card

## Mục đích

Model phân loại bình luận mua sắm tiếng Việt thành hai nhãn `POS` và `NEG`. Use case phù hợp nhất là baseline phân tích hoặc bước sàng lọc ban đầu cho đội chăm sóc khách hàng.

Model không được thiết kế để tự động xử lý khiếu nại, đánh giá người dùng, hoặc ra quyết định có ảnh hưởng trực tiếp đến quyền lợi của khách hàng.

## Dữ liệu

- 15.000 bản ghi ban đầu, gồm `comment` và `label`.
- 12.895 bình luận được dùng sau khi loại nội dung trùng và nhãn mâu thuẫn.
- Tỷ lệ sau làm sạch xấp xỉ 72,32% POS và 27,68% NEG.
- Nguồn gốc và giấy phép tái phân phối của file học tập chưa được xác minh độc lập.

## Pipeline

1. Chuẩn hóa Unicode, emoji, teencode và một số từ tiếng Anh.
2. Bảo vệ cụm phủ định như `không_tốt` trước khi lọc từ.
3. POS-tagging bằng `underthesea` và loại stopword.
4. Vector hóa bằng unigram/bigram.
5. Logistic Regression, có và không có `class_weight="balanced"`.

## Kết quả trên split hiện tại

| Cấu hình | Accuracy | Macro-F1 | NEG Precision | NEG Recall | NEG F1 |
|---|---:|---:|---:|---:|---:|
| TF-IDF, không cân bằng | 0,893 | 0,862 | 0,844 | 0,754 | 0,797 |
| TF-IDF, balanced | 0,874 | 0,854 | 0,716 | 0,904 | 0,799 |

ROC-AUC khoảng 0,950 cho TF-IDF khi xem NEG là lớp dương. Các con số này chỉ mô tả split cố định trong notebook, không phải cam kết hiệu năng ngoài mẫu.

## Rủi ro và giới hạn

- Nhãn gốc có thể có nhiễu; một số câu vừa khen vừa chê khó biểu diễn bằng một nhãn duy nhất.
- Từ mới, tiếng lóng và danh mục sản phẩm khác có thể làm hiệu năng giảm.
- Accuracy dễ gây hiểu nhầm khi POS chiếm đa số; luôn đọc cùng metric của NEG.
- Nếu dùng để ưu tiên ticket CSKH, cần chọn ngưỡng dựa trên năng lực xử lý và kiểm tra công bằng theo nhóm sản phẩm/kênh bán.

## Bước tiếp theo hợp lý

- Cross-validation và một holdout theo thời gian hoặc theo sản phẩm.
- Đánh giá PR-AUC và hiệu chỉnh ngưỡng theo chi phí vận hành.
- Rà soát thủ công một mẫu lỗi có độ tự tin cao.
- So sánh baseline với một mô hình ngữ cảnh tiếng Việt như PhoBERT.


