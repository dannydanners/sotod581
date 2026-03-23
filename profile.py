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
cd /local/repository || exit 1
sudo bash install_docker.sh > /tmp/install_docker.log 2>&1
sudo docker compose up -d > /tmp/compose_up.log 2>&1
"""
))

pc.printRequestRSpec(request)
