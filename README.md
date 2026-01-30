# 🌍 geiger-mqtt-ha - Simple Radiation Monitoring Solution

## 📥 Download Now!
[![Download geiger-mqtt-ha](https://img.shields.io/badge/Download-geiger--mqtt--ha-blue.svg)](https://github.com/mhmdrosyad/geiger-mqtt-ha/releases)

## 📖 Overview
**geiger-mqtt-ha** connects your GQ Electronics GMC Geiger detector to Home Assistant. This application allows you to monitor radiation levels easily and receive real-time updates. You can visualize statistics for informed decisions in your environment. Using Docker, this setup creates a lightweight application that runs smoothly.

## 🚀 Getting Started
To get started with geiger-mqtt-ha, you’ll need to follow a few simple steps:

1. **Prepare Your Environment**
   - Ensure you have Docker installed on your computer. Docker allows you to run applications inside containers, making it easy to manage software without complex setups. You can download Docker from [Docker Hub](https://www.docker.com/get-started).

2. **Download the Application**
   - Visit this page to download: [Releases Page](https://github.com/mhmdrosyad/geiger-mqtt-ha/releases).

3. **Choose the Right Version**
   - On the Releases page, find the latest version. Click on the version number and look for a file labeled for your operating system. If you're not sure which one to choose, most users can opt for the latest stable Docker image.

4. **Install the Application**
   - After downloading, follow the on-screen instructions to set up the application. If you have Docker installed, running the application is as easy as a single command. Open your terminal or command prompt and run:
     ```bash
     docker run -d --name geiger-mqtt-ha --restart unless-stopped -e "MQTT_HOST=YOUR_MQTT_BROKER" -e "DEVICE_ID=YOUR_DEVICE_ID" -p 1883:1883 -v /path/to/config:/geiger/config mhmdrosyad/geiger-mqtt-ha
     ```
   - Replace `YOUR_MQTT_BROKER` with your MQTT broker address and `YOUR_DEVICE_ID` with your Geiger detector ID.

5. **Configure Home Assistant**
   - After the application runs, you can connect it to Home Assistant. Open your Home Assistant dashboard and add the device using your MQTT configuration. You'll find options to add an MQTT integration to help set this up.

## ⚙️ Features
- **Real-time Radiation Detection**: Monitor radiation levels continuously.
- **Statistical Analysis**: Track historical radiation data for trends and insights.
- **MQTT Integration**: Communicate with Home Assistant for easy data visualization and alerts.
- **Docker Support**: Quick and straightforward setup through Docker.

## 📋 System Requirements
- **Operating System**: Compatible with Windows, macOS, and Linux.
- **Docker**: Must have Docker installed (minimum version recommended: 20.10).
- **Network Connection**: An active internet connection for software updates and MQTT integration.

## 🔧 Troubleshooting
If you encounter issues while downloading or running the application, consider the following:

1. **Check Docker Installation**
   - Ensure Docker is installed correctly and running. You can verify this by running the command `docker --version` in your terminal.

2. **Firewall Settings**
   - Make sure that your firewall allows Docker to communicate. You may need to add exceptions for Docker.

3. **Consult the Community**
   - For additional support, visit the project issues on the GitHub page or check for FAQs.

## 🔗 Additional Resources
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [MQTT Protocol Guide](https://mqtt.org/)
- [Docker Documentation](https://docs.docker.com/get-started/)

## 📥 Download & Install
To install geiger-mqtt-ha, return to this link: [Download Page](https://github.com/mhmdrosyad/geiger-mqtt-ha/releases) and follow the steps listed above. You will be monitoring radiation in no time!

This guide aims to make it easy for you to set up your geiger-mqtt-ha application. If you have any questions, refer to the resources above or seek help from the broader community.