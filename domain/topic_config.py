# -*- coding: utf-8 -*-

APP_TITLE = "HỆ THỐNG GỢI Ý CHỦ ĐỀ BÀI VIẾT NGẮN"
HISTORY_FILE = "analysis_history.json"
MIN_WORDS_REQUIRED = 5

TOPICS = ["Công nghệ", "Giáo dục", "Sức khỏe", "Thể thao"]

STOPWORDS = {
    "là", "và", "của", "có", "trong", "một", "những", "các", "cho", "với",
    "được", "khi", "để", "thì", "mà", "này", "đó", "cũng", "rất", "nhiều",
    "về", "từ", "đang", "trên", "theo", "vào", "ra", "ở", "tại", "do", "vì",
    "nên", "đã", "sẽ", "cần", "hơn", "giúp", "việc", "mỗi", "như", "hay",
    "bị", "đến", "cùng", "qua", "lại", "thêm", "nhằm", "sau", "trước",
    "ít", "vẫn", "đều", "vừa", "mới", "rằng", "thật", "sự", "kia", "ấy",
    "nơi", "đây",
}

TOPIC_CONFIG = {
    "Công nghệ": {
        "keywords": {
            "máy tính": 2.0, "phần mềm": 2.0, "internet": 1.0, "dữ liệu": 2.0,
            "ai": 2.0, "trí tuệ nhân tạo": 2.0, "lập trình": 2.0, "thuật toán": 2.0,
            "ứng dụng": 1.0, "bảo mật": 2.0, "hệ thống": 1.5, "mạng": 1.5,
            "thiết bị": 1.5, "server": 1.5, "website": 1.5, "robot": 1.5,
            "cơ sở dữ liệu": 2.0, "điện toán đám mây": 2.0, "công nghệ số": 2.0,
            "tự động hóa": 2.0, "api": 1.5,
        },
        "strong_phrases": {
            "trí tuệ nhân tạo": 3.0, "cơ sở dữ liệu": 3.0, "điện toán đám mây": 3.0,
            "bảo mật thông tin": 3.0, "công nghệ số": 3.0, "tự động hóa": 3.0,
            "hệ thống phần mềm": 3.0, "lập trình python": 3.0, "an ninh mạng": 3.0,
        },
    },
    "Giáo dục": {
        "keywords": {
            "học sinh": 2.0, "sinh viên": 2.0, "giáo viên": 2.0, "lớp học": 2.0,
            "bài giảng": 2.0, "học tập": 1.5, "kiến thức": 1.5, "kỳ thi": 2.0,
            "đào tạo": 2.0, "trường học": 2.0, "nhà trường": 2.0, "giảng dạy": 2.0,
            "môn học": 1.5, "điểm số": 1.5, "giáo trình": 2.0, "sách vở": 1.5,
            "thư viện": 1.5, "bài kiểm tra": 2.0, "kỹ năng": 1.0,
        },
        "strong_phrases": {
            "học trực tuyến": 3.0, "bài giảng online": 3.0, "kỳ thi cuối kỳ": 3.0,
            "lớp học": 3.0, "bài giảng": 3.0, "phương pháp giảng dạy": 3.0,
            "chương trình đào tạo": 3.0, "môi trường học tập": 3.0,
        },
    },
    "Sức khỏe": {
        "keywords": {
            "bác sĩ": 2.0, "bệnh": 1.0, "bệnh viện": 2.0, "thuốc": 2.0,
            "điều trị": 2.0, "khám bệnh": 2.0, "dinh dưỡng": 2.0, "cơ thể": 1.0,
            "giấc ngủ": 2.0, "sức đề kháng": 2.0, "sức khỏe": 1.0, "triệu chứng": 2.0,
            "chế độ ăn": 2.0, "rau xanh": 1.5, "nước uống": 1.5, "miễn dịch": 2.0,
            "huyết áp": 2.0, "xét nghiệm": 2.0, "bệnh nhân": 1.5,
        },
        "strong_phrases": {
            "khám bệnh": 3.0, "điều trị bệnh": 3.0, "chế độ ăn": 3.0,
            "sức đề kháng": 3.0, "giấc ngủ": 3.0, "bác sĩ chuyên khoa": 3.0,
            "phác đồ điều trị": 3.0, "khám bệnh định kỳ": 3.0,
        },
    },
    "Thể thao": {
        "keywords": {
            "bóng đá": 2.0, "cầu thủ": 2.0, "vận động viên": 2.0, "trận đấu": 2.0,
            "thi đấu": 2.0, "huấn luyện viên": 2.0, "ghi bàn": 2.0, "giải đấu": 2.0,
            "sân vận động": 2.0, "trọng tài": 2.0, "đội bóng": 2.0, "bóng rổ": 2.0,
            "chiến thuật": 1.5, "chuyền bóng": 2.0, "sút bóng": 2.0, "huy chương": 2.0,
            "tỷ số": 1.5, "khởi động": 1.0, "thể lực": 1.0,
        },
        "strong_phrases": {
            "trận đấu": 3.0, "ghi bàn": 3.0, "sân vận động": 3.0,
            "huấn luyện viên": 3.0, "đội bóng": 3.0, "vận động viên": 3.0,
            "chiến thuật pressing": 3.0, "đội hình thi đấu": 3.0,
        },
    },
}
