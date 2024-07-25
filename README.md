
## How can i use this?
This is a standard Python script, so it should work on Windows, Mac, and Linux. However, I have only tested it on Ubuntu.


---

## How to Install

1. **Update your package list:**

   ```
   sudo apt update
   ```

2. **Install Python 3:**

   ```
   sudo apt-get install python3
   ```

3. **Install pip:**

   ```
   sudo apt-get install python3-pip
   ```

4. **Install Scapy:**

   ```
   pip3 install scapy
   ```

**You have now installed all the essentials for this script to work.**

5. **Download the script:**

   You can use `git`, download the file manually, or copy the code. To clone the repository with `git`, run:

   ```
   git clone https://github.com/MrDunkel089/find_open_ports.git
   ```

   For all other systems, you can now proceed to the "How to Use" section.

6. **For Linux users:**

   - Make the script executable:

     ```
     sudo chmod +x fop.py
     ```

   - Move the script to `/usr/local/bin`:

     ```
     sudo mv fop.py /usr/local/bin/fop
     ```

**That's it! You have successfully installed the Find Open Ports (fop) script.**---

## How to Use

Using the script is straightforward. You simply use the `fop` command with the desired options. Here’s an example:

```
fop [OPTIONS] [custom_server_ip_address]:[start_port]-[end_port]
```

For example, this command scans all ports from 1 to 250 until an open port is found:

```
fop 127.0.0.1:1-250
```

### Options

To view all available options, type `fop -h` or `fop --help`:

```
-h, --help              Show this help message and exit.
-t, --timeout           Set the timeout duration in seconds. Default is 1 second.
-o, --output            Save the results of open ports to a specified file.
-v, --verbose           Provide detailed output for each step.
-i, --ignore            Continue scanning all ports even if an open port is found.
-e, --exclude           Specify ports to exclude from the scan, separated by commas.
-s, --scan-type-syn     Use stealth (SYN) scan. (Currently not functional)
-p, --protocol          Specify the protocol for the port scan. Default is TCP. (Currently not functional)
```

### Quick Overview

To set a timeout:

```
fop -t [seconds] 127.0.0.1:1-250
```

To save results to a file:

```
fop -o [filename] 127.0.0.1:1-250
```

To exclude specific ports:

```
fop -e [port_to_exclude] 127.0.0.1:1-250
```

**For Windows/Mac users, run the script with:**

```
python3 fop.py [OPTIONS] [custom_server_ip_address]:[start_port]-[end_port]
```

It should work the same way. :)
## FAQ

#### Can I reupload your code?

Please **do not** reupload any code and claim it as your own. You are welcome to improve upon this code, as I created it in about an hour and wanted to share it. However, always give credit to the original creator of the code.

#### Why did you create this?

Because coding is fun!

#### Will you ever make a full Windows version of this?

Short answer: No. Long answer: There is already a way to run this on Windows. You can use a virtual machine (VM) or Windows Subsystem for Linux (WSL). To install WSL, open PowerShell in admin mode and run:

```
wsl install
```

Done!

#### Will you ever make a full macOS version of this?

You can always use the Python option on macOS. Since macOS is UNIX-based, the process should be similar. Install [Homebrew](https://brew.sh/) and use `brew install [...]` to set up everything. All other steps should be the same.

