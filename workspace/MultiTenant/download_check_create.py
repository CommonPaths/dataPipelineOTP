#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

from MultiTenant.Validate_GTFS_and_graph_creation import Validate_GTFS
from MultiTenant.Download_GTFS_data import Download,Meta_Error_Info
from MultiTenant.Primer import File_Management

class create_and_transfer:
    Folder_management = File_Management("county_names","old_county_names")

    Folder_management.create_folders()

    Validation     = Validate_GTFS()
    GTFS_feed_manipulation     = Download()
    Metadata_and_error = Meta_Error_Info(GTFS_feed_manipulation.log_files_path)

    def __init__(self,required_tenant_data = None):
        self.gtfs_quality_flag = True
        if required_tenant_data is None:
            self.router_data = self.Folder_management.get_counties_data()
        else:
            self.router_data = required_tenant_data

    def download_check_GTFS(self):
        self.Metadata_and_error.current_status(self.router_data)
        download_time,update_time = self.GTFS_feed_manipulation.download_latest_GTFS_feeds(self.router_data)
        self.Validation.check_individual_gtfs(self.router_data)
        self.Metadata_and_error.gtfs_error_log(self.Validation.graph_size_dict,download_time,update_time)
        self.gtfs_quality_flag = self.Validation.check_no_errors()

    def create_graph_and_transfer(self):
        if(self.gtfs_quality_flag == False):
            self.Validation.replace_error_gtfs_feeds_with_previous_feeds()

            self.Validation.final_graph_creation(self.router_data)

            self.Validation.copy_current_to_previous_feeds(self.router_data)

            self.Validation.copy_created_graph_gtfs_to_router_directory(self.router_data)
        else:
            self.Validation.final_graph_creation(self.router_data)

            self.Validation.copy_current_to_previous_feeds(self.router_data)

            self.Validation.copy_created_graph_gtfs_to_router_directory(self.router_data)
