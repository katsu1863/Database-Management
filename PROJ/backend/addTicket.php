<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

// Retrieve form values
$data = json_decode(file_get_contents("php://input"), true);
$concertId = $data["concertId"];
$customerId = $data["customerId"];
$seatNumber = $data["seatNumber"];
$price = $data["price"];

// Validate values
if(empty($concertId) || empty($customerId) || empty($seatNumber) || empty($price)) {
    echo json_encode([
        "success" => false,
        "error" => "All fields must have a value."
    ]);
    exit;
}

// Check if price is greater than 0
if($price < 0) {
    echo json_encode([
        "success" => false,
        "error" => "Price must be greater than zero."
    ]);
    exit;
}

// Check if concert ID is valid
$query = $conn->prepare("SELECT 1 FROM Concert WHERE concert_id = ?");
$query->bind_param("i", $concertId);
$query->execute();
$result = $query->get_result();
if($result->num_rows == 0) {
    echo json_encode([
        "success" => false,
        "error" => "Concert ID $concertId does not exist."
    ]);
    exit;
}

// Check if customer ID is valid
$query = $conn->prepare("SELECT 1 FROM Customer WHERE customer_id = ?");
$query->bind_param("i", $customerId);
$query->execute();
$result = $query->get_result();
if($result->num_rows == 0) {
    echo json_encode([
        "success" => false,
        "error" => "Customer ID $customerId does not exist."
    ]);
    exit;
}

// Prepare SQL query
$query = $conn->prepare("INSERT INTO Ticket VALUES (NULL, ?, ?, ?, ?)");
$query->bind_param("iisd",
    $concertId,
    $customerId,
    $seatNumber,
    $price
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