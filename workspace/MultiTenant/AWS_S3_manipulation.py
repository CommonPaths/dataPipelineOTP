#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

import boto3
import json
import ast
import datetime
from MultiTenant.set_env_var import Env

class S3_Bucket_manipulation:

    def __init__(self):
        Env_var = Env()
        self.status_data = {
            "status": "",
            "username": "",
            "last_updated": ""
        }
        self.status_file_name = Env_var.get_env("status_file")
        self.bucket           = Env_var.get_env("S3_bucket_name")

    def s3_create_dir(self,updated_routers):
        s3 = boto3.client('s3')
        for tenant_name in updated_routers.keys():
            bucket_name = self.bucket
            directory_name = tenant_name
            s3.put_object(Bucket=bucket_name, Key=(directory_name+'/'))

    def s3_delete_dir(self,outdated_routers):
        s3 = boto3.resource('s3')
        for tenant_name in outdated_routers.keys():
            bucket = s3.Bucket(self.bucket)
            dir_name = tenant_name+'/'
            for obj in bucket.objects.filter(Prefix=dir_name):
                s3.Object(bucket.name,obj.key).delete()

    def s3_write_status(self,tenant_name,status,username):
        try:
            #The try code block will run if there is a previous status in the S3 bucket
            #Read current status file from s3 bucket if it is there
            s3 = boto3.resource('s3')
            dir_name = tenant_name+'/'+self.status_file_name
            read_obj = s3.Object(self.bucket,dir_name)
            current_status = read_obj.get()['Body'].read()
            current_status_dict_str = current_status.decode("UTF-8")
            current_status_dict = ast.literal_eval(current_status_dict_str)

            #Update status file with updated flags
            current_time = str(datetime.datetime.utcnow())
            current_status_dict["status"] = status
            current_status_dict["username"] = username
            current_status_dict["last_updated"] = current_time
            write_obj = s3.Object(self.bucket,dir_name)
            write_obj.put(Body=json.dumps(current_status_dict))
        except:
            s3 = boto3.resource('s3')
            dir_name = tenant_name+'/'+self.status_file_name

            #Put the status file with given format with the most recent update flags
            current_time = str(datetime.datetime.utcnow())
            self.status_data["status"] = status
            self.status_data["username"] = username
            self.status_data["last_updated"] = current_time
            write_obj = s3.Object(self.bucket,dir_name)
            write_obj.put(Body=json.dumps(self.status_data))
