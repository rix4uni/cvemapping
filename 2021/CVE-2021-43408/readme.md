# CVE-2021-43408: Wordpress Plugin Duplicate Post version 1.1.9 - SQL Injection

## I. Tổng quan
### 1. Wordpress là gì
WordPress là một phần mềm CMS (Content Management System) mã nguồn mở, là hệ thống quản lý nội dung. Thay vì sử dụng ngôn ngữ mã hóa HTML thì WP được viết bằng ngôn ngữ lập trình PHP sử dụng nền tảng dữ liệu của MySQL. WordPress được sáng lập bởi lập trình viên Matt Mullenweg và Mike Little. Hiện nay WordPress thuộc quyền sở hữu của công ty Automattic có trụ sở tại San Francisco, California thuộc Hoa Kỳ.

### 2. CVE-2021-43408
Plugin `Duplicate Post` của Wordpress tại các phiên bản 1.1.9 trở xuống dính phải lỗi SQL Injection. Loại khai thác này cho phép attacker có thể truyền vào những câu truy vấn SQL từ đó có thể đọc, sửa thậm chí xóa các resources trong cơ sở dữ liệu.
Lỗ hổng này có thể được khai thác bởi bất kỳ authenticated user nào có quyền sử dụng chức năng của plugin `Duplicate Post`. Theo mặc định, chỉ có Admin là có quyền này, tuy nhiên quyền hạn có thể được chỉnh sửa từ đó Editor, Author, Contributor thậm chí Subcriber cũng có thể sử dụng plugin này.
CVE-2021-43408 được tìm thấy vào "11/19/2021" và được đánh giá ở mức độ `HIGH` theo thang điểm CVSS.
![](https://i.imgur.com/pOqdida.png)

## II. Phân tích chi tiết
Nguyên nhân cốt lõi của lỗ hổng này do việc dữ liệu được gửi tới từ request phía người dùng không được sanitized trước khi đưa vào thực thi SQL.
Cụ thể  hơn là tại file `post/handler.php`, tại function `cdn_insert_post()`
```php=
 function cdp_insert_post($id, $data, $times, $areWePro, $isChild = false, $p_ids = null, $site) {

        // Get Wordpress database
        global $wpdb;

        // Create empty array for new id(s) and error(s)
        $results = array('ids' => array(), 'error' => 0, 'counter' => 0);

        // Get Counter value
        $prefix = (($site != -1) ? $wpdb->get_blog_prefix($site) : $wpdb->get_blog_prefix());
        $newestId = $wpdb->get_results("SELECT post_id FROM {$prefix}postmeta WHERE meta_key = '_cdp_origin' AND meta_value = {$id} ORDER BY post_id DESC LIMIT 1", ARRAY_A);
```
> `$id` được kiểm soát bởi attacker

Biến `$id` được truyền vào function có chứa câu truy vấn SQL mà không trải qua bất kỳ sanitize nào. Function này được gọi tới thông qua Wordpress Ajax `wp_ajax_cdp_action_handling`.
Có thể thấy rằng param `id` được truyền qua function`cdn_sanitize_array`, tại đây các trường data của post được đi qua function `sanitize_text_field`, tiến hành escape bất kỳ dấu quote nào `'` trong đoạn string dữ liệu.
![](https://i.imgur.com/DNl1eo5.png)
> Các trường dữ liệu được tiến hành `sanitize_text_field`

Tuy nhiên, đoạn code có một lỗ hổng khi tiến hành truyền dữ liệu của trường Integer vào câu thực thi SQL (trường id), attacker có thể lợi dụng điều này và chèn thêm câu lệnh SQL vào giá trị của trường này. Do đó, để có thể kiểm soát được truy vấn SQL, attacker chỉ cần tránh sử dụng ký tự `'`.
## III. Demo
### 1. Môi trường
- OS: Windows
- Xampp: 7.1.33
- Wordpress: 5.0
- Plugin Duplicate Post: 1.1.9
### 2. PoC
**Step 1:** Đăng nhập vào người dùng Admin, tiến hành cài đặt Plugin `Duplicate Post` phiên bản 1.1.9. Plugin này hỗ trợ người sử dụng trong việc nhân bản các bài post có sẵn.
![](https://i.imgur.com/r0mN84h.png)

**Step 2:** Truy cập vào mục `Post`, chọn 1 bài post, chọn action `Copy` và bấm `Apply`.
![](https://i.imgur.com/uf9xEMX.png)

**Step 3:** Chọn `Setting: Default` và bấm `Copy`.
![](https://i.imgur.com/Rsz0bYz.png)

**Step 4:** Intercept HTTP request, trường dữ liệu cần chú ý ở đây chính là `id`, có thể thấy dữ liệu trường này là dạng số Integer.
![](https://i.imgur.com/YKq8SzE.png)

**Step 5:** Tiến hành chèn payload SQL Injection, bấm gửi request và thấy được rằng 9s sau server mới trả response về -> SQL Injection thành công.
Payload: `1 and (select*from(select(sleep(9)))a)-- `
![](https://i.imgur.com/7NmUzUq.png)


### 3. Exploit code
![](https://i.imgur.com/r0XJWFR.png)


## IV. Biện pháp khắc phục
- Update plugin lên những phiên bản 1.2.0 trở lên

## V. Reference
- [https://appcheck-ng.com/security-advisory-duplicate-post-wordpress-plugin-sql-injection-vulnerability](https://appcheck-ng.com/security-advisory-duplicate-post-wordpress-plugin-sql-injection-vulnerability)