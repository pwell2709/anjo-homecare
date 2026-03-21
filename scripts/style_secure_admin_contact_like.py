from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ADMIN = ROOT / "src" / "secure-admin"

FILES = {
    "_layout.php": None,
    "login.php": None,
    "dashboard.php": None,
    "customer-search.php": None,
    "customer-view.php": None,
    "mail-log-view.php": None,
}

layout_php = """<?php
declare(strict_types=1);

function e(?string $value): string
{
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

function admin_layout_start(string $title): void
{
    $fullTitle = e($title);

    echo '<!doctype html>';
    echo '<html lang="en">';
    echo '<head>';
    echo '<meta charset="utf-8">';
    echo '<meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<meta name="robots" content="noindex,nofollow,noarchive">';
    echo '<title>' . $fullTitle . '</title>';

    echo '<link rel="stylesheet" href="/assets/css/base.css">';
    echo '<link rel="stylesheet" href="/assets/css/components.css">';
    echo '<link rel="stylesheet" href="/assets/css/utilities.css">';

    echo '<style>
        body{
            margin:0;
            color:inherit;
        }

        .admin-shell{
            max-width: 1180px;
            margin: 0 auto;
            padding: 22px 16px 32px;
        }

        .admin-top{
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:16px;
            margin-bottom:20px;
            flex-wrap:wrap;
        }

        .admin-brand{
            display:flex;
            align-items:flex-start;
            gap:14px;
        }

        .admin-title{
            font-size:1.45rem;
            font-weight:800;
            line-height:1.15;
            margin:0;
        }

        .admin-subtitle{
            font-size:.98rem;
            opacity:.9;
            margin-top:6px;
        }

        .admin-nav{
            display:flex;
            gap:10px;
            flex-wrap:wrap;
            align-items:center;
        }

        .admin-nav a{
            text-decoration:none;
        }

        .admin-chip{
            display:inline-flex;
            align-items:center;
            justify-content:center;
            padding:10px 14px;
            border-radius:999px;
            background:rgba(255,255,255,.14);
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.10);
            color:inherit;
            font-weight:700;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
        }

        .admin-card{
            background: rgba(255,255,255,.08);
            border-radius: 18px;
            padding: 18px;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            box-shadow: 0 10px 30px rgba(0,0,0,.08);
            margin-bottom:18px;
        }

        .admin-grid2,
        .admin-grid3,
        .admin-grid4,
        .admin-kv{
            display:grid;
            gap:14px;
        }

        .admin-grid2{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .admin-grid3{ grid-template-columns: repeat(3, minmax(0, 1fr)); }
        .admin-grid4{ grid-template-columns: repeat(4, minmax(0, 1fr)); }
        .admin-kv{ grid-template-columns: repeat(3, minmax(0, 1fr)); }

        @media (max-width: 980px){
            .admin-grid2,
            .admin-grid3,
            .admin-grid4,
            .admin-kv{
                grid-template-columns: 1fr;
            }
        }

        .admin-field label{
            display:block;
            font-weight:700;
            margin:0 0 8px;
        }

        .admin-field input,
        .admin-field select,
        .admin-field textarea{
            width:100%;
            border:0;
            outline:none;
            border-radius:16px;
            padding:14px 14px;
            background: rgba(0,0,0,.14);
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
            color: inherit;
            box-sizing:border-box;
            transition: box-shadow .18s ease, background .18s ease;
        }

        .admin-field input:focus,
        .admin-field select:focus,
        .admin-field textarea:focus{
            background: rgba(0,0,0,.10);
            box-shadow:
              inset 0 0 0 1px rgba(255,255,255,.14),
              0 0 0 4px rgba(0,31,63,.18);
        }

        .admin-field textarea{
            min-height:170px;
            resize:vertical;
            line-height:1.35;
        }

        .admin-actions{
            display:flex;
            gap:10px;
            flex-wrap:wrap;
            align-items:center;
            margin-top:14px;
        }

        .admin-btn,
        .admin-table-btn{
            background:none;
            border:none;
            padding:0;
            font-weight:800;
            font-size:1rem;
            color:#001f3f;
            cursor:pointer;
            text-decoration:none;
        }

        .admin-btn:hover,
        .admin-table-btn:hover{
            opacity:.72;
        }

        .admin-muted{
            font-size:.95rem;
            opacity:.86;
        }

        .admin-table-wrap{
            overflow-x:auto;
        }

        .admin-table{
            width:100%;
            border-collapse:collapse;
            min-width:760px;
        }

        .admin-table th,
        .admin-table td{
            text-align:left;
            padding:10px 12px;
            border-bottom:1px solid rgba(255,255,255,.12);
            vertical-align:top;
        }

        .admin-table th{
            font-weight:800;
            background:rgba(0,0,0,.10);
        }

        .admin-status-ok{
            font-weight:700;
        }

        .admin-status-err{
            font-weight:700;
        }

        .admin-msg{
            border-radius:16px;
            padding:12px 14px;
            margin-bottom:14px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.10);
        }

        .admin-msg.err{
            background: rgba(231, 76, 60, .12);
        }

        .admin-msg.ok{
            background: rgba(46, 204, 113, .12);
        }

        .admin-mono{
            font-family: Consolas, Monaco, monospace;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .admin-kv-item{
            background: rgba(0,0,0,.10);
            border-radius:14px;
            padding:12px 14px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
        }

        .admin-kv-label{
            font-size:.9rem;
            opacity:.8;
            margin-bottom:4px;
        }

        .admin-kv-value{
            font-weight:700;
            word-break:break-word;
        }

        .admin-login{
            max-width:560px;
            margin:0 auto;
        }

        .admin-section-title{
            margin:0 0 10px;
            font-size:1.18rem;
            font-weight:800;
        }
    </style>';

    echo '</head>';
    echo '<body class="l-page">';
    echo '<main class="l-main">';
    echo '<div class="admin-shell">';

    if (!empty($_SESSION['admin_logged_in'])) {
        echo '<div class="admin-top">';
        echo '<div class="admin-brand">';
        echo '<div>';
        echo '<h1 class="admin-title">Secure Admin</h1>';
        echo '<div class="admin-subtitle">Internal customer and inquiry view</div>';
        echo '</div>';
        echo '</div>';

        echo '<div class="admin-nav">';
        echo '<a class="admin-chip" href="/secure-admin/dashboard.php">Dashboard</a>';
        echo '<a class="admin-chip" href="/secure-admin/customer-search.php">Customer Search</a>';
        echo '<a class="admin-chip" href="/secure-admin/logout.php">Logout</a>';
        echo '</div>';
        echo '</div>';
    } else {
        echo '<div class="admin-top">';
        echo '<div class="admin-brand">';
        echo '<div>';
        echo '<h1 class="admin-title">Secure Admin</h1>';
        echo '<div class="admin-subtitle">Protected internal access</div>';
        echo '</div>';
        echo '</div>';
        echo '</div>';
    }
}

function admin_layout_end(): void
{
    echo '</div>';
    echo '</main>';
    echo '</body>';
    echo '</html>';
}
"""

