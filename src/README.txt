# Setup
1. Pull the directory, and save to a local folder

# Start Server
1. Open ampps and start apache
2. Open the src/start_interface.ipynb file, and run the first block

# Notes
* To access the files outside of the running server (so mainly just to check out the HTML), navigate to `http://localhost/NWI-Debug/`
    * Just opening the file directly (double clicking the HTML), will likely subvert the css. This may also happen if the server is not running
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
* If you get a 440 error at any point, it is likely from an unimplemented page