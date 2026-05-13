<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve form information
$data = json_decode(file_get_contents("php://input"), true);
$artistName = $data["artistName"];
$genre = $data["genre"];

// Validate values
if(empty($artistName) || empty($genre)) {
    echo json_encode([
        "success" => false,
        "error" => "All fields must have a value."
    ]);
    exit;
}

// Prepare SQL query
$query = $conn->prepare("INSERT INTO Artist VALUES (NULL, ?, ?)");
$query->bind_param("ss",
    $artistName,
    $genre
);

// Send appropriate message back to script
if($query->execute())
    echo json_encode(["success" => true]);
else
    echo json_encode([
        "success" => false,
        "error" => $query->error
    ]);

$query->close();
$conn->close();
?>