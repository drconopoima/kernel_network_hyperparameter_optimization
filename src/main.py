import sys
import getopt
import json
import requests


def status(k6_url):
    return requests.get(k6_url + "/v1/status").json()


def pause(k6_url):
    current_status = new_status = status(k6_url)
    if current_status["data"]["attributes"]["paused"]:
        print("[WARNING]: Test execution was paused already")
        return current_status
    else:
        new_status["data"]["attributes"]["paused"] = True
    return requests.patch(k6_url + "/v1/status", data=json.dumps(new_status)).json()


def unpause(k6_url):
    current_status = new_status = status(k6_url)
    if current_status["data"]["attributes"]["paused"]:
        new_status["data"]["attributes"]["paused"] = False
    else:
        print("[WARNING]: Test execution was paused already")
        return current_status
    return requests.patch(k6_url + "/v1/status", data=json.dumps(new_status)).json()


def change_vus(k6_url, delta):
    current_status = new_status = status(k6_url)
    if delta == 0:
        return current_status
    current_vus = target_vus = current_status["data"]["attributes"]["vus"]
    target_vus += delta
    if target_vus < 0:
        print("ERROR: Cannot decrease virtual users below 0.")
        return current_status
    max_vus = new_status["data"]["attributes"]["vus-max"]
    new_status["data"]["attributes"]["vus"] = target_vus
    if max_vus < target_vus:
        new_status["data"]["attributes"]["vus-max"] = target_vus
    if not current_status["data"]["attributes"]["paused"]:
        pause(k6_url)
    else:
        new_status["data"]["attributes"]["paused"] = False
    return requests.patch(k6_url + "/v1/status", data=json.dumps(new_status)).json()


def no_vus(k6_url):
    current_status = new_status = status(k6_url)
    current_vus = current_status["data"]["attributes"]["vus"]
    if current_vus == 0:
        print("[WARNING]: Number of virtual users was zero already")
        return current_status
    new_status["data"]["attributes"]["vus"] = 0
    return requests.patch(k6_url + "/v1/status", data=json.dumps(new_status)).json()


def get_rps(k6_url, max_vus):
    pass


def maximize_requests(k6_url, max_vus):
    pause(k6_url)
    no_vus(k6_url)
    pass


def main():
    global k6_url
    k6_url = "http://localhost:6565"
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "a:push",
            ["address=", "change-vus=", "pause", "unpause", "status", "help"],
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ("-a", "--address"):
            k6_url = a
        elif o in ("-p", "--pause"):
            print(pause(k6_url))
        elif o in ("-u", "--unpause"):
            print(unpause(k6_url))
        elif o in ("--change-vus"):
            try:
                print(change_vus(k6_url, int(a)))
            except:
                print("ERROR: Could not change virtual users")
        elif o in ("-s", "--status"):
            print(status(k6_url))
        else:
            usage()
            if not o in ("-h", "--help"):
                sys.exit(1)
            sys.exit(0)


def usage():
    print("Usage: kernel_network_hyperparameter_optimization.py [options]")
    print("")
    print("Options:")
    print(" -a <k6_address>                Specify the running k6 server")
    print("    --address=<k6_address>")
    print(" --change-vus=<change-by>       Adjust number of virtual users by argument")
    print(" -s                             Return the status of the k6 server")
    print("    --status")
    print(" -p                             Pause the K6 server")
    print("    --pause")
    print(" -u                             Unpause the K6 server")
    print("    --unpause")
    print(" -h                             Show this help text")
    print("    --help")
    print("")
