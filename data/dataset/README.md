# Dataset folder

Nguồn dataset dự kiến: [Roboflow Smoking Detection](https://universe.roboflow.com/kyunghee-university-ada5d/smoking-detection-3gefl).

Dataset này thuộc workspace/project công khai trên Roboflow, nhưng thao tác export/download yêu cầu Roboflow API key. Không lưu API key trong repository.

## Tải dataset

1. Mở project trên Roboflow và lấy API key cá nhân trong phần Roboflow Settings.
2. Chọn version muốn export, sau đó chạy PowerShell tại thư mục gốc project:

```powershell
$env:ROBOFLOW_API_KEY = "your-roboflow-api-key"
& .\.venv\Scripts\python.exe scripts\download_roboflow_dataset.py --version 1
```

Có thể thay `--version 1` bằng version thực tế của project. Script mặc định xuất định dạng `yolov8` vào `data/dataset`.

Nếu muốn dùng version hoặc thư mục khác:

```powershell
& .\.venv\Scripts\python.exe scripts\download_roboflow_dataset.py --version 1 --format yolov8 --output data\dataset
```

Thư mục này được tạo sẵn để lưu dữ liệu huấn luyện cho custom YOLO model của AIRIS.

Cấu trúc đề xuất:

```text
data/
└── dataset/
    ├── README.md
    ├── train/
    │   ├── images/
    │   └── labels/
    └── val/
        ├── images/
        └── labels/
```

Hướng dẫn:
- đặt ảnh train vào `data/dataset/train/images/`
- đặt file annotation YOLO tương ứng vào `data/dataset/train/labels/`
- tương tự với `val/`
- khi tôi cung cấp ảnh thật sau này, bạn có thể đặt vào đây và tiếp tục train custom model

Lưu ý:
- đây là thư mục dữ liệu huấn luyện; chưa chứa ảnh thật để tránh làm project quá nặng
- hiện tại mục tiêu là chuẩn bị cấu trúc sẵn sàng cho custom dataset sau này
