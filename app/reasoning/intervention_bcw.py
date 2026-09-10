import os
import json

class InterventionMapper:
    def __init__(self, kb_dir=None):
        if not kb_dir:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_dir = os.path.join(current_dir, "../../knowledge_base")
        
        self.bcw_path = os.path.join(kb_dir, "kb_bcw_map.json")
        self.bcw_data = self._load_json(self.bcw_path)
        self.com_b_to_functions = self.bcw_data.get("com_b_to_functions", {})
        self.functions_to_policy = self.bcw_data.get("functions_to_policy", {})
        self.function_definitions = self.bcw_data.get("function_definitions", {})

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File basis pengetahuan tidak ditemukan: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def map_interventions(self, deficits):
        """
        Memetakan defisit COM-B ke Fungsi Intervensi BCW dan Kategori Kebijakan pendukung.
        deficits: list berisi kode komponen COM-B yang defisit (misal: ["C-Ps", "M-Au"])
        """
        recommended_functions = set()
        function_rationale = {}
        recommended_policies = set()
        policy_rationale = {}

        # 1. Peta COM-B -> Fungsi Intervensi
        for deficit in deficits:
            funcs = self.com_b_to_functions.get(deficit, [])
            for func in funcs:
                recommended_functions.add(func)
                if func not in function_rationale:
                    function_rationale[func] = []
                function_rationale[func].append(f"Membantu mengatasi defisit '{deficit}' ({self._get_component_name(deficit)})")

        # 2. Peta Fungsi Intervensi -> Kategori Kebijakan
        for func in recommended_functions:
            policies = self.functions_to_policy.get(func, [])
            for policy in policies:
                recommended_policies.add(policy)
                if policy not in policy_rationale:
                    policy_rationale[policy] = []
                policy_rationale[policy].append(f"Mendukung pelaksanaan fungsi intervensi '{func}'")

        # 3. Bentuk detail fungsi intervensi beserta definisi dan contohnya
        functions_detail = []
        for func in sorted(recommended_functions):
            def_info = self.function_definitions.get(func, {"definition": "-", "example": "-"})
            functions_detail.append({
                "function": func,
                "definition": def_info["definition"],
                "example": def_info["example"],
                "rationale": function_rationale.get(func, [])
            })

        # Urutkan fungsi intervensi berdasarkan jumlah cakupan defisit yang diatasi (sebagai bobot prioritas)
        functions_detail.sort(key=lambda x: len(x["rationale"]), reverse=True)

        return {
            "functions": functions_detail,
            "policies": sorted(list(recommended_policies)),
            "policy_rationale": policy_rationale
        }

    def _get_component_name(self, code):
        names = {
            "C-Ph": "Physical Capability",
            "C-Ps": "Psychological Capability",
            "O-Ph": "Physical Opportunity",
            "O-So": "Social Opportunity",
            "M-Re": "Reflective Motivation",
            "M-Au": "Automatic Motivation"
        }
        return names.get(code, code)
