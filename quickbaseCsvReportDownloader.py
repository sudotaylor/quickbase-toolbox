#!/usr/bin/env python3
# Quickbase CSV Report Downloader
# Download .csv files from tables using 'qid' strings.

from requests import Session
from time import sleep
from random import random
from os.path import join, isfile


######### User-specified values #########      ## THESE ARE EXAMPLES -- FILL WITH INFORMATION USED IN YOUR APP
loginid = 'example@example.com'
password = 'SecretPassword1234'
base_url = 'https://example.quickbase.com'
download_dir = 'Downloads/'
sleep_timer_seconds = random()*3 + 2 # wait 2-5 seconds
tables: dict[str, str] = {                     ## THESE ARE EXAMPLES -- FILL WITH INFORMATION USED IN YOUR APP
    # [TABLE_NAME: TABLE_URL_STRING]
    'Clients': 'ba897fdkj',
    'Products': 'bn6lue3o7',
    'Sales': 'b5pomv73a'
}
download_requests: list[list] = [              ## THESE ARE EXAMPLES -- FILL WITH INFORMATION USED IN YOUR APP
    # [TABLE_NAME, REPORT_QID, ?FILENAME]
    ['Clients', -1000000], # will use a default filename if not specified
    ['Products', 47, 'products__47.csv'],
    ['Clients', 13, 'clients__13.csv']
]
#########################################



########### Quickbase Setting ###########
payload: dict[str, str] = {
    'loginid': loginid,
    'password': password
}
signin_url = base_url + '/db/main?a=SignIn'
#########################################

def download(session: Session, target_url: str, filename: str) -> str | None:
    if target_url == "":
        print("No URL specified. Nothing to download.")
        return
    if filename == "":
        filename: str = target_url.split('/')[-1].split('?')[0] + ".csv"
    filename = join(download_dir, filename)
    with session.get(target_url, stream=True) as response:
        response.raise_for_status()
        if isfile(filename):
            count = 1
            while True:
                if isfile(filename + '(' + count + ')'):
                    count += 1
                else:
                    filename = filename + '(' + count + ')'
                    break
        with open(filename, 'wb') as filestream:
            for chunk in response.iter_content(chunk_size=10*1024):
                filestream.write(chunk)
        return filename

def process_request(request: list) -> list[str]:
    if len(request) == 2:
        return [base_url + '/db/' + tables[request[0]] + '?a=q&qid=' + str(request[1]) + '&dlta=xs', ''] # '&opts=csv'
    elif len(request) == 3:
        return [base_url + '/db/' + tables[request[0]] + '?a=q&qid=' + str(request[1]) + '&dlta=xs', str(request[2])] # '&opts=csv'
    else:
        print("Could not process request '" + request + "'")
        return ["", ""]

def main() -> None:
    with Session() as session:
        session.post(signin_url, data=payload)
        print("Connection established.\n")
        for req in download_requests:
            sleep(sleep_timer_seconds)
            print("Downloading '" +  str(req[1]) + "' from '" + req[0] + "'\n")
            args: list[str] = process_request(req)
            download(session, args[0], args[1])


if __name__ == '__main__':
    main()
