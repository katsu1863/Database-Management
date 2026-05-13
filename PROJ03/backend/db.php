<?php
$HOST = "localhost";
$USERNAME = "shirleyl";
$PASSWORD = "ahjael7B";
$DB_NAME = "shirleyl";

$conn = new mysqli($HOST, $USERNAME, $PASSWORD, $DB_NAME);

if($conn->connect_error)
    die("Connection failed: " . $conn->connect_error);
?>