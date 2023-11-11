# -*- encoding: utf-8 -*-
import threading
import time
import os
import re
import tarfile

from datetime import datetime
from app import db
from app.base.models import Sfssum, ArrayMetric, Suffix

class DBThread(threading.Thread):
    
    def __init__(self, name, app):
        threading.Thread.__init__(self)
        self.name = name
        self.app = app
    
    def run(self):
        print("Starting " + self.name)
        while(True):
            print("{}: Collecting Data".format(self.name))
            with self.app.app_context():
                self.collect_logs()
                print("{}: Collecting Data Done".format(self.name))
                time.sleep(300)

    def collect_logs(self):
        log_path = self.app.config['SFS_LOG_PATH']
        l1 = os.listdir(log_path)
        for f1name in l1:
            if (os.path.isdir(log_path + os.sep + f1name)):
                l2 = os.listdir(log_path + os.sep + f1name)
                tar_log = ''
                sfssum_log = ''
                build_log = ''
                for fname in l2:
                    if (os.path.isfile(log_path + os.sep + f1name + os.sep + fname)):
                        #Full path
                        # 1. if sfsnum_<suffix>.txt
                        # print("Matching {}".format(fname))
                        match = re.match(r"sfssum_(.*).txt", fname)
                        if (match):
                            suffix = match.group(1)
                            sfssum_log = log_path + os.sep + f1name + os.sep + fname
                            build_log = log_path + os.sep + f1name + os.sep + "build"
                            self.parse_suffix(suffix, build_log)
                            self.parse_sfssum(sfssum_log, suffix)

                        match2 = re.match(r"(.*).tgz", fname)
                        if (match2):
                            suffix = match2.group(1)
                            tar_log = log_path + os.sep + f1name + os.sep + fname

                        match3 = re.match(r"(.*).csv", fname)
                        if (match3):
                            suffix = match3.group(1)
                            csv_log = log_path + os.sep + f1name + os.sep + fname
                            build_log = log_path + os.sep + f1name + os.sep + "build"
                            self.parse_suffix(suffix, build_log)
                            self.parse_ArrayMetric(csv_log, suffix)

                if (not sfssum_log and tar_log):
                    print("Extracting tgz log file {}".format(tar_log))
                    t = tarfile.open(tar_log)
                    t.extractall(log_path + os.sep + f1name)
                    os.remove(tar_log)
                    self.collect_logs()
                
    def parse_suffix(self, suffix, build_log):
        entry = Suffix.query.filter_by(suffix=suffix).first()
        buildid = "unknown"

        if entry:
            # print("Suffix {} already in database.".format(suffix))
            pass
        else:
            try:
                # suffix = 'v5.1.0.1.3.228_nfs_3_swbuild_test-20208302591'
                sfxa = re.split(r'-', suffix)
                dt = datetime.strptime(sfxa[-1],'%Y%m%d%H%M%S')
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                # v5.1.0.1.3.228_nfs_3_swbuild_test-20208302591
                with open(build_log, 'r') as f:
                    buildid = f.readline()

            except:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print("Adding Suffix entry: suffix = {}, Timestamp = {}, build = {}".format(suffix, timestamp, buildid))
                sfx = Suffix(suffix = suffix, Timestamp = timestamp, build = buildid, hidden = False)
                db.session.add(sfx)
                db.session.commit()
            except Exception as e:
                print("Some error happened: {}".format(e))


    def parse_sfssum(self, log, suffix):
        # print("Got SFS log file {}".format(log))
        # Add sfssum
        entry = Sfssum.query.filter_by(suffix=suffix).first()
        if entry:
            # print("Sfssum {} already in database.".format(suffix))
            pass
        else:
            with open(log, 'r') as f:
                for line in f.readlines():
                    # print(line)
                    s1 = re.search(r'^[ ]+\d+', line)
                    if(s1):
                        entry = re.split(r'[ ]+', line.strip())
                        valid = 'VALID_RUN'
                        if len(entry) > 16:
                            valid = 'INVALID_RUN'
                        try:
                            sum = Sfssum(
                                        suffix = suffix,
                                        BizMetric = entry[0],
                                        ReqOpRate = entry[1],
                                        AchiOpRate = entry[2],
                                        AvgLat = entry[3],
                                        TotalKBps = entry[4],
                                        RdKBps = entry[5],
                                        WrtKBps = entry[6],
                                        RunSec = entry[7],
                                        Cl = entry[8],
                                        ClProc = entry[9],
                                        AvgFileSizeKB = entry[10],
                                        ClDataSetMiB = entry[11],
                                        StartDataSetMiB = entry[12],
                                        InitFileSetMiB = entry[13],
                                        MaxFileSpaceMiB = entry[14],
                                        WorkloadName = entry[15],
                                        ValidRun = valid
                                        )
                            db.session.add(sum)
                            db.session.commit()
                        except Exception as e:
                            print("Some error happened: {}".format(e))
                        print("Biz metric {} is added to Table Sfssum for suffix {}".format(entry[0], suffix))


        
    
    def parse_ArrayMetric(self, log, suffix):
        # print("Got CSV log file {}".format(log))
        entry = ArrayMetric.query.filter_by(suffix=suffix).first()
        if entry:
            # print("ArrayMetric {} already in database.".format(suffix))
            pass
        else:
            with open(log, 'r') as f:
                for line in f.readlines():
                    # print(line)
                    s1 = re.search(r'^\d+', line)
                    if(s1):
                        entry = re.split(r',', line.strip())
                        try:
                            metric = ArrayMetric(
                                            suffix = suffix,
                                            Timestamp = entry[0],
                                            SpaCpu = entry[1],
                                            SpbCpu = entry[2],
                                            SpaTotalIOPS = entry[3],
                                            SpbTotalIOPS = entry[4],
                                            SpaAvgIOPS = entry[5],
                                            SpbAvgIOPS = entry[6],
                                            SpaRdKBPS = entry[7],
                                            SpbRdKBPS = entry[8],
                                            SpaWrtKBPS = entry[9],
                                            SpbWrtKBPS = entry[10],
                                            SpaAvgRdSize = entry[11],
                                            SpbAvgRdSize = entry[12],
                                            SpaAvgWrtSize = entry[13],
                                            SpbAvgWrtSize = entry[14]
                                        )
                            db.session.add(metric)
                            db.session.commit()
                        except Exception as e:
                            print("Some error happened: {}".format(e))
                        print("Array Metric on {} is added to Table ArrayMetric for suffix {}".format(entry[0], suffix))
