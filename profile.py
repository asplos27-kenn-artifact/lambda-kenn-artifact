r"""
\lambda_{\text{Ken-n}} Framework Artifact Evaluation Testbed (ASPLOS 2027)

ARCHIVAL PROTOCOL:
This profile securely fetches the purely functional extraction functor and physical bare-metal payload (.tar.gz) 
exclusively from the anonymous GitHub repository. It is strictly configured to physically enforce the empirical 
claims established in the evaluation.

STRATEGIC PIVOT (AI/ML WORKLOADS):
Transitioning to a distributed 10-node GPU-enabled bare-metal cluster (CloudLab Wisconsin d7525) is now 
required to pivot this compiler to AI/ML workloads. This allows us to evaluate memory footprint determinism 
and Layer-4 data-routing bottlenecks across concurrent, physical GPU-host boundaries, mathematically proving 
that our eBPF extraction compiler protects expensive AI interconnects (NVLink and GPUDirect RDMA) from 
volumetric saturation to achieve Zero-Waste Distributed AI.

Instructions for the Evaluator:
Once your CloudLab experiment turns green and all 10 nodes are active:
1. Do NOT manually SSH into the nodes to orchestrate the deployment. 
2. Execute the mathematically sterile `run_experiment.sh` script provided in the repository from your local terminal.
3. The script will dynamically orchestrate the hardware binding (Layer-4 eBPF / Layer-7 Wasm) and the rigorous statistical benchmark natively in Ring-0.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()
request = pc.makeRequestRSpec()

num_nodes = 10

tour_description = r"""
### \lambda_{\text{Ken-n}} Framework Evaluation Testbed: AI/ML Edition (ASPLOS 2027)
This profile provisions an Ubuntu 24.04 LTS bare-metal cluster on AMD EPYC d7525 nodes with strictly 
isolated kernel 6.8 support, pre-configured for hardware-bound eBPF XDP socket acceleration, WebAssembly 
sidecar proxy deployment, and GPUDirect RDMA lane protection. It is specifically designed to bypass the orchestration overhead and evaluate AI/ML Ring-AllReduce topologies.
"""

lan = rspec.LAN("nodelan")
lan.bandwidth = 100000  # 100 Gbps Mellanox ConnectX-6 required for physical wire-speed saturation and GPUDirect RDMA

for i in range(num_nodes):
    node = request.RawPC("node-{}".format(i))
    
    # SILICON PIVOT: Ampere Architecture for Zero-Waste Distributed AI
    # CloudLab Wisconsin d7525 (Dual 16-core AMD EPYC 7302, 128 GB RAM, discrete NVIDIA PCIe GPUs)
    # Physical Systems Reality: Virtualization is strictly prohibited as it falls back to xdpgeneric,
    # physically invalidating the 142 CPU cycle execution claim and failing to expose PCIe topology.
    node.hardware_type = "d7525"
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD"

    iface = node.addInterface("if{}".format(i))
    iface.addAddress(rspec.IPv4Address("192.168.1.{}".format(10 + i), "255.255.255.0"))
    lan.addInterface(iface)

    # SECURE INGESTION: Pulling directly from the anonymous GitHub artifact root via native git clone.
    # Enforces strict apt-lock polling to prevent race conditions during distributed boot.
    # Extracts the payload preserving the `lambda-kenn-artifact` internal directory structure.
    setup_command = (
        "while sudo fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do sleep 5; done; "
        "while sudo fuser /var/lib/apt/lists/lock >/dev/null 2>&1; do sleep 5; done; "
        "sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git tar curl && "
        "sudo mkdir -p /local/repository && "
        "sudo git clone https://github.com/asplos27-kenn-artifact/lambda-kenn-artifact.git /local/repository/lambda-kenn-artifact && "
        "if [ -f /local/repository/lambda-kenn-artifact/lambda-kenn-artifact.tar.gz ]; then "
        "  sudo tar -xzvf /local/repository/lambda-kenn-artifact/lambda-kenn-artifact.tar.gz -C /local/repository/; "
        "fi && "
        "sudo chown -R sysres:distsysperfeval- /local/repository/lambda-kenn-artifact && "
        "sudo bash /local/repository/lambda-kenn-artifact/scripts/01-setup.sh > /local/setup.log 2>&1"
    )

    node.addService(rspec.Execute(shell="sh", command=setup_command))

pc.printRequestRSpec(request)
