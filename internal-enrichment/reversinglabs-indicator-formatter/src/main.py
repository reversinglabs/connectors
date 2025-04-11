import os
import re
import json
from typing import Dict
import stix2
from lib.internal_enrichment import InternalEnrichmentConnector
from pycti import (
    STIX_EXT_OCTI_SCO,
    Identity,
    Indicator,
    Malware,
    Note,
    OpenCTIConnectorHelper,
    StixCoreRelationship,
)


class ReversingLabsIndicatorFormatterConnector(InternalEnrichmentConnector):
    def __init__(self):
        super().__init__()
        self._get_config_variables()
        self.reversinglabs_identity = self.helper.api.identity.create(
            type="Organization",
            name="ReversingLabs",
            description="www.reversinglabs.com"
        )

    def _get_config_variables(self):
        self.helper.log_info(f"{self.helper.connect_name}: Reading configuration env variables!")
        self.connector_name = os.environ.get("CONNECTOR_NAME", None)
        self.opencti_url = os.environ.get("OPENCTI_URL", None)
        self.opencti_token = os.environ.get("OPENCTI_TOKEN", None)

    def _process_message(self, data: Dict):
        stix_entity = data["stix_entity"]
        self.helper.log_info(f"Incoming STIX entity:\n{json.dumps(stix_entity, indent=2)}")

        if not stix_entity or stix_entity["type"] != "indicator":
            self.helper.log_info("Skipping non-Indicator entity")
            return

        indicator_id = stix_entity["id"]
        pattern = stix_entity.get("pattern")[1:-1]

        value = None


        if "file:hashes" in pattern:

            components = pattern.split("OR")
            for comp in components:
                comp = comp.strip()
                match = re.search(r"SHA-1\s*=\s*'([^']+)'", comp)
                if match:
                    candidate = match.group(1)
                    if len(candidate) == 40:
                        value = candidate
                        break
        else:
            supported_types = {"ipv4-addr", "domain-name", "url"}
            components = pattern.split("OR")
            for comp in components:
                comp = comp.strip()
                match = re.match(r"([\w\-]+):value\s*=\s*'([^']+)'", comp)
                if match:
                    obs_type = match.group(1)
                    candidate = match.group(2)
                    if obs_type in supported_types:
                        value = candidate
                        break

        if not value:
            self.helper.log_info(f"Could not extract a valid name from the pattern of {indicator_id}")
            return

        self.helper.log_info(f"Updating indicator {indicator_id} name to '{value}'")
        self.helper.api.stix_domain_object.update_field(
            id=indicator_id,
            input={"key": "name", "value": value},
        )


if __name__ == "__main__":
    try:
        ReversingLabsIndicatorFormatterConnector().start()
    except Exception as e:
        print(f"[ERROR] Connector crashed: {e}")
