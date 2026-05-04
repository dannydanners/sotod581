import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()

pc.defineParameter(
    "gh_pat",
    "GitHub PAT",
    portal.ParameterType.STRING,
    ""
)

pc.defineParameter(
    "gh_owner",
    "GitHub owner",
    portal.ParameterType.STRING,
    "",
)

pc.defineParameter(
    "gh_repo",
    "GitHub Repo",
    portal.ParameterType.STRING,
    "",
)

params = pc.bindParameters()
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

node = request.XenVM("docker")
node.cores = 4
node.ram = 8
node.routable_control_ip = "true" 
  
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"
node.routable_control_ip = "true"
node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/cloudlab/bootstrap.sh"))

pc.printRequestRSpec(request)
