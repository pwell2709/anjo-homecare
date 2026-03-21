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

$stmt = $pdo->prepare("SELECT * FROM booking_consents WHERE id = :id LIMIT 1");
$stmt->execute([':id' => $id]);
$row = $stmt->fetch();

if (!$row) {
    admin_layout_start('Customer Ansehen');
    echo '<div class="admin-msg err">Eintrag nicht gefunden.</div>';
    admin_layout_end();
    exit;
}

$relatedStmt = $pdo->prepare("
    SELECT id, created_at, service, lang, mail_sent
    FROM booking_consents
    WHERE email = :email
    ORDER BY id DESC
");
$relatedStmt->execute([':email' => $row['email']]);
$relatedRows = $relatedStmt->fetchAll();

$mailStmt = $pdo->prepare("
    SELECT id, created_at, recipient, reply_to, subject, send_status
    FROM mail_log
    WHERE booking_consent_id = :booking_id
    ORDER BY id DESC
");
$mailStmt->execute([':booking_id' => $id]);
$mailRows = $mailStmt->fetchAll();

audit_log('view_customer', (string)$id, (string)$row['email']);

admin_layout_start('Customer Ansehen');

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px">';
echo '<h2 class="admin-section-title" style="margin:0">Customer Ansehen</h2>';
echo '<a class="admin-btn" href="/secure-admin/customer-search.php">Zurück zur Suche</a>';
echo '</div>';

echo '<div class="admin-kv">';
$items = [
    ['ID', $row['id']],
    ['Datum', $row['created_at']],
    ['Sprache', $row['lang']],
    ['Name', $row['name']],
    ['E-Mail', $row['email']],
    ['Telefon', $row['phone'] ?? ''],
    ['Leistung', $row['service']],
    ['Seite', $row['page']],
    ['Mail gesendet', $row['mail_sent'] ? 'yes' : 'no'],
    ['Datumnschutz bestätigt', $row['consent'] ? 'yes' : 'no'],
    ['AGB bestätigt', $row['accept_terms'] ? 'yes' : 'no'],
    ['Widerruf bestätigt', $row['accept_withdrawal'] ? 'yes' : 'no'],
    ['Vorzeitiger Beginn', $row['accept_early'] ? 'yes' : 'no'],
    ['AGB-Version', $row['terms_version']],
    ['Widerrufs-Version', $row['withdrawal_version']],
    ['IP', $row['ip_address'] ?? ''],
];
foreach ($items as $item) {
    echo '<div class="admin-kv-item"><div class="admin-kv-label">' . e((string)$item[0]) . '</div><div class="admin-kv-value">' . e((string)$item[1]) . '</div></div>';
}
echo '</div>';

echo '<div style="margin-top:16px"><div class="admin-kv-label">Nachricht</div><div class="admin-card admin-mono" style="margin-top:8px">' . e((string)$row['message']) . '</div></div>';
echo '<div style="margin-top:16px"><div class="admin-kv-label">User-Agent</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)($row['user_agent'] ?? '')) . '</div></div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Alle Anfragen zu dieser E-Mail</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Datum</th><th>Leistung</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($relatedRows as $r) {
    echo '<tr>';
    echo '<td>' . e((string)$r['id']) . '</td>';
    echo '<td>' . e((string)$r['created_at']) . '</td>';
    echo '<td>' . e((string)$r['service']) . '</td>';
    echo '<td>' . e((string)$r['lang']) . '</td>';
    echo '<td>' . ($r['mail_sent'] ? '<span class="admin-status-ok">gesendet</span>' : '<span class="admin-status-err">nicht gesendet</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$r['id']) . '">Öffnen</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Mail-Logs zu dieser Anfrage</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Datum</th><th>Empfänger</th><th>Reply-To</th><th>Betreff</th><th>Status</th><th></th></tr></thead><tbody>';
foreach ($mailRows as $m) {
    echo '<tr>';
    echo '<td>' . e((string)$m['id']) . '</td>';
    echo '<td>' . e((string)$m['created_at']) . '</td>';
    echo '<td>' . e((string)$m['recipient']) . '</td>';
    echo '<td>' . e((string)($m['reply_to'] ?? '')) . '</td>';
    echo '<td>' . e((string)$m['subject']) . '</td>';
    echo '<td>' . e((string)$m['send_status']) . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/mail-log-view.php?id=' . urlencode((string)$m['id']) . '">Öffnen</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
