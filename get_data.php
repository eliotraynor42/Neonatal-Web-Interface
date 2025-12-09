<html>
    <head>
    </head>
    <body>
        
        <?php

        $PatientID=1; #<!-- NEED TO LINK THIS BACK INTO THE MAIN CODE-->
        $DataNames=["Date Updated","Age (days)","Weight (kg)","Length (cm)","Head Circumference (cm)","Temperature (c)","Heart Rate (bpm)","Respiratory Rate (bpm)","Oxygen Saturation","Primary Feeding Type","Feeding Frequency per Day","Urination Count per Day","Stool Count per Day","Imunizations Needed","Reflexes Normal","Risk Level"];


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
        ?>
        <table border="1">
            <thead>
                <th>Data Type</th>
                <th>Current Status</th>
            </thead>
            <tbody>
                <?php

                for ($i=0; $i<count($DataNames); $i++){
                    echo "<tr><td>{$DataNames[$i]}</td><td>{$data[0][$i+2]}</td></tr>"; #Writes a row of the table and inserts the data into it.
                }
                
                ?>
            </tbody>
        </table>


    </body>
</html>