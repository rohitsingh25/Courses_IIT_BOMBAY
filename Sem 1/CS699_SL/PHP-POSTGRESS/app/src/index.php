<!DOCTYPE html>
<html>

<head>
    <style>
        label {
            display: inline-block;
            width: 100px;
            margin-bottom: 10px;
        }
    </style>


    <title>Login</title>
</head>

<body>

    <form method="post" action="process.php">
        <label>Roll Number</label>
        <input type="text" name="roll_number" />
        <br />
        <label>Password</label>
        <input type="password" name="password" />
        <br />
        <input type="submit" value="Login">
    </form>



</body>

</html>