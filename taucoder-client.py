#!/usr/bin/env python3

import os
import argparse
import requests
import json
import base64
import mimetypes
import time


def connection(apikey):
    base_url = f'https://taucoder.com/api/v1'

    base64_apikey = base64.b64encode(str.encode(apikey)).decode('ascii')
    headers = {
        'Authorization': f'Basic {base64_apikey}'
    }

    return base_url, headers

def create_job(conn, input_file_list):
    base_url, headers = conn

    formfields = [
        ('options', (None, json.dumps({"encoder_version": "latest", "quality": 50}))),
    ]

    for input_file in input_file_list:
        mime_type, _ = mimetypes.guess_type(input_file)
        formfields.append(
            ('image', (input_file, open(input_file, 'rb'), mime_type))
        )

    response = requests.post(base_url + "/job-create", headers=headers, files=formfields)
    response.raise_for_status()
    return response.status_code, response.json()

def get_job_status(conn, job_id_list):
    base_url, headers = conn
    response = requests.post(base_url + "/job-status", headers=headers, json={"job_ids": job_id_list})
    response.raise_for_status()
    return response.status_code, response.json()

def download_job(job, output):
    job_id = job["job_id"]
    download_url = job["output_url"]
    output_file = os.path.join(output, f"{job['input_filename']}-{job_id}.jpg" ) if os.path.isdir(output) else output
    print(f'Job {job_id} is done. Downloading to {output_file}...')
    response = requests.get(download_url)
    response.raise_for_status()
    with open(output_file, 'wb') as f:
        f.write(response.content)
    print("Downloaded")

def main(apikey, input_file_list, output):
    conn = connection(apikey)

    print("creating new jobs...")
    status_code, response_json = create_job(conn, input_file_list)

    if status_code != 200:
        print(f'Error: {response_json["error"]}')
        return

    print("jobs created. waiting for jobs to finish...")

    downloaded_jobs = set()
    job_id_list = [job["job_id"] for job in response_json["jobs"]]

    while len(downloaded_jobs) < len(job_id_list):
        time.sleep(5)
        status_code, response_json = get_job_status(conn, job_id_list)
        if status_code != 200:
            print(f'Error: {response_json["error"]}')
            continue

        for job in response_json["jobs"]:
            if job["job_id"] in downloaded_jobs:
                continue
            elif job["status"] == "error":
                print(f'Job {job["job_id"]} failed')
                downloaded_jobs.add(job["job_id"])
            elif job["status"] == "done":
                download_job(job, output)
                downloaded_jobs.add(job["job_id"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='taucoder test client')
    parser.add_argument('--apikey', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('input', type=str, nargs='+')

    args = parser.parse_args()

    if not args.apikey:
        print("Error: apikey is required")
        exit(1)

    if not os.path.isdir(args.output):
        print("Error: output must be a directory")
        exit(1)

    if len(args.input) == 0:
        print("Error: input files are required")
        exit(1)

    main(args.apikey, args.input, args.output)