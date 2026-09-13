# $\lambda_{\text{Ken-n}}$ Artifact Evaluation Package: Bare-Metal Extraction & Hardware Bounding

**Target Venue:** ASPLOS 2027  
**Title:** Cutting the Data Center 'Guess-and-Check' Program Correctness Verification Cost with Formal Verification: The $\lambda_{\text{Ken-n}}$ Framework  
**Architecture:** Bipartite Extraction to Bare-Metal Silicon (CloudLab Wisconsin `d7525`)  
**Repository:** `https://github.com/asplos27-kenn-artifact/lambda-kenn-artifact.git`

---

## 1. Architectural Foundation: Eradicating the Staging Thermal Cost

The explosive expansion of cloud-native AI workloads is precipitating a global data center energy crisis. A significant, yet largely unquantified, portion of this energy expenditure is the **'guess-and-check' program correctness verification cost**. We define the massive physical footprint of this epistemological failure as the **"staging thermal cost"**—the megawatts of redundant compute and cooling capacity dedicated exclusively to the empirical "guess-and-check" testing of microservice scaling policies. 

Transitioning to a distributed 10-node GPU-enabled bare-metal cluster (CloudLab Wisconsin d7525) is now required to pivot this compiler to AI/ML workloads. This allows us to evaluate memory footprint determinism and Layer-4 data-routing bottlenecks across concurrent, physical GPU-host boundaries, mathematically proving that our eBPF extraction compiler protects expensive AI interconnects (NVLink and GPUDirect RDMA) from volumetric saturation to achieve Zero-Waste Distributed AI.

The $\lambda_{\text{Ken-n}}$ framework applies the rigorous discipline of Denotational Design to distributed systems orchestration to physically eradicate this verification cost and its resulting thermal cost. We reject the empirical, inductive testing loops of traditional Site Reliability Engineering (SRE) and the monolithic, stateful complexity of multi-pass compilers, which inherently suffer from catastrophic $\mathcal{O}(2^N)$ state-space explosions.

In hyperscale distributed AI workloads, accelerators frequently sit idle (GPU starvation) waiting for collective communication primitives (e.g., Ring-AllReduce) to synchronize. By completely bypassing user-space orchestration overhead and kernel network stack traversal, this architecture drops out-of-bounds volumetric traffic directly at the native driver queue via `XDP_DROP`, protecting expensive host-GPU interconnects (NVLink and GPUDirect RDMA) from saturation and state exhaustion.

---

## 2. Reconciling the Semantic Gap: Bipartite Extraction

This artifact demonstrates a **Bipartite Verification Pipeline**:
1. **The Proof Phase (Cubical Agda):** The univalent type-checker natively models distributed microservices and gradient routing as continuous topological open sets. It proves arbitrary unions for horizontal elasticity and guarantees spatial memory bounds offline in strict $\mathcal{O}(1)$ time (averaging **0.226 seconds**).
2. **The Extraction Phase (Haskell, Clang, eBPF):** Because the computational state space is resolved upstream, the compiler does not require complex intermediate representations. It ingests the verified AST and applies an extraction functor ($\mathbb{L}^*$) to project verified bounds directly into physical deployment targets: Layer-4 eBPF C-code for kernel-level packet isolation and Layer-7 WebAssembly for temporal sequencing. Standard Linux utilities then physically compile and bind these artifacts to the bare-metal OS.

**The Theoretical Extraction vs. Practical Implementation:**
* *The Theoretical Model:* The extraction functor ($\mathbb{L}^*$) defines an F-Algebra fold that translates verified univalent continuous geometry into discrete execution domains.
* *The Systems Implementation:* To satisfy the stringent safety checks of the Linux eBPF verifier and avoid monolithic compiler complexity, the artifact uses a stateless Haskell generator (`Main.hs`) and standard Linux toolchains (`clang -target bpf`, `bpftool`). Verified capacity bounds are injected directly into static C-preprocessor macros (`#define MAX_CAPACITY`), producing hardened kernel objects that execute at wire speed.

---

## 3. Directory Tree & Architecture

The artifact boundary strictly bifurcates the evaluator's local orchestrator (**Control Plane**) from the remote bare-metal execution payload (**Data Plane**) to preserve SIGARCH double-blind integrity and maintain an explicit separation of concerns:

```text
asplos-anonymous-artifact/
├── profile.py                     # Control Plane (Provisions 10x d7525 nodes on CloudLab Wisconsin)
├── run_experiment.sh              # Control Plane (Executed from evaluator laptop)
├── README.md                      # Control Plane (AEC instructions & project guide)
└── lambda-kenn-artifact.tar.gz    # Data Plane Payload (Ingested autonomously by nodes)
    └── lambda-kenn-artifact/
        ├── Makefile               # Deterministic build automation (make reproduce-rigorous)
        ├── README.md              # Node-level execution documentation
        ├── model/                 # Declarative DSEL topology definitions
        │   ├── ai_ring_reduce.kenn# AI/ML gradient sync & tensor routing bounds
        │   └── ecommerce.kenn     # Microservice baseline validation topology
        ├── scripts/
        │   ├── 01-setup.sh        # Toolchain bootstrap & kernel telemetry unlock
        │   ├── 02-compile.sh      # Proof checking & lowering to eBPF/Wasm
        │   ├── 03-deploy.sh       # NIC auto-discovery & native XDP driver injection
        │   └── 04-benchmark.sh    # wrk2 120k RPS tensor saturation & Ring-0 telemetry
        ├── src/
        │   ├── Agda/              # Cubical Agda univalent mechanizations
        │   │   ├── Choreography.agda
        │   │   ├── LinearQueue.agda
        │   │   └── PathEquivalence.agda
        │   └── Compiler/          # Categorical extraction functor implementation (L*)
        │       └── Main.hs        # Generates static eBPF maps and Wasm bytecode
        └── vendor/                # Vendored dependencies (Offline Air-Gap)
            └── cubical-v0.7.0.tar.gz
```

