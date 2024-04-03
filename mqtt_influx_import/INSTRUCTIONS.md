# Project Setup Guide

This guide provides instructions on setting up the project environment, which includes installing InfluxDB v2, running Grafana in a Docker container, and configuring the necessary elements for a Python script. 
You can run it on a VPS (Virtual Private Server) with Debian/Ubuntu or on your local machine for testing purposes.

## Installing InfluxDB v2

1. **VPS/Local Machine Setup:** Ensure you have access to a VPS with Debian/Ubuntu or decide to run it on your local machine.
2. **Installation:** Follow the official [InfluxDB v2 installation guide](https://docs.influxdata.com/influxdb/v2/install/) to install InfluxDB on your chosen environment.

## Installing Grafana

Grafana will be run in a Docker container for simplicity:

```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana-oss
```

For more deployment options with Docker, refer to the [official documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/).

## Configuring InfluxDB

### Getting Your Access Token

1. **Login to InfluxDB.** Navigate to the InfluxDB UI and sign in.
2. **Generate Access Token:**
   - Go to **Getting Started > Python**.
   - On the left-hand side, click **Get Token**.
   - Save the token in the project's `docker-compose.yml` as the value for `influxdb_token`.

   > **Important:** Keep your access token in a secure location and do not push it to Git.


### Creating a Bucket

1. **Navigate to Load Data:** In the InfluxDB UI, go to **Load Data > Sources > Create Bucket**.
2. **Bucket Configuration:** Name your bucket and set the retention period. Update `docker-compose.yml` with your bucket name under `influxdb_bucket`.


### Setting the Host and Organization

- **Local Machine:** If running locally, set `influxdb_host` in `docker-compose.yml` to `http://localhost:8086`.
- **External VPS:** For VPS, use the external IP address, ensure port 8086 is exposed, and update `influxdb_org` to the organization you specified during the InfluxDB setup.

## MQTT Configuration

Update the MQTT related environment variables in `docker-compose.yml`:

```yaml
MQTT_USER:
MQTT_PASSWORD:
MQTT_HOST:
MQTT_PORT: 8883
MQTT_TOPIC:
```

Set the ```MQTT_TOPIC``` variable to correspond with your MQTT topic configuration for targeted data communication.
Ensure each variable is set correctly to match your MQTT broker's configurations for seamless integration.

## Running the Docker Container

With all configurations in place:

```bash
sudo docker-compose up --build
```

Run this command from the repository root where `docker-compose.yml` is located.

## Verifying Data in InfluxDB

To check if data is being inserted:

1. **Login to InfluxDB** and navigate to **Load Data > Buckets**.
2. **Select your Bucket:** Click on the bucket you created earlier.
3. **Check for Data:** Use the query builder at the bottom. If no values appear immediately, wait a few seconds as data is inserted every 10 seconds.

## Grafana, setting Up a Data Connection to InfluxDB using Flux
--
### Step 1: Accessing the InfluxDB UI

Ensure that your InfluxDB instance is up and running. Access the InfluxDB UI by navigating to the address where your InfluxDB is hosted, typically `http://localhost:8086` if hosted locally.

### Step 2: Creating a Data Source in Grafana for InfluxDB

1. **Open Grafana:** Access the Grafana dashboard. By default, this is usually `http://localhost:3000`. Or replace it with your external IP to the VPS. 
   
2. **Navigate to Data Sources:** Click on the Settings icon in the side menu and select "Data Sources."

3. **Add Data Source:** Click the "Add data source" button and search for "InfluxDB."

4. **Configure Data Source with Flux:**
   - Choose **InfluxDB** as the data source type.
   - Under **Query Language**, select **Flux**.
   - Input your InfluxDB details:
     - **URL:** Your InfluxDB instance URL, e.g., `http://localhost:8086` or the external IP.
     - **Organization:** Your InfluxDB organization name.
     - **Token:** The API token you generated earlier for authentication.
   - Under **Default Bucket**, enter the bucket name you created in your InfluxDB setup.

5. **Save & Test:** After setting your configurations, click “Save & Test” to ensure Grafana can successfully connect to your InfluxDB instance.

### Step 3: Querying Data Using Flux

Now that you have connected Grafana to your InfluxDB data source using Flux, you can begin querying your data:

1. **Create a New Dashboard:** From the Grafana side menu, select "+ > Dashboard" to create a new dashboard.

2. **Add a New Panel:** Click the "Add new panel" button.

3. **Write Your Query:** In the query editor, you can write your Flux query to retrieve and display data. For example, to fetch CPU usage data, you might use:
**Important:** Update ```bucket``` below in the query to match your bucket in InfluxDB.   
```flux
      from(bucket: "energy")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r["_measurement"] == "WL1_A1DA1")
        |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
        |> yield(name: "mean")

