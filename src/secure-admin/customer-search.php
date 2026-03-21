<?php
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';

admin_require_login();
$pdo = admin_db();

$name = trim((string)($_GET['name'] ?? ''));
$email = trim((string)($_GET['email'] ?? ''));
$phone = trim((string)($_GET['phone'] ?? ''));
$service = trim((string)($_GET['service'] ?? ''));
$lang = trim((string)($_GET['lang'] ?? ''));
$dateFrom = trim((string)($_GET['date_from'] ?? ''));
$dateTo = trim((string)($_GET['date_to'] ?? ''));

$sql = "SELECT id, created_at, name, email, phone, service, lang, mail_sent
        FROM booking_consents
        WHERE 1=1";
$params = [];

if ($name !== '') {
    $sql .= " AND name LIKE :name";
    $params[':name'] = '%' . $name . '%';
}
if ($email !== '') {
    $sql .= " AND email LIKE :email";
    $params[':email'] = '%' . $email . '%';
}
if ($phone !== '') {
    $sql .= " AND phone LIKE :phone";
    $params[':phone'] = '%' . $phone . '%';
}
if ($service !== '') {
    $sql .= " AND service = :service";
    $params[':service'] = $service;
}
if ($lang !== '') {
    $sql .= " AND lang = :lang";
    $params[':lang'] = $lang;
}
if ($dateFrom !== '') {
    $sql .= " AND created_at >= :date_from";
    $params[':date_from'] = $dateFrom . ' 00:00:00';
}
if ($dateTo !== '') {
    $sql .= " AND created_at <= :date_to";
    $params[':date_to'] = $dateTo . ' 23:59:59';
}

$sql .= " ORDER BY id DESC LIMIT 100";
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$rows = $stmt->fetchAll();

$serviceRows = $pdo->query("SELECT DISTINCT service FROM booking_consents WHERE service <> '' ORDER BY service ASC")->fetchAll();
$langRows = [['code' => 'de'], ['code' => 'en'], ['code' => 'fr'], ['code' => 'pt']];

audit_log('search_customers', null, json_encode([
    'name' => $name,
    'email' => $email,
    'phone' => $phone,
    'service' => $service,
    'lang' => $lang,
    'date_from' => $dateFrom,
    'date_to' => $dateTo,
], JSON_UNESCAPED_UNICODE));

admin_layout_start('Kundensuche');

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Kundensuche</h2>';
echo '<form method="get" action="/secure-admin/customer-search.php">';
echo '<div class="admin-grid4">';

echo '<div class="admin-field"><label for="name">Name</label><input id="name" name="name" value="' . e($name) . '"></div>';
echo '<div class="admin-field"><label for="email">E-Mail</label><input id="email" name="email" value="' . e($email) . '"></div>';
echo '<div class="admin-field"><label for="phone">Telefon</label><input id="phone" name="phone" value="' . e($phone) . '"></div>';

echo '<div class="admin-field"><label for="service">Leistung</label><select id="service" name="service"><option value="">Alle</option>';
foreach ($serviceRows as $sr) {
    $v = (string)$sr['service'];
    echo '<option value="' . e($v) . '"' . ($service == $v ? ' selected' : '') . '>' . e($v) . '</option>';
}
echo '</select></div>';

echo '<div class="admin-field"><label for="lang">Sprache</label><select id="lang" name="lang"><option value="">Alle</option>';
foreach ($langRows as $lr) {
    $v = (string)$lr['code'];
    echo '<option value="' . e($v) . '"' . ($lang == $v ? ' selected' : '') . '>' . e(strtoupper($v)) . '</option>';
}
echo '</select></div>';

echo '<div class="admin-field"><label for="date_from">Datum von</label><input id="date_from" name="date_from" type="date" value="' . e($dateFrom) . '"></div>';
echo '<div class="admin-field"><label for="date_to">Datum bis</label><input id="date_to" name="date_to" type="date" value="' . e($dateTo) . '"></div>';
echo '</div>';

echo '<div class="admin-actions"><button class="admin-btn" type="submit">Suchen</button></div>';
echo '</form>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Ergebnisse (' . e((string)count($rows)) . ')</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Datum</th><th>Name</th><th>E-Mail</th><th>Telefon</th><th>Leistung</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($rows as $row) {
    echo '<tr>';
    echo '<td>' . e((string)$row['id']) . '</td>';
    echo '<td>' . e((string)$row['created_at']) . '</td>';
    echo '<td>' . e((string)$row['name']) . '</td>';
    echo '<td>' . e((string)$row['email']) . '</td>';
    echo '<td>' . e((string)($row['phone'] ?? '')) . '</td>';
    echo '<td>' . e((string)$row['service']) . '</td>';
    echo '<td>' . e((string)$row['lang']) . '</td>';
    echo '<td>' . ($row['mail_sent'] ? '<span class="admin-status-ok">gesendet</span>' : '<span class="admin-status-err">nicht gesendet</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['id']) . '">Öffnen</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
