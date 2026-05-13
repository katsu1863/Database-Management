<?php
// Replace with your own credentials
$HOST = "localhost";
$USERNAME = "USERNAME";
$PASSWORD = "PASSWORD";
$DB_NAME = "DATABASE_NAME";

$conn = new mysqli($HOST, $USERNAME, $PASSWORD, $DB_NAME);

if($conn->connect_error)
    die("Connection failed: " . $conn->connect_error);
?>