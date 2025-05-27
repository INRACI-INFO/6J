<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


header("Content-Type: application/json");


$data = json_decode(file_get_contents("php://input"), true);

$username = $data["username"] ?? null;
$password = $data["password"] ?? null;

if (!$username || !$password) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Champs manquants"]);
    exit;
}


$host = "infoemb.inraci.be";
$db_user = "MDerick";
$db_pass = "jUml4fSCNUIqHmhs";
$db_name = "naitotest";


$conn = new mysqli($host, $db_user, $db_pass, $db_name);


if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["success" => false, "message" => "Erreur de connexion à la base"]);

    exit;
}

$stmt = $conn->prepare("SELECT * FROM yassine_usr WHERE email = ? AND password = ?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();

if ($result && $result->num_rows > 0) {
    echo json_encode(["success" => true]);
} else {
    echo json_encode(["success" => false, "message" => "Identifiants incorrects"]);
}
