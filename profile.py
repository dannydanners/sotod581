import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = \
"""
This profile provides the template for a compute node with Docker installed on Ubuntu 22.04
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT, tourDescription)
request.addTour(tour)

node = request.XenVM("sharks")
node.cores = 8
node.ram = 16
node.routable_control_ip = "true" 

bs_landing = node.Blockstore("bs_image", "/image")
bs_landing.size = "500GB"
  
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"
node.routable_control_ip = "true"
node.addService(pg.Execute(
    shell="/bin/bash",
    command="""
set -eux
until [ -d /local/repository ]; do
  echo "Waiting for repository..."
  sleep 2
done

until [ -d /local/repository/apps/node_project ]; do
  echo "Waiting for repository..."
  sleep 2
done

cd /local/repository

while sudo lsof /var/lib/dpkg/lock >/dev/null 2>&1; do
  echo "Waiting for dpkg lock..."
  sleep 2
done

sudo bash install_docker.sh > /tmp/install_docker.log 2>&1

until command -v docker >/dev/null 2>&1; do
  echo "Waiting for docker..."
  sleep 2
done

until sudo docker info >/dev/null 2>&1; do
  echo "Waiting for docker daemon..."
  sleep 2
done

until docker compose version >/dev/null 2>&1; do
  echo "Waiting for docker compose..."
  sleep 2
done

sudo docker compose up -d > /tmp/compose_up.log 2>&1
"""
))

pc.printRequestRSpec(request)
