<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh sách</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
        }
        header {
            background-color: #0078D7;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 20px auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #0078D7;
            color: white;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box input[type="text"] {
            width: calc(100% - 110px);
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .search-box button {
            padding: 10px;
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .search-box button:hover {
            background-color: #005BBB;
        }
    </style>
</head>
<body>
    <header>
        <h1>Attendance Viewer</h1>
    </header>
    <div class="container">
        <div class="search-box">
            <form method="GET" action="">
                <input type="text" name="search" placeholder="Search by Name" value="<?php echo isset($_GET['search']) ? htmlspecialchars($_GET['search']) : ''; ?>">
                <button type="submit">Search</button>
            </form>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Check-In</th>
                    <th>Check-Out</th>
                </tr>
            </thead>
            <tbody>
                <?php
                // Connect to database
                $conn = new mysqli('localhost', 'root', '', 'tiennvoai');

                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                }

                // Search functionality
                $search = isset($_GET['search']) ? $conn->real_escape_string($_GET['search']) : '';
                $query = "SELECT attendance.id, people.Name, attendance.timeCheckIn, attendance.timeCheckOut 
                          FROM attendance 
                          LEFT JOIN people ON attendance.idPeople = people.Id 
                          WHERE people.Name LIKE '%$search%';";

                $result = $conn->query($query);

                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . htmlspecialchars($row['id']) . "</td>";
                        echo "<td>" . htmlspecialchars($row['Name']) . "</td>";
                        echo "<td>" . htmlspecialchars($row['timeCheckIn']) . "</td>";
                        echo "<td>" . htmlspecialchars($row['timeCheckOut']) . "</td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='4'>No results found</td></tr>";
                }

                $conn->close();
                ?>
            </tbody>
        </table>
    </div>
</body>
</html>