---

## 4. Hardware Testbed Requirements (CRITICAL)

**Virtualization Warning:** This artifact **cannot** be evaluated inside Docker containers, Virtual Machines, or standard hypervisor-virtualized cloud instances (e.g., standard AWS EC2). Virtualization introduces hypervisor scheduling jitter and silently falls back to Generic XDP (`xdpgeneric`), invalidating the 142-cycle telemetry constraint and masking physical PCIe/GPU interconnect behavior.

* **CloudLab Target:** Wisconsin Cluster
* **Bare-Metal Silicon:** 10 physical bare-metal `d7525` nodes (Dell PowerEdge R7525, Dual 16-core AMD EPYC 7302 CPUs, 128 GB RAM, discrete NVIDIA PCIe GPU per node)
* **Network Fabric:** Dual-port Mellanox ConnectX 100 Gbps interfaces configured for native hardware-offloaded XDP (`mlx5_core` driver) and direct RDMA routing
* **Air-Gapped Toolchain:** Vendored `vendor/cubical-v0.7.0.tar.gz` is pre-packaged directly inside the payload to prevent remote Git/network timeouts and IPv4 lock race conditions during the Agda bootstrap phase.
* **Operating System:** Ubuntu 24.04 LTS pinned to Linux Kernel 6.8.0-generic

---

## 5. Supported Empirical Claims

Executing the automated evaluation suite via `run_experiment.sh` reproduces the following physical claims from **Section 7** of the ASPLOS manuscript across 10 independent trials:

1. **$\mathcal{O}(1)$ Verification:** Upstream continuous type-checking resolves geometric open-set bounds in strictly $\mathcal{O}(1)$ time (averaging **0.226 seconds**), mathematically bypassing the $\mathcal{O}(2^N)$ distributed state-space explosion.
2. **Execution Efficiency (CPU Amortization):** Native `XDP_DROP` directives, triggered by the mathematically derived `-E2BIG` threshold, execute volumetric rejection natively on the bare-metal NIC in precisely **~142 CPU cycles** ($\pm 1.5\%$ variance).
3. **Spatial Memory Flatline (0 OOMs):** Under a 120,000 RPS volumetric saturation barrage, the Layer-4 eBPF spatial map completely bypasses dynamic heap allocation, remaining statically locked in Kernel Space at exactly **87,168 bytes** with strictly **0 OOM panics**.
4. **DDoS Immunization (TCP Hang):** The Layer-4 drop entirely bypasses the Linux TCP stack, offloading exhaustion to the upstream client and inducing a deterministic **~86.4-second** TCP connection hang without degrading host performance.
5. **Statistical Rigor:** Telemetry harvested across 10 evaluation trials confirms latency and cycle variance remains strictly **$< 1.5\%$**.

---

## 6. Evaluation Workflow (AEC Quick Start)

The evaluation workflow operates entirely in zero-touch mode. Evaluators do not need to manually configure dependencies or push local payloads over SSH.

### Step 1: Provision CloudLab Cluster
1. Log into the CloudLab web console.
2. Select **Experiments** > **Start Experiment** > **Upload Profile**.
3. Upload the provided `profile.py` script.
4. Instantiate the profile using 10 bare-metal `d7525` nodes at the **Wisconsin** cluster.
5. Wait until all 10 nodes turn green in both the `Status` and `Startup` columns. During boot, the cluster autonomously clones the repository and extracts the execution harness to `/local/repository/lambda-kenn-artifact`.

### Step 2: Configure Orchestrator
1. Copy the SSH target string for `node-0` from the CloudLab dashboard (e.g., `sysres@clnodeXXX.wisconsin.cloudlab.us`).
2. Open `run_experiment.sh` on your local terminal and update the `CLOUDLAB_NODE` variable:
   ```bash
   CLOUDLAB_NODE="sysres@clnodeXXX.wisconsin.cloudlab.us"
   ```

### Step 3: Execute the Reproducibility Pipeline
Run the master evaluation script from your local workstation:

```bash
chmod +x run_experiment.sh
./run_experiment.sh
```

### Step 4: Validate Results
`run_experiment.sh` triggers `make reproduce-rigorous` remotely on `node-0`. The suite executes across 10 evaluation trials (300 seconds per trial, ~50 minutes total), queries hardware Performance Monitoring Counters (PMCs), extracts `bpftool` memory metrics, and downloads all evaluation logs (`artifact_evaluation_*.log`, `rigorous_evaluation_*.log`) directly to your local machine for verification.
