<?php
declare(strict_types=1);

require_once __DIR__ . '/_db.php';
require_once __DIR__ . '/_csrf.php';
require_once __DIR__ . '/_audit.php';

function admin_config(): array
{
    return $GLOBALS['config']['admin'];
}

function admin_start_session(): void
{
    $cfg = admin_config();

    if (session_status() === PHP_SESSION_NONE) {
        session_name($cfg['session_name']);
        session_set_cookie_params([
            'lifetime' => 0,
            'path' => '/',
            'domain' => '',
            'secure' => (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off'),
            'httponly' => True,
            'samesite' => 'Strict',
        ]);
        session_start();
    }

    if (!isset($_SESSION['initiated'])) {
        session_regenerate_id(true);
        $_SESSION['initiated'] = time();
    }

    $timeout = (int)$cfg['session_timeout'];
    $now = time();

    if (isset($_SESSION['last_activity']) && ($now - (int)$_SESSION['last_activity']) > $timeout) {
        admin_logout(false);
        header('Location: /secure-admin/login.php?timeout=1');
        exit;
    }

    $_SESSION['last_activity'] = $now;
}

function admin_password_verify_custom(string $plain): bool
{
    $cfg = admin_config();
    $salt = base64_decode($cfg['password_salt_b64'], true);

    if ($salt === false) {
        return false;
    }

    $calc = base64_encode(hash_pbkdf2(
        'sha256',
        $plain,
        $salt,
        (int)$cfg['password_iterations'],
        32,
        true
    ));

    return hash_equals((string)$cfg['password_hash'], $calc);
}

function admin_login_attempt_allowed(): bool
{
    if (!isset($_SESSION['login_fail_count'])) {
        return true;
    }

    $count = (int)$_SESSION['login_fail_count'];
    $last = (int)($_SESSION['login_fail_time'] ?? 0);

    if ($count >= 5 && (time() - $last) < 600) {
        return false;
    }

    if ((time() - $last) >= 600) {
        $_SESSION['login_fail_count'] = 0;
    }

    return true;
}

function admin_login(string $username, string $password): bool
{
    $cfg = admin_config();

    if (!admin_login_attempt_allowed()) {
        return false;
    }

    $ok = hash_equals((string)$cfg['username'], $username) && admin_password_verify_custom($password);

    if ($ok) {
        session_regenerate_id(true);
        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_user'] = $cfg['username'];
        $_SESSION['login_fail_count'] = 0;
        $_SESSION['login_fail_time'] = 0;
        audit_log('login_success');
        return true;
    }

    $_SESSION['login_fail_count'] = ((int)($_SESSION['login_fail_count'] ?? 0)) + 1;
    $_SESSION['login_fail_time'] = time();
    audit_log('login_failure');
    return false;
}

function admin_is_logged_in(): bool
{
    return !empty($_SESSION['admin_logged_in']) && !empty($_SESSION['admin_user']);
}

function admin_require_login(): void
{
    admin_start_session();

    if (!admin_is_logged_in()) {
        header('Location: /secure-admin/login.php');
        exit;
    }
}

function admin_logout(bool $log = true): void
{
    if ($log && !empty($_SESSION['admin_user'])) {
        audit_log('logout');
    }

    $_SESSION = [];

    if (ini_get('session.use_cookies')) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $params['path'], $params['domain'], (bool)$params['secure'], (bool)$params['httponly']);
    }

    if (session_status() === PHP_SESSION_ACTIVE) {
        session_destroy();
    }
}
