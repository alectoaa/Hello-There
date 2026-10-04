# 👋 Hello There

**Hello There** is a professional pen-test tool designed for target IP scanning, RTSP service analysis, default credential testing, and live stream playback.

## 🚀 Features
* Target port scanning (554, 80, 8080) with optional anonymity (Proxychains support)
* RTSP authentication type detection (Basic / Digest)
* Brand-specific default credential testing (Hikvision, Dahua, Axis, Uniview, etc.)
* Instant live stream playback via `ffplay`

### 📐 System Architecture & Workflow

```mermaid
flowchart TD
    A[Target Input / IP Range] --> B[Port & RTSP Discovery Module]
    B --> C{RTSP Port 554 Open?}
    C -- No --> D[Log: Host Unreachable / Port Closed]
    C -- Yes --> E[Credential Assessment Engine]
    E --> F[RTSP Stream Validation / OpenCV Frame Grab]
    F --> G[Results Logger & Output Format]
















## ⚙️ Requirements
* Python 3.x
* Nmap
* FFmpeg (`ffplay`)

## 📦 Installation & Usage
```bash
git clone https://github.com/alectoaa/Hello-There.git
cd Hello-There
sudo chmod +x install.sh
sudo ./install.sh
hellothere




