"""Spawn a cluster and setup the networking, don't do anything else. You get bare metal machines."""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab
DISK_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU16-64-STD'
# Create a portal object,
pc = portal.Context()

pc.defineParameter("slaveCount", "Number of slave nodes",
                   portal.ParameterType.INTEGER, 1)
pc.defineParameter("osNodeTypeSlave", "Hardware Type for slaves",
                   portal.ParameterType.NODETYPE, "",
                   longDescription='''A specific hardware type to use for each
                   node. Cloudlab clusters all have machines of specific types.
                     When you set this field to a value that is a specific
                     hardware type, you will only be able to instantiate this
                     profile on clusters with machines of that type.
                     If unset, when you instantiate the profile, the resulting
                     experiment may have machines of any available type
                     allocated.''')
pc.defineParameter("osNodeTypeMaster", "Hardware Type for master",
                   portal.ParameterType.NODETYPE, "",
                   longDescription='''A specific hardware type to use for each
                   node. Cloudlab clusters all have machines of specific types.
                     When you set this field to a value that is a specific
                     hardware type, you will only be able to instantiate this
                     profile on clusters with machines of that type.
                     If unset, when you instantiate the profile, the resulting
                     experiment may have machines of any available type
                     allocated.''')
pc.defineParameter("publicIPSlaves", "Request public IP addresses for the slaves or not",
                   portal.ParameterType.BOOLEAN, True)


params = pc.bindParameters()


def create_request(request, role, ip, worker_num=None):
    if role == 'm':
        name = 'master'
    elif role == 's':
        name = 'worker{}'.format(worker_num)
    req = request.RawPC(name)
    if role == 'm':
        req.routable_control_ip = True
        if params.osNodeTypeMaster:
            req.hardware_type = params.osNodeTypeMaster
    elif role == 's':
        req.routable_control_ip = params.publicIPSlaves
        if params.osNodeTypeSlave:
            req.hardware_type = params.osNodeTypeSlave
    req.disk_image = DISK_IMG
    req.addService(pg.Execute(
        'bash',
        "sudo bash /local/repository/bootstrap.sh '{}' 2>&1 | sudo tee -a /local/logs/setup.log".format(
            role)))
    iface = req.addInterface(
        'eth1', pg.IPv4Address(ip, '255.255.255.0'))
    return iface


# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Link link-0
link_0 = request.LAN('link-0')
link_0.Site('undefined')

# Master Node
iface = create_request(request, 'm', '10.10.1.1')
link_0.addInterface(iface)

# Slave Nodes
for i in range(params.slaveCount):
    iface = create_request(
        request, 's', '10.10.1.{}'.format(i + 2), worker_num=i)
    link_0.addInterface(iface)


# Print the generated rspec
pc.printRequestRSpec(request)
