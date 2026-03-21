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
$timeout = isset($_GET['timeout']) ? 'Deine Sitzung ist abgelaufen. Bitte melde dich erneut an.' : '';

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!csrf_check()) {
        $error = 'Ungültige Anfrage.';
    } elseif (!admin_login_attempt_allowed()) {
        $error = 'Zu viele Fehlversuche. Bitte warte 10 Minuten.';
    } else {
        $username = trim((string)($_POST['username'] ?? ''));
        $password = (string)($_POST['password'] ?? '');

        if (admin_login($username, $password)) {

            if (!empty($_POST['remember'])) {
                admin_set_remember_cookie($username);
            }

            header('Location: /secure-admin/dashboard.php');
            exit;
        }

        $error = 'Anmeldung fehlgeschlagen.';
    }
}

admin_layout_start('Admin-Bereich Anmeldung');

echo '<div class="admin-login">';

if ($timeout !== '') {
    echo '<div class="admin-msg ok">' . e($timeout) . '</div>';
}
if ($error !== '') {
    echo '<div class="admin-msg err">' . e($error) . '</div>';
}

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Anmeldung</h2>';
echo '<form method="post" action="/secure-admin/login.php">';
echo csrf_input();

echo '<div class="admin-field" style="margin-bottom:12px">';
echo '<label for="username">Benutzername</label>';
echo '<input id="username" name="username" type="text" autocomplete="username" required>';
echo '</div>';

echo '<div class="admin-field" style="margin-bottom:12px">';
echo '<label for="password">Passwort</label>';
echo '<input id="password" name="password" type="password" autocomplete="current-password" required>';
echo '</div>';

echo '<div class="admin-actions">';
echo '
<div class="admin-field" style="margin-bottom:12px">
<label>
<input type="checkbox" name="remember">
Angemeldet bleiben
</label>
</div>
<button class="admin-btn" type="submit">Anmeldung</button>
';
echo '</div>';

echo '</form>';
echo '</div>';
echo '</div>';

admin_layout_end();
