import argparse
import json
import os
import re
from collections import Counter, defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--file", dest="file", action="store", help="Choose file")
parser.add_argument("--dir", action="store", help="Choose directory")
parser.add_argument("--ext", default='.log', action="store", help="Filter extension")

args = parser.parse_args()

request_methods = defaultdict(lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0})
top_ip_requests = Counter()
top_error_user_requests = Counter()
top_error_server_requests = Counter()
top_requests_time = []


def create_list_of_files():
    file_list = []
    if args.file is not None:
        file_list.append(args.file)
        return file_list
    if os.listdir(args.dir) is not None:
        return os.listdir(args.dir)


file_counter = 0
for item in create_list_of_files():
    if item.endswith(args.ext):
        with open(item) as file:
            try:
                for index, line in enumerate(file.readlines()):
                    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                    method = re.search(r"(POST|GET|PUT|DELETE|HEAD)", line)
                    url = re.search(r'"(http.*?)"', line)
                    request_time = re.search(r"(20\d{1}|30\d{1}|40\d{1}|50{1}) (\d{1,})", line)
                    error_user = re.search(r"\s40\d{1}$", line)
                    error_server = re.search(r"\s50\d{1}$", line)

                    if ip is not None and method is not None:
                        request_methods[ip.group()][method.group()] += 1

                    if ip is not None:
                        top_ip_requests[ip.group()] += 1

                    if request_time is not None and url is not None and method is not None:
                        top_requests_time.append(
                            (f"{ip.group()} {method.group()} {url.group()}", int(request_time.group(2))))

                    if error_user is not None and url is not None and method is not None:
                        err_usr = f"{ip.group()} {method.group()} {url.group()} {error_user.group()}"
                        top_error_user_requests[err_usr] += 1

                    if error_server is not None and url is not None and method is not None:
                        err_srv = f"{ip.group()} {method.group()} {url.group()} {error_server.group()}"
                        top_error_server_requests[err_srv] += 1

            except Exception as err:
                print(str(err) + f"{index} {line}")

            top_requests_time.sort(key=lambda x: x[1])

        file_counter += 1
        with open(f"result{item.title()}.json", "a+") as write:
            data = {
                "METHODS": [
                    request_methods
                ],
                "TOP IP REQUESTS": [
                    top_ip_requests.most_common(10)
                ],
                "TOP LONGEST REQUEST TIME": [
                    top_requests_time[-10:-1]
                ],
                "TOP USER ERRORS": [
                    top_error_user_requests.most_common(10)
                ],
                "TOP SERVER ERRORS": [
                    top_error_server_requests.most_common(10)
                ]
            }
            result = json.dumps(data, indent=4)
            write.write(result)
