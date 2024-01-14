from flask import Flask, render_template, request
import re, subprocess
import time
from flask import jsonify

app = Flask(__name__)

allowed_command_list = ["tcpdump", "ls", "arp", "ifconfig", "ping", "time"]

# "hping3" 사용한 Syn Flooding 공격,


def is_allowed_command(command):
    for pattern in allowed_command_list:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


@app.route("/")
def home():
    return render_template("ctfindex.html")


def get_ifconfig_result():
    return """
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.81.131  netmask 255.255.255.0  broadcast 192.168.81.255
        inet6 fe80::3c63:21fc:5734:a7da  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:9a:95:b2  txqueuelen 1000  (Ethernet)
        RX packets 196649  bytes 12891943 (12.8 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 833  bytes 67605 (67.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens37: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.80.129  netmask 255.255.255.0  broadcast 192.168.80.255
        inet6 fe80::9007:dbd:d711:26e0  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:9a:95:bc  txqueuelen 1000  (Ethernet)
        RX packets 314  bytes 32224 (32.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 377  bytes 32850 (32.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 828  bytes 85670 (85.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 828  bytes 85670 (85.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""  # linux에서 아무거나 긁어와서 붙여넣기


def get_tcpdump_no_result():
    return """
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes

0 packets captured
0 packets received by filter
0 packets dropped by kernel
"""  # linux에서 아무거나 긁어와서 붙여넣기


def get_tcpdump_help():
    return """tcpdump version 4.9.3
