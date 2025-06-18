

<?php
/* code fait par Maxime Derick
*/


$host = "infoemb.inraci.be";
$db_user = "MDerick";
$db_pass = "jUml4fSCNUIqHmhs";
$db_name = "naitotest";
function get_all()
{
    header("Content-Type: application/json");

    try {
        $pdo = new PDO('mysql:host=infoemb.inraci.be;dbname=naitotest;charset=utf8', 'MDerick', 'jUml4fSCNUIqHmhs');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


        $stmt = $pdo->query("SELECT nom,prenom,email,telephone,created_at,sexe,role,heure_arrive,duree_last_session FROM yassine_usr");

        $utilisateurs = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($utilisateurs);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(["error" => "Erreur BDD : " . $e->getMessage()]);
    }
}

// Nouvelle fonction pour récupérer les paiements
function get_payments()
{
    header("Content-Type: application/json");

    try {
        $pdo = new PDO('mysql:host=infoemb.inraci.be;dbname=naitotest;charset=utf8', 'MDerick', 'jUml4fSCNUIqHmhs');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $pdo->query("SELECT nom, prenom, prix, statut, date_debut, date_fin FROM paiement_anasss ORDER BY date_debut DESC");

        $paiements = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($paiements);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(["error" => "Erreur BDD : " . $e->getMessage()]);
    }
}

function check_credentials()
{
    $pdo = new PDO('mysql:host=infoemb.inraci.be;dbname=naitotest;charset=utf8', 'MDerick', 'jUml4fSCNUIqHmhs');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $data = json_decode(file_get_contents("php://input"), true);
    $username = $data['username'] ?? '';
    $password = $data['password'] ?? '';

    $stmt = $pdo->prepare("SELECT * FROM administrateurs WHERE email = :username AND password = :password");
    $stmt->bindParam(':username', $username);
    $stmt->bindParam(':password', $password);
    $stmt->execute();

    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($user) {
        echo json_encode(["success" => true, "redirect" => "admin.html"]);
    } else {
        echo json_encode(["success" => false, "message" => "Identifiants incorrects."]);
    }
}


if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_GET['action']) && $_GET['action'] === 'check_credentials') {
    check_credentials();
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'get_all') {
    get_all();
    exit;
}

// Nouvelle route pour les paiements
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'get_payments') {
    get_payments();
    exit;
}
