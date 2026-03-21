<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';

admin_require_login();

$pdo = admin_db();

$totalBookings = (int)$pdo->query("SELECT COUNT(*) FROM booking_consents")->fetchColumn();
$totalMails = (int)$pdo->query("SELECT COUNT(*) FROM mail_log")->fetchColumn();
$recent = $pdo->query("
    SELECT id, created_at, name, email, service, lang, mail_sent
    FROM booking_consents
    ORDER BY id DESC
    LIMIT 10
")->fetchAll();

audit_log('view_dashboard');

admin_layout_start('Admin-Bereich Dashboard');

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Dashboard</h2>';
echo '<div class="admin-grid3">';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Gespeicherte Anfragen</div><div class="admin-kv-value" style="font-size:28px;">' . e((string)$totalBookings) . '</div></div>';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Gespeicherte Mail-Logs</div><div class="admin-kv-value" style="font-size:28px;">' . e((string)$totalMails) . '</div></div>';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Umfang</div><div class="admin-kv-value">Nur-Lesen Testphase</div></div>';
echo '</div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px"><h2 class="admin-section-title" style="margin:0">Letzte Anfragen</h2><a class="admin-btn" href="/secure-admin/customer-search.php">Suche öffnen</a></div>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Datum</th><th>Name</th><th>Email</th><th>Leistung</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($recent as $row) {
    echo '<tr>';
    echo '<td>' . e((string)$row['id']) . '</td>';
    echo '<td>' . e((string)$row['created_at']) . '</td>';
    echo '<td>' . e((string)$row['name']) . '</td>';
    echo '<td>' . e((string)$row['email']) . '</td>';
    echo '<td>' . e((string)$row['service']) . '</td>';
    echo '<td>' . e((string)$row['lang']) . '</td>';
    echo '<td>' . ($row['mail_sent'] ? '<span class="admin-status-ok">gesendet</span>' : '<span class="admin-status-err">nicht gesendet</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['id']) . '">Ansehen</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
