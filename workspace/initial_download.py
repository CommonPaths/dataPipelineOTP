#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

import json
from MultiTenant.Validate_GTFS_and_graph_creation import Validate_GTFS
from MultiTenant.Download_GTFS_data import Download,Meta_Error_Info
from MultiTenant.Primer import File_Management
from MultiTenant.set_env_var import Env
from MultiTenant.AWS_S3_manipulation import S3_Bucket_manipulation

def main():
    Folder_management = File_Management("county_names","old_county_names")
    Validation     = Validate_GTFS()
    GTFS_feed_manipulation     = Download()
    Env_var = Env()
    Metadata_and_error = Meta_Error_Info(GTFS_feed_manipulation.log_files_path)
    S3_manipulation = S3_Bucket_manipulation()

    gtfs_quality_flag = False

    updated_routers,outdated_files = Folder_management.find_diff_in_json()
    with open(Env_var.get_env("new_router_names"),"w") as f:
        json.dump(updated_routers,f)

    initial_meta = open(GTFS_feed_manipulation.log_files_path+"initial_download_program_metadata.txt", "w")
    initial_meta.writelines("The following information for manual initial download is for date: "+ Metadata_and_error.current_time+"\n")
    initial_meta.writelines("\n")
    initial_meta.writelines("\n")
    initial_meta.close()

    f_name = "initial_download_program_metadata.txt"
    message = []
    message.append("---- The Following files and folders will be deleted as they are no longer included in county_names.json config file-------------- \n \n")
    for router,agency_feed_id in outdated_files.items():
        if(len(agency_feed_id) == 0):
            message.append("-- The router/county with name ' "+router+" ' is deleted with all its content as it is no longer considered as a tenant \n")
        else:
            message.append("-> The following GTFS files will be removed from router: "+router+" \n")
            for agency in agency_feed_id:
                message.append("- The GTFS file ' "+agency+" ' is removed from all the places where it is inside the above mentioned router")
    Metadata_and_error.program_metadata(message,f_name)

    Folder_management.delete_outdated_folders_files(outdated_files)
    S3_manipulation.s3_delete_dir(outdated_files)

    Folder_management.create_folders(updated_routers)
    S3_manipulation.s3_create_dir(updated_routers)


    while(gtfs_quality_flag == False):
        download_time,update_time = GTFS_feed_manipulation.download_latest_GTFS_feeds(router_data = updated_routers)
        print("CHECKING INDIVIDUAL GTFS FILES")
        Validation.check_individual_gtfs(router_data = updated_routers)
        Metadata_and_error.gtfs_error_log(Validation.graph_size_dict,download_time,update_time)

        gtfs_quality_flag = Validation.check_no_errors()

        if(gtfs_quality_flag == True):
            Validation.copy_current_to_previous_feeds(initial = True)
            print("\n \n \n")
            print("The downloaded GTFS files are up to date, Continue with STEP-2 of Manual process")
        else:
            print("\n \n \n")
            print("Some of the downloaded GTFS files are error prone and steps need to be taken for this.")
            print("For extra information regarding the files with error and when they were downloaded check the log file GTFS_error_log.txt")
            print("Open the file GTFS_metadata.txt")
            cnt = 1
            for k,v in Validation.graph_size_dict.items():
                print(k[1])
                if(v == 0):
                    c_name = k[0]
                    f_name = k[1].split("/")[-1]
                    print("\n \n \n")
                    print("The errror file is: ",f_name)
                    print()
                    print(f_name+" belong to path: current/"+c_name+"/"+f_name+"/"+f_name+".zip")
                    print()
                    print("STEP-1.1 = Go to the following web address: https://transitfeeds.com/p/"+k[1])
                    print()
                    print("STEP-1.2 = Open the file GTFS_metadata.txt and look at the last_modified date of file with error")
                    print()
                    print("STEP-1.3 = Download the file before latest date and keep going down chronologically with every iteration,save it to the path mentioned before and enter any key to continue")
                    print("Download a different GTFS file everytime from the web address given above. This is to be done in order to download the latest gtfs file with no errors.")
                    print()
                    print("STEP-1.4 = After the new downloaded GTFS file is saved to the respective folder PRESS ENTER")
                    print()
                    print("Keep following the promt until you get the message that files are good and up to date.")

                    input("PRESS ENTER TO CONTINUE:")
        Folder_management.copy_content_from_new_to_old("county_names","old_county_names")



if __name__ == "__main__":
    main()
