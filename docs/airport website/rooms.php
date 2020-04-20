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
	<link rel="stylesheet" type="text/css" href="css/main2.css">
<!--===============================================================================================-->
</head>
<body>
	<div class="limiter">
		<div class="container-table100">
			<div class="wrap-table100">
				<div class="table100">
					<table>
					<?php
						$conn = new mysqli('localhost', 'root', '1234', 'airportinfo');

						if(isset($_GET['Hotel_ID']) and (int)$_GET['Hotel_ID'] >= 1){
							$query =  "SELECT * FROM rooms WHERE Hotel_ID = " . $_GET['Hotel_ID'] . ";";
							$hotel_name = "SELECT * FROM hotels WHERE Hotel_ID = " . $_GET['Hotel_ID'] . ";";
							$hotel_name = $conn->query($hotel_name);
							while($row = $hotel_name->fetch_array()){
								$hotel_name = $row['Name'];
								break;
							}


							$result = $conn->query($query);
							echo "<h1 style = \"color:white;text-align:center;margin: -20px 0px 20px 0px;font-family: OpenSans-Regular;\">" . (is_string($hotel_name) ? $hotel_name . " - Rooms" : "NO RESULTS" ) . "</h1>";
						} else if (isset($_GET['Hotel_ID'])){
							$query =  "SELECT * FROM rooms WHERE Hotel_ID = " . $_GET['Hotel_ID'] . ";";
							$result = $conn->query($query);
							echo "<h1 style = \"color:white;text-align:center;margin: -20px 0px 20px 0px;font-family: OpenSans-Regular;\">NO RESULTS</h1>";
						} else {
							$query =  "SELECT * FROM rooms;";
							$result = $conn->query($query);
							echo "<h1 style = \"color:white;text-align:center;margin: -20px 0px 20px 0px;font-family: OpenSans-Regular;\"> All - Rooms </h1>";
						}
						 ?>
						 <p style = "color:white;margin:20px 0px 5px 0px;font-family: OpenSans-Regular;font-size:0.9em;"> *Scrolling: Tell the assitant to either "Scroll up/Go up" or "Scroll down/Go down"</p>
						 <p style = "color:white;margin:5px 0px 20px 0px;font-family: OpenSans-Regular;font-size:0.9em;"> *Exiting: Tell the assitant "Close Google Chrome"</p>
						<thead>
							<tr class="table100-head">
								<th class="column1">Room ID</th>
								<th class="column2">Number of Beds</th>
								<th class="column3">Price</th>
								<th class="column4">Details</th>
								<th class="column5">Hotel ID</th>
							</tr>
						</thead>
						<tbody>
							<?php
								while($row = $result->fetch_array()){
										echo "<tr>";
											echo "<td class='column1'>" . $row['Room_ID'] . '</td>';
											echo "<td class='column2'>" . $row['Number_beds'] . '</td>';
											echo "<td class='column3'>" . $row['Price'] . '</td>';
											echo "<td class='column4'>" . $row['Details'] . '</td>';
											echo "<td class='column5'>" . $row['Hotel_ID'] . '</td>';
										echo "</tr>";
								}
							?>
							<h3 style="padding-left: 6px;margin-bottom: 5px;font-size:17px;"><a href="http://localhost/airport/">← Back to browsing hotels</a></h3>
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
