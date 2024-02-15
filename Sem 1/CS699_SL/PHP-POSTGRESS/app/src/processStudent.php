<?php
$errorMessage = ""; // Variable to hold error message
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    include 'database.php'; // Assuming this includes the database connection
    // Add logic to insert the data to DB and update errorMessage incase of error
    $roll_number=$_POST["roll_number"];
    $name=$_POST["name"];
    $email_address=$_POST["email"];
    $password=$_POST["password"];
    if($roll_number === ""){
        $errorMessage = "Error: Insertion failed.";
    }
    else{
        try {
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "INSERT INTO users (roll_number, name, email_address, password)
            VALUES ('$roll_number', '$name', '$email_address', '$password')";
            $conn->exec($sql);
            $errorMessage = "Insertion Successful";
        } catch(PDOException $e) {
            $errorMessage = "Error: Insertion failed. Reason: " . extractErrorMessage($e->getMessage());
        }
        $conn = null; // Close the database connection
    }
}

// Function to extract the error message from the exception
function extractErrorMessage($fullErrorMessage) {
    $startPos = strpos($fullErrorMessage, "ERROR:");
    $endPos = strpos($fullErrorMessage, "DETAIL:");
    
    if ($startPos !== false && $endPos !== false) {
        return trim(substr($fullErrorMessage, $startPos, $endPos - $startPos));
    }

    return $fullErrorMessage;
}

?>

<!DOCTYPE html>
<html>

<head>
    <title>Add Student</title>
</head>

<body>

    <a href="index.php"> Logout</a>
    <?php if ($errorMessage !== ""): ?>
        <p>
            <?php echo $errorMessage; ?>
        </p>
    <?php endif; ?>

    <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
        Roll Number: <input type="text" name="roll_number"><br>
        Name: <input type="text" name="name"><br>
        Email: <input type="text" name="email"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Submit">
    </form>
    <a href="processMarks.php"> Add Marks </a>
</body>

</html>