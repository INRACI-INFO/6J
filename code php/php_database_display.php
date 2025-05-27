<?php
// Configuration de la base de données
$serveur = "localhost";
$utilisateur = "votre_utilisateur";
$mot_de_passe = "votre_mot_de_passe";
$nom_base = "votre_base_de_donnees";

try {
    // Connexion à la base de données avec PDO
    $pdo = new PDO("mysql:host=$serveur;dbname=$nom_base;charset=utf8", $utilisateur, $mot_de_passe);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Récupération de la liste des tables
    $stmt = $pdo->query("SHOW TABLES");
    $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
    
} catch(PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Données de la Base MySQL</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            text-align: center;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #4CAF50;
            margin-top: 30px;
            border-left: 4px solid #4CAF50;
            padding-left: 15px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .info-box {
            background-color: #e8f5e8;
            border: 1px solid #4CAF50;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        
        .error {
            background-color: #ffe6e6;
            border: 1px solid #ff0000;
            color: #cc0000;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .table-count {
            font-style: italic;
            color: #666;
            margin-bottom: 10px;
        }
        
        .no-data {
            text-align: center;
            color: #999;
            font-style: italic;
            padding: 20px;
        }
        
        .navigation {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            padding: 10px;
            border-radius: 5px;
        }
        
        .navigation a {
            color: white;
            text-decoration: none;
            display: block;
            margin: 5px 0;
            padding: 5px;
            border-radius: 3px;
            transition: background-color 0.3s;
        }
        
        .navigation a:hover {
            background-color: rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Données de la Base de Données MySQL</h1>
        
        <div class="info-box">
            <strong>Base de données :</strong> <?php echo htmlspecialchars($nom_base); ?><br>
            <strong>Serveur :</strong> <?php echo htmlspecialchars($serveur); ?><br>
            <strong>Nombre de tables :</strong> <?php echo count($tables); ?>
        </div>

        <!-- Navigation rapide -->
        <div class="navigation">
            <strong style="color: white;">Navigation :</strong>
            <?php foreach($tables as $table): ?>
                <a href="#table-<?php echo htmlspecialchars($table); ?>">
                    <?php echo htmlspecialchars($table); ?>
                </a>
            <?php endforeach; ?>
        </div>

        <?php
        // Affichage des données de chaque table
        foreach($tables as $table) {
            echo "<h2 id='table-" . htmlspecialchars($table) . "'>Table : " . htmlspecialchars($table) . "</h2>";
            
            try {
                // Compter le nombre d'enregistrements
                $countStmt = $pdo->prepare("SELECT COUNT(*) FROM `$table`");
                $countStmt->execute();
                $count = $countStmt->fetchColumn();
                
                echo "<div class='table-count'>Nombre d'enregistrements : $count</div>";
                
                if($count > 0) {
                    // Récupérer les données de la table
                    $stmt = $pdo->prepare("SELECT * FROM `$table` LIMIT 100");
                    $stmt->execute();
                    $donnees = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    
                    if($donnees) {
                        echo "<table>";
                        
                        // En-têtes du tableau
                        echo "<tr>";
                        foreach(array_keys($donnees[0]) as $colonne) {
                            echo "<th>" . htmlspecialchars($colonne) . "</th>";
                        }
                        echo "</tr>";
                        
                        // Données du tableau
                        foreach($donnees as $ligne) {
                            echo "<tr>";
                            foreach($ligne as $valeur) {
                                // Gérer les valeurs NULL et longues
                                if($valeur === null) {
                                    echo "<td><em>NULL</em></td>";
                                } else {
                                    $valeur_affichee = strlen($valeur) > 100 ? 
                                        substr(htmlspecialchars($valeur), 0, 100) . "..." : 
                                        htmlspecialchars($valeur);
                                    echo "<td>" . $valeur_affichee . "</td>";
                                }
                            }
                            echo "</tr>";
                        }
                        
                        echo "</table>";
                        
                        if($count > 100) {
                            echo "<div class='info-box'>Note : Seuls les 100 premiers enregistrements sont affichés.</div>";
                        }
                    }
                } else {
                    echo "<div class='no-data'>Aucune donnée dans cette table</div>";
                }
                
            } catch(PDOException $e) {
                echo "<div class='error'>Erreur lors de la lecture de la table '$table' : " . htmlspecialchars($e->getMessage()) . "</div>";
            }
        }
        ?>
        
        <div style="margin-top: 50px; text-align: center; color: #666; font-size: 0.9em;">
            Page générée le <?php echo date('d/m/Y à H:i:s'); ?>
        </div>
    </div>

    <script>
        // Scroll fluide pour la navigation
        document.querySelectorAll('.navigation a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if(target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>