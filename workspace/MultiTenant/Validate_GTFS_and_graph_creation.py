#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

import shutil, os
import subprocess
import glob
from MultiTenant.Primer import File_Management
from MultiTenant.set_env_var import Env
from MultiTenant.Download_GTFS_data import Meta_Error_Info

class Validate_GTFS:
    Env_var = Env()
    Folder_management   = File_Management("county_names","old_county_names")
    Metadata_and_error  = Meta_Error_Info(Env_var.get_env("log_files"))

    def __init__(self):
        self.otp_graph_build     = self.Env_var.get_env("otp_graph_build_cmd")
        self.graph_creation_dest = "graph_creation"
        self.OTP_server_path     = "otp"
        self.GTFS_val_folder     = "current"
        self.GTFS_previous_path  = "previous"
        self.graph_size_dict     = {}
        self.counties            = self.Folder_management.counties

    def graph_builder_individual_gtfs(self,graph_build_top_folder,router,agency_feed_id=""):
        if(len(agency_feed_id) != 0):
            source_path = self.Folder_management.get_path(graph_build_top_folder,router,agency_feed_id.split("/")[0])+"/"
        else:
            source_path = self.Folder_management.get_path(graph_build_top_folder,router)+"/"

        self.Folder_management.run_shell_command([self.otp_graph_build,source_path])
        graph_size = os.stat(source_path+'Graph.obj').st_size
        self.Folder_management.run_shell_command(["rm",source_path+"Graph.obj"])
        return graph_size


    def check_individual_gtfs(self,router_data = None):
        if router_data is None:
            router_data = self.counties
        for county,agency_feed_names in router_data.items():
            for agency_feed_id in agency_feed_names:
                graph_s = self.graph_builder_individual_gtfs("current",county,agency_feed_id)
                path_to_validated_gtfs = self.Folder_management.get_path("current",county,agency_feed_id.split("/")[0],agency_feed_id.split("/")[0] + ".zip")
                self.graph_size_dict[(county,path_to_validated_gtfs)] = graph_s


    def replace_error_gtfs_feeds_with_previous_feeds(self):
        f_name = "Latest_download_program_metadata.txt"
        copy = "cp "
        message = []
        message.append("-> REPLACING ERRORED GTFS FEEDS WITH OLDER WORKING GTFS FEEDS"+"\n")
        for k,v in self.graph_size_dict.items():
            if(v == 0):
                router = k[0]
                f_name = k[1].split("/")[-1]
                source = self.Folder_management.get_path(self.GTFS_previous_path,router,f_name)
                dest = self.Folder_management.get_path(self.GTFS_val_folder,router,f_name.split(".")[0],f_name)
                final_cmd = copy+source+dest
                self.Folder_management.run_shell_command([copy,source,dest])
                message.append("- "+f_name+" was successfully copied from "+source+" to "+dest+" because the latest downloaded file had errors in it."+"\n")
        message.append("\n \n")
        self.Metadata_and_error.program_metadata(message,f_name)


    def copy_current_to_previous_feeds(self,initial = False,router_data = None):
        if router_data is None:
            router_data = self.counties
        f_name = ""
        if(initial == True):
            f_name = "initial_download_program_metadata.txt"
        else:
            f_name = "Latest_download_program_metadata.txt"
        copy = "cp "
        message = []
        message.append("-> COPYING ALL WORKING GTFS FROM Folder 'current' TO Folder 'previous' FOR FUTURE REFERENCES"+"\n")
        for router,agency_feed_names in router_data.items():
            for agency_feed_id in agency_feed_names:
                source = self.Folder_management.get_path(self.GTFS_val_folder,router,agency_feed_id.split("/")[0],agency_feed_id.split("/")[0] + ".zip")
                dest = self.Folder_management.get_path(self.GTFS_previous_path,router,agency_feed_id.split("/")[0] + ".zip")
                final_cmd = copy + source + dest
                self.Folder_management.run_shell_command([copy,source,dest])
                message.append("- Copying GTFS file "+agency_feed_id.split("/")[0]+" from 'current' to 'previous'. "+"\n")
        message.append("\n \n")
        self.Metadata_and_error.program_metadata(message,f_name)


    def check_no_errors(self):
        for k,v in self.graph_size_dict.items():
            if(v == 0):
                return False
        return True


    def final_graph_creation(self,router_data = None):
        if router_data is None:
            router_data = self.counties
        f_name = "Latest_download_program_metadata.txt"
        copy = "cp "
        message = []
        message.append("-> CREATING NEW GRAPHS FOR ALL PRESENT ROUTERS WITH LATEST GTFS"+"\n")
        for router in router_data.keys():
            source_osm_elev = self.Folder_management.get_path(self.OTP_server_path,router)+"/*"
            dest_osm_elev   = self.Folder_management.get_path(self.graph_creation_dest,router)+"/"
            self.Folder_management.run_shell_command([copy,"-R",source_osm_elev,dest_osm_elev])

            source_gtfs = self.Folder_management.get_path(self.GTFS_previous_path,router)+"/*"
            dest_gtfs   = self.Folder_management.get_path(self.graph_creation_dest,router)+"/"
            self.Folder_management.run_shell_command([copy,"-R",source_gtfs,dest_gtfs])

            graph_for_router_dir = self.Folder_management.get_path(self.graph_creation_dest,router)+"/"
            self.Folder_management.run_shell_command([self.otp_graph_build,graph_for_router_dir])
            message.append("- The graph.obj object of router/county: "+router+" was created."+"\n")
        message.append("\n \n")
        self.Metadata_and_error.program_metadata(message,f_name)


    def copy_created_graph_gtfs_to_router_directory(self,router_data = None):
        if router_data is None:
            router_data = self.counties
        f_name = "Latest_download_program_metadata.txt"
        message = []
        message.append("-> COPYING CREATED INDIVIDUAL GRAPHS,GTFS data TO THE RESPECTIVE 'otp/router/' DIRECTORY")
        cnt_r = 1
        move = "mv "
        for router in router_data.keys():
            source = self.Folder_management.get_path(self.graph_creation_dest,router)+"/"
            dest = self.Folder_management.get_path(self.OTP_server_path,router)+"/"
            gtfs_f_names = [f for f in os.listdir(source) if f.endswith('.zip')]
            graph_f_name = [f for f in os.listdir(source) if f.endswith('.obj')]
            file_names_to_be_copied = gtfs_f_names+graph_f_name
            message.append(str(cnt_r)+".) "+" Copying files for router/county: "+router+"\n")
            cnt_r += 1
            source_folder = source + "*"
            self.Folder_management.run_shell_command([move,"-v ",source_folder,dest])
            for file_name in file_names_to_be_copied:
                message.append("- Moved file: "+file_name+" from folder 'graph_creation' to respective otp server router 'otp/router'."+"\n")
        message.append("\n \n")
        self.Metadata_and_error.program_metadata(message,f_name)
