<?php
include 'database.php';

// Simulated admin credentials
$admin_username = 'admin';
$admin_password = 'admin';

$errorMessage = null;
$marksData = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['roll_number'];
    $password = $_POST['password'];

    if ($username === $admin_username && $password === $admin_password) {
        header("Location: processStudent.php");
        exit;
    } else {
        try {
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "SELECT COUNT(*) FROM users WHERE roll_number='$username' AND password='$password'";
            $result = $conn->query($sql);
            if ($result !== false) {
                $count = $result->fetchColumn();
                if ($count > 0) {
                    $sql="SELECT * FROM marks WHERE roll_number='$username'";
                    $result = $conn->query($sql);
                    if($result !== false){
                        $marksData = $result->fetch(PDO::FETCH_ASSOC);
                        if(is_array($marksData) === false){
                            $marksData=null;
                            $errorMessage = "No marks found for Roll Number: $username";
                        }
                    }
                    else{
                        $errorMessage = "Login Failed";
                    }
                } else {
                    $errorMessage = "Login Failed";
                }
            } else {
                $errorMessage = "Login Failed";
            }
        } catch (PDOException $e) {
            $errorMessage = "Login Failed";
        }
        $conn = null; // Close the database connection
    }
    
}

?>

<!DOCTYPE html>
<html>

<body>
    <a href="index.php"> Logout</a>
    <?php if ($marksData !== null): ?>
        <h1>Marks for Roll Number:</h1>
        <ul>
            <?php foreach ($marksData as $subject => $mark): ?>
                <?php if($subject!=="roll_number"): ?>
                    <li><?php echo "$subject: $mark"; ?></li>
                <?php endif; ?>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>
            <?php echo $errorMessage; ?>
        </p>
    <?php endif; ?>
</body>

</html>
