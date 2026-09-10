class Context3TFilter:
    def __init__(self):
        pass

    def apply_filter(self, functions, profile_3t):
        """
        Menyaring dan mengadaptasi fungsi intervensi dan rencana komunikasi berdasarkan profil 3T.
        functions: list of dict dari InterventionMapper.map_interventions
        profile_3t: dict berisi variabel profil daerah 3T:
            - konektivitas_internet: "tidak_ada" | "lemah" | "memadai"
            - listrik: "tidak_stabil" | "stabil"
            - bahasa_dominan: "Indonesia" | "bahasa_daerah" (nama daerah spesifik)
            - literasi: "rendah" | "sedang" | "tinggi"
            - kanal_terpercaya: list of string, e.g. ["guru", "tokoh_agama"]
            - akses_layanan: "jauh" | "sedang" | "dekat"
        """
        notes = []
        warnings = []
        
        # 1. Tentukan kelayakan Multipliers (Kanal Penyebaran)
        internet = profile_3t.get("konektivitas_internet", "memadai")
        listrik = profile_3t.get("listrik", "stabil")
        
        eligible_channels = []
        
        if internet == "tidak_ada":
            eligible_channels.extend(["kunjungan_rumah", "pertemuan_tatap_muka", "poster_cetak", "pengumuman_rumah_ibadah", "radio_komunitas"])
            notes.append("Konektivitas internet TIDAK ADA: Menonaktifkan semua kanal digital (media sosial, aplikasi web, video streaming). Mengutamakan media luar ruang cetak dan komunikasi tatap muka.")
        elif internet == "lemah":
            eligible_channels.extend(["pertemuan_tatap_muka", "pesan_singkat_sms_wa", "poster_cetak", "radio_komunitas"])
            notes.append("Konektivitas internet LEMAH: Membatasi penggunaan media digital berat (video streaming). Mengutamakan komunikasi teks ringan (WhatsApp/SMS) dan media cetak.")
        else:
            eligible_channels.extend(["media_sosial", "aplikasi_web", "video_sosialisasi", "pertemuan_tatap_muka", "poster_cetak"])
            notes.append("Konektivitas internet memadai: Kanal digital dapat digunakan secara optimal.")

        if listrik == "tidak_stabil":
            # Hapus media elektronik yang butuh daya kontinu
            if "video_sosialisasi" in eligible_channels:
                eligible_channels.remove("video_sosialisasi")
            eligible_channels.append("kegiatan_interpersonal")
            notes.append("Listrik TIDAK STABIL: Menghindari pemutaran video elektronik terjadwal di posyandu/puskesmas. Mengutamakan selebaran/materi cetak fisik.")

        # 2. Lokalisasi bahasa
        bahasa = profile_3t.get("bahasa_dominan", "Indonesia")
        translate_required = bahasa != "Indonesia"
        if translate_required:
            notes.append(f"Bahasa dominan adalah '{bahasa}': Pesan wajib diterjemahkan/dilokalkan menggunakan dialek dan idiom daerah setempat.")
        
        # 3. Format materi berdasarkan tingkat literasi
        literasi = profile_3t.get("literasi", "tinggi")
        material_formats = []
        if literasi == "rendah":
            material_formats.extend(["visual_dominan", "audio_lisan", "storytelling_dongeng"])
            notes.append("Tingkat literasi RENDAH: Mengurangi teks padat. Desain materi wajib didominasi gambar/ilustrasi dan disampaikan secara lisan atau cerita/demonstrasi praktis.")
        elif literasi == "sedang":
            material_formats.extend(["visual_dan_teks_sederhana", "lisan"])
            notes.append("Tingkat literasi SEDANG: Menggunakan perpaduan gambar dan kalimat pendek yang mudah dimengerti.")
        else:
            material_formats.extend(["teks_lengkap", "infografis_detail"])
            notes.append("Tingkat literasi TINGGI: Dapat menggunakan infografis detail dengan teks penjelas yang lengkap.")

        # 4. Tentukan Mobilizers tepercaya
        trusted_sources = profile_3t.get("kanal_terpercaya", [])
        mobilizers = []
        for src in trusted_sources:
            if src == "tokoh_agama":
                mobilizers.append("Tokoh Agama setempat (Ustadz/Pendeta/Pastor)")
            elif src == "tokoh_adat":
                mobilizers.append("Kepala Adat / Tokoh Adat Desa")
            elif src == "guru":
                mobilizers.append("Guru Sekolah (UKS / Wali Kelas)")
            elif src == "tenaga_kesehatan":
                mobilizers.append("Bidan Desa / Petugas Puskesmas / Kader Posyandu")
            elif src == "peer":
                mobilizers.append("Kader Remaja Sebaya / Sahabat Dekat")
            else:
                mobilizers.append(src)
                
        if not mobilizers:
            mobilizers = ["Kader Posyandu / Bidan Desa"]
            notes.append("Kanal tepercaya kosong: Menggunakan kader posyandu/bidan desa sebagai default mobilizer.")
        else:
            notes.append(f"Kanal kepercayaan teridentifikasi: Melibatkan {', '.join(mobilizers)} sebagai komunikator utama.")

        # 5. Cek Akses Layanan untuk Advokasi
        akses = profile_3t.get("akses_layanan", "dekat")
        if akses == "jauh":
            warnings.append("Hambatan Fisik Terdeteksi: Lokasi akses layanan kesehatan sangat jauh dari pemukiman warga. Disarankan merekomendasikan advokasi tingkat desa (Service Provision) berupa layanan Puskesmas Keliling atau Posyandu jemput bola.")

        return {
            "eligible_channels": eligible_channels,
            "mobilizers": mobilizers,
            "material_formats": material_formats,
            "translate_required": translate_required,
            "target_language": bahasa,
            "notes": notes,
            "warnings": warnings
        }
