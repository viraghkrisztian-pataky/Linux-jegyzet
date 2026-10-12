<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTTP GET vs POST Bejelentkezési Demonstráció</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #f4f7f6;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        h1 {
            margin-bottom: 8px;
            color: #2c3e50;
            font-size: 1.8rem;
        }
        p.subtitle {
            margin-bottom: 28px;
            color: #7f8c8d;
            font-size: 0.95rem;
            text-align: center;
        }
        .container {
            display: flex;
            gap: 25px;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 850px;
            width: 100%;
        }
        .card {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            padding: 28px;
            flex: 1;
            min-width: 300px;
            border-top: 4px solid #3498db;
        }
        .card.post-card {
            border-top-color: #2ecc71;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .card h2 {
            font-size: 1.2rem;
            color: #34495e;
        }
        .badge {
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge-get { background-color: #ebf5fb; color: #2980b9; }
        .badge-post { background-color: #eafaf1; color: #27ae60; }
        
        .form-group {
            margin-bottom: 16px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-size: 0.85rem;
            color: #555;
            font-weight: 600;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #dcdfe6;
            border-radius: 6px;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #3498db;
            outline: none;
        }
        button {
            width: 100%;
            padding: 11px;
            border: none;
            border-radius: 6px;
            background-color: #3498db;
            color: white;
            font-size: 0.95rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .post-card button {
            background-color: #2ecc71;
        }
        button:hover { opacity: 0.9; }
        
        .response-box {
            margin-top: 25px;
            width: 100%;
            max-width: 850px;
            padding: 15px 20px;
            border-radius: 8px;
            background: #ffffff;
            border-left: 4px solid #f39c12;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            font-size: 0.9rem;
            color: #333;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>

    <h1>Hálózati Protokoll Demonstráció</h1>
    <p class="subtitle">Oktatási célú felület HTTP GET és POST kérések elkapásához Wireshark segítségével</p>

    <div class="container">
        <!-- GET Metódusú Keret -->
        <div class="card">
            <div class="card-header">
                <h2>Bejelentkezés</h2>
                <span class="badge badge-get">HTTP GET</span>
            </div>
            <form action="index.php" method="GET">
                <div class="form-group">
                    <label for="get-user">Felhasználónév</label>
                    <input type="text" id="get-user" name="username_get" required placeholder="pld. oktato">
                </div>
                <div class="form-group">
                    <label for="get-pass">Jelszó</label>
                    <input type="password" id="get-pass" name="password_get" required placeholder="••••••••">
                </div>
                <button type="submit">Küldés GET metódussal</button>
            </form>
        </div>

        <!-- POST Metódusú Keret -->
        <div class="card post-card">
            <div class="card-header">
                <h2>Bejelentkezés</h2>
                <span class="badge badge-post">HTTP POST</span>
            </div>
            <form action="index.php" method="POST">
                <div class="form-group">
                    <label for="post-user">Felhasználónév</label>
                    <input type="text" id="post-user" name="username_post" required placeholder="pld. oktato">
                </div>
                <div class="form-group">
                    <label for="post-pass">Jelszó</label>
                    <input type="password" id="post-pass" name="password_post" required placeholder="••••••••">
                </div>
                <button type="submit">Küldés POST metódussal</button>
            </form>
        </div>
    </div>

    <?php if (!empty($_GET) || !empty($_POST)): ?>
        <div class="response-box">
            <strong>Szerver válasza:</strong> Adatok sikeresen megérkeztek a hálózaton keresztül.
            <?php
            if (isset($_GET['username_get'])) {
                echo "<br>Kérés típusa: <code>GET</code> | Felhasználó: <code>" . htmlspecialchars($_GET['username_get']) . "</code>";
            } elseif (isset($_POST['username_post'])) {
                echo "<br>Kérés típusa: <code>POST</code> | Felhasználó: <code>" . htmlspecialchars($_POST['username_post']) . "</code>";
            }
            ?>
        </div>
    <?php endif; ?>

</body>
</html>
