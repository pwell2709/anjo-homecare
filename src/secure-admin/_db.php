<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';

function admin_db(): PDO
{
    static $pdo = null;

    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $cfg = $GLOBALS['config']['db'];
    $dsn = "mysql:host={$cfg['host']};dbname={$cfg['name']};charset=utf8mb4";

    $pdo = new PDO(
        $dsn,
        $cfg['user'],
        $cfg['pass'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );

    return $pdo;
}
