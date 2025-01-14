#!/usr/bin/env python
import json
import glob
import numpy as np
import tqdm
import os
import argparse
def main():
    parser = argparse.ArgumentParser(prog="Trace combing")
    parser.add_argument("--log_dir", default="./", help="Directory where the trace is stored")
    parser.add_argument("--output", default="trace.pfw", help="output combined trace filename")
    args = parser.parse_args()
    nf = glob.glob(f"{args.log_dir}/.trace*.pfw")
    if (len(nf==0)):
        raise Exception(f"No trace files found in the log_dir specfied: {args.log_dir}")
    print(f"Total number of traces: {len(nf)}")
    data = []
    for f in tqdm.tqdm(np.sort(nf)):
        cmd = "sed \"s/}}/}},/g\" %s > %s" %(f, f+".tmp")
        os.system(cmd)
        cmd = "sed -i '$ s/}},/}}/' %s" %(f+".tmp")
        os.system(cmd)
    with open(f+".tmp", "a") as fin:
        fin.write("]")
    with open(f+".tmp", "r") as fin:
        data = data+json.load(fin)
    with open(args.output, "w") as fin:
        json.dump(data, fin)


if __name__=="__main__":
    main()
