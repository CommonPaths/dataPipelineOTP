#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

#import set_env_var
from MultiTenant.set_env_var import Env
import shutil, os
import json

class File_Management:
    env_var = Env()

    def __init__(self,counties,old_counties):
        with open(self.env_var.get_env(counties)) as json_file:
            self.counties = json.load(json_file)
        with open(self.env_var.get_env(old_counties)) as json_file:
            self.old_counties = json.load(json_file)



    def create_sub_folders_in_current(self,county_name):
        for feed in self.counties[county_name]:
            feed_name = feed.split("/")[0]
            if not os.path.exists(self.env_var.get_env("current")+county_name+"/"+feed_name):
                os.makedirs(self.env_var.get_env("current")+county_name+"/"+feed_name)


    def create_folders(self,router_data = None):
        flag = False
        if router_data is None:
            router_data = self.counties
            flag = True
        for name in router_data.keys():
            if(flag == True):
                if not os.path.exists(self.env_var.get_env("current")+name):
                    os.makedirs(self.env_var.get_env("current")+name)
                    self.create_sub_folders_in_current(name)
            else:
                if not os.path.exists(self.env_var.get_env("current")+name):
                    os.makedirs(self.env_var.get_env("current")+name)
                    self.create_sub_folders_in_current(name)
                else:
                    self.create_sub_folders_in_current(name)
            if not os.path.exists(self.env_var.get_env("previous")+name):
                os.makedirs(self.env_var.get_env("previous")+name)
            if not os.path.exists(self.env_var.get_env("elevation")+name):
                os.makedirs(self.env_var.get_env("elevation")+name)
            if not os.path.exists(self.env_var.get_env("graph_creation")+name):
                os.makedirs(self.env_var.get_env("graph_creation")+name)
            if not os.path.exists(self.env_var.get_env("otp")+name):
                os.makedirs(self.env_var.get_env("otp")+name)

    def delete_outdated_folders_files(self,outdated_files):
        for county,agency_feed_names in outdated_files.items():
            if(len(agency_feed_names) == 0):
                delete_paths = []
                delete_paths.append(self.env_var.get_env("current")+county)
                delete_paths.append(self.env_var.get_env("previous")+county)
                delete_paths.append(self.env_var.get_env("elevation")+county)
                delete_paths.append(self.env_var.get_env("graph_creation")+county)
                delete_paths.append(self.env_var.get_env("otp")+county)
                for path in delete_paths:
                    try:
                        shutil.rmtree(path)
                    except OSError as e:
                        print("Error deleting directory: %s : %s" % (path, e.strerror))
            else:
                delete_paths = []
                for agency_feed_id in agency_feed_names:
                    current_folder_name = agency_feed_id.split("/")[0]
                    f_name = agency_feed_id.split("/")[0] + ".zip"
                    try:
                        shutil.rmtree(self.env_var.get_env("current")+county+"/"+current_folder_name)
                    except OSError as e:
                        print("Error deleting directory in current folder: %s : %s" % (path, e.strerror))
                    # delete_paths.append(self.env_var.get_env("current")+county+"/"+current_folder_name+"/"+f_name)
                    delete_paths.append(self.env_var.get_env("previous")+county+"/"+f_name)
                    delete_paths.append(self.env_var.get_env("graph_creation")+county+"/"+f_name)
                    delete_paths.append(self.env_var.get_env("otp")+county+"/"+f_name)
                    for path in delete_paths:
                        try:
                            os.unlink(path)
                        except OSError as e:
                            print("Error deleting files: %s : %s" % (path, e.strerror))

    def find_diff_in_json(self):
        updated_routers = {}
        remove_files    = {}
        new_counties = self.counties.keys() - self.old_counties.keys()
        delete_counties = self.old_counties.keys() - self.counties.keys()
        common_keys = set(self.counties.keys()).intersection(set(self.old_counties.keys()))
        while(bool(new_counties) == True):
            router_name = new_counties.pop()
            updated_routers[router_name] = self.counties[router_name]
        while(bool(delete_counties) == True):
            router_name = delete_counties.pop()
            remove_files[router_name] = []
        for router,agency_feed_names in self.old_counties.items():
            updated_agency_feed_names = self.counties.get(router,None)
            if(updated_agency_feed_names != None):
                if(updated_agency_feed_names != agency_feed_names):
                    updated_routers[router] = updated_agency_feed_names
        for key in common_keys:
            new_names = self.counties.get(key,[])
            old_names = self.old_counties.get(key,[])
            if(new_names != old_names):
                outdated_names = list(set(old_names).difference(set(new_names)))
                if(len(outdated_names) != 0):
                    remove_files[key] = outdated_names
        return updated_routers,remove_files

    def copy_content_from_new_to_old(self,counties,old_counties):
        with open(self.env_var.get_env(counties),"r") as new_data:
            with open(self.env_var.get_env(old_counties),"w") as old_data:
                for line in new_data:
                    old_data.writelines(line)

    def get_path(self,base,*args):
        base_path = self.env_var.get_env(base)
        for i in range(len(args)-1):
            base_path += args[i]+"/"
        final_path = base_path+args[-1]
        return final_path

    def get_counties_data(self):
        return self.counties

    def run_shell_command(self,string_list):
        final_cmd = ""
        for i in range(len(string_list)-1):
            final_cmd += string_list[i]+" "
        final_cmd += string_list[-1]
        os.system(final_cmd)
