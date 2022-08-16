"""
Backend for CCS Annotator
"""

import argparse, re
import json
import logging

import uvicorn

from DigitalFootprintsBackend.api import app

from DigitalFootprintsBackend.crud import crud_project
from DigitalFootprintsBackend.database import SessionLocal
from DigitalFootprintsBackend.auth import get_token, verify_token, hash_password, verify_password

def run(args):
    logging.info(f"Starting server at port {args.port}, reload={not args.noreload}")
    uvicorn.run("DigitalFootprintsBackend.api:app", host="0.0.0.0", port=args.port, reload=not args.noreload)
   
def create_project(args):
    db = SessionLocal()
    p = crud_project.create_project(db, args.project, args.password)
    if p:
        print(p.name)
        print(p.password)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--verbose", "-v", help="Verbose (debug) output", action="store_true", default=False)
subparsers = parser.add_subparsers(dest="action", title="action", help='Action to perform:', required=True)

p = subparsers.add_parser('run', help='Run the annotator in dev mode')
p.add_argument("-p", '--port', help='Port', default=5000)
p.add_argument("--no-reload", action='store_true', dest='noreload', help='Disable reload (when files change)')
p.set_defaults(func=run)

p = subparsers.add_parser('create_project', help='Create a project')
p.add_argument("project", help='Name of the new project')
p.add_argument("password", help='Password of the new project')



p.set_defaults(func=create_project)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                    format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

args.func(args)
