<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

require "db.php";

$result = $conn->query("SELECT c.customer_id, c.customer_name,
    SUM(t.price) AS total_spending
    FROM Customer c LEFT JOIN Ticket t ON c.customer_id = t.customer_id
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