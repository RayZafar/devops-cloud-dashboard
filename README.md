# DevOps & Cloud Monitoring Dashboard

This project is a **barebones** cloud monitoring dashboard using **Flask**, **Prometheus**, **Node Exporter**, and **Grafana**. It allows monitoring of system metrics and a sample Flask application.

## **Connecting to Your Ubuntu-Based EC2 Instance**

### **Ensure Your EC2 Instance is Running**

Before connecting, your EC2 instance must be **running**. If it's stopped, go to the **AWS EC2 Dashboard**, find your instance, and click **"Start Instance"**.

### **Connect via SSH**

Run the following command from your local machine:

```sh
ssh -i /path/to/your-key.pem ubuntu@your-ec2-ip
```

Replace `/path/to/your-key.pem` with the correct path to your **EC2 key pair**, and `your-ec2-ip` with the **public IP** of your instance.

## **Installation & Setup**

### **Ensure Security Group Allows Inbound Traffic**

Make sure your **AWS Security Group** has inbound rules allowing traffic for all necessary services:

- **Flask App:** Port `5000`
- **Prometheus:** Port `9090`
- **Grafana:** Port `3000`
- **Node Exporter:** Port `9100`

If these ports are blocked, you won’t be able to access the services from your browser.

### **One-Time Setup vs. Every Restart**

- **Steps 1, 2, and 3** are **only required the first time** you set up the project.
- **Step 4 must be repeated every time the EC2 instance is restarted** to bring the services back up.

### **1️⃣ Install Dependencies**

Run the following commands on your Ubuntu-based EC2 instance:

```sh
sudo apt update
sudo apt install -y python3 python3-pip
```

### **2️⃣ Clone the Repository**

```sh
git clone https://github.com/RayZafar/devops-cloud-dashboard.git
cd devops-cloud-dashboard
```

### **3️⃣ Install Flask & Prometheus Client**

```sh
pip3 install --break-system-packages flask prometheus_client
```

### **4️⃣ Start Services Manually**

#### **Start Flask App**

```sh
cd ~/devops-cloud-dashboard
nohup python3 app.py > /dev/null 2>&1 &
disown
```

✅ **Flask is now running in the background.**

#### **Start Node Exporter**

```sh
cd ~/node_exporter-*
nohup ./node_exporter > /dev/null 2>&1 &
disown
```

✅ **Node Exporter is running in the background.**

#### **Start Prometheus**

```sh
cd ~/prometheus-*
nohup ./prometheus --config.file=prometheus.yml > /dev/null 2>&1 &
disown
```

✅ **Prometheus is running in the background.**

#### **Start Grafana**

```sh
sudo systemctl start grafana-server
```

✅ **Grafana is running.**

### **5️⃣ Verify Everything is Running**

Run:

```sh
ps aux | grep -E "flask|node_exporter|prometheus"
sudo systemctl status grafana-server
```

✅ If all services are listed as running, your monitoring dashboard is live!

---

## **Accessing the Dashboard**

- **Flask App** → [http://your-ec2-ip:5000](http://your-ec2-ip:5000)
- **Prometheus UI** → [http://your-ec2-ip:9090](http://your-ec2-ip:9090)
- **Grafana UI** → [http://your-ec2-ip:3000](http://your-ec2-ip:3000)
  - Default **username/password**: `admin/admin`
- **Node Exporter Metrics** → [http://your-ec2-ip:9100/metrics](http://your-ec2-ip:9100/metrics)

---

## **Stopping Services Before Shutting Down the Instance**

To prevent issues when restarting the instance, it's recommended to manually stop the services before stopping the EC2 instance.
To prevent issues when restarting the instance, it's recommended to manually stop the services before stopping the EC2 instance.

#### **1️⃣ Stop Flask**

```sh
ps aux | grep python
sudo kill -9 <PID>  # Replace <PID> with the Flask process ID
```

#### **2️⃣ Stop Node Exporter**

```sh
ps aux | grep node_exporter
sudo kill -9 <PID>  # Replace <PID> with the Node Exporter process ID
```

#### **3️⃣ Stop Prometheus**

```sh
ps aux | grep prometheus
sudo kill -9 <PID>  # Replace <PID> with the Prometheus process ID
```

#### **4️⃣ Stop Grafana**

```sh
sudo systemctl stop grafana-server
```

Once all services are stopped, you can **safely stop the EC2 instance** from the AWS Console to avoid charges.

---

## **Future Plans: Automating the Setup**

In the future, I plan to **automate** running these services using Docker and `docker-compose`. Here’s a high-level approach to implement it:

### **1️⃣ Install Docker**

```sh
sudo apt update
sudo apt install -y docker.io docker-compose
```

### **2️⃣ Create a ********`docker-compose.yml`******** File**

```yaml
version: '3.8'
services:
  flask_app:
    build: .
    ports:
      - "5000:5000"
    restart: always
    container_name: flask_app
  
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    restart: always
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    restart: always
  
  node_exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    restart: always
```

### **3️⃣ Start Everything with Docker Compose**

```sh
docker-compose up -d --build
```

✅ This will **automate** running all services inside containers.

---

## **Contributing**

Feel free to **fork and contribute** to improve automation and monitoring!

---

✅ **Project is now documented!** Let me know if you’d like any final tweaks! 🚀

