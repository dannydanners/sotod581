import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()
# Create a XenVM
node = request.XenVM("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"
node.routable_control_ip = "true"

node.addService(rspec.Execute(
    shell="/bin/sh",
    command="""
    sudo apt update
    sudo apt install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
    Types: deb
    URIs: https://download.docker.com/linux/ubuntu
    Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
    Components: stable
    Signed-By: /etc/apt/keyrings/docker.asc
    EOF

    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    sudo systemctl enable docker
    sudo systemctl start docker

    sudo docker version
    sudo docker compose version

    cd /local/repository
    sudo docker compose up -d
    """
    ))
#node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y apache2"))
#node.addService(rspec.Execute(shell="/bin/sh", command='sudo systemctl status apache2'))
#node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y curl"))
#node.addService(rspec.Execute(shell="/bin/sh", command='curl -fsSL https://get.docker.com -o get-docker.sh'))
#node.addService(rspec.Execute(shell="/bin/sh", command='sudo sh get-docker.sh'))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
