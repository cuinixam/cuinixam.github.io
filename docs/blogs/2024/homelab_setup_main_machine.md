---
tags: homelab, getting started, setup, docker, ansible, portainer
category: diy
date: 2024-11-17
title: Homelab - setup main machine
---

# Homelab - setup main machine

## Introduction

When starting my homelab journey, I needed a main machine to manage all devices and services in my network. Many homelab enthusiasts typically choose Linux for this purpose. However, my primary computer runs Windows 11, so I decided to use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) with an Ubuntu distribution to fulfill this role.

## Installing WSL2

I followed the instructions provided in the [official documentation](https://learn.microsoft.com/en-us/windows/wsl/install) to install WSL2 and had Ubuntu up and running quickly.

### Network configuration

By default, WSL2 uses `NAT` networking mode, assigning dynamic IP addresses, which prevents access to other devices in the local network, like routers and Raspberry Pis. To solve this, I switched WSL2 to `mirrored` network mode via the `WSL Settings`. After shutting down (`wsl --shutdown`) and restarting WSL2 (`wsl`), I could successfully ping other devices in my network:

```bash
ping router.local
ping rpi3.local
```

### Using VS Code Remote - WSL

I found the easiest way to interact with files inside WSL2 was to use the [VS Code Remote - WSL](https://code.visualstudio.com/docs/remote/wsl) extension. Installing this extension allowed me to seamlessly edit files inside the Ubuntu distribution directly through VS Code's interface.

## Installing Ansible

To automate the configuration of remote devices, I chose Ansible. Following the instructions from Ansible's [installation page](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible-with-pipx), I created a script called `bootstrap_main_machine.sh` to install both `pipx` and `ansible`:

```bash
# Install pipx - see https://pipx.pypa.io/stable/
sudo apt update
sudo apt install pipx
pipx ensurepath

# Install ansible - see https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
pipx install --include-deps ansible
ansible --version
```

### Creating the Ansible inventory

I created an Ansible inventory file named `inventory.yml` within a new directory `~/ansible`. It lists the devices I want to manage:

```yaml
all:
  hosts:
    rpi3test.local:
      ansible_user: pi
```

I initially tested my Ansible setup using the ping module:

```bash
ansible -i ~/ansible/inventory.yml rpi3test.local -m ping
```

This attempt failed, showing the following SSH error:

```
rpi3test.local | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: pi@rpi3test.local: Permission denied (publickey,password).",
    "unreachable": true
}
```

Since I wasn't using SSH keys yet, I tried providing the password explicitly with the `--ask-pass` option:

```bash
ansible -i ~/ansible/inventory.yml rpi3test.local -m ping --ask-pass
```

However, this still didn't work due to a missing package:

```
rpi3test.local | FAILED! => {
    "msg": "to use the 'ssh' connection type with passwords or pkcs11_provider, you must install the sshpass program"
}
```

To resolve this, I installed the required package:

```bash
sudo apt install sshpass
```

After installing `sshpass`, running the ping command with `--ask-pass` succeeded:

```
rpi3test.local | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.11"
    },
    "changed": false,
    "ping": "pong"
}
```

```{important}
It is not recommended to authenticate using passwords because this opens the possibility for brute force attacks. The best practice is to use SSH keys for authentication. We will cover this in the next section.
```

### Creating SSH keys

To enhance security, I generated SSH keys specifically for Ansible connections using the `ED25519` algorithm:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/ansible
```

Next, I wrote an Ansible playbook to automate the process of copying SSH keys to the devices and disabling password authentication:

```yaml
---
- name: Setup authentication
  hosts: all
  become: yes
  tasks:
    - name: Create .ssh directory if it doesn't exist
      file:
        path: /home/{{ ansible_user }}/.ssh
        state: directory
        mode: "0700"
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"

    - name: Copy public key from local .ssh directory
      copy:
        src: "~/.ssh/ansible.pub"
        dest: /home/{{ ansible_user }}/.ssh/authorized_keys
        mode: "0600"
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"

    - name: Ensure password authentication is disabled in SSHD
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "^PasswordAuthentication"
        line: "PasswordAuthentication no"
        state: present
      notify:
        - Restart SSHD

    - name: Lock password for {{ ansible_user }}
      user:
        name: "{{ ansible_user }}"
        password_lock: yes

  handlers:
    - name: Restart SSHD
      service:
        name: sshd
        state: restarted
```
