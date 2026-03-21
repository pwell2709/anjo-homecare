<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';

admin_start_session();

if (admin_is_logged_in()) {
    header('Location: /secure-admin/dashboard.php');
    exit;
}

$error = '';
$timeout = isset($_GET['timeout']) ? 'Your session expired. Please log in again.' : '';

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!csrf_check()) {
        $error = 'Invalid request.';
    } elseif (!admin_login_attempt_allowed()) {
        $error = 'Too many failed attempts. Please wait 10 minutes.';
    } else {
        $username = trim((string)($_POST['username'] ?? ''));
        $password = (string)($_POST['password'] ?? '');

        if (admin_login($username, $password)) {
            header('Location: /secure-admin/dashboard.php');
            exit;
        }

        $error = 'Login failed.';
    }
}

admin_layout_start('Secure Admin Login');

echo '<div class="admin-login">';

if ($timeout !== '') {
    echo '<div class="admin-msg ok">' . e($timeout) . '</div>';
}
if ($error !== '') {
    echo '<div class="admin-msg err">' . e($error) . '</div>';
}

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Login</h2>';
echo '<form method="post" action="/secure-admin/login.php">';
echo csrf_input();

echo '<div class="admin-field" style="margin-bottom:12px">';
echo '<label for="username">Username</label>';
echo '<input id="username" name="username" type="text" autocomplete="username" required>';
echo '</div>';

echo '<div class="admin-field" style="margin-bottom:12px">';
echo '<label for="password">Password</label>';
echo '<input id="password" name="password" type="password" autocomplete="current-password" required>';
echo '</div>';

echo '<div class="admin-actions">';
echo '<button class="admin-btn" type="submit">Login</button>';
echo '</div>';

echo '</form>';
echo '</div>';
echo '</div>';

admin_layout_end();