libpcap version 1.9.1 (with TPACKET_V3)
OpenSSL 1.1.1f  31 Mar 2020
Usage: tcpdump [-aAbdDefhHIJKlLnNOpqStuUvxX#] [ -B size ] [ -c count ]
		[ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
		[ -i interface ] [ -j tstamptype ] [ -M secret ] [ --number ]
		[ -Q in|out|inout ]
		[ -r file ] [ -s snaplen ] [ --time-stamp-precision precision ]
		[ --immediate-mode ] [ -T type ] [ --version ] [ -V file ]
		[ -w file ] [ -W filecount ] [ -y datalinktype ] [ -z postrotate-command ]
		[ -Z user ] [ expression ]
    """


def get_tcpdump_result():
    return """
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes
18:14:45.383773 IP 192.168.81.135.2804 > 192.168.131.81.tcpmux: Flags [S], seq 1607810441, win 512, length 0
18:14:46.384309 IP 192.168.81.135.2805 > 192.168.131.81.2: Flags [S], seq 1185647212, win 512, length 0
18:14:47.385857 IP 192.168.81.135.2806 > 192.168.131.81.3: Flags [S], seq 1779872831, win 512, length 0
18:14:48.386488 IP 192.168.81.135.2807 > 192.168.131.81.4: Flags [S], seq 834713544, win 512, length 0
18:14:49.387796 IP 192.168.81.135.2808 > 192.168.131.81.5: Flags [S], seq 1397796302, win 512, length 0
18:14:50.388715 IP 192.168.81.135.2809 > 192.168.131.81.6: Flags [S], seq 1878010635, win 512, length 0
18:14:51.392111 IP 192.168.81.135.2810 > 192.168.131.81.echo: Flags [S], seq 50090977, win 512, length 0
18:14:52.392808 IP 192.168.81.135.gsiftp > 192.168.131.81.8: Flags [S], seq 1834322125, win 512, length 0
18:14:53.395266 IP 192.168.81.135.2812 > 192.168.131.81.discard: Flags [S], seq 73125094, win 512, length 0
18:14:54.396237 IP 192.168.81.135.2813 > 192.168.131.81.10: Flags [S], seq 463601079, win 512, length 0
18:14:55.397621 IP 192.168.81.135.2814 > 192.168.131.81.systat: Flags [S], seq 880198859, win 512, length 0
18:14:56.398159 IP 192.168.81.135.2815 > 192.168.131.81.12: Flags [S], seq 387177857, win 512, length 0
18:14:57.401889 IP 192.168.81.135.2816 > 192.168.131.81.daytime: Flags [S], seq 1848718498, win 512, length 0
18:14:58.403149 IP 192.168.81.135.2817 > 192.168.131.81.14: Flags [S], seq 748407344, win 512, length 0
18:14:59.402940 IP 192.168.81.135.2818 > 192.168.131.81.netstat: Flags [S], seq 1987516715, win 512, length 0
18:15:00.404192 IP 192.168.81.135.2819 > 192.168.131.81.16: Flags [S], seq 1331243801, win 512, length 0
18:15:01.405963 IP 192.168.81.135.2820 > 192.168.131.81.qotd: Flags [S], seq 820572818, win 512, length 0
18:15:02.406997 IP 192.168.81.135.2821 > 192.168.131.81.18: Flags [S], seq 809163130, win 512, length 0
18:15:03.407716 IP 192.168.81.135.2822 > 192.168.131.81.chargen: Flags [S], seq 1492204067, win 512, length 0
18:15:04.408305 IP 192.168.81.135.2823 > 192.168.131.81.ftp-data: Flags [S], seq 1897859330, win 512, length 0
18:15:05.409132 IP 192.168.81.135.2824 > 192.168.131.81.ftp: Flags [S], seq 803451027, win 512, length 0
18:15:06.409302 IP 192.168.81.135.2825 > 192.168.131.81.ssh: Flags [S], seq 256019593, win 512, length 0
18:15:07.412761 IP 192.168.81.135.2826 > 192.168.131.81.telnet: Flags [S], seq 962988874, win 512, length 0
18:15:08.414136 IP 192.168.81.135.2827 > 192.168.131.81.24: Flags [S], seq 1661152015, win 512, length 0
18:15:09.415056 IP 192.168.81.135.2828 > 192.168.131.81.smtp: Flags [S], seq 966350698, win 512, length 0
18:15:10.415229 IP 192.168.81.135.2829 > 192.168.131.81.26: Flags [S], seq 1833113438, win 512, length 0
18:15:11.416448 IP 192.168.81.135.2830 > 192.168.131.81.27: Flags [S], seq 290955213, win 512, length 0
18:15:12.416968 IP 192.168.81.135.2831 > 192.168.131.81.28: Flags [S], seq 1608950622, win 512, length 0
18:20:04.294776 IP 192.168.81.135.1944 > 192.168.131.81.ssh: Flags [S], seq 39492882, win 512, length 0
18:20:04.294865 IP 192.168.81.135.1945 > 192.168.131.81.ssh: Flags [S], seq 1085665769, win 512, length 0
18:20:04.294886 IP 192.168.81.135.1946 > 192.168.131.81.ssh: Flags [S], seq 2017556103, win 512, length 0
18:20:04.294946 IP 192.168.81.135.1947 > 192.168.131.81.ssh: Flags [S], seq 873934303, win 512, length 0
18:20:04.294962 IP 192.168.81.135.1948 > 192.168.131.81.ssh: Flags [S], seq 356824729, win 512, length 0
18:20:04.294980 IP 192.168.81.135.1949 > 192.168.131.81.ssh: Flags [S], seq 666097382, win 512, length 0
18:20:04.294998 IP 192.168.81.135.1950 > 192.168.131.81.ssh: Flags [S], seq 342336345, win 512, length 0
18:20:04.295486 IP 192.168.81.135.1951 > 192.168.131.81.ssh: Flags [S], seq 1220292568, win 512, length 0
18:20:04.295506 IP 192.168.81.135.1952 > 192.168.131.81.ssh: Flags [S], seq 980678625, win 512, length 0
18:20:04.295524 IP 192.168.81.135.1953 > 192.168.131.81.ssh: Flags [S], seq 1638736694, win 512, length 0
18:20:04.295542 IP 192.168.81.135.1954 > 192.168.131.81.ssh: Flags [S], seq 1672471614, win 512, length 0
18:20:04.295560 IP 192.168.81.135.1955 > 192.168.131.81.ssh: Flags [S], seq 1421751326, win 512, length 0
18:20:04.295577 IP 192.168.81.135.1956 > 192.168.131.81.ssh: Flags [S], seq 1087355107, win 512, length 0
18:20:04.295593 IP 192.168.81.135.1957 > 192.168.131.81.ssh: Flags [S], seq 5977134, win 512, length 0
18:20:04.295611 IP 192.168.81.135.1958 > 192.168.131.81.ssh: Flags [S], seq 1282461194, win 512, length 0
18:20:04.295690 IP 192.168.81.135.1959 > 192.168.131.81.ssh: Flags [S], seq 895544433, win 512, length 0
18:20:04.295708 IP 192.168.81.135.1960 > 192.168.131.81.ssh: Flags [S], seq 1788604468, win 512, length 0
18:20:04.295726 IP 192.168.81.135.1961 > 192.168.131.81.ssh: Flags [S], seq 876168218, win 512, length 0
18:20:04.295743 IP 192.168.81.135.1962 > 192.168.131.81.ssh: Flags [S], seq 23905074, win 512, length 0
18:20:04.295760 IP 192.168.81.135.1963 > 192.168.131.81.ssh: Flags [S], seq 1330271545, win 512, length 0
18:20:04.295777 IP 192.168.81.135.1964 > 192.168.131.81.ssh: Flags [S], seq 395332384, win 512, length 0
18:20:04.295793 IP 192.168.81.135.1965 > 192.168.131.81.ssh: Flags [S], seq 100363008, win 512, length 0
18:20:04.295811 IP 192.168.81.135.1966 > 192.168.131.81.ssh: Flags [S], seq 2007706153, win 512, length 0
18:20:04.295872 IP 192.168.81.135.1967 > 192.168.131.81.ssh: Flags [S], seq 580520814, win 512, length 0
18:20:04.295890 IP 192.168.81.135.1968 > 192.168.131.81.ssh: Flags [S], seq 1295982122, win 512, length 0
18:20:04.295907 IP 192.168.81.135.1969 > 192.168.131.81.ssh: Flags [S], seq 2123297820, win 512, length 0
18:20:04.295924 IP 192.168.81.135.1970 > 192.168.131.81.ssh: Flags [S], seq 125388209, win 512, length 0
18:20:04.295941 IP 192.168.81.135.1971 > 192.168.131.81.ssh: Flags [S], seq 1180688943, win 512, length 0
18:20:04.295957 IP 192.168.81.135.1972 > 192.168.131.81.ssh: Flags [S], seq 128148636, win 512, length 0
18:20:04.295974 IP 192.168.81.135.1973 > 192.168.131.81.ssh: Flags [S], seq 1833833973, win 512, length 0
18:20:04.295991 IP 192.168.81.135.1974 > 192.168.131.81.ssh: Flags [S], seq 244934011, win 512, length 0
18:20:04.296040 IP 192.168.81.135.1975 > 192.168.131.81.ssh: Flags [S], seq 1843392578, win 512, length 0

60 packets captured
23909 packets received by filter
23877 packets dropped by kernel

"""  # linux에서 아무거나 긁어와서 붙여넣기


def get_tcp_permission():
    return """
    tcpdump: ens33: You don't have permission to capture on that device
(socket: Operation not permitted)
    """


def get_arp_a():
    return """
        ? (192.168.81.254) at 00:50:56:f4:9c:5e [ether] on ens33
        ? (192.168.80.1) at 00:50:56:c0:00:01 [ether] on ens37
        _gateway (192.168.81.2) at 00:50:56:e1:5a:2f [ether] on ens33
        ? (192.168.80.254) at 00:50:56:f9:02:7c [ether] on ens37
    """


def get_arp_d():
    return """
    Address                  HWtype  HWaddress           Flags Mask            Iface
        192.168.81.254           ether   00:50:56:f4:9c:5e   C                     ens33
        192.168.80.1             ether   00:50:56:c0:00:01   C                     ens37
        _gateway                 ether   00:50:56:e1:5a:2f   C                     ens33
        192.168.80.254           ether   00:50:56:f9:02:7c   C                     ens37

    """


def get_ls():
    return """
    Desktop  Documents  Downloads  iptables  Music  Pictures  Public  snap  Templates  Videos
    """


def get_ls_l():
    return """
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Desktop
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Documents
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Downloads
    drwxrwxr-x 2 sum sum 4096 Aug 10 10:31 iptables
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Music
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Pictures
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Public
    drwx------ 3 sum sum 4096 Aug 11 00:38 snap
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Templates
    drwxr-xr-x 2 sum sum 4096 Aug  3 03:00 Videos
"""


def get_ls_al():
    return """
    drwx------ 19 sum  sum  4096 Aug 11 01:27 .
    drwxr-xr-x  3 root root 4096 Aug  3 00:10 ..
    -rw-------  1 sum  sum  8184 Jan 13 06:50 .bash_history
    -rw-r--r--  1 sum  sum   220 Aug  3 00:10 .bash_logout
    -rw-r--r--  1 sum  sum  3771 Aug  3 00:10 .bashrc
    drwx------ 12 sum  sum  4096 Aug 10 22:58 .cache
    drwx------ 13 sum  sum  4096 Aug 10 09:59 .config
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Desktop
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Documents
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Downloads
    drwx------  3 sum  sum  4096 Aug 11 04:28 .gnupg
    drwxrwxr-x  2 sum  sum  4096 Aug 10 10:31 iptables
    drwxr-xr-x  3 sum  sum  4096 Aug  3 03:00 .local
    drwx------  4 sum  sum  4096 Aug 10 22:57 .mozilla
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Music
    -rw-------  1 sum  sum   101 Aug 11 01:27 .mysql_history
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Pictures
    -rw-r--r--  1 sum  sum   807 Aug  3 00:10 .profile
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Public
    drwx------  3 sum  sum  4096 Aug 11 00:38 snap
    drwx------  2 sum  sum  4096 Aug  5 20:42 .ssh
    -rw-r--r--  1 sum  sum     0 Aug  3 05:13 .sudo_as_admin_successful
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Templates
    drwxr-xr-x  2 sum  sum  4096 Aug  3 03:00 Videos
    drwxrwxr-x  5 sum  sum  4096 Aug 11 05:56 .vscode-server
    -rw-rw-r--  1 sum  sum   183 Aug 11 05:56 .wget-hsts
    """


def ping_command(ip_address):
    return f"""
    PING {ip_address} ({ip_address}) 56(84) bytes of data.
    64 bytes from {ip_address}: icmp_seq=1 ttl=128 time=1522 ms
    64 bytes from {ip_address}: icmp_seq=4 ttl=128 time=1451 ms

    --- {ip_address} ping statistics ---
    15 packets transmitted, 2 received, 86.6667% packet loss, time 14368ms
    rtt min/avg/max/mdev = 1450.846/1486.612/1522.379/35.766 ms, pipe 2
"""


def execute_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10
        )
        return result
    except Exception as e:
        return f"Error:{e.output}"


# def get_arp_result():
#     try:
#         result = execute_command("arp -a")
#     except Exception as e:
#         return "Error:{e.output}"
#     return result


def do_simulation(command):
    if "ifconfig" in command:
        result = get_ifconfig_result()
        return result

    elif "ping" in command:
        ip_address = command.split(" ")[-1]
        time.sleep(3)
        result = ping_command(ip_address)
        return result

    elif "arp" in command:
        if "arp -a" == command:
            result = get_arp_a()
            return result
        elif "arp -d" == command:
            result = get_arp_d()
            return result

    elif "ls" in command:
        if "ls" == command:
            result = get_ls()
            return result
        elif "ls -l" == command:
            result = get_ls_l()
            return result
        elif "ls -al" or "ls -la" == command:
            result = get_ls_al()
            return result

    elif "tcpdump" in command:
        tcpdumpPattern = r"sudo tcpdump -i ens33 (tcp port 22|dst 192\.168\.131\.81)|(tcp port 22|dst 192\.168\.131\.81) sudo tcpdump -i ens33"
        tcpHelpPatter = r"^(sudo )?tcpdump -(h|help|--help|---help)$"
        if re.match(tcpHelpPatter, command):
            result = get_tcpdump_help()
        elif re.search(tcpdumpPattern, command):
            time.sleep(3)
            result = get_tcpdump_result()
        elif not command.startswith("sudo"):
            result = get_tcp_permission()
        else:
            time.sleep(3)
            result = get_tcpdump_no_result()
        return result

    elif "time" in command:
        result = execute_command("time")
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


correct_answer1 = "SYN FLOODING ATTACK"
correct_answer2 = "192.168.81.135"


@app.route("/answer", methods=["POST"])
def check_answer():
    attack_type = request.form.get("attackType", "")
    attacker = request.form.get("attacker", "")
    print("입력된 공격유형:", attack_type)
    print("입력된 공격자:", attacker)
    attack_type = attack_type.upper()

    if attack_type == correct_answer1 and attacker == correct_answer2:
        return jsonify({"result": "Correct! flag is: BoB{haha!you_are_god!}"})
    else:
        return jsonify({"result": "Wrong! Try again!"})


if __name__ == "__main__":
    app.run(debug=True)
