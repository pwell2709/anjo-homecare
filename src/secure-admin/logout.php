<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';

admin_start_session();
admin_logout(true);

header('Location: /secure-admin/login.php');
exit;
