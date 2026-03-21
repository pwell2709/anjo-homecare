<?php
declare(strict_types=1);

/*
  send.php
  PHP 8.x (Strato)
  Erwartet POST:
  name, email, phone, service, message, consent, lang, page, website (honeypot),
  accept_terms, accept_withdrawal, accept_early
  Antwort: JSON
*/

header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

/* ---------- CONFIG ---------- */
$dbHost = 'database-5020060711.webspace-host.com';
$dbName = 'dbs15465310';
$dbUser = 'dbu636856';
$dbPass = 'Q!12pT?=157=?17QZ';

$termsVersion = '2026-03';
$withdrawalVersion = '2026-03';

$to = 'info@anjo-cleaning.com';
$fromMail = 'no-reply@anjo-cleaning.com';
$fromName = 'Website Kontaktformular';

/* ---------- HELPERS ---------- */
function val(string $key, int $max = 4000): string {
    $v = $_POST[$key] ?? '';
    if (!is_string($v)) return '';
    $v = trim($v);
    if (mb_strlen($v, 'UTF-8') > $max) {
        $v = mb_substr($v, 0, $max, 'UTF-8');
    }
    return $v;
}

function checkbox(string $key): int {
    if (!array_key_exists($key, $_POST)) {
        return 0;
    }

    $v = $_POST[$key];

    if (is_string($v)) {
        $v = strtolower(trim($v));
        return in_array($v, ['1', 'true', 'on', 'yes', 'y', 'checked'], true) ? 1 : 0;
    }

    return $v ? 1 : 0;
}

function fail(string $msg, int $code = 400): void {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}

