<form enctype="multipart/form-data" method="post" action="upload.php">
  <input type="file" size="32" name="image_field" value="">
  <input type="submit" name="Submit" value="upload">
</form>


<?php

require_once('vendor/autoload.php');

use Verot\Upload\Upload;


if($_POST) {
mkdir('images');
$handle = new Upload($_FILES['image_field']);
if ($handle->uploaded) {
  $handle->file_new_name_body   = 'image_resized';
  $handle->image_resize         = true;
  $handle->image_x              = 100;
  $handle->image_ratio_y        = true;
  $handle->process('images/');
  if ($handle->processed) {
    echo 'image resized';
    $handle->clean();
  } else {
    echo 'error : ' . $handle->error;
  }
}
}
