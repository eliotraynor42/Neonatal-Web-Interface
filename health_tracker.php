<header>
    <html>
    <head>
    </head>
    <body>
        <?php
        $PatientID=1; #<!-- NEED TO LINK THIS BACK INTO THE MAIN CODE-->
        $DataNames=["Weight (kg)","Length (cm)","Head Circumference (cm)","Temperature (c)","Heart Rate (bpm)","Respiratory Rate (bpm)","Oxygen Saturation","Primary Feeding Type","Feeding Frequency per Day","Urination Count per Day","Stool Count per Day","Imunizations Needed","Reflexes Normal","Risk Level"];
        $newvariables=["weight","length","circumference","temperature","heart_rate","respiratory_rate","oxygen_saturation","primary_feeding_type","feeding_frequence","urination","stool","immunizations","reflexes","risk"];
        $v_type=["number","number","number","number","number","number","number","text","number","number","number","text","text","text"];
        $Today=date('Y-m-d'); #Today's Date

        // Vatiables for Calling Database Python
        $PYEXE='python'; //Prep a python variable for the call
        if(strtoupper(substr(PHP_OS, 0, 3)) === 'WIN'){ 
            if(file_exists($try='C:\ProgramData\Anaconda3\python.exe')) $PYEXE=$try;
        }
        $PatientID=(int)$PatientID; #Removes any possible issues from patient id
        $call = "SELECT * FROM patient_visit_data WHERE id=$PatientID;";
        $cmd = "\"$PYEXE\" query_data.py " . escapeshellarg($call); #Calls the python script with the written call
        $out = shell_exec($cmd); #Calls the output as a single string that can then be decoded
        $data = json_decode($out, true); #Decodes the data into rows

        echo'<form method="POST" class=leform>';
            echo "<label for='Date'>Date of Updates:</label><br>";
            echo "<input type='date' id='Date' name='Date' placeholder=$Today> <br><br>";
            for ($i=0; $i<count($DataNames); $i++){
                echo "<label for={$newvariables[$i]}>{$DataNames[$i]}:</label><br>";
                echo "<input type={$v_type[$i]} id={$newvariables[$i]} name={$newvariables[$i]} value=".htmlspecialchars($data[0][$i+4])."><br><br>";
            };
            
            echo '<input type="submit" name="submit" value="submit">';

        echo "</form>";
        
                

        $Doctor_ID=3; #NEED TO LINK THIS BACK INTO WEBSITE LOGIC

            if(isset($_POST['submit'])){ //Runs when submitted
                $PatientID = (isset($_POST['PatientID']) && $_POST['PatientID'] !=='') ? $_POST['PatientID'] : 0; //If a patient ID is given, store it, if not, save 0 which is not a valid ID
                $PatientName = (isset($_POST['PatientName']) && $_POST['PatientName'] !=='') ? $_POST['PatientName'] : "NULL"; //If a name is given, store it, if not save NULL
                
                // Vatiables for Calling Database Python
                $PYEXE='python'; //Prep a python variable for the call
                if(strtoupper(substr(PHP_OS, 0, 3)) === 'WIN'){
	                if(file_exists($try='C:\ProgramData\Anaconda3\python.exe')) $PYEXE=$try;
                }
                   
                $call="SELECT id,name FROM patients WHERE id=$PatientID OR name='$PatientName';"; #Creates the call    
                $cmd="\"$PYEXE\"  query_data.py " . escapeshellarg($call); #Calls the python script with the written call
                    $out = shell_exec($cmd); #Calls the output as a single string that can then be decoded
                $row_data = json_decode($out, true); #Decodes the data into rows
                
                ?>
                <form method="POST" action="process_selection.php">
                    <table border="1"> <!-- Create Table to Show Data -->
                        <thead>
                            <th>Selection</th>
                            <th>Patient ID</th>
                            <th>Patient Name</th>
                        </thead>
                        <tbody>
                            <?php
                            #For Loop to write the output from the python call to rows of the table
                            for ($i=0; $i<count($row_data); $i++){
                                echo "<tr><td><input type='radio' name='selection' value='{$row_data[$i][0]}'></td>"; #Creates a row to grab the name 
                                echo "<td>{$row_data[$i][0]}</td><td>{$row_data[$i][1]}</td></tr>"; #Writes a row of the table and inserts the data into it.
                            }
                            ?>

                        </tbody>
                    </table>
                     <input type="submit" name="submitselect" value="submit">
                </form>
                
                <?php
            }  
                
            
        ?>

       

      
</html>