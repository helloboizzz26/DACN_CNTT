#!/usr/bin/env python3
"""
Script giả lập bắn sự kiện Falco vào Falcosidekick-UI hoặc Falcosidekick
Dùng để test giao diện và demo đồ án khi cần thiết.
"""
import uuid
import datetime
import json
import urllib.request
import urllib.error
import time

UI_URL = "http://localhost:2802/api/v1/"

sample_events = [
    {
        "priority": "Warning",
        "rule": "Terminal shell in container",
        "output": "10:14:02.123456789: Warning A shell was spawned in a container with an attached terminal (user=root user_loginuid=-1 k8s.ns=<NA> k8s.pod=<NA> container=nginx-web container_id=e19bc8472a12 image=nginx:latest shell=bash parent=docker-runc cmdline=bash)",
        "tags": ["container", "shell", "mitre_execution"],
        "fields": {
            "container.id": "e19bc8472a12",
            "container.name": "nginx-web",
            "container.image.repository": "nginx",
            "proc.name": "bash",
            "proc.cmdline": "bash",
            "user.name": "root"
        }
    },
    {
        "priority": "Critical",
        "rule": "Read sensitive file untrusted",
        "output": "10:15:30.456123789: Critical Sensitive file opened for reading by untrusted program (user=root user_loginuid=-1 program=cat command=cat /etc/shadow file=/etc/shadow parent=bash container_id=a820f12c3491 container_name=payment-service image=node:18)",
        "tags": ["container", "filesystem", "mitre_credential_access"],
        "fields": {
            "container.id": "a820f12c3491",
            "container.name": "payment-service",
            "container.image.repository": "node",
            "proc.name": "cat",
            "proc.cmdline": "cat /etc/shadow",
            "fd.name": "/etc/shadow",
            "user.name": "root"
        }
    },
    {
        "priority": "Error",
        "rule": "Launch Suspicious Network Tool in Container",
        "output": "10:16:45.987654321: Error Network tool launched in container (user=root container_name=redis-cache container_id=7c91fa0231bc tool=nmap cmdline=nmap -sS -p 1-1000 192.168.1.1)",
        "tags": ["container", "network", "mitre_discovery"],
        "fields": {
            "container.id": "7c91fa0231bc",
            "container.name": "redis-cache",
            "container.image.repository": "redis",
            "proc.name": "nmap",
            "proc.cmdline": "nmap -sS -p 1-1000 192.168.1.1",
            "user.name": "root"
        }
    },
    {
        "priority": "Emergency",
        "rule": "Redirect stdout/stdin to network connection (Reverse Shell)",
        "output": "10:17:10.112233445: Emergency Redirect stdout/stdin to network connection (user=www-data container_name=victim-app container_id=99ab12cd34ef connection=10.0.0.5:4444 fd=0(socket) cmdline=sh -i)",
        "tags": ["container", "network", "mitre_command_and_control"],
        "fields": {
            "container.id": "99ab12cd34ef",
            "container.name": "victim-app",
            "container.image.repository": "python:alpine",
            "proc.name": "sh",
            "proc.cmdline": "sh -i",
            "user.name": "www-data"
        }
    },
    {
        "priority": "Notice",
        "rule": "Launch Package Management Process in Container",
        "output": "10:18:22.334455667: Notice Package management process launched in container (user=root container_name=victim-app container_id=99ab12cd34ef proc=apt-get cmdline=apt-get update)",
        "tags": ["container", "software", "mitre_persistence"],
        "fields": {
            "container.id": "99ab12cd34ef",
            "container.name": "victim-app",
            "container.image.repository": "ubuntu:22.04",
            "proc.name": "apt-get",
            "proc.cmdline": "apt-get update",
            "user.name": "root"
        }
    }
]

def send_event(event_data):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    event_id = str(uuid.uuid4())
    payload = {
        "event": {
            "uuid": event_id,
            "output": event_data["output"],
            "priority": event_data["priority"],
            "rule": event_data["rule"],
            "time": now,
            "source": "syscall",
            "output_fields": event_data["fields"],
            "hostname": "k8s-worker-node-01",
            "tags": event_data["tags"]
        },
        "outputs": ["webui"]
    }
    
    req = urllib.request.Request(
        UI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f" [+] Gửi thành công sự kiện: [{event_data['priority']}] {event_data['rule']}")
    except urllib.error.URLError as e:
        print(f" [!] Không thể kết nối tới {UI_URL}: {e}")

if __name__ == "__main__":
    print("=== BẮT ĐẦU GIẢ LẬP GỬI CÁC SỰ KIỆN PHÁT HIỆN BẤT THƯỜNG TRONG CONTAINER ===")
    for evt in sample_events:
        send_event(evt)
        time.sleep(1)
    print("=== HOÀN TẤT GỬI CÁC SỰ KIỆN TEST ===")
