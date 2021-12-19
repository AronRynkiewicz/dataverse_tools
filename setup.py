import argparse
import json

API = {}

parser = argparse.ArgumentParser()
parser.add_argument(
    "-at",
    "--api_token",
    type=str,
    required=False,
    help="Your api token.",
)

args = parser.parse_args()

API["API_TOKEN"] = args.api_token

with open("credentials.json", "w") as file:
    json.dump(API, file, indent=4)
print("API token added!")
