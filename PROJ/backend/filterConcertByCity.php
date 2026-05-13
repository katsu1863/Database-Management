<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve city to filter by
$data = json_decode(file_get_contents("php://input"), true);
$city = $data["city"];

// Retrieve records from Concert that match the city
$result = $conn->query("SELECT * FROM Concert WHERE city = '$city'");

// Convert results into array
$records = [];
while($row = $result->fetch_assoc()) {
    $records[] = $row;
}

// Return back to script
echo json_encode($records);

$conn->close();
?>