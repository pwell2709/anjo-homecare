import os
import re
from datetime import datetime

BASE = "src"

langs = ["en", "de", "fr", "pt"]

# -------------------------
# 1. TERMS + WITHDRAWAL PAGES
# -------------------------

def create_pages():
    for lang in langs:
        for slug, title in [
            ("terms", "Terms and Conditions"),
            ("withdrawal", "Withdrawal Information")
        ]:
            path = os.path.join(BASE, lang, slug)
            os.makedirs(path, exist_ok=True)

            file = os.path.join(path, "index.njk")

            content = f"""---
layout: "base.njk"
lang: "{lang}"
title: "{title}"
permalink: "/{lang}/{slug}/"
---

<section class="text-intro">
  <h1>{title}</h1>

  <p>
    This page contains legally required information for international clients.
  </p>

  <p>
    By booking a service, you agree to the applicable terms and conditions.
  </p>
</section>
"""

            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

# -------------------------
# 2. CONTACT FORM UPDATE
# -------------------------

def update_contact_forms():
    for lang in langs:
        file = os.path.join(BASE, lang, "contact", "index.njk")

        if not os.path.exists(file):
            continue

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if "accept_terms" in content:
            continue

        insert = """
<div class="legal-check" style="margin-top:20px;">
  <label>
    <input type="checkbox" name="accept_terms" required>
    I accept the Terms and Conditions
  </label><br>

  <label>
    <input type="checkbox" name="accept_withdrawal" required>
    I have read the withdrawal information
  </label><br>

  <label>
    <input type="checkbox" name="accept_early">
    I request early execution and understand the loss of withdrawal rights
  </label>
</div>
"""

        content = re.sub(r"(</form>)", insert + r"\n\1", content, count=1)

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

# -------------------------
# 3. SEND.PHP UPDATE
# -------------------------

def update_send_php():
    file = os.path.join(BASE, "send.php")

    if not os.path.exists(file):
        return

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    if "accept_terms" in content:
        return

    validation = """
if(empty($_POST['accept_terms']) || empty($_POST['accept_withdrawal'])){
    die("Legal confirmation missing.");
}
"""

    logging = """
$log = date("c") . " | IP: " . $_SERVER['REMOTE_ADDR'] .
" | Terms: " . $_POST['accept_terms'] .
" | Withdrawal: " . $_POST['accept_withdrawal'] . "\\n";

file_put_contents("booking_log.txt", $log, FILE_APPEND);
"""

    content = content.replace("<?php", "<?php\n" + validation)
    content += logging

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    create_pages()
    update_contact_forms()
    update_send_php()

    print("DONE: Legal setup applied.")