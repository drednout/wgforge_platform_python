"""Parse nginx log-file obtained from command line

Usage:
    parse_nginx_logs.py <path_to_file>
"""
import sys
import re
import datetime
import calendar

NOT_FOUND = ''
MONTH_NAME_DICT = {v: k for k,v in enumerate(calendar.month_abbr)}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]

    resp_time_re = re.compile(r'r:[0-9]+[.][0-9]+')
    upstream_time_re = re.compile(r'up:[0-9]+[.][0-9]+')
    http_url_re = re.compile(r'"(POST|GET|PUT|DELETE) (/[a-zA-Z0-9/]*) HTTP/\d.\d"')
    src_ip_re = re.compile(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}')
    datetime_re = re.compile(r'\[(\d{1,2})/([a-zA-Z]+)/(\d{4}):(\d{2}):(\d{2}):(\d{2}).*\]')

    print("source ip; datetime; http method; url ; resp_time; upstream_time; http_code")
    for line in open(path):
        src_ip = NOT_FOUND
        req_datetime = NOT_FOUND
        http_method = NOT_FOUND
        url = NOT_FOUND
        resp_time = NOT_FOUND
        upstream_time = NOT_FOUND
        http_code = NOT_FOUND

        resp_time_match = resp_time_re.search(line)
        if resp_time_match:
            resp_time = resp_time_match.group(0)

        upstream_time_match = upstream_time_re.search(line)
        if upstream_time_match:
            upstream_time = upstream_time_match.group(0)

        http_url_match = http_url_re.search(line)
        if http_url_match:
            http_method = http_url_match.group(1)
            url = http_url_match.group(2)

        src_ip_match = src_ip_re.search(line)
        if src_ip_match:
            src_ip = src_ip_match.group(0)

        datetime_match = datetime_re.search(line)
        if datetime_match:
            day = int(datetime_match.group(1))
            month_as_str = datetime_match.group(2)
            month = MONTH_NAME_DICT[month_as_str]
            year = int(datetime_match.group(3))
            hour = int(datetime_match.group(4))
            minute = int(datetime_match.group(5))
            second = int(datetime_match.group(6))
            req_datetime = datetime.datetime(year, month, day, hour, minute, second)



        print(";".join([src_ip, str(req_datetime), http_method, url, resp_time, upstream_time, http_code]))
            

if __name__ == "__main__":
    main()
