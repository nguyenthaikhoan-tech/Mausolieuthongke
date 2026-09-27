import re
import math


def so_thuc(chuoi):
    """
    Chuyển số dạng Việt Nam:
    2,5 -> 2.5
    """
    return float(chuoi.strip().replace(",", "."))
def hien_thi_so(x):
    """
    Hiển thị số đẹp:
    10.0 -> 10
    2.5 -> 2,5
    """

    if math.isclose(x, round(x)):
        return str(int(round(x)))

    return f"{x:.10g}".replace(".", ",")


def tao_bang_tu_dong():
    """
    Tự động tạo bảng khoảng.

    Ví dụ:
    Đầu: 10
    Cuối: 20
    Độ rộng: 2

    Tạo ra:
    [10;12)
    [12;14)
    [14;16)
    [16;18)
    [18;20)
    """

    while True:
        try:
            a_dau = so_thuc(
                input("Nhập giá trị đầu của khoảng đầu tiên: ")
            )

            b_cuoi = so_thuc(
                input("Nhập giá trị cuối của khoảng cuối cùng: ")
            )

            do_rong = so_thuc(
                input("Nhập độ rộng mỗi khoảng: ")
            )

            if b_cuoi <= a_dau:
                print("Giá trị cuối phải lớn hơn giá trị đầu.")
                continue

            if do_rong <= 0:
                print("Độ rộng khoảng phải lớn hơn 0.")
                continue

            so_khoang_thuc = (b_cuoi - a_dau) / do_rong
            so_khoang = round(so_khoang_thuc)

            # Không cho phép khoảng cuối bị ngắn hơn các khoảng còn lại
            if not math.isclose(
                so_khoang_thuc,
                so_khoang,
                rel_tol=1e-9,
                abs_tol=1e-9
            ):
                print(
                    "Khoảng từ đầu đến cuối phải chia hết cho độ rộng."
                )
                print(
                    f"Ví dụ hợp lệ: từ 10 đến 20, độ rộng 2."
                )
                continue

            break

        except ValueError:
            print("Vui lòng nhập số hợp lệ.")

    bang = []

    for i in range(so_khoang):
        dau = a_dau + i * do_rong
        cuoi = dau + do_rong

        text = f"[{hien_thi_so(dau)};{hien_thi_so(cuoi)})"

        lop = {
            "a": dau,
            "b": cuoi,
            "h": do_rong,
            "f": 0,
            "mid": (dau + cuoi) / 2,
            "text": text
        }

        bang.append(lop)

    print("\nCÁC KHOẢNG ĐÃ TẠO:")
    print("-" * 40)

    for i, lop in enumerate(bang, start=1):
        print(f"{i}. {lop['text']}")

    print("\nNHẬP TẦN SỐ:")

    for lop in bang:
        print(f"\nKhoảng {lop['text']}")
        lop["f"] = nhap_tan_so()

    return bang

def nhap_khoang():
    """
    Nhập khoảng dạng:
    [0;10)
    [10;20)
    """

    while True:
        text = input("Nhập khoảng [a;b): ").strip()

        # Cho phép nhập [0;10), [0,10), [0 ; 10)
        pattern = r"^\[\s*([-+]?\d+(?:[.,]\d+)?)\s*[;,]\s*([-+]?\d+(?:[.,]\d+)?)\s*\)$"
        match = re.match(pattern, text)

        if not match:
            print("Sai định dạng. Hãy nhập như: [0;10)")
            continue

        a = so_thuc(match.group(1))
        b = so_thuc(match.group(2))

        if b <= a:
            print("Đầu mút bên phải phải lớn hơn đầu mút bên trái.")
            continue

        return a, b, text


def nhap_tan_so():
    while True:
        try:
            f = int(input("Nhập tần số: "))

            if f < 0:
                print("Tần số không được âm.")
                continue

            return f

        except ValueError:
            print("Tần số phải là số nguyên.")


def tim_lop_chua_vi_tri(bang, vi_tri):
    """
    Tìm lớp chứa vị trí vi_tri trong bảng tần số tích lũy.
    """

    tan_so_tich_luy_truoc = 0

    for lop in bang:
        tan_so_tich_luy = tan_so_tich_luy_truoc + lop["f"]

        if vi_tri <= tan_so_tich_luy:
            return lop, tan_so_tich_luy_truoc

        tan_so_tich_luy_truoc = tan_so_tich_luy

    return bang[-1], tan_so_tich_luy_truoc - bang[-1]["f"]


