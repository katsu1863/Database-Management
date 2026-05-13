<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve form values
$data = json_decode(file_get_contents("php://input"), true);
$venueName = $data["venueName"];
$city = $data["city"];
$concertDate = $data["concertDate"];
$artistId = $data["artistId"];

// Validate values
if(empty($venueName) || empty($city) || empty($concertDate) || empty($artistId)) {
    echo json_encode([
        "success" => false,
        "error" => "All fields must have a value."
    ]);
    exit;
}

// Check if Artist ID exists in Artist table
$query = $conn->prepare("SELECT 1 FROM Artist WHERE artist_id = ?");
$query->bind_param("i", $artistId);
$query->execute();
$result = $query->get_result();
if($result->num_rows == 0) {
    echo json_encode([
        "success" => false,
        "error" => "Artist ID $artistId does not exist."
    ]);
    exit;
}

// Prepare SQL query
$query = $conn->prepare("INSERT INTO Concert VALUES (NULL, ?, ?, ?, ?)");
$query->bind_param("sssi",
    $venueName,
    $city,
    $concertDate,
    $artistId
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