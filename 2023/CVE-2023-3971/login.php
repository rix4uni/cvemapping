<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controller - HTML Injection</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #eaeded;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        h1 {
            color: #333;
        }

        form {
            max-width: 400px;
            width: 100%;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
        }

        input {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            display: inline-block;
        }

        input[type="submit"] {
            background-color: #cc0000;
            color: #fff;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
        }

        input[type="submit"]:hover {
            background-color: #990000;
        }

        #searchResult {
            max-width: 400px;
            width: 100%;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
    </style>
</head>
<body>

    

    <form action="" method="post">
<h1>Log in to your Red Hat account</h1>
        <label for="username">Red Hat login or email</label>
        <input type="text" id="username" name="username" required>
        <br>

        <label for="password">Red Hat password</label>
        <input type="password" id="password" name="password" required>
        <br>

        <input type="submit" value="Login">
    </form>

    <div id="searchResult">
        <h2>Search Result:</h2>
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $injectedUsername = $_POST['username'] ?? '';
            echo "<p>Username: $injectedUsername</p>";
        }
        ?>
    </div>

</body>
</html>
