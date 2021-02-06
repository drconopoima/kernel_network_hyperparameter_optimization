import sys
import getopt
import json
import requests


def pause(k6_url):
    current_status = status(k6_url)
    if current_status["data"]["attributes"]["paused"]:
        print("[WARNING]: Test execution was paused already")
        return current_status
    else:
        current_status["data"]["attributes"]["paused"] = True
    return requests.patch(k6_url + "/v1/status", data=json.dumps(current_status)).json()


def unpause(k6_url):
    current_status = status(k6_url)
    if current_status["data"]["attributes"]["paused"]:
        current_status["data"]["attributes"]["paused"] = False
    else:
        print("[WARNING]: Test execution was paused already")
        return current_status
    return requests.patch(k6_url + "/v1/status", data=json.dumps(current_status)).json()


def status(k6_url):
    return requests.get(k6_url + "/v1/status").json()


def main():
    global k6_url
    k6_url = "http://localhost:6565"
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "a:push",
            ["address=", "pause", "unpause", "status", "help"],
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ("-i", "--interval"):
            try:
                refresh_interval = int(a)
            except:
                usage()
                sys.exit(1)
        elif o in ("-a", "--address"):
            k6_url = a
        elif o in ("-p", "--pause"):
            print(pause(k6_url))
        elif o in ("-u", "--unpause"):
            print(unpause(k6_url))
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
    print(" -s                             Return the status of the k6 server")
    print("    --status")
    print(" -p                             Pause the K6 server")
    print("    --pause")
    print(" -u                             Unpause the K6 server")
    print("    --unpause")
    print(" -h                             Show this help text")
    print("    --help")
    print("")
