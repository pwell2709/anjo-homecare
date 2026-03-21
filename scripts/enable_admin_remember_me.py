from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIN = ROOT / "src" / "secure-admin"

AUTH_FILE = ADMIN / "_auth.php"
LOGIN_FILE = ADMIN / "login.php"

if not AUTH_FILE.exists():
    raise SystemExit("FEHLER: _auth.php nicht gefunden")

auth = AUTH_FILE.read_text(encoding="utf-8")

# === 1. Session verlängern (2 Stunden statt kurz) ===
auth = auth.replace(
    "session.gc_maxlifetime = 1800",
    "session.gc_maxlifetime = 7200"
)

# === 2. Remember Token Funktionen hinzufügen ===
if "function admin_set_remember_cookie" not in auth:
    auth += """

function admin_set_remember_cookie(string $user): void {
    $token = bin2hex(random_bytes(32));
    $hash = hash('sha256', $token);

    file_put_contents(__DIR__ . '/.remember_token', $hash);

    setcookie(
        'admin_remember',
        $token,
        time() + (60*60*24*30),
        '/',
        '',
        false,
        true
    );
}

function admin_check_remember(): bool {
    if (empty($_COOKIE['admin_remember'])) return false;

    $token = $_COOKIE['admin_remember'];
    $hash = hash('sha256', $token);

    $file = __DIR__ . '/.remember_token';
    if (!file_exists($file)) return false;

    $stored = trim(file_get_contents($file));

    if (hash_equals($stored, $hash)) {
        $_SESSION['admin_logged_in'] = true;
        return true;
    }

    return false;
}
"""

# === 3. Auto-Login beim Start ===
if "admin_check_remember();" not in auth:
    auth = auth.replace(
        "admin_start_session();",
        "admin_start_session();\nadmin_check_remember();"
    )

AUTH_FILE.write_text(auth, encoding="utf-8")

# === 4. Login-Seite erweitern ===

login = LOGIN_FILE.read_text(encoding="utf-8")

if 'name="remember"' not in login:
    login = login.replace(
        '<button class="admin-btn" type="submit">Login</button>',
        """
<div class="admin-field" style="margin-bottom:12px">
<label>
<input type="checkbox" name="remember">
Remember me
</label>
</div>
<button class="admin-btn" type="submit">Login</button>
"""
    )

if "admin_set_remember_cookie" not in login:
    login = login.replace(
        "if (admin_login($username, $password)) {",
        """if (admin_login($username, $password)) {

            if (!empty($_POST['remember'])) {
                admin_set_remember_cookie($username);
            }
"""
    )

LOGIN_FILE.write_text(login, encoding="utf-8")

print("FERTIG: Auto-Login + Session-Verlängerung aktiv")