login_php = """<?php
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
"""

dashboard_php = """<?php
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

admin_layout_start('Secure Admin Dashboard');

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Dashboard</h2>';
echo '<div class="admin-grid3">';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Stored inquiries</div><div class="admin-kv-value" style="font-size:28px;">' . e((string)$totalBookings) . '</div></div>';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Stored mail logs</div><div class="admin-kv-value" style="font-size:28px;">' . e((string)$totalMails) . '</div></div>';
echo '<div class="admin-kv-item"><div class="admin-kv-label">Scope</div><div class="admin-kv-value">Read-only test phase</div></div>';
echo '</div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px"><h2 class="admin-section-title" style="margin:0">Recent inquiries</h2><a class="admin-btn" href="/secure-admin/customer-search.php">Open search</a></div>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Date</th><th>Name</th><th>Email</th><th>Service</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($recent as $row) {
    echo '<tr>';
    echo '<td>' . e((string)$row['id']) . '</td>';
    echo '<td>' . e((string)$row['created_at']) . '</td>';
    echo '<td>' . e((string)$row['name']) . '</td>';
    echo '<td>' . e((string)$row['email']) . '</td>';
    echo '<td>' . e((string)$row['service']) . '</td>';
    echo '<td>' . e((string)$row['lang']) . '</td>';
    echo '<td>' . ($row['mail_sent'] ? '<span class="admin-status-ok">sent</span>' : '<span class="admin-status-err">not sent</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['id']) . '">View</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
"""

