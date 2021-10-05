# Commonpaths-Open_Trip_Planner_Multi_Tenant_service
  - The Open Trip Planner (OTP) service will be used as a resource for planning trips.
  - The codes in the current repository will help the user in downloading, validating and creating/updating Graph.obj with minimal Manual work.

#### Requirements for downloading GTFS feed
1. Create api key by signing into github account on: https://transitfeeds.com/api/
2. Save the api key in the file set_env_var.py by setting the variable os.environ["API_KEY"] as the corresponding api key.

## Folder Structures for Downloading GTFS feeds and updating the Graph.obj in router directory
### Folder structure 1(base level)

```
ec2-user
|
└── Multi-tenant-otp-server [All codes for running multi-tenant otp server | refer to: https://github.dxc.com/mv-transportation/MVT--OTP-SERVER/]
    └── otp (Multi tenant otp server:running at http://##.##.##.##:8080//otp/**tenant_name**/default/plan/**arguments** [refer to folder structure 2]
    └── workspace [refer to folder structure 3]
```
- In the above example of querying the OTP server API the variable name **tenant_name** will be the name of the tenant/router whose routes we want to query. So if we have two tenants **kcm** and **portland** in our otp server and we want to query the routes for portland, the way we query it is as follows: "http://##.##.##.##:8080//otp/**portland**/default/plan/**arguments**".
- More information on querying the hosted OTP server can be found [here](http://docs.opentripplanner.org/en/v1.5.0/Intermediate-Tutorial/)

### Folder structure 2(otp):
```
otp
└── cache
└── graphs
    └── kcm
    |   └── community-transit.zip (tested and working GTFS feed)
    |   └── king-county-metro.zip (tested and working GTFS feed)
    |   └── kitsap-transit.zip    (tested and working GTFS feed)
    |   └── pierce-transit.zip    (tested and working GTFS feed)
    |   └── sound-transit.zip     (tested and working GTFS feed)
    |   └── pr_osm_to_otp.osm     (OSM data)
    |   └── merged_n47_w122_n47_w123_n48_w123.tif (Elevation data)
    └── router_1
    |   └── gtfs_1.zip (tested and working GTFS feed)
    |   └── gtfs_2.zip (tested and working GTFS feed)
    |   └── gtfs_3.zip    (tested and working GTFS feed)
    |   .
    |   .
    |   └── gtfs_n.zip     (tested and working GTFS feed)
    |   └── router_1.osm     (OSM data)
    |   └── router_1.tif (Elevation data)
    .
    .
    .
    └── router_n
        └── gtfs_n_1.zip (tested and working GTFS feed)
        └── gtfs_n_2.zip (tested and working GTFS feed)
        └── gtfs_n_3.zip    (tested and working GTFS feed)
        .
        .
        └── gtfs_n_n.zip     (tested and working GTFS feed)
        └── router_n.osm     (OSM data)
        └── router_n.tif (Elevation data)
```

### Folder structure 3(workspace):
```
workspace
└── config_files
|    └── county_names.json
|    └── osm_db_config.json
|
└── reference_files
|    └── old_county_names.json
|    └── new_routers.json
|
└── log_files
|    └── current_status.txt
|    └── GTFS_error_log.txt
|    └── GTFS_metadata.txt
|    └── initial_download_program_metadata.txt
|    └── latest_download_program_metadata.txt
|    └── OSM_download_meta.txt
|
|
└── GTFS_feeds [refer to folder structure 4]
|   └── current
|   └── elevation
|   └── graph_creation
|   └── previous
|
└── MultiTenant [Python class files for automated process]
|   └── download_check_create.py
|   └── Download_GTFS_data.py
|   └── Primer.py
|   └── set_env_var.py
|   └── Validate_GTFS_and_graph_creation.py
|
└── fetch_osm_create_graph_existing.py
|
└── fetch_osm_create_graph_new.py
|
└── initial_download.py
|
└── multi-tenant-otp-server.sh
|
└── otp-1.4.0.shaded.jar
```
#### DESCRIPTION OF FILES AND FOLDERS IN DIRECTORY WORKSPACE

##### config_files

- There will be two configuration files in .json format
  i .  county_names.json
  ii. osm_db_config.json

1. county_names.json
   - This file contains the names of the router and their corresponding agency ids from the Transitfeed website in a specific format.
   - FOLLOW THE FORMAT CAREFULLY OR ELSE IT CAN LEAD TO BAD RESULTS.(Note: Take care of commas, or a better option is to create a python dictionary,
   - print it to make sure it is error free, then copy the printed dictionary to county_name.json file)
   - For example: If our Open_Trip_Planner as a Multi_tenant_service contains two areas namely King County Metro(kcm) and Portland(portland),
     then the format would be something like this:   
     ```
     {
       "kcm":["king-county-metro/73","sound-transit/44","community-transit/454","pierce-transit/448","kitsap-transit/296"],
       "portland":["trimet/43","washington-park-shuttle/758","blue-star-transportation/437"]
     }
     ```
 2. osm_db_config.json
    - This is the database configuration file which contains the credentials of the private OSM hosted on AWS from which the .osm file will be pulled
    - Whenever a new county is to be added simply put the credentials of the private OSM of new county in the osm_db_config.json config file and save it.
    - For example: If the new tenant is portland then the file osm_db_config.json should be something like this:
      ```
      {
        "kcm" : {
          "HOSTNAME":   "ABC",
          "DATABASE":   "osm_kcm",
          "USERNAME":   "***",
          "PASSWORD":   "########",
          "PGPASSWORD": "########"
        },
        "portland" : {
          "HOSTNAME":   "XYZ",
          "DATABASE":   "osm_portland",
          "USERNAME":   "***",
          "PASSWORD":   "########",
          "PGPASSWORD": "########"
        }
      }
      ```

##### reference_files

- There is a file in this directory namely **old_county_names.json** (DO NOT TOUCH THIS FILE.) The purpose of this file is to keep track of existing routers (kcm in our case) and is useful for internal automated processes when a new tenant is added.
- The other file namely **new_routers.json** is also not to be touched or manipulated. Its purpose is for internal automated processes and is used internally by the program when a new tenant is added.

##### log_files

- This directory contains the log of the process that is happening inside MVT--OTP-SERVER. There are six files in it namely:
  i  . current_status.txt
  ii . GTFS_error_log.txt
  iii. GTFS_metadata.txt
  iv . initial_download_program_metadata.txt
  v  . latest_download_program_metadata.txt
  vi . OSM_download_meta.txt

1. current_status.txt
  - This log file tells us which county/counties the OTP-SERVER give us the routes for. It also gives us information on which GTFS feeds are currently in use.
2. GTFS_error_log.txt
  - If there is error in GTFS file that is downloaded via transit-feed api, this log file will contain its information along with the time, date and name of the bad GTFS feed.
3. GTFS_metadata.txt
  - This log file gives us all the information detailing when the last GTFS feed was downloaded, and when that feed was modified at source.
4. initial_download_program_metadata.txt
  - This file gives you information about the internal program workings when new tenant is added. More on this later.
5. latest_download_program_metadata.txt
  - The OTP-SERVER is created in such a way that it downloads news GTFS feeds and the OSM file every day at midnight. This file gives information for that process.
6. OSM_download_meta.txt
  - Whenever there is a changeset file generated at the private OSM side, the MVT--OTP-SERVER will download new OSM file. This log file gives you the information when such a process occurs.

- For more info on log_files take a look at them in the specified directory.

##### GTFS_feeds

MODIFY
##### MultiTenant

- This directory is strictly for internal processes, DO NOT MODIFY IT, unless absolutely necessary.

##### fetch_osm_create_graph_existing.py

- Do not change this file.
- This python script checks for changeset(.osc) files. If there is a newly created changeset file, it will download osm data to the router directory, download GTFS data, create graph objects and update the router, so that MVT--OTP-SERVER gives the most updated routes.
- Even if there is no changeset file created, it will download the GTFS files and carry on the task of updating the router with existing OSM data.
- This python script is triggered every day at midnight (UTC 12.00 AM) by an AWS Lambda function:

##### fetch_osm_create_graph_new.py

- This script is the same as fetch_osm_create_graph_existing.py, only it will not check for the changeset file.
- This script will be used whenever a new tenant is added.

##### initial_download.py

- This script will be used whenever a new tenant is added.
- This script will download the initial GTFS data, and will have to be run manually.
- If there is any error in the downloaded GTFS data, manual download will have to be done from the web address provided from a message from the script. Errors in GTFS feeds are rare and do not occur often.

##### multi-tenant-otp-server.sh

- The shell script that starts the multi-tenant-otp-server. It is set up as a daemon.
- More on this later.

### Folder structure 4(GTFS_feeds):
```
GTFS_feeds
└── current
|    └── kcm
|    |   └── community-transit
|    |   |   └── community-transit.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── king-county-metro
|    |   |   └── king-county-metro.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── kitsap-transit
|    |   |   └── kitsap-transit.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── pierce-transit
|    |   |   └── pierce-transit.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── sound-transit
|    |       └── sound-transit.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    └── portland
|    |   └── trimet
|    |   |   └── trimet.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── blue-star-transportation
|    |   |   └── blue-star-transportation.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   └── washington-park-shuttle
|    |       └── washington-park-shuttle.zip (latest downloaded via download_latest_gtfs_feeds.py)
|    |   .
|    |   .
|    |   .
|    |   .
|    └── router_n
|        └── service_1
|        |   └── gtfs_1.zip (latest downloaded via download_latest_gtfs_feeds.py)
|        └── service_2
|        |   └── gtfs_2.zip (latest downloaded via download_latest_gtfs_feeds.py)
|        |   .
|        |   .
|        |   .
|        └── service_n
|            └── gtfs_n.zip (latest downloaded via download_latest_gtfs_feeds.py)         
|
└── graph_creation
|   └── kcm
|   |   └── community-transit.zip (tested and working GTFS feed)
|   |   └── king-county-metro.zip (tested and working GTFS feed)
|   |   └── kitsap-transit.zip    (tested and working GTFS feed)
|   |   └── pierce-transit.zip    (tested and working GTFS feed)
|   |   └── sound-transit.zip     (tested and working GTFS feed)
|   |   └── pr_osm_to_otp.osm     (OSM data)
|   |   └── elev_1.tif            (Elevation data)
|   └── portland
|   |   └── trimet.zip                   (tested and working GTFS feed)
|   |   └── blue-star-transportation.zip (tested and working GTFS feed)
|   |   └── washington-park-shuttle.zip  (tested and working GTFS feed)
|   |   └── portland.osm                 (OSM data)
|   |   └── elev_2.tif                   (Elevation data)
|   .
|   .
|   .
|   └── router_n
|       └── gtfs_1.zip         (tested and working GTFS feed)
|       └── gtfs_2.zip         (tested and working GTFS feed)
|       .
|       .
|       .
|       └── gtfs_n.zip          (tested and working GTFS feed)
|       └── open_street_map.osm (OSM data)
|       └── elev_n.tif          (Elevation data)
|
└── previous
    └── kcm
    |   └── community-transit.zip (Most recent working GTFS feed)
    |   └── king-county-metro.zip (Most recent working GTFS feed)
    |   └── kitsap-transit.zip (Most recent working GTFS feed)
    |   └── pierce-transit.zip (Most recent working GTFS feed)
    |   └── sound-transit.zip (Most recent working GTFS feed)
    └── portland
    |   └── trimet.zip (Most recent working GTFS feed)
    |   └── blue-star-transportation.zip (Most recent working GTFS feed)
    |   └── washington-park-shuttle.zip (Most recent working GTFS feed)
    .
    .
    .
    └── router_n
        └── gtfs_1.zip (Most recent working GTFS feed)
        └── gtfs_2.zip (Most recent working GTFS feed)
        .
        .
        .
        └── gtfs_n.zip (Most recent working GTFS feed)
```

## Initial Manual process to add new tenant.(These steps are to be taken once for every tenant, after that the process will be automatic)

- Assumptions:
    - The private OSM for a new tenant is already set up and credentials for the same are available.

- Reason for the Manual process:
    - Initial download and validation of GTFS files is necessary as these files are error prone.
    - FAILURE TO FOLLOW THE GIVEN STEPS CAREFULLY COULD RESULT IN OSM SERVER CRASHING OR WORKING ON OLD DATA, SO PLEASE DO EXACTLY AS SPECIFIED

- Note:
    - Follow the steps and the sub-steps chronologically.

### STEP-1
- Suppose that we have only one tenant which is kcm and we want to add portland to our multi-tenant-otp trip planner server.

1. First thing we need to do is to add the name and agency ids that we get from Transitfeed into **county_names.json** as follows:
    ```
    {
      "kcm":["king-county-metro/73","sound-transit/44","community-transit/454","pierce-transit/448","kitsap-transit/296"],
      "portland":["trimet/43","washington-park-shuttle/758","blue-star-transportation/437"]
    }
    ```
    - Save **county_names.json** after adding the line for portland.
2. Add the credentials for the Private OSM database in file **osm_db_config.json** as follows:
    ```
    {
      "kcm" : {
        "HOSTNAME":   "ABC",
        "DATABASE":   "osm_kcm",
        "USERNAME":   "***",
        "PASSWORD":   "########",
        "PGPASSWORD": "########"
      },
      "portland" : {
        "HOSTNAME":   "XYZ",
        "DATABASE":   "osm_portland",
        "USERNAME":   "***",
        "PASSWORD":   "########",
        "PGPASSWORD": "########"
      }
    }
    ```


3. Run the script **initial_download.py** from command line using the following command: ***python initial_download.py***
    ```
    python3 /home/ec2-user/MVT--OTP-SERVER/workspace/initial_download.py
    ```
   - IF everything is fine with the GTFS file that is downloaded, then the script will give the following message on command line:
      - *The downloaded GTFS files are up to date, Continue with STEP-2 of Manual process*.
      - If the above message appears skip everything else in STEP-1 from this point and continue with STEP-2
   - If there are errors a different message will be delivered and the message will guide you what to do next. For simplicity the below mentioned general process is to be followed in the case when downloaded GTFS file has errors.
      - The message will give you the web address from where to download a new file and where to save it. You should refer the folder structure first.
      - After placing the files in the respective folders, you will have to run ***point 2.*** again and again until you get the message:
        - *The downloaded GTFS files are up to date, Continue with STEP-2 of Manual process*.

### STEP-2

1. Add the elevation data of the particular router in its directory as shown below:

```
otp
└── cache
└── graphs
    └── kcm
    |   └── community-transit.zip (tested and working GTFS feed)
    |   └── king-county-metro.zip (tested and working GTFS feed)
    |   └── kitsap-transit.zip    (tested and working GTFS feed)
    |   └── pierce-transit.zip    (tested and working GTFS feed)
    |   └── sound-transit.zip     (tested and working GTFS feed)
    |   └── pr_osm_to_otp.osm     (OSM data)
    |   └── merged_n47_w122_n47_w123_n48_w123.tif (Elevation data)
    └── router_1
    |   └── gtfs_1.zip (tested and working GTFS feed)
    |   .
    |   .
    |   └── gtfs_n.zip     (tested and working GTFS feed)
    |   └── router_1.osm     (OSM data)
    |   └── router_1.tif (Elevation data)
    .
    .
    └── router_n
        └── gtfs_n_1.zip (tested and working GTFS feed)
        .
        .
        └── gtfs_n_n.zip     (tested and working GTFS feed)
        └── router_n.osm     (OSM data)
        └── router_n.tif (Elevation data)
```


2. After the initial GTFS data are downloaded and elevation data added to the respective folder as shown above, you need to create graphs for the new router which in our case as an example is portland.
  - To do this run the script **fetch_osm_create_graph_new.py** from the command line using the following command:
  ```
  python3 /home/ec2-user/MVT--OTP-SERVER/workspace/fetch_osm_create_graph_new.py
  ```
  - This will take around 40 minutes to an hour. Once the process is finished, the multi-tenant-otp server will give routes for the new county as well.

## Updating the current OTP server to new OSM file and latest GTFS feeds for a specific tenant

  - This feature is included in order to update the OTP server when a particular tenant has made changes to the private OSM and wishes to update the OTP server to new OSM file along with latest GTFS feeds.
  - In order to use this we use the script:
    ```
      python3 /home/ec2-user/MVT--OTP-SERVER/workspace/fetch_osm_create_graph_existing.py [-t <Name of tenant who wishes to update OTP server to new OSM file>] [-u <Username of the person making the update>]    
    ```
    - **Note**: The parameter **t** can be uses in the following ways:
    1. If name of the tenant/county/router is given as an argument to parameter **t**, then the the Graph.obj related to that particular tenant will get updated with the latest private OSM and GTFS feeds belonging to that particular tenant. *Note: The name of the tenant should be the same as specified in workspace/config_files/county_names.json*

    2. It is not mandatory to give arguments to parameter **t**. When no arguments are given to the script mentioned above, the program automatically updates OSM and GTFS feeds of all tenants in the running OTP server. This is necessary to periodically update the OTP server with latest data(OSM and GTFS)
    3. The parameter **u** is the username of the logeed person in the webapp who is demanding the update.
    4. Both of the parameters **t** and **u** come from the webapp. You can specify it manually in case of bugs in the webapp but its not needed generally as the functionality is integrated with the webapp.

## Running otp server as a Daemon

- The multi-tenant-otp-server is already running as a daemon, so you don't need to do anything. The information is for development purposes only.

1. In your /home/ec2-user directory enter the following command:
    ```
    sudo vim /etc/systemd/system/multi-tenant-otp-application.service
    ```
    - Copy the following script and press **:wq** .
    ```
    [Unit]
    Description=Java Application as a Service
    [Service]
    Environment="otp_version=otp-1.4.0-shaded.jar"
    Environment="otp=/home/ec2-user/MVT--OTP-SERVER/otp/graphs/"
    User=ec2-user
    #change this directory into your workspace
    #mkdir workspace
    WorkingDirectory=/home/ec2-user/MVT--OTP-SERVER/workspace
    #path to the executable bash script which executes the jar file
    ExecStart=/bin/bash /home/ec2-user/MVT--OTP-SERVER/workspace/multi-tenant-otp-server.sh
    SuccessExitStatus=143
    TimeoutStopSec=10
    Restart=on-failure
    RestartSec=5
    [Install]
    WantedBy=multi-user.target
      ```
2. Go to the directory **workspace** and enter the following in terminal:
    ```
    sudo chmod u+x multi-tenant-otp-server.sh
    ```
3. Start/stop service

   - Initial steps:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable multi-tenant-otp-application.service
   ```

   - **Start** OTP-SERVER as a daemon(It will run continuously in background) [Note it has already been started and is running in background:

   ```
   sudo systemctl start multi-tenant-otp-application
   ```

   - **Stop** OTP-SERVER as a daemon(Don't do it unless absolutely needed)
   ```
   sudo systemctl stop multi-tenant-otp-application
   ```

   - Check **status** of the OTP-SERVER
   ```
   sudo systemctl status multi-tenant-otp-application -l
   ```

## Environment variables

- All environment variables are defined in the file **/etc/profile.d/otp_set_env_var.sh**
- Any changes to be made to the environment variables should be done in the file **otp_set_env_var.sh** which resides in the path mentioned above.
- The changes to these environment variables come in handy, say for example if we want to upgrade the version of **Open Trip Planner**.

## Updating or changing to a different version of Open trip Planner

- In order to upgrade or change the version of Open Trip Planner, there are three essential steps that we need to take into consideration.

### STEP-1

- Download the appropriate version of the Open Trip Planner .jar file to the location shown below.

```
ec2-user
|
└── Multi-tenant-otp-server
    └── otp
    └── workspace
        └── config_files
        |
        └── reference_files
        |
        └── log_files
        |
        └── GTFS_feeds [refer to folder structure 4]
        |
        └── MultiTenant [Python class files for automated process]
        |
        └── fetch_osm_create_graph_existing.py
        |
        └── fetch_osm_create_graph_new.py
        |
        └── initial_download.py
        |
        └── multi-tenant-otp-server.sh
        |
        └── **otp-1.4.0.shaded.jar**(This is the otp jar file which is to be placed inside folder workspace)
```

### STEP-2

- Change the name of the environment variable. The steps to follow are:

1. Type the following command:
    ```
    vim /etc/profile.d/otp_set_env_var.sh
    ```

2. Press "i" to enter into edit mode and make the following changes:
    - Look for variable **otp_version** and change its value to the desired version of open trip planner.
    - The value assigned to **otp_version** variable should be the same as the name of the jar file downloaded in previous step.

3. After completing the above steps press **esc** and type the following to, save and quit the changes made to environment variables.
    ```
    :wq
    ```
    - Press **enter** after typing the above values.
    - Your changes will be made.

### STEP-3
- This step takes care of the otp Java application that is running as a service.
- The following steps need to be performed.

1. Stop the otp server running as a daemon with the following command:
    ```
   sudo systemctl stop multi-tenant-otp-application
   ```
2. Change the environment variable in the service that corresponds to the OTP .jar file. to do this follow the steps below:
    i. Open service to make changes:
        ```
        sudo vim /etc/systemd/system/multi-tenant-otp-application.service
        ```

    ii. Look at the following lines and change the value of variable **otp_version** to the name of the new jar file of open trip planner downloaded in **STEP-1** :
        ```
        [Service]
        Environment="otp_version=otp-1.4.0-shaded.jar"
        Environment="otp=/home/ec2-user/MVT--OTP-SERVER/otp/graphs/"
        User=ec2-user
          ```

    iii. Press **esc** type **:wq** and press **enter**

    iv. Go to the directory **workspace** and enter the following in terminal:
        ```
        sudo chmod u+x multi-tenant-otp-server.sh
        ```

    v. Run the following three commands one by one:
        ```
        sudo systemctl daemon-reload
        sudo systemctl enable multi-tenant-otp-application.service
        sudo systemctl start multi-tenant-otp-application
        ```
