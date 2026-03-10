<?php
declare(strict_types=1);

/*
  send.php (final)
  PHP 8.x (Strato)
  Erwartet POST: name, email, phone, service, message, consent, lang, website (honeypot)
  Antwort: JSON
*/

header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok'=>false,'error'=>'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

/* --- Determine language early (for messages) --- */
$lang = strtolower(is_string($_POST['lang'] ?? '') ? trim((string)($_POST['lang'] ?? '')) : '');
if ($lang === '') $lang = 'de';

/* --- Honeypot: field 'website' must stay empty --- */
$honeypot = $_POST['website'] ?? '';
if (is_string($honeypot) && trim($honeypot) !== '') {
    // Pretend success to bots, but do not send email
    echo json_encode(['ok'=>true,'message'=>'OK'], JSON_UNESCAPED_UNICODE);
    exit;
}

/* --- Simple rate limit per IP (1 request / 45 seconds) --- */
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$ipKey = preg_replace('/[^0-9a-f:\.]/i','', $ip);
$rlFile = rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'ac_rl_' . hash('sha256', $ipKey) . '.txt';
$now = time();
$window = 45; // seconds

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

        echo json_encode(['ok'=>false,'error'=>$msg,'retry_after'=>$retry], JSON_UNESCAPED_UNICODE);
        exit;
    }
}
@file_put_contents($rlFile, (string)$now, LOCK_EX);

function val(string $key, int $max=4000): string {
    $v = $_POST[$key] ?? '';
    if (!is_string($v)) return '';
    $v = trim($v);
    if (mb_strlen($v,'UTF-8') > $max) $v = mb_substr($v,0,$max,'UTF-8');
    return $v;
}

function fail(string $msg, int $code=400): void {
    http_response_code($code);
    echo json_encode(['ok'=>false,'error'=>$msg], JSON_UNESCAPED_UNICODE);
    exit;
}

function ok(string $msg): void {
    echo json_encode(['ok'=>true,'message'=>$msg], JSON_UNESCAPED_UNICODE);
    exit;
}

/* i18n messages */
function t(string $lang, string $key): string {
    $lang = strtolower($lang);
    $m = [
        'de' => [
            'required' => 'Bitte fülle alle Pflichtfelder aus.',
            'email'    => 'Bitte gib eine gültige E-Mail-Adresse ein.',
            'ack'      => 'Bitte bestätige den Datenschutzhinweis (Checkbox).',
            'sendFail' => 'Senden fehlgeschlagen. Bitte später erneut versuchen.',
            'ok'       => 'Danke! Deine Nachricht wurde gesendet.',
        ],
        'en' => [
            'required' => 'Please fill in all required fields.',
            'email'    => 'Please enter a valid email address.',
            'ack'      => 'Please acknowledge the privacy notice (checkbox).',
            'sendFail' => 'Sending failed. Please try again later.',
            'ok'       => 'Thank you! Your message has been sent.',
        ],
        'fr' => [
            'required' => 'Veuillez remplir tous les champs obligatoires.',
            'email'    => 'Veuillez saisir une adresse email valide.',
            'ack'      => 'Veuillez confirmer la notice de confidentialité (case).',
            'sendFail' => 'Échec de l’envoi. Veuillez réessayer plus tard.',
            'ok'       => 'Merci ! Votre message a été envoyé.',
        ],
        'pt' => [
            'required' => 'Por favor, preencha todos os campos obrigatórios.',
            'email'    => 'Por favor, indique um email válido.',
            'ack'      => 'Por favor, confirme a nota de privacidade (caixa).',
            'sendFail' => 'Falha ao enviar. Por favor tente novamente mais tarde.',
            'ok'       => 'Obrigado! A sua mensagem foi enviada.',
        ],
    ];
    if (!isset($m[$lang])) $lang = 'de';
    return $m[$lang][$key] ?? $m['de'][$key] ?? 'Error';
}

$lang    = strtolower(val('lang',5));
if ($lang === '') $lang = 'de';
$name    = val('name',200);
$email   = val('email',200);
$phone   = val('phone',200);
$service = val('service',200);
$message = val('message',5000);

/* Required fields */
if ($name==='' || $email==='' || $service==='' || $message==='') {
    fail(t($lang,'required'));
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(t($lang,'email'));
}

/* Consent: must be explicitly checked */
$hasConsentField = array_key_exists('consent', $_POST);
$consentVal = $_POST['consent'] ?? '';
$consentOk = false;

if ($hasConsentField) {
    if (is_string($consentVal)) {
        $v = strtolower(trim($consentVal));
        $consentOk = in_array($v, ['1','true','on','yes','y','checked'], true);
    } else {
        $consentOk = (bool)$consentVal;
    }
}

if (!$consentOk) {
    fail(t($lang,'ack'));
}

/* Fixed recipient (avoid SERVER_NAME pitfalls) */
$to = 'info@anjo-cleaning.com';

/* From should be domain-based (DMARC-friendly) */
$fromMail = 'no-reply@anjo-cleaning.com';
$fromName = 'Website Kontaktformular';

$clean = static fn(string $s): string => str_replace(["\r","\n"],' ',$s);

$subject = ($lang==='en') ? "New contact request: $service"
        : (($lang==='fr') ? "Nouvelle demande de contact : $service"
        : (($lang==='pt') ? "Novo pedido de contacto: $service"
        : "Neue Kontaktanfrage: $service"));

$subject = $clean($subject);
$service = $clean($service);
$name    = $clean($name);
$email   = $clean($email);
$phone   = $clean($phone);

$when = (new DateTimeImmutable('now', new DateTimeZone('Europe/Berlin')))->format('Y-m-d H:i:s');

$body =
"Name: $name\n".
"E-Mail: $email\n".
"Telefon: ".($phone!==''?$phone:'-')."\n".
"Service: $service\n".
"Zeit: $when (Europe/Berlin)\n".
"IP: ".($_SERVER['REMOTE_ADDR'] ?? '')."\n\n".
"Nachricht:\n$message";

$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'Content-Transfer-Encoding: 8bit';
$headers[] = 'From: '.$clean($fromName).' <'.$clean($fromMail).'>';
$headers[] = 'Reply-To: '.$clean($email);
$headers[] = 'X-Mailer: PHP/'.PHP_VERSION;

$sent = @mail($to, $subject, $body, implode("\r\n", $headers));

if (!$sent) {
    fail(t($lang,'sendFail'), 500);
}

ok(t($lang,'ok'));
