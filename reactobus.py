#!/usr/bin/python3

import argparse
import itertools
import logging
import signal
import sys
import yaml

from lib.core import Core


FORMAT = "%(asctime)-15s %(levelname)7s %(name)s %(message)s"
LOG = logging.getLogger("ROB")


def configure_logger(log_file, level):
    if level == "ERROR":
        LOG.setLevel(logging.ERROR)
    elif level == "WARN":
        LOG.setLevel(logging.WARN)
    elif level == "INFO":
        LOG.setLevel(logging.INFO)
    else:
        LOG.setLevel(logging.DEBUG)

    if log_file == "-":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(log_file, "a")
    handler.setFormatter(logging.Formatter(FORMAT))
    LOG.addHandler(handler)


def configure_pipeline(conffile):
    from lib import inputs
    from lib import outputs

    LOG.info("Creating the pipeline")
    with open(conffile) as f_in:
        conf = yaml.load(f_in)

    # Parse inputs
    LOG.debug("Inputs:")
    ins = []
    outs = []
    for i in conf["inputs"]:
        LOG.debug("- %s (%s)", i["class"], i["name"])
        new_in = inputs.Input.select(i["class"], i["name"],
                                     i.get("options", {}),
                                     conf["core"]["inbound"])
        ins.append(new_in)

    LOG.debug("Outputs:")
    for o in conf["outputs"]:
        LOG.debug("- %s (%s)", o["class"], o["name"])
        new_out = outputs.Output.select(o["class"], o["name"],
                                        o.get("options", {}),
                                        conf["core"]["outbound"])
        outs.append(new_out)

    return (ins, Core(conf["core"]["inbound"], conf["core"]["outbound"]), outs)


def start_pipeline(inputs, core, outputs):
    LOG.info("Setting-up the pipeline")
    # Ignore the signals in the sub-processes. The main process will take care
    # of the propagation

    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start the core
    core.start()

    # Start the stages
    for i in inputs:
        i.start()
    for o in outputs:
        o.start()

    # Restaure the default signal handler
    signal.signal(signal.SIGINT, default_handler)


def main():
    # Parse the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", default="/etc/reactobus.yaml",
                        help="ReactOBus configuration")
    loggrp = parser.add_argument_group('Logging')
    loggrp.add_argument("-l", "--level", default="INFO", type=str,
                        choices=["DEBUG", "ERROR", "INFO", "WARN"],
                        help="Log level (DEBUG, ERROR, INFO, WARN), default to INFO")
    loggrp.add_argument("--log-file", default="-", type=str,
                        help="Log file, use '-' for stdout")

    options = parser.parse_args()

    # Configure everything
    configure_logger(options.log_file, options.level)
    (inputs, core, outputs) = configure_pipeline(options.conf)

    # Setup and start the pipeline
    start_pipeline(inputs, core, outputs)

    # Wait for a signal and then quit
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass

    LOG.info("Signal received, leaving")

    # Wait for all threads
    for t in itertools.chain([core], inputs, outputs):
        t.terminate()
        t.join()


if __name__ == '__main__':
    main()
