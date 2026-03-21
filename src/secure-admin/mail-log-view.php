<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';

admin_require_login();
$pdo = admin_db();

$id = (int)($_GET['id'] ?? 0);
if ($id <= 0) {
    header('Location: /secure-admin/customer-search.php');
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM mail_log WHERE id = :id LIMIT 1");
$stmt->execute([':id' => $id]);
$row = $stmt->fetch();

if (!$row) {
    admin_layout_start('Mail-Protokoll Ansehen');
    echo '<div class="admin-msg err">Mail-Log nicht gefunden.</div>';
    admin_layout_end();
    exit;
}

audit_log('view_mail_log', (string)$id, (string)$row['subject']);

admin_layout_start('Mail-Protokoll Ansehen');

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px">';
echo '<h2 class="admin-section-title" style="margin:0">Mail-Protokoll</h2>';
echo '<a class="admin-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['booking_consent_id']) . '">Zurück zur Anfrage</a>';
echo '</div>';

echo '<div class="admin-kv">';
$items = [
    ['Mail-Protokoll ID', $row['id']],
    ['Anfrage-ID', $row['booking_consent_id']],
    ['Datum', $row['created_at']],
    ['Richtung', $row['direction']],
    ['Empfänger', $row['recipient']],
    ['Reply-To', $row['reply_to'] ?? ''],
    ['Status', $row['send_status']],
    ['Betreff', $row['subject']],
];
foreach ($items as $item) {
    echo '<div class="admin-kv-item"><div class="admin-kv-label">' . e((string)$item[0]) . '</div><div class="admin-kv-value">' . e((string)$item[1]) . '</div></div>';
}
echo '</div>';

echo '<div style="margin-top:16px"><div class="admin-kv-label">Header</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)($row['headers'] ?? '')) . '</div></div>';
echo '<div style="margin-top:16px"><div class="admin-kv-label">Inhalt</div><div class="admin-card admin-mono" style="margin-top:8px">' . e((string)$row['body']) . '</div></div>';

if (!empty($row['error_message'])) {
    echo '<div style="margin-top:16px"><div class="admin-kv-label">Fehler</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)$row['error_message']) . '</div></div>';
}

echo '</div>';

admin_layout_end();
