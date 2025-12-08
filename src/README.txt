# Setup
1. Pull the directory, and save to a local folder

# Start Server
1. Open the src/start_interface.ipynb file, and run the first block

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