def tinh_tu_phan_vi(bang, N, ty_le):
    """
    Công thức nội suy cho bảng phân lớp:

    Q = L + [(vị trí - F) / f] * h

    L: cận dưới lớp chứa tứ phân vị
    F: tần số tích lũy trước lớp
    f: tần số lớp chứa tứ phân vị
    h: độ rộng lớp
    """

    vi_tri = ty_le * N
    lop, F = tim_lop_chua_vi_tri(bang, vi_tri)

    L = lop["a"]
    f = lop["f"]
    h = lop["h"]

    if f == 0:
        return None

    return L + ((vi_tri - F) / f) * h


def tinh_trung_binh(bang, N):
    """
    Dùng trung điểm mỗi khoảng:

    x_i = (a_i + b_i) / 2
    x_bar = tổng(f_i * x_i) / N
    """

    tong = sum(lop["f"] * lop["mid"] for lop in bang)

    return tong / N


def tinh_phuong_sai(bang, N, trung_binh):
    """
    Phương sai mẫu số liệu phân lớp:

    s² = tổng(f_i * (x_i - x_bar)²) / N
    """

    tong = sum(
        lop["f"] * (lop["mid"] - trung_binh) ** 2
        for lop in bang
    )

    return tong / N
def tinh_mot(bang):
    """
    Công thức mốt cho bảng phân lớp:

    Mo = L + [d1 / (d1 + d2)] * h

    d1 = fm - f_truoc
    d2 = fm - f_sau
    """

    # Tìm lớp có tần số lớn nhất
    vi_tri_mot = max(
        range(len(bang)),
        key=lambda i: bang[i]["f"]
    )

    lop_mot = bang[vi_tri_mot]

    f_m = lop_mot["f"]

    f_truoc = (
        bang[vi_tri_mot - 1]["f"]
        if vi_tri_mot > 0
        else 0
    )

    f_sau = (
        bang[vi_tri_mot + 1]["f"]
        if vi_tri_mot < len(bang) - 1
        else 0
    )

    d1 = f_m - f_truoc
    d2 = f_m - f_sau

    if d1 + d2 == 0:
        return None, vi_tri_mot

    L = lop_mot["a"]
    h = lop_mot["h"]

    mode = L + (d1 / (d1 + d2)) * h

    return mode, vi_tri_mot


def kiem_tra_ngoai_le(Q1, Q3):
    """
    Kiểm tra các giá trị có phải là giá trị ngoại lệ không.

    IQR = Q3 - Q1
    Ngưỡng dưới = Q1 - 1.5 * IQR
    Ngưỡng trên = Q3 + 1.5 * IQR

    Giá trị ngoại lệ nếu:
    x < ngưỡng dưới hoặc x > ngưỡng trên
    """

    IQR = Q3 - Q1
    nguong_duoi = Q1 - 1.5 * IQR
    nguong_tren = Q3 + 1.5 * IQR

    print("\n" + "=" * 65)
    print("KIỂM TRA GIÁ TRỊ NGOẠI LỆ")
    print("=" * 65)

    print(f"Q1                 = {Q1:.4f}")
    print(f"Q3                 = {Q3:.4f}")
    print(f"Khoảng tứ phân vị  = {IQR:.4f}")
    print(f"Ngưỡng dưới        = {nguong_duoi:.4f}")
    print(f"Ngưỡng trên        = {nguong_tren:.4f}")

    print("\nNhập các giá trị cần kiểm tra.")
    print("Có thể cách nhau bằng dấu cách hoặc dấu chấm phẩy.")
    print("Ví dụ: 5 12 20 100")
    print("Hoặc: 2,5; 12,75; 100")

    chuoi = input("\nCác giá trị cần kiểm tra: ").strip()

    if chuoi == "":
        print("Không có giá trị nào được nhập.")
        return

    # Tách bằng dấu cách hoặc dấu chấm phẩy.
    # Không tách bằng dấu phẩy vì dấu phẩy có thể là dấu thập phân.
    danh_sach = re.split(r"[;\s]+", chuoi)

    print("\nKẾT QUẢ:")

    for gia_tri_text in danh_sach:
        try:
            x = so_thuc(gia_tri_text)

            if x < nguong_duoi or x > nguong_tren:
                print(
                    f"{x:g} -> GIÁ TRỊ NGOẠI LỆ "
                    f"(ngoài khoảng "
                    f"[{nguong_duoi:.4f}; {nguong_tren:.4f}])"
                )
            else:
                print(
                    f"{x:g} -> Không phải giá trị ngoại lệ "
                    f"(trong khoảng "
                    f"[{nguong_duoi:.4f}; {nguong_tren:.4f}])"
                )

        except ValueError:
            print(
                f"{gia_tri_text} -> Giá trị không hợp lệ, bỏ qua."
            )



