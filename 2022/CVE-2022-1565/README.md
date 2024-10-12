# WordPress Plugin WP All Import <= 3.6.7 - Thực thi mã từ xa (RCE) (Đã xác thực)

```
Ngày: 05 tháng 11 năm 2023
Tác giả khai thác: Việt HÙng (https://github.com/phanthibichtram12)
Trang chủ của nhà cung cấp: https://www.wpallimport.com/
Link phần mềm: https://wordpress.org/plugins/wp-all-import/advanced/ (kéo xuống chọn phiên bản)
Phiên bản: <= 3.6.7 (đã thử nghiệm: 3.6.7)
Đã thử nghiệm trên: WordPress 6.1 (không phụ thuộc vào hệ điều hành vì việc khai thác này KHÔNG cung cấp tải trọng)
CVE: CVE-2022-1565
```

## MÔ TẢ LỖI LỖI
Plugin WP All Import dễ bị tấn công khi tải tệp lên tùy ý do thiếu xác thực loại tệp thông qua tệp wp_all_import_get_gz.php ở các phiên bản lên đến và bao gồm 3.6.7.
Điều này giúp những kẻ tấn công đã được xác thực, có quyền cấp quản trị viên trở lên, có thể tải các tệp tùy ý lên máy chủ của trang web bị ảnh hưởng, điều này có thể giúp thực thi mã từ xa.

## CÁCH KHAI THÁC HOẠT ĐỘNG
### 1. Chuẩn bị file zip:
 - tạo tệp PHP với tải trọng của bạn (ví dụ: shell đảo ngược)
 - đặt biến "payload_file_name" bằng tên của tệp này (ví dụ: "shell.php")
 - tạo một tệp zip có tải trọng
 - đặt biến "zip_file_to_upload" bằng PATH của tệp này (ví dụ: "/root/shell.zip")
### 2. Đăng nhập bằng tài khoản quản trị viên:
 - đặt biến "target_url" bằng URL cơ sở của mục tiêu (KHÔNG kết thúc chuỗi bằng dấu gạch chéo /)
 - đặt biến "admin_user" bằng tên người dùng của tài khoản quản trị viên
 - đặt biến "admin_pass" bằng mật khẩu của tài khoản quản trị viên
### 3. Lấy wpnonce bằng phương thức get_wpnonce_upload_file()
 - thực tế có 2 loại wpnonce:
 - wpnonce đầu tiên sẽ được truy xuất bằng phương thức get_wpnonce_edit_settings() bên trong lớp PluginSetting.
 WPnonce này cho phép chúng tôi thay đổi cài đặt plugin (kiểm tra bước 4)
 - wpnonce thứ hai sẽ được truy xuất bằng phương thức get_wpnonce_upload_file() bên trong lớp PluginSetting.
 WPnonce này cho phép chúng tôi tải tệp lên

### 4. Kiểm tra xem chế độ bảo mật plugin đã được bật hay chưa bằng phương thức check_if_secure_mode_is_enabled() bên trong lớp PluginSetting
 - nếu Chế độ bảo mật được bật, nội dung zip sẽ được đặt trong một thư mục có tên ngẫu nhiên.
 Việc khai thác sẽ vô hiệu hóa Chế độ bảo mật.
 Bằng cách tắt Chế độ bảo mật, nội dung zip sẽ được đưa vào thư mục chính (kiểm tra biến payload_url).
 Phương thức được gọi để bật và tắt Chế độ bảo mật là set_plugin_secure_mode(set_to_enabled:bool, wpnonce:str)
 - nếu Chế độ bảo mật KHÔNG được bật, việc khai thác sẽ tải tệp lên nhưng sau đó nó sẽ KHÔNG bật Chế độ bảo mật.
### 5. Tải file lên bằng phương thức upload_file(wpnonce_upload_file: str)
 - sau khi tải lên, máy chủ sẽ trả lời bằng HTTP 200 OK nhưng điều đó không có nghĩa là quá trình tải lên đã hoàn tất thành công.
 Phản hồi sẽ chứa JSON trông như thế này:
 {"jsonrpc":2.0","error":{"code":102,"message": Vui lòng xác minh rằng tệp bạn tải lên là tệp ZIP hợp lệ."},"is_valid":false,"id" :"nhận dạng"}
 Như bạn có thể thấy, nó báo rằng có lỗi với mã 102 nhưng theo kiểm tra tôi đã thực hiện thì quá trình tải lên đã hoàn tất
### 6. Kích hoạt lại Chế độ bảo mật nếu nó được bật bằng phương thức switch_back_to_secure_mode()
### 7. Kích hoạt payload bằng phương thức activate_payload()
 - bạn có thể xác định phương thức để kích hoạt tải trọng.
 Lý do đằng sau sự lựa chọn này là việc khai thác này KHÔNG cung cấp bất kỳ tải trọng nào.
 Vì bạn có thể sử dụng tải trọng tùy chỉnh nên bạn có thể muốn kích hoạt nó bằng yêu cầu HTTP POST thay vì yêu cầu HTTP GET hoặc bạn có thể muốn truyền tham số

## TẠI SAO KHAI THÁC KHAI THÁC CHẾ ĐỘ AN TOÀN?
Theo PoC của lỗ hổng này do WPSCAN cung cấp, chúng tôi có thể truy xuất các tệp đã tải lên bằng cách truy cập "trang Nhập được quản lý".
Tôi không biết tại sao nhưng sau khi tải lên bất kỳ tệp nào, tôi không thể thấy tệp đã tải lên trong trang đó (có thể cần có phiên bản Pro?).
Tôi phải tìm một giải pháp thay thế và tôi đã làm như vậy bằng cách khai thác tùy chọn này.

Trang WPSCAN: https://wpscan.com/vulnerability/578093db-a025-4148-8c4b-ec2df31743f7


### CẬP NHẬT Ngày 06 tháng 11 năm 2022
Trong khi kiểm tra, tôi nhận thấy rằng tôi đang tải lên một tệp XML không hợp lệ và đó là lý do tại sao tệp đó không hiển thị trong "trang Nhập được quản lý"

Dù sao, cách vô hiệu hóa chế độ bảo mật này có tính "tàng hình" hơn một chút vì nội dung tải lên không hiển thị trên trang quản trị.
Nếu bạn muốn xem video tải lên trên trang quản trị thì phải thực hiện nhiều bước hơn.

## CÓ VẤN ĐỀ NÀO KHI KHAI THÁC?
Để khai thác có hiệu quả, vui lòng xem xét những điều sau:
1. kiểm tra target_url và thông tin đăng nhập của quản trị viên
2. kiểm tra đường dẫn của tệp zip và tên của tải trọng (chúng có thể khác nhau)
3. nếu bạn đang kiểm tra cục bộ, hãy thử đặt verify_ssl_certificate thành Sai
4. bạn có thể sử dụng print_response(http_response) để điều tra thêm