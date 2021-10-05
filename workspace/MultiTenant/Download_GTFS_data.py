#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
###############################################################################

from MultiTenant.set_env_var import Env
from MultiTenant.Primer import File_Management
import requests
import datetime
import os

class Download:

    Env_var = Env()
    Folder_management = File_Management("county_names","old_county_names")

    def __init__(self):
        self.GTFS_feeds_path      = self.Env_var.get_env("GTFS_feeds")
        self.log_files_path       = self.Env_var.get_env("log_files")
        self.API_KEY              = self.Env_var.get_env("API_KEY")
        self.counties             = self.Folder_management.get_counties_data()
        self.base_download_folder = "current"
        self.download_date        = ""
        self.last_modified        = ""


    def download_latest_GTFS_feeds(self,chunk_size = 128,router_data = None):
        if router_data is None:
            router_data = self.counties
        Metadata_and_error = Meta_Error_Info(self.log_files_path)
        for county,agency_feed_names in router_data.items():
            for agency_feed_id in agency_feed_names:
                base_url = self.Env_var.get_env("transitfeed_url")
                url = base_url.replace("your-api-key",self.API_KEY)
                url = url.replace("transit-id",agency_feed_id)
                save_path = self.Folder_management.get_path(self.base_download_folder,county,agency_feed_id.split("/")[0],agency_feed_id.split("/")[0] + ".zip")
                r = requests.get(url)
                self.download_date = r.headers.get("Date","Not specified")
                self.last_modified = r.headers.get("Last-Modified","Not Specified")
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                Metadata_and_error.write_download_metadata(self.download_date,self.last_modified,agency_feed_id)
        return (self.download_date,self.last_modified)


class Meta_Error_Info:

    def __init__(self,log_files_path):
        self.current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%A, %d %b %Y %H:%M:%S")+" "+"GMT"
        self.log_files_path = log_files_path
        self.gtfs_meta = open(log_files_path+"GTFS_metadata.txt", "w")
        self.gtfs_meta.close()

        self.program_meta = open(log_files_path+"Latest_download_program_metadata.txt", "w")
        self.program_meta.writelines("The following information is for date: "+self.current_time+"\n")
        self.program_meta.writelines("\n")
        self.program_meta.writelines("\n")
        self.program_meta.close()


    def write_download_metadata(self,download_time,update_time,agency_feed_id):
        gtfs_m = open(self.log_files_path+"GTFS_metadata.txt", "a")
        gtfs_m.writelines("File downloaded as "+ agency_feed_id.split("/")[0] + ".zip"+"\n")
        gtfs_m.writelines("File downloaded at: "+download_time+"\n")
        gtfs_m.writelines("File last_modified on source at: "+update_time+"\n")
        gtfs_m.writelines("\n")
        gtfs_m.writelines("\n")
        gtfs_m.writelines("\n")
        gtfs_m.close()

    def gtfs_error_log(self,graph_size_dict,download_time,update_time):
        gtfs_error = open(self.log_files_path +"GTFS_error_log.txt", "w")
        for k,v in graph_size_dict.items():
            if(v == 0):
                c_name = k[0]
                f_name = k[1].split("/")[-1]
                gtfs_error.writelines("router/county name: "+c_name+"\n")
                gtfs_error.writelines("-> The GTFS file "+f_name+" has unknown errors and is inhibiting graph building process. "+"\n")
                gtfs_error.writelines("-> The GTFS file "+f_name+" was downloaded into MVT_OTP server on "+download_time+" "+"\n")
                gtfs_error.writelines("-> File last modified on source at: "+update_time+"\n")
                gtfs_error.writelines("-> For more info about when "+f_name+" was downloaded and its last update, refer to GTFS_metadata.txt "+"\n")
                gtfs_error.writelines("\n")
                gtfs_error.writelines("\n")
                gtfs_error.writelines("\n")
        gtfs_error.close()

    def program_metadata(self,message,f_name):
        program_m = open(self.log_files_path+f_name, "a")
        for msg in message:
            program_m.writelines(msg+"\n")
            program_m.writelines("\n")
        program_m.close()

    def current_status(self,counties):
        current_status = open(self.log_files_path+"current_status.txt", "w")
        current_status.writelines("The current run of software on date: "+self.current_time+", works on the following things: ")
        current_status.writelines("\n")
        current_status.writelines("\n")
        cnt_r = 1
        for county,agency_feed_names in counties.items():
            current_status.writelines(str(cnt_r)+".) "+"county/router name: "+county)
            current_status.writelines("\n")
            cnt_r += 1
            for agency_feed_id in agency_feed_names:
                current_status.writelines("-> Agency for current county/router: "+agency_feed_id.split("/")[0]+" "+"\n")
            current_status.writelines("\n")
            current_status.writelines("\n")
        current_status.close()