customer_search_php = """<?php
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

admin_layout_start('Customer Search');

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Customer Search</h2>';
echo '<form method="get" action="/secure-admin/customer-search.php">';
echo '<div class="admin-grid4">';

echo '<div class="admin-field"><label for="name">Name</label><input id="name" name="name" value="' . e($name) . '"></div>';
echo '<div class="admin-field"><label for="email">E-Mail</label><input id="email" name="email" value="' . e($email) . '"></div>';
echo '<div class="admin-field"><label for="phone">Phone</label><input id="phone" name="phone" value="' . e($phone) . '"></div>';

echo '<div class="admin-field"><label for="service">Service</label><select id="service" name="service"><option value="">All</option>';
foreach ($serviceRows as $sr) {
    $v = (string)$sr['service'];
    echo '<option value="' . e($v) . '"' . ($service == $v ? ' selected' : '') . '>' . e($v) . '</option>';
}
echo '</select></div>';

echo '<div class="admin-field"><label for="lang">Language</label><select id="lang" name="lang"><option value="">All</option>';
foreach ($langRows as $lr) {
    $v = (string)$lr['code'];
    echo '<option value="' . e($v) . '"' . ($lang == $v ? ' selected' : '') . '>' . e(strtoupper($v)) . '</option>';
}
echo '</select></div>';

echo '<div class="admin-field"><label for="date_from">Date from</label><input id="date_from" name="date_from" type="date" value="' . e($dateFrom) . '"></div>';
echo '<div class="admin-field"><label for="date_to">Date to</label><input id="date_to" name="date_to" type="date" value="' . e($dateTo) . '"></div>';
echo '</div>';

echo '<div class="admin-actions"><button class="admin-btn" type="submit">Search</button></div>';
echo '</form>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Results (' . e((string)count($rows)) . ')</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Date</th><th>Name</th><th>E-Mail</th><th>Phone</th><th>Service</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($rows as $row) {
    echo '<tr>';
    echo '<td>' . e((string)$row['id']) . '</td>';
    echo '<td>' . e((string)$row['created_at']) . '</td>';
    echo '<td>' . e((string)$row['name']) . '</td>';
    echo '<td>' . e((string)$row['email']) . '</td>';
    echo '<td>' . e((string)($row['phone'] ?? '')) . '</td>';
    echo '<td>' . e((string)$row['service']) . '</td>';
    echo '<td>' . e((string)$row['lang']) . '</td>';
    echo '<td>' . ($row['mail_sent'] ? '<span class="admin-status-ok">sent</span>' : '<span class="admin-status-err">not sent</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['id']) . '">Open</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
"""

customer_view_php = """<?php
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
    admin_layout_start('Customer View');
    echo '<div class="admin-msg err">Entry not found.</div>';
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

admin_layout_start('Customer View');

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px">';
echo '<h2 class="admin-section-title" style="margin:0">Customer View</h2>';
echo '<a class="admin-btn" href="/secure-admin/customer-search.php">Back to search</a>';
echo '</div>';

echo '<div class="admin-kv">';
$items = [
    ['ID', $row['id']],
    ['Date', $row['created_at']],
    ['Language', $row['lang']],
    ['Name', $row['name']],
    ['E-Mail', $row['email']],
    ['Phone', $row['phone'] ?? ''],
    ['Service', $row['service']],
    ['Page', $row['page']],
    ['Mail sent', $row['mail_sent'] ? 'yes' : 'no'],
    ['Privacy consent', $row['consent'] ? 'yes' : 'no'],
    ['Terms accepted', $row['accept_terms'] ? 'yes' : 'no'],
    ['Withdrawal accepted', $row['accept_withdrawal'] ? 'yes' : 'no'],
    ['Early execution', $row['accept_early'] ? 'yes' : 'no'],
    ['Terms version', $row['terms_version']],
    ['Withdrawal version', $row['withdrawal_version']],
    ['IP', $row['ip_address'] ?? ''],
];
foreach ($items as $item) {
    echo '<div class="admin-kv-item"><div class="admin-kv-label">' . e((string)$item[0]) . '</div><div class="admin-kv-value">' . e((string)$item[1]) . '</div></div>';
}
echo '</div>';

echo '<div style="margin-top:16px"><div class="admin-kv-label">Message</div><div class="admin-card admin-mono" style="margin-top:8px">' . e((string)$row['message']) . '</div></div>';
echo '<div style="margin-top:16px"><div class="admin-kv-label">User-Agent</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)($row['user_agent'] ?? '')) . '</div></div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">All inquiries for this e-mail</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Date</th><th>Service</th><th>Lang</th><th>Mail</th><th></th></tr></thead><tbody>';
foreach ($relatedRows as $r) {
    echo '<tr>';
    echo '<td>' . e((string)$r['id']) . '</td>';
    echo '<td>' . e((string)$r['created_at']) . '</td>';
    echo '<td>' . e((string)$r['service']) . '</td>';
    echo '<td>' . e((string)$r['lang']) . '</td>';
    echo '<td>' . ($r['mail_sent'] ? '<span class="admin-status-ok">sent</span>' : '<span class="admin-status-err">not sent</span>') . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$r['id']) . '">Open</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

echo '<div class="admin-card">';
echo '<h2 class="admin-section-title">Mail logs for this inquiry</h2>';
echo '<div class="admin-table-wrap">';
echo '<table class="admin-table"><thead><tr><th>ID</th><th>Date</th><th>Recipient</th><th>Reply-To</th><th>Subject</th><th>Status</th><th></th></tr></thead><tbody>';
foreach ($mailRows as $m) {
    echo '<tr>';
    echo '<td>' . e((string)$m['id']) . '</td>';
    echo '<td>' . e((string)$m['created_at']) . '</td>';
    echo '<td>' . e((string)$m['recipient']) . '</td>';
    echo '<td>' . e((string)($m['reply_to'] ?? '')) . '</td>';
    echo '<td>' . e((string)$m['subject']) . '</td>';
    echo '<td>' . e((string)$m['send_status']) . '</td>';
    echo '<td><a class="admin-table-btn" href="/secure-admin/mail-log-view.php?id=' . urlencode((string)$m['id']) . '">Open</a></td>';
    echo '</tr>';
}
echo '</tbody></table>';
echo '</div>';
echo '</div>';

admin_layout_end();
"""

