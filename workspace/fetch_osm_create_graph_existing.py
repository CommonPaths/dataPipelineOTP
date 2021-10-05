import os
import json
import re
import datetime
import argparse
from MultiTenant.set_env_var import Env
from MultiTenant.download_check_create import create_and_transfer
from MultiTenant.AWS_S3_manipulation import S3_Bucket_manipulation

def main(graph_update_county_name,username):
    Env_var = Env()
    S3_manipulation = S3_Bucket_manipulation()
    router_to_update = dict()

    with open(Env_var.get_env("county_names")) as json_file:
        county = json.load(json_file)

    with open(Env_var.get_env("osm_db_config")) as json_file:
        osm_db_config = json.load(json_file)

    if(graph_update_county_name == "all_counties"):
        router_to_update = county
    else:
        for county_name,agency_gtfs_feed_names in county.items():
            if(county_name == graph_update_county_name):
                router_to_update[county_name] = agency_gtfs_feed_names

    graph_gen_and_transfer = create_and_transfer(router_to_update)

    pattern = re.compile(".*id=*")
    osm_download = open(Env_var.get_env("log_files") +"OSM_download_meta.txt", "w")

    for k in router_to_update.keys():
        HOSTNAME   = osm_db_config[k]["HOSTNAME"]
        DATABASE   = osm_db_config[k]["DATABASE"]
        USERNAME   = osm_db_config[k]["USERNAME"]
        PASSWORD   = osm_db_config[k]["PASSWORD"]
        osmosis    = Env_var.get_env("osmosis")
        if(graph_update_county_name == "all_counties"):
            os.system(osmosis + " --read-apidb-change host="+HOSTNAME+" database="+DATABASE+" user="+USERNAME+" password="+PASSWORD+" \
                                validateSchemaVersion=no readFullHistory=no intervalBegin=2020-10-19_10:10:10 \
                                --write-xml-change file="+Env_var.get_env("otp")+k+"/"+"daily_pr_osm.osc")
            with open(Env_var.get_env("otp")+k+"/"+"daily_pr_osm.osc") as myfile:
                if pattern.match(myfile.read()):
                    S3_manipulation.s3_write_status(k,"executing",username)
                    os.system(osmosis + " --read-apidb host="+HOSTNAME+" database="+DATABASE+" user="+USERNAME+" password="+PASSWORD+" \
                                        validateSchemaVersion=no \
                                        --write-xml file="+Env_var.get_env("otp")+k+"/"+"pr_osm_to_otp.osm")
                    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%A, %d %b %Y %H:%M:%S")+" "+"GMT"
                    osm_download.writelines("OSM File with name "+k+".osm"+" downloaded at time: "+current_time+"\n")
                else:
                    S3_manipulation.s3_write_status(k,"executing",username)
                    print("INFO: No updates in the changeset file")
        else:
            S3_manipulation.s3_write_status(k,"executing",username)
            os.system(osmosis + " --read-apidb host="+HOSTNAME+" database="+DATABASE+" user="+USERNAME+" password="+PASSWORD+" \
                        validateSchemaVersion=no \
                        --write-xml file="+Env_var.get_env("otp")+k+"/"+"pr_osm_to_otp.osm")

            current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%A, %d %b %Y %H:%M:%S")+" "+"GMT"
            osm_download.writelines("OSM File with name "+k+".osm"+" downloaded at time: "+current_time+"\n")
    osm_download.close()
    graph_gen_and_transfer.download_check_GTFS()
    graph_gen_and_transfer.create_graph_and_transfer()
    if(graph_update_county_name != "all_counties"):
        S3_manipulation.s3_write_status(graph_update_county_name,"completed",username)
    else:
        for k in router_to_update.keys():
            S3_manipulation.s3_write_status(k,"completed",username)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--tenant", type=str, default="all_counties", help="The name of the router/tenant/county whose Graph object has to be regenerated. \
                                                                            NOTE: It should be the same as specified in /workspace/config_files/county_names.json")
    ap.add_argument("-u", "--username", type=str, default="System_regular_update", help="Username of the person updating the OTP Graph manually from the front end.")

    args = vars(ap.parse_args())
    graph_update_county_name = args["tenant"]
    username = args["username"]

    main(graph_update_county_name,username)
