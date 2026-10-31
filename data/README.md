# Dữ liệu

`raw/lazada_data.csv` là file đầu vào của notebook, gồm hai cột:

| Cột | Ý nghĩa |
|---|---|
| `comment` | Nội dung bình luận tiếng Việt |
| `label` | Nhãn cảm xúc `POS` hoặc `NEG` |

File có 15.000 dòng. Notebook thực hiện kiểm tra missing, trùng lặp và nhãn mâu thuẫn trước khi tạo tập train/test.

Nguồn gốc và giấy phép tái phân phối của file học tập chưa được xác minh độc lập. Nếu chuyển repository sang public, cần kiểm tra quyền sử dụng dữ liệu và cân nhắc thay file đầy đủ bằng một sample nhỏ có nguồn rõ ràng.


