<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve table name
$data = json_decode(file_get_contents("php://input"), true);
$tableName = $data["tableName"];

// Retrieve all the records from selected table
$result = $conn->query("SELECT * FROM $tableName");

// Convert results into an array
$records = [];
while($row = $result->fetch_assoc()) {
    $records[] = $row;
}

// Return results back to script
echo json_encode($records);

$conn->close();
?>