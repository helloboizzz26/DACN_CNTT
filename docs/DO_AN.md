# XÂY DỰNG HỆ THỐNG GIÁM SÁT VÀ PHÁT HIỆN HÀNH VI BẤT THƯỜNG CỦA CONTAINER LÚC CHẠY

**Người thực hiện đồ án: Hồ Quốc Trí**

Repository: https://github.com/helloboizzz26/DACN_CNTT

## Mục tiêu

Xây dựng hệ thống thu thập, hiển thị và hỗ trợ điều tra các hành vi bất thường
trong container đang chạy. Đối tượng triển khai và đánh giá là Docker trên Linux.
Tên hiển thị ngắn: **Giám sát Container**.

## Nền tảng kế thừa và đóng góp

- Falco: thu thập sự kiện lúc chạy và phát hiện theo luật.
- Falcosidekick: chuyển tiếp cảnh báo.
- Falcosidekick-UI: nền tảng Go, Vue và Redis/RediSearch được kế thừa.
- Các file `falco_rules.local.yaml`, `simulate_events.py` và
  `demo_attack_scenarios.sh` đã có trong workspace trước đợt tùy biến này;
  cần kiểm chứng trước khi dùng làm bằng chứng đánh giá.

Giữ giấy phép và ghi nhận tác giả của mã nguồn kế thừa. Trong báo cáo, phân biệt
chức năng sẵn có, phần tùy biến và chức năng tự phát triển. Đổi tên giao diện
không được tính là đóng góp về phương pháp phát hiện.

## Kiến trúc

Container trên Linux → Falco → Falcosidekick → API Go → Redis/RediSearch → Vue.

Phát hiện hiện tại dựa trên luật; chưa có mô hình học máy hoặc cơ chế học hành vi
bình thường. Dữ liệu giả lập kiểm tra được đường truyền và giao diện, nhưng
không chứng minh Falco phát hiện được hành vi thực tế.

## Lộ trình và tiêu chí hoàn thành

1. **Nền tảng riêng:** build giao diện và backend từ mã nguồn; xác nhận thay đổi
   xuất hiện khi chạy Docker; tiếp nhận và tìm kiếm được cảnh báo.
2. **Bộ luật theo đề tài:** kiểm chứng các tình huống mở shell, đọc file nhạy cảm,
   chạy công cụ mạng; ghi điều kiện phát hiện, ngoại lệ và tình huống hợp lệ.
3. **Hỗ trợ điều tra:** bổ sung trang chi tiết theo container, trạng thái xử lý
   cảnh báo, ghi chú và xuất báo cáo. Đây là chức năng dự kiến, chưa triển khai.
4. **Đánh giá:** lưu phiên bản môi trường, bộ luật, kịch bản, số lần chạy, kết quả
   mong đợi và thực tế; đo precision/recall trên tập có nhãn và độ trễ cảnh báo.

Mỗi lần chạy cần lưu bằng chứng: thời điểm thực hiện hành vi, container liên quan,
luật kích hoạt, cảnh báo nhận được và nguyên nhân nếu bỏ sót hoặc cảnh báo sai.
Chỉ báo cáo số liệu đo thực tế; tách kết quả giả lập khỏi kết quả phát hiện thật.

## Chạy bản mã nguồn riêng

Từ thư mục gốc, trên máy có Docker và Docker Compose:

```sh
docker compose -f docker-compose.yml -f compose.source.yml build falcosidekick-ui
docker compose -f docker-compose.yml -f compose.source.yml up -d redis falcosidekick-ui falcosidekick
```

Truy cập `http://localhost:2802`. Cấu hình nền hiện dùng tài khoản `admin:admin`.
Lệnh trên khởi động pipeline tiếp nhận cảnh báo, chưa khởi động Falco.
Sau khi kiểm chứng cấu hình Falco trên máy Linux phù hợp, chạy:

```sh
docker compose -f docker-compose.yml -f compose.source.yml up -d falco
```

File override giúp dùng image được build tại chỗ thay cho image UI tải sẵn.
Các biến `FALCOSIDEKICK_UI_*` được giữ để tương thích backend hiện có.
Chưa xác nhận build và chạy end-to-end trong môi trường hiện tại.
