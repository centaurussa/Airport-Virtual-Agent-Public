<!DOCTYPE html>
<html lang="en">
<head>
	<title>Airport - Hotels and Rooms</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>
	<?php
	  $conn = new mysqli('localhost', 'root', '1234', 'airportinfo');
	  $query = "SELECT * FROM hotels;";
	  $result = $conn->query($query);
	 ?>
	<div class="limiter">
		<div class="container-table100">
			<div class="wrap-table100">
				<div class="table100">
					<table>
						<h1 style = "color:white;text-align:center;margin: -20px 0px 20px 0px;font-family: OpenSans-Regular;">Hotels</h1>
						<p style = "color:white;margin:20px 0px 5px 0px;font-family: OpenSans-Regular;font-size:0.9em;"> *Scrolling: Tell the assitant to either "Scroll up/Go up" or "Scroll down/Go down"</p>
						<p style = "color:white;margin:5px 0px 20px 0px;font-family: OpenSans-Regular;font-size:0.9em;"> *Exiting: Tell the assitant "Close Google Chrome"</p>
						<thead>
							<tr class="table100-head">
								<th class="column1">Hotle ID</th>
								<th class="column2">Name</th>
								<th class="column3">Stars</th>
								<th class="column4">Location</th>
							</tr>
						</thead>
						<tbody>
							<?php
								while($row = $result->fetch_array()){
										echo "<tr>";
											echo "<td class='column1'>" . "<a href='http://localhost/airport/rooms.php?Hotel_ID=" . $row['Hotel_ID'] .  "'>" . $row['Hotel_ID'] . '</a></td>';
											echo "<td class='column2'>" . "<a href='http://localhost/airport/rooms.php?Hotel_ID=" . $row['Hotel_ID'] .  "'>" . $row['Name'] . '</a></td>';
											echo "<td class='column3'>" . "<a href='http://localhost/airport/rooms.php?Hotel_ID=" . $row['Hotel_ID'] .  "'>" . $row['Number_Stars'] . '</a></td>';
											echo "<td class='column4'>" . "<a href='http://localhost/airport/rooms.php?Hotel_ID=" . $row['Hotel_ID'] .  "'>" . $row['Location'] . '</a></td>';
										echo "</tr>";
								}
							?>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>




<!--===============================================================================================-->
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>