mail_log_view_php = """<?php
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
    admin_layout_start('Mail Log View');
    echo '<div class="admin-msg err">Mail log not found.</div>';
    admin_layout_end();
    exit;
}

audit_log('view_mail_log', (string)$id, (string)$row['subject']);

admin_layout_start('Mail Log View');

echo '<div class="admin-card">';
echo '<div class="admin-top" style="margin-bottom:10px">';
echo '<h2 class="admin-section-title" style="margin:0">Mail Log</h2>';
echo '<a class="admin-btn" href="/secure-admin/customer-view.php?id=' . urlencode((string)$row['booking_consent_id']) . '">Back to inquiry</a>';
echo '</div>';

echo '<div class="admin-kv">';
$items = [
    ['Mail Log ID', $row['id']],
    ['Booking ID', $row['booking_consent_id']],
    ['Date', $row['created_at']],
    ['Direction', $row['direction']],
    ['Recipient', $row['recipient']],
    ['Reply-To', $row['reply_to'] ?? ''],
    ['Status', $row['send_status']],
    ['Subject', $row['subject']],
];
foreach ($items as $item) {
    echo '<div class="admin-kv-item"><div class="admin-kv-label">' . e((string)$item[0]) . '</div><div class="admin-kv-value">' . e((string)$item[1]) . '</div></div>';
}
echo '</div>';

echo '<div style="margin-top:16px"><div class="admin-kv-label">Headers</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)($row['headers'] ?? '')) . '</div></div>';
echo '<div style="margin-top:16px"><div class="admin-kv-label">Body</div><div class="admin-card admin-mono" style="margin-top:8px">' . e((string)$row['body']) . '</div></div>';

if (!empty($row['error_message'])) {
    echo '<div style="margin-top:16px"><div class="admin-kv-label">Error</div><div class="admin-card admin-mono admin-muted" style="margin-top:8px">' . e((string)$row['error_message']) . '</div></div>';
}

echo '</div>';

admin_layout_end();
"""

FILES["_layout.php"] = layout_php
FILES["login.php"] = login_php
FILES["dashboard.php"] = dashboard_php
FILES["customer-search.php"] = customer_search_php
FILES["customer-view.php"] = customer_view_php
FILES["mail-log-view.php"] = mail_log_view_php

for name, content in FILES.items():
    path = ADMIN / name
    if not path.exists():
        raise SystemExit(f"FEHLER: {path} nicht gefunden.")
    path.write_text(content, encoding="utf-8")
    print(f"Aktualisiert: {path.relative_to(ROOT)}")

print("FERTIG: Secure Admin ist jetzt komplett im Kontaktformular-/Website-Stil und ohne Logo aufgebaut.")