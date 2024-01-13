from flask import Flask, render_template, request
import re, subprocess
import time
from flask import jsonify

app = Flask(__name__)

allowed_command_list = ["ping", "arping", "icmp", "tcpdump", "arp", "ifconfig"]

# "hping3" 사용


def is_allowed_command(command):
    for pattern in allowed_command_list:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


@app.route("/")
def home():
    return render_template("ctfindex.html")


def get_ifconfig_result():
    return """ifconfig
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.24.70.200  netmask 255.255.240.0  broadcast 172.24.79.255
        inet6 fe80::215:5dff:fecc:58ed  prefixlen 64  scopeid 0x20<link>
        ether 00:15:5d:cc:58:ed  txqueuelen 1000  (Ethernet)
        RX packets 2062  bytes 366584 (366.5 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 184  bytes 16027 (16.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 6829  bytes 70118455 (70.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6829  bytes 70118455 (70.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""  # linux에서 아무거나 긁어와서 붙여넣기


def execute_command(command):
    result = subprocess.check_output(
        command, shell=True, stderr=subprocess.STDOUT, text=True
    )
    return result


def get_arp_result():
    try:
        result = execute_command("arp -a")
    except Exception as e:
        return "Error:{e.output}"
    return result


def do_simulation(command):
    if "ifconfig" in command:
        result = get_ifconfig_result()
        return result
    elif "arp" in command:
        result = get_arp_result()
        time.sleep(1)  # 리얼하게 하기 위해서 딜레이...
        return result

    return "입력명령어 처리 예정"


@app.route("/simulate", methods=["POST"])
def simulate():
    command = request.form["command"]
    print("입력 명령어:", command)
    if is_allowed_command(command):
        result = do_simulation(command)
    else:
        result = "허용되지 않은 명령어"

    return render_template("ctfindex.html", command=command, result=result)


correct_answer = "00:15:5d:cc:58:ed"


@app.route("/answer", methods=["POST"])
def check_answer():
    user_input = request.form.get("macAddress", "")
    if user_input == correct_answer:
        return jsonify({"result": "Correct! flag is: BoB{haha!you_are_god!}"})
    else:
        return jsonify({"result": "Wrong! Try again!"})


if __name__ == "__main__":
    app.run(debug=True)
