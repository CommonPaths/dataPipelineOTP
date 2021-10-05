#!/bin/sh
cp -RT ${code_deploy_artifacts}workspace/MultiTenant ${workspace}MultiTenant;
cp ${code_deploy_artifacts}workspace/after_install_script.sh ${workspace}after_install_script.sh;
cp ${code_deploy_artifacts}workspace/fetch_osm_create_graph_existing.py ${workspace}fetch_osm_create_graph_existing.py;
cp ${code_deploy_artifacts}workspace/fetch_osm_create_graph_new.py ${workspace}fetch_osm_create_graph_new.py;
cp ${code_deploy_artifacts}workspace/initial_download.py ${workspace}initial_download.py;
cp ${code_deploy_artifacts}workspace/multi-tenant-otp-server.sh ${workspace}multi-tenant-otp-server.sh;
rm -rf ${code_deploy_artifacts}