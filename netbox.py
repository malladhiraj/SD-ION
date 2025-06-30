import pynetbox
import csv
import re

NETBOX_URL = "http://192.168.2.218:9000"  # e.g., "http://localhost:8000"
NETBOX_TOKEN = "3538fd7b70bdd9f49fa9a28db099ee1d1a3894b6"

nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)

def slugify(name):
    # Lowercase, replace spaces with hyphens, remove non-alphanumeric except hyphens
    slug = name.lower().replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug

DEVICE_TYPE = "ION"  # Change as needed
DEVICE_ROLE = "Branch"  # Change as needed
MANUFACTURER = "Palo Alto"  # Change as needed

with open("MasterTemplate.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        site_name = row["site_name"]
        slug = slugify(site_name)
        existing = nb.dcim.sites.get(name=site_name)
        if existing:
            print(f"Site '{site_name}' already exists, skipping.")
            continue

        # Map standard fields
        site_data = {
            "name": site_name,
            "slug": slug,
            "physical_address": row.get("street", ""),
            "description": row.get("city", ""),  # Example: use city as description
        }

        # If you use regions in NetBox, map region by name (must exist in NetBox)
        if "state" in row and row["state"]:
            region = nb.dcim.regions.get(name=row["state"])
            if region:
                site_data["region"] = region.id

        # Add all other fields as custom fields (must exist in NetBox)
        custom_fields = {}
        for k, v in row.items():
            if k not in ["site_name", "street", "city", "state"]:
                custom_fields[k] = v
        if custom_fields:
            site_data["custom_fields"] = custom_fields

        site = nb.dcim.sites.create(**site_data)
        print(f"Created site: {site_name}")

        # Get device type, role, manufacturer objects
        device_type = nb.dcim.device_types.get(model=DEVICE_TYPE)
        device_role = nb.dcim.device_roles.get(name=DEVICE_ROLE)
        manufacturer = nb.dcim.manufacturers.get(name=MANUFACTURER)

        if not device_type or not device_role or not manufacturer:
            print(f"Device type, role, or manufacturer not found in NetBox, skipping.")
            continue

        # Create device for ion_serial_number_1
        serial1 = row.get("ion_serial_number_1", "")
        if serial1:
            device_name_1 = f"{site_name}-ION1"
            existing_1 = nb.dcim.devices.get(name=device_name_1)
            if not existing_1:
                nb.dcim.devices.create(
                    name=device_name_1,
                    device_type=device_type.id,
                    device_role=device_role.id,
                    site=site.id,
                    serial=serial1,
                    manufacturer=manufacturer.id,
                    # Add more standard fields as needed
                )
                print(f"Created device: {device_name_1}")
            else:
                print(f"Device '{device_name_1}' already exists, skipping.")

        # Create device for ion_serial_number_2 (if present)
        serial2 = row.get("ion_serial_number_2", "")
        if serial2:
            device_name_2 = f"{site_name}-ION2"
            existing_2 = nb.dcim.devices.get(name=device_name_2)
            if not existing_2:
                nb.dcim.devices.create(
                    name=device_name_2,
                    device_type=device_type.id,
                    device_role=device_role.id,
                    site=site.id,
                    serial=serial2,
                    manufacturer=manufacturer.id,
                    # Add more standard fields as needed
                )
                print(f"Created device: {device_name_2}")
            else:
                print(f"Device '{device_name_2}' already exists, skipping.")