def hien_thi_bang(bang):
    print("\nBẢNG DỮ LIỆU")
    print("-" * 65)
    print(f"{'Khoảng':<18}{'Tần số':<12}{'Trung điểm':<15}{'Tích lũy':<15}")
    print("-" * 65)

    tich_luy = 0

    for lop in bang:
        tich_luy += lop["f"]

        print(
            f"{lop['text']:<18}"
            f"{lop['f']:<12}"
            f"{lop['mid']:<15.4f}"
            f"{tich_luy:<15}"
        )

    print("-" * 65)


def main():
    print("=" * 65)
    print("TÍNH THỐNG KÊ CHO BẢNG SỐ LIỆU PHÂN LỚP")
    print("=" * 65)
    
    bang = tao_bang_tu_dong()
    # Sắp xếp theo cận dưới
    bang.sort(key=lambda lop: lop["a"])

    N = sum(lop["f"] for lop in bang)

    if N == 0:
        print("\nTổng tần số bằng 0, không thể tính.")
        return

    # Kiểm tra độ rộng các lớp
    do_rong_dau = bang[0]["h"]
    lop_khong_deu = any(
        not math.isclose(lop["h"], do_rong_dau, rel_tol=1e-9)
        for lop in bang
    )

    hien_thi_bang(bang)

    trung_binh = tinh_trung_binh(bang, N)
    phuong_sai = tinh_phuong_sai(bang, N, trung_binh)
    do_lech_chuan = math.sqrt(phuong_sai)

    Q1 = tinh_tu_phan_vi(bang, N, 1 / 4)
    Q2 = tinh_tu_phan_vi(bang, N, 1 / 2)
    Q3 = tinh_tu_phan_vi(bang, N, 3 / 4)

    khoang_bien_thien = bang[-1]["b"] - bang[0]["a"]
    khoang_tu_phan_vi = Q3 - Q1

    mode, vi_tri_mot = tinh_mot(bang)

    he_so_bien_thien = None
    if trung_binh != 0:
        he_so_bien_thien = do_lech_chuan / abs(trung_binh) * 100

    print("\n" + "=" * 65)
    print("KẾT QUẢ")
    print("=" * 65)

    print(f"Tổng số quan sát N        = {N}")
    print(f"Số trung bình x̄          = {trung_binh:.4f}")
    print(f"Phương sai s²             = {phuong_sai:.4f}")
    print(f"Độ lệch chuẩn s           = {do_lech_chuan:.4f}")

    if mode is not None:
        print(f"Mốt Mo                    ≈ {mode:.4f}")
        print(f"Lớp chứa mốt              = {bang[vi_tri_mot]['text']}")
    else:
        print("Mốt                       = Không xác định rõ")

    print(f"Trung vị Me = Q2          ≈ {Q2:.4f}")
    print(f"Tứ phân vị thứ nhất Q1   ≈ {Q1:.4f}")
    print(f"Tứ phân vị thứ ba Q3      ≈ {Q3:.4f}")

    print(f"Khoảng biến thiên R       ≈ {khoang_bien_thien:.4f}")
    print(f"Khoảng tứ phân vị ΔQ      ≈ {khoang_tu_phan_vi:.4f}")

    if he_so_bien_thien is not None:
        print(f"Hệ số biến thiên         ≈ {he_so_bien_thien:.4f}%")
     # Kiểm tra các giá trị đề bài cho có phải ngoại lệ không
    kiem_tra_ngoai_le(Q1, Q3)
    if lop_khong_deu:
        print("\nLƯU Ý:")
        print("- Các khoảng có độ rộng không bằng nhau.")
        print("- Công thức mốt cho bảng phân lớp thường chính xác hơn khi")
        print("  các khoảng có cùng độ rộng.")

    print("\nGiải thích:")
    print("- Số trung bình dùng trung điểm của từng khoảng.")
    print("- Trung vị và tứ phân vị được nội suy trong khoảng chứa nó.")
    print("- Khoảng biến thiên được lấy xấp xỉ bằng:")
    print("  cận phải khoảng cuối - cận trái khoảng đầu.")
    print("- Vì không có số liệu cụ thể nên tất cả kết quả là xấp xỉ.")


if __name__ == "__main__":
    main() 