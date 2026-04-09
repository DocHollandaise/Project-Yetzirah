# FILE: seed_harvester.py
# Project: Yoga Fire (Project Yetzirah)
# Author: Doc Hollandaise
# Description: Automates the retrieval of CIF data from COD and converts to Suture Seed DNA.

import os
import json
import requests

class SeedHarvester:
    def __init__(self):
        self.base_url = "https://www.crystallography.net/cod/result"
        self.download_url = "https://www.crystallography.net/cod"
        self.output_dir = "seeds"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def search_mineral(self, name):
        """Finds COD IDs for a specific mineral name."""
        print(f"[*] Searching Seed Vault for: {name}...")
        # COD uses a simple GET search
        params = {
            'text': name,
            'format': 'json'
        }
        try:
            response = requests.get(f"{self.base_url}.json", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[!] Search failed: {e}")
            return []

    def harvest_seed(self, cod_id):
        """Downloads CIF and converts to Yoga Fire Seed JSON."""
        cif_url = f"{self.download_url}/{cod_id}.cif"
        print(f"[*] Harvesting {cod_id}...")
        
        try:
            cif_response = requests.get(cif_url)
            cif_response.raise_for_status()
            cif_data = cif_response.text
            
            # Simplified CIF Parsing (Targeting Unit Cell & Citations)
            seed = self.parse_cif_to_dna(cod_id, cif_data)
            
            filename = os.path.join(self.output_dir, f"{seed['seed_id']}.json")
            with open(filename, 'w') as f:
                json.dump(seed, f, indent=2)
            
            print(f"[+] Seed germinated: {filename}")
        except Exception as e:
            print(f"[!] Harvest failed for {cod_id}: {e}")

    def parse_cif_to_dna(self, cod_id, cif_text):
        """Extracts the math and the citations from raw CIF strings."""
        dna = {
            "seed_id": f"cod_{cod_id}",
            "metadata": {
                "source": "Crystallography Open Database",
                "cod_id": cod_id,
                "citation": "Unknown Publication"
            },
            "material_dna": {
                "mechanical": {"bulk_density": 0.0, "youngs_modulus": 0.0},
                "optical": {"refractive_index_base": 1.0}
            },
            "lattice_logic": {"unit_cell": {}}
        }

        # Regex-lite extraction for key CIF tags
        lines = cif_text.split('\n')
        for line in lines:
            if "_cell_length_a" in line: dna["lattice_logic"]["unit_cell"]["a"] = line.split()[-1]
            if "_cell_length_b" in line: dna["lattice_logic"]["unit_cell"]["b"] = line.split()[-1]
            if "_cell_length_c" in line: dna["lattice_logic"]["unit_cell"]["c"] = line.split()[-1]
            if "_publ_section_title" in line: dna["metadata"]["citation"] = line.split("'")[-1].strip("'")
            # Note: Density and Refractive Index often require secondary lookup or estimation from chemical formula
            
        return dna

if __name__ == "__main__":
    harvester = SeedHarvester()
    
    # Example: Grab the first 3 Quartz variants found
    results = harvester.search_mineral("Quartz")
    if results:
        # Taking top 3 to keep it clean
        for entry in results[:3]:
            harvester.harvest_seed(entry['file'])

# END FILE: seed_harvester.py
