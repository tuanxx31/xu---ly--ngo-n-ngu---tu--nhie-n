# -*- coding: utf-8 -*-

APP_TITLE = "HỆ THỐNG GỢI Ý CHỦ ĐỀ BÀI VIẾT NGẮN"
HISTORY_FILE = "analysis_history.json"
MIN_WORDS_REQUIRED = 5

TOPICS = [
    "Công nghệ", "Giáo dục", "Sức khỏe", "Thể thao", "Kinh tế", "Ẩm thực",
    "Văn hóa - Nghệ thuật", "Pháp luật", "Du lịch", "Xe", "Đời sống", "Bất động sản",
]

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
            "tự động hóa": 2.0, "api": 1.5, "phần cứng": 2.0, "blockchain": 2.0,
            "thực tế ảo": 2.0, "kỹ thuật số": 2.0, "linh kiện": 1.5, "công nghệ thông tin": 2.5,
        },
        "strong_phrases": {
            "trí tuệ nhân tạo": 3.0, "cơ sở dữ liệu": 3.0, "điện toán đám mây": 3.0,
            "bảo mật thông tin": 3.0, "công nghệ số": 3.0, "tự động hóa": 3.0,
            "hệ thống phần mềm": 3.0, "lập trình python": 3.0, "an ninh mạng": 3.0,
            "công nghệ blockchain": 3.0, "chuyển đổi số": 3.0, "phát triển ứng dụng": 3.0,
        },
    },
    "Giáo dục": {
        "keywords": {
            "học sinh": 2.0, "sinh viên": 2.0, "giáo viên": 2.0, "lớp học": 2.0,
            "bài giảng": 2.0, "học tập": 1.5, "kiến thức": 1.5, "kỳ thi": 2.0,
            "đào tạo": 2.0, "trường học": 2.0, "nhà trường": 2.0, "giảng dạy": 2.0,
            "môn học": 1.5, "điểm số": 1.5, "giáo trình": 2.0, "sách vở": 1.5,
            "thư viện": 1.5, "bài kiểm tra": 2.0, "kỹ năng": 1.0, "học bổng": 2.0,
            "du học": 2.0, "nghiên cứu": 1.5, "đại học": 2.0, "phổ thông": 1.5,
        },
        "strong_phrases": {
            "học trực tuyến": 3.0, "bài giảng online": 3.0, "kỳ thi cuối kỳ": 3.0,
            "lớp học": 3.0, "bài giảng": 3.0, "phương pháp giảng dạy": 3.0,
            "chương trình đào tạo": 3.0, "môi trường học tập": 3.0, "tuyển sinh đại học": 3.0,
            "phát triển kỹ năng": 3.0, "đổi mới giáo dục": 3.0,
        },
    },
    "Sức khỏe": {
        "keywords": {
            "bác sĩ": 2.0, "bệnh": 1.0, "bệnh viện": 2.0, "thuốc": 2.0,
            "điều trị": 2.0, "khám bệnh": 2.0, "dinh dưỡng": 2.0, "cơ thể": 1.0,
            "giấc ngủ": 2.0, "sức đề kháng": 2.0, "sức khỏe": 1.0, "triệu chứng": 2.0,
            "chế độ ăn": 2.0, "rau xanh": 1.5, "nước uống": 1.5, "miễn dịch": 2.0,
            "huyết áp": 2.0, "xét nghiệm": 2.0, "bệnh nhân": 1.5, "yoga": 1.5,
            "tập thể dục": 2.0, "vắc-xin": 2.0, "y tế": 2.0, "tâm lý": 1.5,
        },
        "strong_phrases": {
            "khám bệnh": 3.0, "điều trị bệnh": 3.0, "chế độ ăn": 3.0,
            "sức đề kháng": 3.0, "giấc ngủ": 3.0, "bác sĩ chuyên khoa": 3.0,
            "phác đồ điều trị": 3.0, "khám bệnh định kỳ": 3.0, "chăm sóc sức khỏe": 3.0,
            "phòng chống dịch bệnh": 3.0, "lối sống lành mạnh": 3.0,
        },
    },
    "Thể thao": {
        "keywords": {
            "bóng đá": 2.0, "cầu thủ": 2.0, "vận động viên": 2.0, "trận đấu": 2.0,
            "thi đấu": 2.0, "huấn luyện viên": 2.0, "ghi bàn": 2.0, "giải đấu": 2.0,
            "sân vận động": 2.0, "trọng tài": 2.0, "đội bóng": 2.0, "bóng rổ": 2.0,
            "chiến thuật": 1.5, "chuyền bóng": 2.0, "sút bóng": 2.0, "huy chương": 2.0,
            "tỷ số": 1.5, "khởi động": 1.0, "thể lực": 1.0, "đua xe": 2.0,
            "quần vợt": 2.0, "bơi lội": 2.0, "cúp": 1.5, "olympic": 2.0,
        },
        "strong_phrases": {
            "trận đấu": 3.0, "ghi bàn": 3.0, "sân vận động": 3.0,
            "huấn luyện viên": 3.0, "đội bóng": 3.0, "vận động viên": 3.0,
            "chiến thuật pressing": 3.0, "đội hình thi đấu": 3.0, "giải ngoại hạng": 3.0,
            "tinh thần thể thao": 3.0, "thành tích thi đấu": 3.0,
        },
    },
    "Kinh tế": {
        "keywords": {
            "thị trường": 2.0, "cổ phiếu": 2.0, "lạm phát": 2.0, "lãi suất": 2.0,
            "doanh thu": 2.0, "đầu tư": 2.0, "ngân hàng": 2.0, "xuất khẩu": 2.0,
            "nhập khẩu": 2.0, "ngoại tệ": 2.0, "gdp": 2.0, "tài chính": 2.0,
            "kinh doanh": 1.5, "lợi nhuận": 2.0, "vốn": 1.5, "chứng khoán": 2.0,
            "doanh nghiệp": 1.5, "thuế": 1.5, "ngân sách": 2.0, "kinh tế": 1.0,
            "thương mại": 2.0, "tiền tệ": 2.0, "trái phiếu": 2.0, "tài khoản": 1.5,
            "startup": 2.0, "tín dụng": 2.0, "vàng": 1.5, "công ty": 1.5,
        },
        "strong_phrases": {
            "thị trường chứng khoán": 3.0, "tăng trưởng kinh tế": 3.0,
            "chính sách tiền tệ": 3.0, "lãi suất ngân hàng": 3.0,
            "tỷ giá ngoại tệ": 3.0, "cán cân thương mại": 3.0,
            "đầu tư nước ngoài": 3.0, "ngân sách nhà nước": 3.0, "khởi nghiệp startup": 3.0,
            "phát triển kinh tế": 3.0, "quản lý tài chính": 3.0,
        },
    },
    "Ẩm thực": {
        "keywords": {
            "món ăn": 2.0, "nấu ăn": 2.0, "đầu bếp": 2.0, "gia vị": 2.0,
            "thực phẩm": 1.5, "nguyên liệu": 2.0, "nhà hàng": 2.0, "hương vị": 2.0,
            "công thức": 2.0, "nêm nếm": 2.0, "chế biến": 2.0, "thực đơn": 2.0,
            "quán ăn": 2.0, "đặc sản": 2.0, "bánh": 1.5, "nước chấm": 2.0,
            "xào": 1.5, "luộc": 1.5, "nướng": 1.5, "chiên": 1.5,
            "bếp": 1.5, "phở": 2.0, "bún": 1.5, "canh": 1.5, "dinh dưỡng": 1.0,
            "tráng miệng": 2.0, "đồ uống": 1.5, "ẩm thực": 2.0, "lẩu": 2.0,
        },
        "strong_phrases": {
            "ẩm thực đường phố": 3.0, "nguyên liệu tươi sống": 3.0,
            "món ăn truyền thống": 3.0, "công thức nấu ăn": 3.0,
            "đặc sản vùng miền": 3.0, "nghệ thuật ẩm thực": 3.0,
            "hương vị đặc trưng": 3.0, "chế biến món ăn": 3.0, "nhà hàng cao cấp": 3.0,
            "ẩm thực vùng miền": 3.0, "bí quyết nấu ăn": 3.0,
        },
    },
    "Văn hóa - Nghệ thuật": {
        "keywords": {
            "nghệ sĩ": 2.0, "ca sĩ": 2.0, "phim": 1.5, "sân khấu": 2.0,
            "triển lãm": 2.0, "tranh": 1.5, "âm nhạc": 2.0, "hội họa": 2.0,
            "diễn viên": 2.0, "nhạc sĩ": 2.0, "đạo diễn": 2.0, "kịch": 2.0,
            "thơ": 1.5, "văn học": 2.0, "điện ảnh": 2.0, "ca khúc": 2.0,
            "biểu diễn": 2.0, "lễ hội": 2.0, "di sản": 2.0, "múa": 1.5,
            "truyền thống": 1.0, "tác phẩm": 2.0, "nhà văn": 2.0, "nhạc cụ": 2.0,
            "văn hóa": 2.0, "bảo tàng": 2.0, "di tích": 2.0, "nghệ thuật": 2.0,
        },
        "strong_phrases": {
            "nghệ thuật đương đại": 3.0, "lễ hội văn hóa": 3.0,
            "di sản văn hóa": 3.0, "sân khấu kịch": 3.0,
            "điện ảnh việt nam": 3.0, "triển lãm nghệ thuật": 3.0,
            "âm nhạc truyền thống": 3.0, "văn hóa dân gian": 3.0, "tác phẩm nghệ thuật": 3.0,
            "biểu diễn nghệ thuật": 3.0, "văn hóa nghệ thuật": 3.0,
        },
    },
    "Pháp luật": {
        "keywords": {
            "tòa án": 2.0, "bị cáo": 2.0, "luật sư": 2.0, "khởi tố": 2.0,
            "xét xử": 2.0, "hình sự": 2.0, "bản án": 2.0, "vi phạm": 2.0,
            "pháp luật": 1.0, "tội phạm": 2.0, "hình phạt": 2.0, "công an": 1.5,
            "điều tra": 2.0, "truy tố": 2.0, "luật": 1.0, "quy định": 1.0,
            "chứng cứ": 2.0, "bồi thường": 2.0, "kiện": 1.5, "phạm tội": 2.0,
            "viện kiểm sát": 2.0, "thẩm phán": 2.0, "bào chữa": 2.0, "tạm giam": 2.0,
            "hiến pháp": 2.0, "dân sự": 2.0, "hợp đồng": 2.0, "quyền lợi": 2.0,
        },
        "strong_phrases": {
            "vi phạm pháp luật": 3.0, "bộ luật hình sự": 3.0,
            "quyền công dân": 3.0, "tòa án nhân dân": 3.0,
            "viện kiểm sát nhân dân": 3.0, "khởi tố vụ án": 3.0,
            "xét xử sơ thẩm": 3.0, "bản án tử hình": 3.0, "tư vấn pháp luật": 3.0,
            "quy định pháp luật": 3.0, "tranh chấp dân sự": 3.0,
        },
    },
    "Du lịch": {
        "keywords": {
            "du khách": 2.0, "khách sạn": 2.0, "resort": 2.0, "tham quan": 2.0,
            "địa điểm": 1.5, "vé máy bay": 2.0, "hành trình": 2.0, "tour": 2.0,
            "du lịch": 1.0, "cảnh đẹp": 2.0, "bãi biển": 2.0, "di tích": 2.0,
            "lữ hành": 2.0, "homestay": 2.0, "hướng dẫn viên": 2.0, "danh lam": 2.0,
            "thắng cảnh": 2.0, "đặt phòng": 2.0, "khám phá": 1.5, "trải nghiệm": 1.0,
            "phượt": 2.0, "visa": 2.0, "hành lý": 2.0, "chuyến bay": 2.0,
            "điểm đến": 2.0, "vườn quốc gia": 2.0, "di sản": 2.0, "nghỉ dưỡng": 2.0,
        },
        "strong_phrases": {
            "du lịch sinh thái": 3.0, "điểm đến du lịch": 3.0,
            "khách sạn nghỉ dưỡng": 3.0, "danh lam thắng cảnh": 3.0,
            "tour du lịch": 3.0, "hướng dẫn viên du lịch": 3.0,
            "du lịch trải nghiệm": 3.0, "khu nghỉ dưỡng": 3.0, "đặt vé máy bay": 3.0,
            "hành trình khám phá": 3.0, "du lịch bụi": 3.0,
        },
    },
    "Xe": {
        "keywords": {
            "ô tô": 2.0, "xe máy": 2.0, "động cơ": 2.0, "mã lực": 2.0,
            "sedan": 2.0, "suv": 2.0, "nhiên liệu": 2.0, "lái xe": 2.0,
            "xe hơi": 2.0, "hộp số": 2.0, "tăng tốc": 1.5, "phanh": 2.0,
            "xe điện": 2.0, "hybrid": 2.0, "lốp xe": 2.0, "khung gầm": 2.0,
            "công suất": 1.5, "xe tải": 2.0, "bảo dưỡng": 2.0, "đại lý": 1.5,
            "xe bán tải": 2.0, "hãng xe": 2.0, "phiên bản": 1.0, "nội thất": 1.5,
            "giao thông": 1.5, "phụ tùng": 2.0, "an toàn": 1.5, "siêu xe": 2.0,
        },
        "strong_phrases": {
            "xe ô tô": 3.0, "động cơ turbo": 3.0,
            "xe máy điện": 3.0, "hộp số tự động": 3.0,
            "xe bán tải": 3.0, "bảo dưỡng xe": 3.0,
            "xe điện thông minh": 3.0, "đại lý ủy quyền": 3.0, "công nghệ ô tô": 3.0,
            "an toàn giao thông": 3.0, "nội thất xe hơi": 3.0,
        },
    },
    "Đời sống": {
        "keywords": {
            "gia đình": 2.0, "hôn nhân": 2.0, "nuôi dạy": 2.0, "tiêu dùng": 2.0,
            "mua sắm": 2.0, "nhà cửa": 2.0, "con cái": 2.0, "vợ chồng": 2.0,
            "nội trợ": 2.0, "chi tiêu": 2.0, "phụ huynh": 1.5, "hàng xóm": 2.0,
            "đám cưới": 2.0, "ly hôn": 2.0, "sinh hoạt": 1.5, "thời trang": 1.5,
            "làm đẹp": 2.0, "mỹ phẩm": 2.0, "trang trí": 1.5, "cuộc sống": 1.0,
            "bỉm sữa": 2.0, "thai kỳ": 2.0, "dọn dẹp": 1.5, "tiết kiệm": 1.5,
            "chăm sóc": 2.0, "sức khỏe": 1.5, "hạnh phúc": 2.0, "xã hội": 1.5,
        },
        "strong_phrases": {
            "nuôi dạy con": 3.0, "đời sống gia đình": 3.0,
            "chi tiêu tiết kiệm": 3.0, "mua sắm online": 3.0,
            "hôn nhân gia đình": 3.0, "cuộc sống hàng ngày": 3.0,
            "chăm sóc gia đình": 3.0, "trang trí nhà cửa": 3.0,
        },
    },
    "Bất động sản": {
        "keywords": {
            "chung cư": 2.0, "đất nền": 2.0, "nhà phố": 2.0, "dự án": 2.0,
            "quy hoạch": 2.0, "giá đất": 2.0, "căn hộ": 2.0, "biệt thự": 2.0,
            "sổ đỏ": 2.0, "sổ hồng": 2.0, "mua bán": 1.5, "cho thuê": 1.5,
            "bất động sản": 1.0, "môi giới": 2.0, "thổ cư": 2.0, "sang nhượng": 2.0,
            "diện tích": 1.5, "xây dựng": 1.5, "tầng": 1.0, "phòng ngủ": 1.5,
            "mặt bằng": 2.0, "khu đô thị": 2.0, "pháp lý": 1.5, "chủ đầu tư": 2.0,
        },
        "strong_phrases": {
            "mua bán nhà đất": 3.0, "chung cư cao cấp": 3.0,
            "khu đô thị mới": 3.0, "dự án bất động sản": 3.0,
            "sổ đỏ chính chủ": 3.0, "giá bất động sản": 3.0,
            "căn hộ chung cư": 3.0, "đất nền dự án": 3.0,
        },
    },
}
