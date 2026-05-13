<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

require "db.php";

// Retrieve all distinct cities from Concert
$result = $conn->query("SELECT DISTINCT city FROM Concert");

// Convert results into array
$cities = [];
while($row = $result->fetch_assoc()) {
    $cities[] = $row["city"];
}

// Return back to script
echo json_encode($cities);

$conn->close();
?>