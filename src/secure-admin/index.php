<?php
declare(strict_types=1);

require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';

admin_start_session();

if (admin_is_logged_in()) {
    header('Location: /secure-admin/dashboard.php');
    exit;
}

header('Location: /secure-admin/login.php');
exit;
