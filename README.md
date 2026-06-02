# Local Enterprise Data Lake Architecture (Fedora Linux)

This repository tracks the configuration, deployment, and testing pipelines for a production-grade local data lake. The architecture decouples storage and compute by running a bare-metal distributed object storage layer managed by systemd, alongside an isolated Python virtual environment executing PySpark pipelines.

---

## Architecture Overview

* **Storage Layer:** MinIO Object Storage (Native Linux Binary running as a system daemon)
* **Compute Engine:** Apache Spark / PySpark 3.x
* **Execution Environment:** Isolated Python 3 Virtual Environment (`pyspark_env`)
* **Runtime Dependency:** OpenJDK 21 (Java Virtual Machine backend)
* **Storage Pool:** Local 500GB NVMe/HDD storage mounted at `/mnt/minio_data`

---

## Phase 1: Storage Layer Configuration (MinIO Native)

### 1. System Directories & Security Boundary
MinIO is executed via an isolated system user with no interactive login shells for host security.

* **Binary Path:** `/usr/local/bin/minio`
* **Data Directory:** `/mnt/minio_data` (Owned exclusively by `minio-user:minio-user`)
* **Configuration Profile:** `/etc/default/minio`
* **Systemd Service Definition:** `/etc/systemd/system/minio.service'


## Phase 2: Compute Layer Configuration (PySpark)

### 1. Java Installation
```bash
# Install the exact Java 21 backend required by Spark on Fedora
sudo dnf install java-21-openjdk-devel -y
-----

### 2. Python Virtual Environment Setup
'''bash
# Install the core Python virtual environment package if missing
sudo dnf install python3-venv -y

# Create the clean environment wrapper
python3 -m venv pyspark_env

# Hot-reload and activate it
source pyspark_env/bin/activate


## 2. Core Linux Service Commands
Use these standard systemd utilities to manage the object storage daemon:

```bash
# Upgrade the package manager and install the engine components
pip install --upgrade pip
pip install pyspark jupyterlab


# Check service health and runtime logs
sudo systemctl status minio

# Start, stop, or restart the storage server
sudo systemctl start minio
sudo systemctl stop minio
sudo systemctl restart minio

# View live systemd journal logs for debugging
sudo journalctl -u minio.service -f

3. Network & Firewall Topology
Fedora blocks ingress traffic by default. The following rules expose the S3 API and the administrator web console to your local network:

Bash
sudo firewall-cmd --add-port=9000/tcp --permanent  # S3 API Port
sudo firewall-cmd --add-port=9001/tcp --permanent  # Web Console Port
sudo firewall-cmd --reload
