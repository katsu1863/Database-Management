<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

require "db.php";

$result = $conn->query("SELECT artist_name, venue_name, city, concert_date
    FROM Artist NATURAL JOIN Concert");

$records = [];
while($row = $result->fetch_assoc()) {
    $records[] = $row;
}

echo json_encode($records);

$conn->close();
?>