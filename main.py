from google.cloud import compute_v1
from google.api_core.exceptions import Conflict

PROJECT_ID = "pytthon-auto"


def create_vpc(project_id):
    client = compute_v1.NetworksClient()

    network = compute_v1.Network(
        name="prod-vpc",
        auto_create_subnetworks=False,
        routing_config=compute_v1.NetworkRoutingConfig(
            routing_mode="REGIONAL"
        ),
    )

    try:
        client.insert(project=project_id, network_resource=network)
        print("Creating VPC: prod-vpc")
    except Conflict:
        print("VPC prod-vpc already exists — skipping")


def create_subnet(project_id, region, name, cidr):
    client = compute_v1.SubnetworksClient()

    subnet = compute_v1.Subnetwork(
        name=name,
        ip_cidr_range=cidr,
        network=f"projects/{project_id}/global/networks/prod-vpc",
        region=region,
    )

    try:
        client.insert(
            project=project_id,
            region=region,
            subnetwork_resource=subnet,
        )
        print(f"Creating subnet {name} in {region}")
    except Conflict:
        print(f"Subnet {name} already exists in {region} — skipping")


if __name__ == "__main__":
    print("\n=== PHASE 2: NETWORK SETUP ===")

    create_vpc(PROJECT_ID)

    create_subnet(
        PROJECT_ID,
        "us-central1",
        "prod-subnet-us",
        "10.10.0.0/24",
    )

    create_subnet(
        PROJECT_ID,
        "europe-west1",
        "prod-subnet-eu",
        "10.20.0.0/24",
    )

    print("\n=== NETWORK SETUP COMPLETE ===")
