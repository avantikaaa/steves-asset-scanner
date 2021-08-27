import driver
import subprocess

def get_local_subnet():
    command = "ip -o -f inet addr show | awk '/scope global/ {print $4}'"
    subnet = subprocess.check_output(command, shell=True)
    subnet = subnet.decode('UTF-8')[:-1]
    return subnet

def main(error_popup, ui):
    subnet = get_local_subnet()
    driver.main(subnet, "local", error_popup, ui)
