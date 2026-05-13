<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

$data = json_decode(file_get_contents("php://input"), true);
$artist = $data["artist"];

$result = $conn->query("SELECT artist_name, venue_name, city, concert_date
    FROM Artist NATURAL JOIN Concert
    WHERE artist_name = '$artist'");

$records = [];
while($row = $result->fetch_assoc()) {
    $records[] = $row;
}

echo json_encode($records);

$conn->close();
?>