import os
import json
import re
import datetime
from MultiTenant.set_env_var import Env
from MultiTenant.download_check_create import create_and_transfer

def main():
    Env_var = Env()

    with open(Env_var.get_env("osm_db_config")) as json_file:
        osm_db_config = json.load(json_file)

    with open(Env_var.get_env("new_router_names")) as json_file:
        new_routers = json.load(json_file)

    graph_gen_and_transfer = create_and_transfer(new_routers)         

    osm_download = open(Env_var.get_env("log_files") +"OSM_download_meta.txt", "w")
    for k in new_routers.keys():
        HOSTNAME   = osm_db_config[k]["HOSTNAME"]
        DATABASE   = osm_db_config[k]["DATABASE"]
        USERNAME   = osm_db_config[k]["USERNAME"]
        PASSWORD   = osm_db_config[k]["PASSWORD"]
        osmosis    = Env_var.get_env("osmosis")
        os.system(osmosis + " --read-apidb host="+HOSTNAME+" database="+DATABASE+" user="+USERNAME+" password="+PASSWORD+" \
                        validateSchemaVersion=no \
                        --write-xml file="+Env_var.get_env("otp")+k+"/"+"pr_osm_to_otp.osm")

        current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%A, %d %b %Y %H:%M:%S")+" "+"GMT"
        osm_download.writelines("OSM File with name "+k+".osm"+" downloaded at time: "+current_time+"\n")
    osm_download.close()
    graph_gen_and_transfer.download_check_GTFS()
    graph_gen_and_transfer.create_graph_and_transfer()

if __name__ == "__main__":
    main()
