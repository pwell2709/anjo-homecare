<?php
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
