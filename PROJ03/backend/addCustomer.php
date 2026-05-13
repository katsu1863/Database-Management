<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve form values
$data = json_decode(file_get_contents("php://input"), true);
$customerName = $data["customerName"];

// Validate values
if(empty($customerName)) {
    echo json_encode([
        "success" => false,
        "error" => "All fields must have a value."
    ]);
    exit;
}

// Prepare SQL query
$query = $conn->prepare("INSERT INTO Customer VALUES (NULL, ?)");
$query->bind_param("s", $customerName);

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