# Setup
1. Pull the directory, and save to a local folder

# Start Server
1. Open the src/start_interface.ipynb file, and run the first block
2. To test the application, use the username "demo" with password "demo" for both patient and doctor logins

# Notes
* It is not advised to try and access any files outside of the running server, but this may be done by starting apache and navigating to `http://localhost/NWI-Debug/`
    * Just opening the file directly (double clicking the HTML), will likely subvert the css
    * Attempting to submit a form in this mode will throw a 502 error
    * You must add the following lines to your apache httpd.conf file:
        ```
        Alias /NWI-Debug "<path to src foler>"
        <Directory "<path to src folder>">
            Options Indexes FollowSymLinks Multiviews
            MultiviewsMatch Any
            AllowOverride None
            Require local
        </Directory>
        ```

# Function Descriptions

1. app.py
* Sets up the flask system to map HTML and outputs to python files.

2. background.py
* File being used for the background for databasing and background work. 

3. bmes_ahmet_loader
* This file adjusts the python path so you can include Ahmet's shared dropbox folder.

4. DB_maker.py 
* Builds a sample database. 

5. get_comm_doctor.py
* Returns all past communications between doctor and the specific patient.

6. get_data.py
* Gets the newest data for a patient through a SQL query. 

7. get_doctor_notif.py
* Returns all new notifications for a specific doctor that have not been read.

8. get_patient.py
* Returns patient information for the Doctor View Patient webpage.

9. get_patient_list.py
* Gets all patients for doctor.

10. get_user_login.py
* Validates user login and redirects traffic accordingly.

11. graph_data.py
* Returns data from database to build graphs.

12. send_message.py
* Returns message data from health tracker to database.

13. submit_patient_data.py
* Returns patient data from health tracker to database.




# References. 
1. Average baby weight: Chart and development. (2019, July 2). https://www.medicalnewstoday.com/articles/325630
2. What is the average baby length? Growth chart by month. (2019, March 18). https://www.medicalnewstoday.com/articles/324728
3. Average newborn head circumference. (n.d.). BabyCenter. Retrieved December 10, 2025, from https://www.babycenter.com/baby/baby-development/baby-head-circumference_40009394
4. A guide to your kid’s vital signs. (n.d.). Cleveland Clinic. Retrieved December 10, 2025, from https://health.clevelandclinic.org/pediatric-vital-signs
5. Thilo, E. H., Park, C. K., & Sedaghat, V. S. (1991). Oxygen saturation by pulse oximetry in healthy infants at an altitude of 1610 meters. American Journal of Diseases of Children, 145(10), 1137–1140. https://jamanetwork.com/journals/jamapediatrics/fullarticle/515871
6. Drakeford, K., MA, RD, CSP, LD, & CLC. (n.d.). Here’s a handy feeding chart for newborns and babies. Parents. Retrieved December 10, 2025, from https://www.parents.com/baby/feeding/baby-feeding-chart-how-much-and-when-to-feed-infants-the-first-year/ 
7. Garbi, L. & MD. (n.d.). Does your baby have enough wet diapers? Parents. Retrieved December 10, 2025, from https://www.parents.com/breastfeeding-and-wet-diapers-whats-normal-431621
8. Baby poop guide. (n.d.). Retrieved December 10, 2025, from https://www.childrenscolorado.org/just-ask-childrens/articles/baby-poop-guide/ 
9. Geeksforgeeks | quiz hub: Test your knowledge. (n.d.). GeeksforGeeks. Retrieved December 10, 2025, from https://www.geeksforgeeks.org/quizzes/.  
10. Goyal, S. (2019, January 17). Open browser automatically when Python code is executed [Online forum post]. Stack Overflow. https://stackoverflow.com/questions/54235347/open-browser-automatically-when-python-code-is-executed/54235461#5423546 
