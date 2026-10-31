# Vietnamese Sentiment Analysis for Lazada Reviews

Một project nhỏ để phân loại bình luận tiếng Việt thành `POS` và `NEG`. Trọng tâm của project là một pipeline dễ đọc, có thể chạy lại và đủ rõ để thảo luận về chất lượng dữ liệu, tiền xử lý tiếng Việt và sự đánh đổi giữa Precision/Recall.

## Kết quả chính

Trên tập test stratified cố định (`random_state=42`):

- Dữ liệu gốc có 15.000 dòng. Sau khi loại bình luận trùng và các nội dung có nhãn mâu thuẫn, còn 12.895 dòng.
- TF-IDF + Logistic Regression (không cân bằng lớp) đạt Accuracy khoảng **0,893**, Macro-F1 **0,862** và ROC-AUC cho lớp NEG khoảng **0,950**.
- Khi dùng `class_weight="balanced"`, Recall của NEG tăng lên khoảng **0,904**, nhưng Precision giảm còn khoảng **0,716**.

Không có một cấu hình tốt nhất cho mọi tình huống. Nếu mục tiêu là sàng lọc phản hồi xấu cho đội CSKH, cấu hình balanced đáng cân nhắc vì bỏ sót ít bình luận NEG hơn. Nếu chi phí rà soát thủ công cao, cần tối ưu thêm ngưỡng dự đoán để giữ Precision ở mức chấp nhận được.

## Cấu trúc project

```text
.
├── data/
│   ├── README.md
│   └── raw/lazada_data.csv
├── notebooks/lazada_sentiment_analysis.ipynb
├── resources/nlp/
├── src/lazada_sentiment/
│   ├── modeling.py
│   └── preprocessing.py
├── tests/
├── MODEL_CARD.md
└── pyproject.toml
```

Notebook giữ phần khám phá, biểu đồ và diễn giải. Các đoạn xử lý có thể tái sử dụng được tách sang `src/` để tránh biến notebook thành một file code dài khó bảo trì.

## Chạy project

Project dùng Python 3.10 hoặc 3.11.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
jupyter lab notebooks/lazada_sentiment_analysis.ipynb
```

Chạy test và kiểm tra notebook đã có đủ output:

```powershell
pytest
python scripts/validate_notebook.py
```

Để chạy lại notebook từ đầu:

```powershell
python -m jupyter nbconvert --execute --to notebook --inplace `
  --ExecutePreprocessor.timeout=1800 notebooks/lazada_sentiment_analysis.ipynb
```

## Một vài lựa chọn kỹ thuật

- Loại bình luận trùng trước khi chia train/test để cùng một câu không xuất hiện ở cả hai tập.
- Bỏ toàn bộ nội dung có nhãn mâu thuẫn thay vì chọn ngẫu nhiên một nhãn.
- Chuẩn hóa Unicode, emoji, teencode, một số từ tiếng Anh và cấu trúc phủ định.
- So sánh CountVectorizer và TF-IDF trên cùng một split.
- Xem `NEG` là lớp dương khi vẽ ROC vì đây là lớp cần phát hiện trong bài toán sàng lọc khiếu nại.

## Giới hạn

- Nguồn và giấy phép của tập dữ liệu học tập chưa được xác minh độc lập. Hãy kiểm tra lại trước khi public hoặc tái phân phối dữ liệu.
- Kết quả hiện tại dựa trên một train/test split, chưa thay thế cho cross-validation hoặc đánh giá trên dữ liệu mới theo thời gian.
- POS-tagging tổng quát có thể xử lý chưa tốt teencode, tên sản phẩm và câu vừa khen vừa chê.
- Đây là baseline nghiên cứu, chưa phải model production. Project chưa có monitoring drift, versioning model hay API inference.

