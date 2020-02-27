import datetime
import subprocess
import smtplib
import os


def send_email(text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("actionchase@gmail.com", "lnkyaliduvshwicn")
    try:
        server.sendmail("actionchase@gmail.com", "grrapport@gmail.com", text)
    except Exception as e:
        print(e)


def kill_and_restart_service():
    # get list of processes and finds process id for the running script NcaabLineGetter.py
    p = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    process_string = str(p.communicate()[0], 'utf-8').splitlines()
    for proc in process_string:
        if "NcaabLineGetter.py" in proc:
            process_id = int(proc.split(" ")[1])

    # get the end of the log file
    p = subprocess.Popen(["tail", "/home/grrapport/workspace/ncaab_lines.log"], stdout=subprocess.PIPE)
    print("Getting end of log file")
    end_log = str(p.communicate()[0], 'utf-8')

    # kill the process
    if process_id is not None and process_id != 0:
        subprocess.call(["kill", str(process_id)])
        print("Killing stale process")

    # delete the log file for cleanup
    subprocess.call(["rm", "/home/grrapport/workspace/ncaab_lines.log"])
    print("Deleting old log file")

    # restart the process
    subprocess.Popen(["nohup", "python3", "/home/grrapport/workspace/Line-Tracking/NcaabLineGetter.py",
                          ">>", "/home/grrapport/workspace/ncaab_lines.log",
                          "2>&1", "&"],
                     stdout=open('/home/grrapport/workspace/ncaab_lines.log', 'w'),
                     stderr=open('/home/grrapport/workspace/ncaab_lines.log', 'a'),
                     preexec_fn=os.setpgrp
                     )
    # nohup python3 /home/grrapport/workspace/Line-Tracking/NcaabLineGetter.py >> /home/grrapport/workspace/ncaab_lines.log 2>&1 &


    # compose email with info of service restart
    email_str = "NCAAB Line Getter Service Restarted"
    email_str += "\n\n End of log: \n" + end_log
    print(email_str)
    send_email(email_str)


try:
    # get last modified time of log file, and check to see how long it has been
    p = subprocess.Popen(["stat", "/home/grrapport/workspace/ncaab_lines.log"], stdout=subprocess.PIPE)
    logfile_stat = str(p.communicate()[0], 'utf-8').splitlines()
    for prop in logfile_stat:
        print(prop)
        if "Modify" in prop:
            parts = prop.replace("Modify:", "")
            date_part = parts.split(" +")
            date_spec_part = date_part[0].strip()
            date_spec_part = "2020-02-26 03:35:46.443139896"
            date_string = date_spec_part.split(".")[0]
            last_modified = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            break

    if last_modified < datetime.datetime.now() - datetime.timedelta(minutes=6):
        kill_and_restart_service()
except Exception as e:
    fail_email = "Service restarter has failed with the following exception: \n\n"
    fail_email += str(e)
    send_email(fail_email)