function ok(string $msg): void {
    echo json_encode(['ok' => true, 'message' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}

function t(string $lang, string $key): string {
    $lang = strtolower($lang);

    $m = [
        'de' => [
            'required' => 'Bitte fülle alle Pflichtfelder aus.',
            'email'    => 'Bitte gib eine gültige E-Mail-Adresse ein.',
            'ack'      => 'Bitte bestätige den Datenschutzhinweis (Checkbox).',
            'legal'    => 'Bitte bestätige AGB und Widerrufsbelehrung.',
            'sendFail' => 'Senden fehlgeschlagen. Bitte später erneut versuchen.',
            'dbFail'   => 'Speichern fehlgeschlagen. Bitte später erneut versuchen.',
            'ok'       => 'Danke! Deine Nachricht wurde gesendet.',
        ],
        'en' => [
            'required' => 'Please fill in all required fields.',
            'email'    => 'Please enter a valid email address.',
            'ack'      => 'Please acknowledge the privacy notice (checkbox).',
            'legal'    => 'Please confirm the Terms and Withdrawal Information.',
            'sendFail' => 'Sending failed. Please try again later.',
            'dbFail'   => 'Saving failed. Please try again later.',
            'ok'       => 'Thank you! Your message has been sent.',
        ],
        'fr' => [
            'required' => 'Veuillez remplir tous les champs obligatoires.',
            'email'    => 'Veuillez saisir une adresse email valide.',
            'ack'      => 'Veuillez confirmer la notice de confidentialité (case).',
            'legal'    => 'Veuillez confirmer les conditions et les informations de rétractation.',
            'sendFail' => 'Échec de l’envoi. Veuillez réessayer plus tard.',
            'dbFail'   => 'Échec de l’enregistrement. Veuillez réessayer plus tard.',
            'ok'       => 'Merci ! Votre message a été envoyé.',
        ],
        'pt' => [
            'required' => 'Por favor, preencha todos os campos obrigatórios.',
            'email'    => 'Por favor, indique um email válido.',
            'ack'      => 'Por favor, confirme a nota de privacidade (caixa).',
            'legal'    => 'Por favor confirme os Termos e a informação sobre livre resolução.',
            'sendFail' => 'Falha ao enviar. Por favor tente novamente mais tarde.',
            'dbFail'   => 'Falha ao guardar. Por favor tente novamente mais tarde.',
            'ok'       => 'Obrigado! A sua mensagem foi enviada.',
        ],
    ];

    if (!isset($m[$lang])) $lang = 'de';
    return $m[$lang][$key] ?? $m['de'][$key] ?? 'Error';
}

function cleanHeader(string $s): string {
    return str_replace(["\r", "\n"], ' ', $s);
}

/* ---------- LANGUAGE ---------- */
$lang = strtolower(val('lang', 5));
if ($lang === '') {
    $lang = 'de';
}

/* ---------- HONEYPOT ---------- */
$honeypot = $_POST['website'] ?? '';
if (is_string($honeypot) && trim($honeypot) !== '') {
    echo json_encode(['ok' => true, 'message' => 'OK'], JSON_UNESCAPED_UNICODE);
    exit;
}

/* ---------- RATE LIMIT ---------- */
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$ipKey = preg_replace('/[^0-9a-f:\.]/i', '', $ip);
$rlFile = rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'ac_rl_' . hash('sha256', $ipKey) . '.txt';
$now = time();
$window = 45;

if (is_file($rlFile)) {
    $last = (int)@file_get_contents($rlFile);
    if ($last > 0 && ($now - $last) < $window) {
        http_response_code(429);
        $retry = max(1, $window - ($now - $last));
        header('Retry-After: ' . $retry);

        $msgMap = [
            'de' => 'Bitte warte kurz und versuche es dann erneut.',
            'en' => 'Please wait a moment and try again.',
            'fr' => 'Veuillez patienter un instant puis réessayer.',
            'pt' => 'Por favor aguarde um momento e tente novamente.'
        ];
        $msg = $msgMap[$lang] ?? $msgMap['de'];

        echo json_encode(['ok' => false, 'error' => $msg, 'retry_after' => $retry], JSON_UNESCAPED_UNICODE);
        exit;
    }
}
@file_put_contents($rlFile, (string)$now, LOCK_EX);

/* ---------- INPUT ---------- */
$page = val('page', 255);
$name = val('name', 200);
$email = val('email', 200);
$phone = val('phone', 200);
$service = val('service', 200);
$message = val('message', 5000);

$consent = checkbox('consent');
$acceptTerms = checkbox('accept_terms');
$acceptWithdrawal = checkbox('accept_withdrawal');
$acceptEarly = checkbox('accept_early');

$userAgent = substr((string)($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 4000);

/* ---------- VALIDATION ---------- */
if ($name === '' || $email === '' || $service === '' || $message === '') {
    fail(t($lang, 'required'));
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(t($lang, 'email'));
}

if ($consent !== 1) {
    fail(t($lang, 'ack'));
}

if ($acceptTerms !== 1 || $acceptWithdrawal !== 1) {
    fail(t($lang, 'legal'));
}

/* ---------- DATABASE ---------- */
$pdo = null;
$bookingId = null;
$mailLogId = null;

try {
    $dsn = "mysql:host={$dbHost};dbname={$dbName};charset=utf8mb4";
    $pdo = new PDO(
        $dsn,
        $dbUser,
        $dbPass,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );
} catch (Throwable $e) {
    error_log('DB connection failed in send.php: ' . $e->getMessage());
    fail(t($lang, 'dbFail'), 500);
}

try {
    $stmt = $pdo->prepare("
        INSERT INTO booking_consents (
            lang,
            page,
            name,
            email,
            phone,
            service,
            message,
            ip_address,
            user_agent,
            consent,
            accept_terms,
            accept_withdrawal,
            accept_early,
            terms_version,
            withdrawal_version,
            mail_sent
        ) VALUES (
            :lang,
            :page,
            :name,
            :email,
            :phone,
            :service,
            :message,
            :ip_address,
            :user_agent,
            :consent,
            :accept_terms,
            :accept_withdrawal,
            :accept_early,
            :terms_version,
            :withdrawal_version,
            0
        )
    ");

    $stmt->execute([
        ':lang' => $lang,
        ':page' => $page,
        ':name' => $name,
        ':email' => $email,
        ':phone' => $phone !== '' ? $phone : null,
        ':service' => $service,
        ':message' => $message,
        ':ip_address' => $ip,
        ':user_agent' => $userAgent,
        ':consent' => $consent,
        ':accept_terms' => $acceptTerms,
        ':accept_withdrawal' => $acceptWithdrawal,
        ':accept_early' => $acceptEarly,
        ':terms_version' => $termsVersion,
        ':withdrawal_version' => $withdrawalVersion,
    ]);

    $bookingId = (int)$pdo->lastInsertId();
} catch (Throwable $e) {
    error_log('DB insert booking_consents failed in send.php: ' . $e->getMessage());
    fail(t($lang, 'dbFail'), 500);
}

/* ---------- MAIL PREP ---------- */
$subject = ($lang === 'en') ? "New contact request: $service"
    : (($lang === 'fr') ? "Nouvelle demande de contact : $service"
    : (($lang === 'pt') ? "Novo pedido de contacto: $service"
    : "Neue Kontaktanfrage: $service"));

$subject = cleanHeader($subject);

$mailName = cleanHeader($name);
$mailEmail = cleanHeader($email);
$mailPhone = cleanHeader($phone);
$mailService = cleanHeader($service);

$when = (new DateTimeImmutable('now', new DateTimeZone('Europe/Berlin')))->format('Y-m-d H:i:s');

$body =
"Name: $mailName\n" .
"E-Mail: $mailEmail\n" .
"Telefon: " . ($mailPhone !== '' ? $mailPhone : '-') . "\n" .
"Service: $mailService\n" .
"Sprache: $lang\n" .
"Seite: " . ($page !== '' ? $page : '-') . "\n" .
"Zeit: $when (Europe/Berlin)\n" .
"IP: $ip\n" .
"User-Agent: " . ($userAgent !== '' ? $userAgent : '-') . "\n" .
"Consent Privacy: " . ($consent ? 'yes' : 'no') . "\n" .
"Accept Terms: " . ($acceptTerms ? 'yes' : 'no') . "\n" .
"Accept Withdrawal: " . ($acceptWithdrawal ? 'yes' : 'no') . "\n" .
"Accept Early Execution: " . ($acceptEarly ? 'yes' : 'no') . "\n" .
"Terms Version: $termsVersion\n" .
"Withdrawal Version: $withdrawalVersion\n" .
"Booking ID: " . ($bookingId ?? 0) . "\n\n" .
"Nachricht:\n$message";

$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'Content-Transfer-Encoding: 8bit';
$headers[] = 'From: ' . cleanHeader($fromName) . ' <' . cleanHeader($fromMail) . '>';
$headers[] = 'Reply-To: ' . $mailEmail;
$headers[] = 'X-Mailer: PHP/' . PHP_VERSION;

$headersText = implode("\r\n", $headers);

/* ---------- MAIL LOG INSERT BEFORE SEND ---------- */
try {
    $stmt = $pdo->prepare("
        INSERT INTO mail_log (
            booking_consent_id,
            direction,
            recipient,
            reply_to,
            subject,
            body,
            headers,
            send_status,
            error_message
        ) VALUES (
            :booking_consent_id,
            'outgoing',
            :recipient,
            :reply_to,
            :subject,
            :body,
            :headers,
            'pending',
            NULL
        )
    ");

    $stmt->execute([
        ':booking_consent_id' => $bookingId,
        ':recipient' => $to,
        ':reply_to' => $mailEmail,
        ':subject' => $subject,
        ':body' => $body,
        ':headers' => $headersText,
    ]);

    $mailLogId = (int)$pdo->lastInsertId();
} catch (Throwable $e) {
    error_log('DB insert mail_log failed in send.php: ' . $e->getMessage());
    fail(t($lang, 'dbFail'), 500);
}

/* ---------- SEND MAIL ---------- */
$sent = @mail($to, $subject, $body, $headersText);

if (!$sent) {
    try {
        if ($mailLogId) {
            $upd = $pdo->prepare("
                UPDATE mail_log
                SET send_status = 'failed',
                    error_message = :error_message
                WHERE id = :id
                LIMIT 1
            ");
            $upd->execute([
                ':error_message' => 'PHP mail() returned false',
                ':id' => $mailLogId,
            ]);
        }
    } catch (Throwable $e) {
        error_log('DB update mail_log failed status=failed: ' . $e->getMessage());
    }

    error_log('Mail send failed in send.php for booking ID ' . ($bookingId ?? 0));
    fail(t($lang, 'sendFail'), 500);
}

/* ---------- UPDATE LOGS AFTER SUCCESS ---------- */
try {
    if ($mailLogId) {
        $updMail = $pdo->prepare("
            UPDATE mail_log
            SET send_status = 'sent',
                error_message = NULL
            WHERE id = :id
            LIMIT 1
        ");
        $updMail->execute([':id' => $mailLogId]);
    }

    if ($bookingId) {
        $updBooking = $pdo->prepare("
            UPDATE booking_consents
            SET mail_sent = 1
            WHERE id = :id
            LIMIT 1
        ");
        $updBooking->execute([':id' => $bookingId]);
    }
} catch (Throwable $e) {
    error_log('DB update success flags failed in send.php: ' . $e->getMessage());
}

/* ---------- OPTIONAL TEXT LOG ---------- */
$logLine =
    date("c") .
    " | booking_id=" . ($bookingId ?? 0) .
    " | mail_log_id=" . ($mailLogId ?? 0) .
    " | ip=" . $ip .
    " | lang=" . $lang .
    " | page=" . $page .
    " | terms=" . $acceptTerms .
    " | withdrawal=" . $acceptWithdrawal .
    " | early=" . $acceptEarly .
    "\n";

@file_put_contents(__DIR__ . '/booking_log.txt', $logLine, FILE_APPEND | LOCK_EX);

/* ---------- SUCCESS ---------- */
ok(t($lang, 'ok'));