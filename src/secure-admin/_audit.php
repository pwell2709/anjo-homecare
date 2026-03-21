<?php
declare(strict_types=1);

function audit_log(string $action, ?string $target = null, ?string $details = null): void
{
    try {
        $pdo = admin_db();
        $stmt = $pdo->prepare("
            INSERT INTO admin_audit_log (actor, action, ip_address, target, details)
            VALUES (:actor, :action, :ip, :target, :details)
        ");
        $stmt->execute([
            ':actor' => (string)($_SESSION['admin_user'] ?? 'guest'),
            ':action' => $action,
            ':ip' => (string)($_SERVER['REMOTE_ADDR'] ?? ''),
            ':target' => $target,
            ':details' => $details,
        ]);
    } catch (Throwable $e) {
        // absichtlich still
    }
}
