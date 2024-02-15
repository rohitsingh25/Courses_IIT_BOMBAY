<?php
$errorMessage = ""; 
if ($_SERVER["REQUEST_METHOD"] == "POST") 
{
    include 'database.php';
    $roll_number=$_POST["roll_number"];
    $lab=$_POST["lab"];
    $midsem=$_POST["midsem"];
    $project=$_POST["project"];
    $endsem=$_POST["endsem"];
    if($roll_number === "")
    {
        $errorMessage = "Error: Insertion failed.";
    }
    else
    {
        try 
        {
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "INSERT INTO marks (roll_number, lab, midsem, project, endsem)
            VALUES ('$roll_number', $lab, $midsem, $project, $endsem)";
            $conn->exec($sql);
            $errorMessage = "Insertion Successful";
        } 
        catch(PDOException $e) 
        {
            $errorMessage = "Error: Insertion failed. Reason: " . extractErrorMessage($e->getMessage());
        }
        $conn = null; 
    }   
}

function extractErrorMessage($fullErrorMessage) 
{
    $startPos = strpos($fullErrorMessage, "ERROR:");
    $endPos = strpos($fullErrorMessage, "DETAIL:");
    
    if ($startPos !== false && $endPos !== false) 
    {
        return trim(substr($fullErrorMessage, $startPos, $endPos - $startPos));
    }

    return $fullErrorMessage;
}

?>

<!DOCTYPE html>
<html>

<head>
    <title>Add Marks</title>
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
        Lab: <input type="number" name="lab"><br>
        Midsem: <input type="number" name="midsem"><br>
        Project: <input type="number" name="project"><br>
        Endsem : <input type="number" name="endsem"><br>
        <input type="submit" value="Submit">
    </form>
    <a href="processStudent.php"> Add Student </a>
</body>

</html>
