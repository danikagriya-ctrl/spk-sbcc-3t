import os
import sys

# Tambahkan direktori root proyek ke sys.path agar modul app dapat diimport
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.reasoning.diagnosis_combo import DiagnosisEngine
from app.reasoning.intervention_bcw import InterventionMapper
from app.reasoning.context_3t import Context3TFilter
from app.reasoning.composer_sbcc import MessagePlanComposer

def test_diagnosis_and_mapping_flow():
    # Inisialisasi engine
    dx_engine = DiagnosisEngine()
    mapper = InterventionMapper()
    filter_3t = Context3TFilter()
    composer = MessagePlanComposer()

    # Skenario: Sasaran Remaja Putri tidak minum TTD
    # Hambatan: Takut efek samping (mual), kurang tahu manfaat, tapi sarana tersedia di sekolah
    signals = {
        "tidak_tahu_manfaat": True,
        "takut_efek_samping": True,
        "sarana_tersedia": True,
        "sarana_tidak_tersedia": False,
        "akses_jauh_atau_biaya_mahal": False
    }
    behavior_status = "tetap_tidak_dilakukan"

    # 1. Jalankan Diagnosis
    dx_result = dx_engine.diagnose(signals, behavior_status)
    assert "C-Ps" in dx_result["deficits"]  # Karena tidak_tahu_manfaat = True
    assert "M-Au" in dx_result["deficits"]  # Karena takut_efek_samping = True
    assert "O-Ph" not in dx_result["deficits"] # Karena sarana_tersedia = True, maka O-Ph dideprioritaskan

    # 2. Jalankan Pemetaan Intervensi
    bcw_result = mapper.map_interventions(dx_result["deficits"])
    functions = [f["function"] for f in bcw_result["functions"]]
    assert "Education" in functions  # Karena C-Ps defisit
    assert "Persuasion" in functions  # Karena M-Au defisit

    # 3. Jalankan Penyaringan Konteks 3T (Skenario: Tidak ada internet, listrik padam, tokoh guru)
    profile_3t = {
        "konektivitas_internet": "tidak_ada",
        "listrik": "tidak_stabil",
        "bahasa_dominan": "Sunda",
        "literasi": "sedang",
        "kanal_terpercaya": ["guru"],
        "akses_layanan": "dekat",
        "audience": "Remaja Putri"
    }
    t3_result = filter_3t.apply_filter(bcw_result["functions"], profile_3t)
    # Harus membuang media sosial dan video sosialisasi
    assert "media_sosial" not in t3_result["eligible_channels"]
    assert "video_sosialisasi" not in t3_result["eligible_channels"]
    assert "poster_cetak" in t3_result["eligible_channels"]
    assert "Guru Sekolah (UKS / Wali Kelas)" in t3_result["mobilizers"]
    assert t3_result["translate_required"] is True

    # 4. Jalankan Composer Rencana SBCC
    plan = composer.compose_plan(
        topic="tablet_tambah_darah",
        audience="Remaja Putri",
        functions=bcw_result["functions"],
        filter_3t_result=t3_result
    )
    assert len(plan["message_slots"]["know"]) > 0
    assert "Guru Sekolah (UKS / Wali Kelas)" in plan["four_ms"]["mobilizers"]
    
    print("Semua uji unit untuk core reasoning engine SPK-SBCC 3T BERHASIL!")

if __name__ == "__main__":
    test_diagnosis_and_mapping_flow()
