# Setup
1. Pull the directory, and save to a local folder
2. In ampps, go to apache's httpd.conf
    1. Uncomment "LoadModule proxy_module modules/mod_proxy.so" and "LoadModule proxy_http_module modules/mod_proxy_http.so"
    2. Add the following to the bottom
        ```
        Alias /NWI "C:/Users/emrti/OneDrive - Drexel University/Documents/School_Projects/Neonatal-Web-Interface/main"
        <Directory "C:/Users/emrti/OneDrive - Drexel University/Documents/School_Projects/Neonatal-Web-Interface/main">
            Options Indexes FollowSymLinks Multiviews
            MultiviewsMatch Any
            AllowOverride None

            #Restrict access to localhost:
            Require local
        </Directory>
        ```
    3. Add the following to <VirtualHost 127.0.0.1:80>
        ```
        Alias /NWI/static/ "C:/Users/emrti/OneDrive - Drexel University/Documents/School_Projects/Neonatal-Web-Interface/main/static/"
        <Directory "C:/Users/emrti/OneDrive - Drexel University/Documents/School_Projects/Neonatal-Web-Interface/main/static/">
            Options Indexes FollowSymLinks Multiviews
            MultiviewsMatch Any
            AllowOverride None
            Require all granted
        </Directory>
        ProxyPass /NWI/static/ !
        ProxyPass /NWI/favicon.ico !
        ProxyPass /NWI/ http://127.0.0.1:5000/NWI/
        ProxyPassReverse /NWI/ http://127.0.0.1:5000/NWI/
        ```
    4. Comment out the following in <VirtualHost 127.0.0.1:80>
        ```
        # <Directory "{$path}/www">
        # 	Options FollowSymLinks Indexes
        # 	 AllowOverride All
        #     Require all granted
        # </Directory>

        # ScriptAlias /cgi-bin/ "{$path}/www/cgi-bin/"
        # DocumentRoot "{$path}/www"
        ```

# Start Server
1. Open ampps and start apache
2. Go to a terminal and run `python <path to app.py>`
3. In a browser, navigate to `http://localhost/NWI/

# Notes
* To access the files outside of the running server (so mainly just to check out the HTML), navigate to `http://localhost/NWI-Debug/`
    * Just opening the file directly (double clicking the HTML), will likely subvert the css. This may also happen if the server is not running
    * Attempting to submit a form in this mode will throw a 502 error
* If you get a 440 error at any point, it is likely from an unimplemented page