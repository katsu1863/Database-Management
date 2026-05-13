<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

require "db.php";

$result = $conn->query("SELECT artist_name, SUM(price) AS total_revenue
    FROM Artist NATURAL JOIN Concert NATURAL JOIN Ticket
    GROUP BY artist_id
    ORDER BY total_revenue DESC
    LIMIT 3");

$records = [];
while($row = $result->fetch_assoc()) {
    $records[] = $row;
}

echo json_encode($records);

$conn->close();
?>