<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require "db.php";

$data = json_decode(file_get_contents("php://input"), true);
$customer = $data["customer"];

$result = $conn->query("SELECT c.customer_id, c.customer_name,
    SUM(t.price) AS total_spending
    FROM Customer c LEFT JOIN Ticket t ON c.customer_id = t.customer_id
    WHERE c.customer_name = '$customer'
    GROUP BY c.customer_id");

$records = [];
while($row = $result->fetch_assoc()) {
    // Set total_spending to 0 if a customer has bought zero tickets
    if($row["total_spending"] == null)
        $row["total_spending"] = 0;
    
    $records[] = $row;
}

echo json_encode($records);

$conn->close();
?>