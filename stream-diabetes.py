import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pickle
import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
from streamlit_option_menu import option_menu

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie'] ['name'],
    config['cookie'] ['key'],
    config['cookie'] ['expiry_days'],
    config['pre-authorized']
)

left_pane, right_pane = st.columns(2)
with left_pane:
    name, state, username = authenticator.login()
with right_pane:
    if not st.session_state["authentication_status"]:
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)

if st.session_state["authentication_status"]:
    

    #programnya masuk sini
    with open('scaler.sav', "rb") as f:
        scaler = pickle.load(f)

    #navigasi sidebar
    with st.sidebar :
        selected = option_menu('GlucoCare Apps', 
        ['Hitung Prediksi Diabetes',
        'Chatbot',
        'Setting'
        ],
        default_index=0)


    #halaman Hitung Prediksi Diabetes
    if(selected == 'Hitung Prediksi Diabetes') :
        #membaca model
        diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

        #judul web
        st.title('Hitung Prediksi Diabetes')

        #membagi kolom
        col1, col2 = st.columns(2)

        with col1 :
            Glucose = st.text_input ('masukkan nilai Kadar Gula')

        with col2 :
            BloodPressure = st.text_input ('masukkan nilai Tekanan Darah')

        with col1 :
            BMI = st.text_input ('masukkan nilai BMI')

        with col2 :
            Age = st.text_input ('masukkan nilai Umur')

        #code untuk prediksi
        diab_diagnosis = ''

        #membuat tombol untuk prediksi
        if st.button('Hitung Result'):
            x=(Glucose, BloodPressure, BMI, Age)
            x=np.array(x)
            x=x.reshape(1,-1)
            x=scaler.transform(x)
            diab_prediction = diabetes_model.predict(x)

            st.write(diab_prediction)
            if(diab_prediction[0] == 1):
                diab_diagnosis = 'Pasien terkena Diabetes'
            else :
                diab_diagnosis = 'Pasien tidak terkena Diabetes'
   
            st.success(diab_diagnosis)


    #halaman Chatbot
    if(selected == 'Chatbot'):
        st.title('Chatbot')

                # Fungsi respons Chatbot sederhana
        def chatbot_response(user_input):
                # daftar beberapa respons
                responses = {
                    "hello": "Hi there! apa yang bisa saya bantu hari ini?",
                    "hi": "Hello! apa yang bisa saya bantu?",
                    "bye": "Goodbye! Have a great day!",
                    "apa itu diabetes?": "Diabetes adalah kondisi medis di mana kadar gula (glukosa) dalam darah terlalu tinggi. Ini bisa terjadi karena tubuh tidak menghasilkan cukup insulin atau tidak dapat menggunakan insulin dengan baik.",
                    "apa itu diabetes":  "Diabetes adalah kondisi medis di mana kadar gula (glukosa) dalam darah terlalu tinggi. Ini bisa terjadi karena tubuh tidak menghasilkan cukup insulin atau tidak dapat menggunakan insulin dengan baik.",
                    "diabetes adalah":  "Diabetes adalah kondisi medis di mana kadar gula (glukosa) dalam darah terlalu tinggi. Ini bisa terjadi karena tubuh tidak menghasilkan cukup insulin atau tidak dapat menggunakan insulin dengan baik.",
                    "apa perbedaan antara diabetes tipe 1 dan tipe 2?": "Diabetes tipe 1 terjadi ketika tubuh tidak memproduksi insulin sama sekali, biasanya karena kerusakan autoimun pada sel beta pankreas. Diabetes tipe 2 terjadi ketika tubuh tidak menggunakan insulin dengan baik atau tidak cukup.",
                    "apa saja faktor risiko diabetes tipe 2?": "Faktor risiko termasuk obesitas, gaya hidup sedentari, usia di atas 45 tahun, riwayat keluarga dengan diabetes, hipertensi, dan pola makan tinggi gula dan lemak jenuh.",
                    "bagaimana cara mendiagnosis diabetes?": "Diagnosis diabetes biasanya dilakukan melalui tes darah seperti tes glukosa puasa, tes toleransi glukosa oral, dan tes A1C yang mengukur rata-rata kadar glukosa darah selama 2-3 bulan terakhir.",
                    "apa saja gejala umum diabetes?": "Gejala umum termasuk sering buang air kecil, rasa haus yang berlebihan, penurunan berat badan yang tidak dapat dijelaskan, kelelahan, pandangan kabur, dan luka yang lambat sembuh.",
                    "bagaimana cara mengelola diabetes?": "Pengelolaan diabetes melibatkan kombinasi pola makan sehat, aktivitas fisik teratur, pemantauan kadar glukosa darah, dan obat-obatan atau insulin jika diperlukan.",
                    "apa itu insulin dan apa perannya dalam tubuh?": "Insulin adalah hormon yang diproduksi oleh pankreas yang membantu sel-sel tubuh menyerap glukosa dari darah untuk digunakan sebagai energi atau disimpan sebagai lemak.",
                    "apa saja komplikasi jangka panjang dari diabetes yang tidak terkontrol?": "Komplikasi jangka panjang dapat mencakup penyakit kardiovaskular, kerusakan saraf (neuropati), kerusakan ginjal (nefropati), kerusakan mata (retinopati), dan masalah kaki yang dapat menyebabkan amputasi.",
                    "apakah diabetes bisa disembuhkan?": "Diabetes tipe 1 tidak dapat disembuhkan dan memerlukan manajemen seumur hidup. Diabetes tipe 2 dapat dikontrol dan bahkan masuk ke dalam remisi dengan perubahan gaya hidup yang signifikan dan penurunan berat badan.",
                    "apa itu hipoglikemia dan bagaimana mengatasinya?": "Hipoglikemia adalah kondisi di mana kadar glukosa darah terlalu rendah. Ini dapat diatasi dengan mengonsumsi sumber gula cepat seperti jus buah, tablet glukosa, atau permen, diikuti dengan makanan ringan yang mengandung karbohidrat.",
                    "mengapa penting untuk memonitor kadar glukosa darah secara rutin bagi penderita diabetes?": "Monitoring rutin membantu penderita diabetes untuk mengelola kadar glukosa darah mereka, mencegah komplikasi, dan menyesuaikan pengobatan atau pola makan mereka sesuai kebutuhan.",
                    "bagaimana cara mencegah diabetes tipe 2?": "Pencegahan melibatkan menjaga berat badan yang sehat, berolahraga secara teratur, mengonsumsi makanan yang seimbang rendah gula dan lemak jenuh, dan rutin memeriksa kesehatan untuk mendeteksi dini.",
                    "apa hubungan antara diabetes dan penyakit kardiovaskular?": "Diabetes meningkatkan risiko penyakit kardiovaskular karena kadar glukosa darah yang tinggi dapat merusak pembuluh darah dan saraf yang mengontrol jantung dan pembuluh darah.",
                    "bagaimana diet mempengaruhi pengelolaan diabetes?": "Diet yang sehat dan seimbang membantu mengontrol kadar glukosa darah, menjaga berat badan yang sehat, dan mengurangi risiko komplikasi diabetes. Ini termasuk mengonsumsi serat tinggi, lemak sehat, dan menghindari gula berlebih.",
                    "apakah diabetes dapat mempengaruhi kesehatan mental?": "Ya, penderita diabetes dapat mengalami stres, kecemasan, dan depresi akibat manajemen penyakit yang terus-menerus dan komplikasi terkait diabetes. Dukungan psikologis dan kelompok dukungan bisa membantu.",
                    "apa itu retinopati diabetik?": "Retinopati diabetik adalah komplikasi diabetes yang merusak pembuluh darah di retina mata, yang dapat menyebabkan kehilangan penglihatan jika tidak diobati.",
                    "bagaimana cara mengobati retinopati diabetik?": "Pengobatan meliputi kontrol ketat kadar glukosa darah, tekanan darah, kolesterol, dan mungkin prosedur laser atau operasi untuk menghentikan atau memperlambat kerusakan retina.",
                    "apa saja tanda dan gejala neuropati diabetik?": "Gejala neuropati diabetik termasuk kesemutan, mati rasa, rasa terbakar atau nyeri pada tangan dan kaki, serta kelemahan otot dan kehilangan refleks.",
                    "bagaimana cara mencegah neuropati diabetik?": "Pencegahan melibatkan kontrol yang baik terhadap kadar glukosa darah, menjaga tekanan darah dan kolesterol dalam batas normal, serta melakukan pemeriksaan rutin ke dokter.",
                    "apa itu nefropati diabetik?": "Nefropati diabetik adalah kerusakan pada ginjal yang disebabkan oleh diabetes, yang dapat menyebabkan gagal ginjal jika tidak dikelola dengan baik.",
                    "bagaimana cara mengobati nefropati diabetik?": "Pengobatan meliputi kontrol ketat kadar glukosa darah, tekanan darah, diet rendah protein, dan pengobatan untuk menurunkan tekanan darah seperti inhibitor ACE atau ARB.",
                    "apa itu kaki diabetik?": "Kaki diabetik adalah kondisi di mana luka atau infeksi pada kaki penderita diabetes sulit sembuh, yang dapat menyebabkan ulkus kaki dan bahkan amputasi jika tidak diobati dengan benar.",
                    "bagaimana cara merawat kaki diabetik?": "Perawatan kaki diabetik melibatkan pemeriksaan rutin kaki, menjaga kebersihan kaki, mengenakan sepatu yang nyaman dan sesuai, serta mengobati luka atau infeksi dengan segera.",
                    "apa itu ketoasidosis diabetik (DKA)?": "DKA adalah kondisi serius yang terjadi ketika tubuh memproduksi keton dalam jumlah yang sangat tinggi akibat kekurangan insulin, yang dapat menyebabkan koma atau kematian jika tidak segera ditangani.",
                    "apa saja gejala DKA?": "Gejala DKA meliputi mual, muntah, sakit perut, napas cepat dan dalam, bau napas seperti buah, serta kebingungan atau penurunan kesadaran.",
                    "bagaimana cara mencegah DKA?": "Pencegahan DKA melibatkan pemantauan kadar glukosa darah secara rutin, mengikuti rencana pengobatan yang dianjurkan, dan segera mencari bantuan medis jika kadar glukosa darah sangat tinggi atau ada tanda-tanda keton dalam urin.",
                    "apa itu sindrom hiperglikemia hiperosmolar (HHS)?": "HHS adalah kondisi serius yang terjadi pada penderita diabetes tipe 2, di mana kadar glukosa darah sangat tinggi tanpa adanya keton, yang dapat menyebabkan dehidrasi parah dan koma jika tidak segera ditangani.",
                    "apa saja gejala HHS?": "Gejala HHS meliputi haus yang ekstrem, mulut kering, frekuensi buang air kecil yang berkurang, kebingungan, kejang, dan koma.",
                    "bagaimana cara mencegah HHS?": "Pencegahan HHS melibatkan pemantauan kadar glukosa darah secara rutin, menjaga hidrasi yang baik, dan mengikuti rencana pengobatan diabetes dengan ketat.",
                    "apa itu hiperglikemia?": "Hiperglikemia adalah kondisi di mana kadar glukosa darah terlalu tinggi, yang dapat menyebabkan komplikasi jangka panjang jika tidak dikelola dengan baik.",
                    "apa saja gejala hiperglikemia?": "Gejala hiperglikemia meliputi rasa haus yang berlebihan, sering buang air kecil, pandangan kabur, kelelahan, dan sakit kepala.",
                    "bagaimana cara mengatasi hiperglikemia?": "Mengatasi hiperglikemia melibatkan pemantauan kadar glukosa darah, menyesuaikan dosis obat atau insulin, berolahraga secara teratur, dan menjaga pola makan yang sehat.",
                    "apa itu hipoglikemia?": "Hipoglikemia adalah kondisi di mana kadar glukosa darah terlalu rendah, yang bisa berbahaya dan membutuhkan penanganan segera.",
                    "apa saja gejala hipoglikemia?": "Gejala hipoglikemia meliputi keringat dingin, gemetar, pusing, kelaparan, kebingungan, dan kejang.",
                    "bagaimana cara mencegah hipoglikemia?": "Pencegahan hipoglikemia melibatkan makan secara teratur, memantau kadar glukosa darah, menyesuaikan dosis insulin atau obat-obatan",
                    "Bagaimana cara kerja metformin?": "Metformin bekerja dengan mengurangi produksi glukosa oleh hati dan meningkatkan sensitivitas insulin di otot dan jaringan lainnya.",
                    "Apa itu sulfonilurea dan bagaimana cara kerjanya?": "Sulfonilurea adalah obat yang merangsang pankreas untuk memproduksi lebih banyak insulin. Contoh obat ini termasuk glibenklamid dan glipizid.",
                    "Apa itu GLP-1 agonis dan bagaimana cara kerjanya?": "GLP-1 agonis adalah obat yang meniru hormon incretin untuk meningkatkan sekresi insulin dan menurunkan produksi glukosa oleh hati. Contoh obat ini termasuk liraglutid dan exenatid.",
                    "Bagaimana cara kerja SGLT2 inhibitor?": "SGLT2 inhibitor bekerja dengan mencegah reabsorpsi glukosa di ginjal, sehingga glukosa diekskresikan melalui urin. Contoh obat ini termasuk dapagliflozin dan empagliflozin.",
                    "Apa itu HbA1c dan mengapa penting dalam manajemen diabetes?": "HbA1c adalah tes darah yang mengukur rata-rata kadar glukosa darah selama 2-3 bulan terakhir. Ini penting untuk menilai kontrol diabetes jangka panjang.",
                    "Berapa nilai HbA1c yang dianggap normal?": "Nilai HbA1c di bawah 5,7 persen  dianggap normal, 5,7%-6,4% menunjukkan prediabetes, dan 6,5 persen atau lebih mengindikasikan diabetes.",
                    "Apa itu tes toleransi glukosa oral (OGTT)?": "OGTT adalah tes yang mengukur respons tubuh terhadap glukosa dengan memeriksa kadar glukosa darah sebelum dan setelah mengonsumsi minuman glukosa.",
                    "Bagaimana cara kerja insulin glargine?": "Insulin glargine adalah insulin basal jangka panjang yang bekerja dengan melepaskan insulin secara perlahan untuk menjaga kadar glukosa darah stabil sepanjang hari.",
                    "Apa itu pompa insulin dan bagaimana cara kerjanya?": "Pompa insulin adalah perangkat kecil yang memberikan insulin secara kontinu melalui selang yang ditempatkan di bawah kulit, membantu menjaga kadar glukosa darah stabil.",
                    "Apa saja manfaat olahraga bagi penderita diabetes?": "Manfaat olahraga termasuk meningkatkan sensitivitas insulin, membantu kontrol berat badan, mengurangi risiko komplikasi kardiovaskular, dan meningkatkan kesehatan mental.",
                    "Bagaimana cara kerja terapi insulin pada diabetes tipe 1?": "Terapi insulin pada diabetes tipe 1 menggantikan insulin yang tidak dapat diproduksi oleh tubuh, membantu mengatur kadar glukosa darah dan mencegah komplikasi.",
                    "Apa itu diabetes gestasional?": "Diabetes gestasional adalah diabetes yang didiagnosis selama kehamilan dan biasanya hilang setelah melahirkan, namun meningkatkan risiko diabetes tipe 2 di kemudian hari.",
                    "Apa saja faktor risiko diabetes gestasional?": "Faktor risiko termasuk obesitas, riwayat keluarga dengan diabetes, usia di atas 25 tahun, dan riwayat diabetes gestasional pada kehamilan sebelumnya.",
                    "Bagaimana cara mencegah diabetes gestasional?": "Pencegahan melibatkan menjaga berat badan yang sehat, makan makanan yang seimbang, dan berolahraga secara teratur sebelum dan selama kehamilan.",
                    "Apa itu prediabetes?": "Prediabetes adalah kondisi di mana kadar glukosa darah lebih tinggi dari normal tetapi belum cukup tinggi untuk didiagnosis sebagai diabetes, meningkatkan risiko diabetes tipe 2.",
                    "Bagaimana cara mengelola prediabetes?": "Pengelolaan prediabetes melibatkan perubahan gaya hidup seperti diet sehat, penurunan berat badan, dan peningkatan aktivitas fisik untuk mencegah perkembangan menjadi diabetes tipe 2.",
                    "Apa itu sindrom metabolik?": "Sindrom metabolik adalah kumpulan kondisi yang meliputi tekanan darah tinggi, kadar gula darah tinggi, kelebihan lemak di sekitar pinggang, dan kadar kolesterol atau trigliserida abnormal, meningkatkan risiko penyakit jantung dan diabetes tipe 2.",
                    "Apa saja komplikasi jangka pendek dari diabetes?": "Komplikasi jangka pendek meliputi hipoglikemia, hiperglikemia, ketoasidosis diabetik (DKA), dan sindrom hiperglikemia hiperosmolar (HHS).",
                    "Bagaimana cara kerja inhibitor DPP-4?": "Inhibitor DPP-4 bekerja dengan menghambat enzim dipeptidil peptidase-4, yang meningkatkan kadar hormon incretin dan meningkatkan sekresi insulin setelah makan.",
                    "Apa itu insulin lispro?": "Insulin lispro adalah insulin kerja cepat yang digunakan untuk mengontrol kenaikan kadar glukosa darah setelah makan.",
                    "Bagaimana cara mengatasi luka pada penderita diabetes?": "Mengatasi luka melibatkan menjaga luka tetap bersih, menghindari tekanan pada luka, mengonsumsi antibiotik jika diperlukan, dan memeriksakan luka secara rutin ke tenaga medis.",
                    "Apa itu diet rendah glikemik dan bagaimana ini membantu penderita diabetes?": "Diet rendah glikemik melibatkan mengonsumsi makanan yang tidak menyebabkan lonjakan besar dalam kadar glukosa darah, membantu mengontrol kadar glukosa darah dan mencegah lonjakan insulin.",
                    "Apa itu indeks glikemik (GI)?": "Indeks glikemik adalah sistem peringkat yang mengukur seberapa cepat makanan tertentu meningkatkan kadar glukosa darah setelah dikonsumsi.",
                    "Apa itu fruktosamin dan bagaimana ini berbeda dari HbA1c?": "Fruktosamin adalah tes darah yang mengukur kadar glukosa darah rata-rata selama 2-3 minggu terakhir, berbeda dari HbA1c yang mengukur selama 2-3 bulan.",
                    "Bagaimana cara kerja pioglitazon?": "Pioglitazon adalah obat yang meningkatkan sensitivitas insulin di otot dan jaringan lemak, serta mengurangi produksi glukosa oleh hati.",
                    "Apa itu insulin detemir?": "Insulin detemir adalah insulin basal jangka panjang yang digunakan untuk mengontrol kadar glukosa darah sepanjang hari dan malam.",
                    "Apa saja tanda dan gejala diabetes pada anak-anak?": "Tanda dan gejala termasuk sering buang air kecil, rasa haus yang berlebihan, penurunan berat badan yang tidak dapat dijelaskan, kelelahan, dan perubahan perilaku atau kinerja akademis yang menurun.",
                    "Bagaimana cara mengelola diabetes pada anak-anak?": "Pengelolaan melibatkan pemantauan kadar glukosa darah, terapi insulin, diet sehat, olahraga, dan pendidikan serta dukungan keluarga.",
                    "Apa itu diabetes autoimun laten pada orang dewasa (LADA)?": "LADA adalah bentuk diabetes tipe 1 yang berkembang lebih lambat pada orang dewasa, sering kali salah didiagnosis sebagai diabetes tipe 2 pada awalnya.",
                    "Bagaimana cara mendiagnosis LADA?": "Diagnosis LADA melibatkan tes darah untuk antibodi autoimun terhadap sel beta pankreas dan pemeriksaan kadar C-peptida untuk menilai produksi insulin.",
                    "Apa itu honeymoon period pada diabetes tipe 1?": "Honeymoon period adalah fase awal setelah diagnosis diabetes tipe 1 ketika kebutuhan insulin berkurang dan kadar glukosa darah lebih mudah dikontrol karena masih ada beberapa sel beta yang berfungsi.",
                    "Bagaimana cara kerja glukagon?": "Glukagon adalah hormon yang meningkatkan kadar glukosa darah dengan merangsang pelepasan glukosa dari hati, digunakan dalam keadaan darurat untuk mengatasi hipoglikemia berat.",
                    "Apa itu sensor glukosa kontinu (CGM)?": "CGM adalah perangkat yang secara terus-menerus memantau kadar glukosa darah melalui sensor yang ditempatkan di bawah kulit, memberikan data real-time kepada pengguna.",
                    "Bagaimana cara kerja tes A1C?": "Tes A1C mengukur persentase hemoglobin yang terikat glukosa, memberikan gambaran tentang kadar glukosa darah rata-rata selama 2-3 bulan terakhir.",
                    "Apa itu sindrom kaki Charcot?": "Sindrom kaki Charcot adalah kondisi serius pada penderita diabetes di mana tulang kaki melemah dan dapat retak atau bergeser, menyebabkan deformitas kaki yang parah jika tidak segera diobati.",
                    "Bagaimana cara mengelola sindrom kaki Charcot?": "Pengelolaan melibatkan menjaga berat badan dari kaki yang terkena, menggunakan sepatu khusus atau alat bantu, dan kadang-kadang memerlukan pembedahan untuk memperbaiki deformitas.",
                    "Apa itu transplantasi sel islet?": "Transplantasi sel islet adalah prosedur di mana sel beta pankreas yang menghasilkan insulin ditransplantasikan ke tubuh penderita diabetes tipe 1 untuk mengembalikan kemampuan tubuh memproduksi insulin.",
                    "Apa saja tantangan dalam transplantasi sel islet?": "Tantangan meliputi penolakan imun, kebutuhan akan imunosupresi, dan keterbatasan donor sel islet.",
                    "Apa itu glikasi?": "Glikasi adalah proses di mana glukosa menempel pada protein atau lipid tanpa enzim, yang dapat menyebabkan kerusakan jaringan dan berperan dalam komplikasi diabetes.",
                    "Bagaimana cara kerja inhibitor alfa-glukosidase?": "Inhibitor alfa-glukosidase bekerja dengan menghambat enzim di usus yang memecah karbohidrat kompleks menjadi glukosa, sehingga memperlambat penyerapan glukosa dan mencegah lonjakan kadar glukosa darah setelah makan.",
                    "Apa itu efek dawn phenomenon?": "Dawn phenomenon adalah peningkatan kadar glukosa darah yang terjadi pada pagi hari, biasanya disebabkan oleh pelepasan hormon seperti kortisol dan hormon pertumbuhan yang meningkatkan resistensi insulin.",
                    "Bagaimana cara mengatasi efek dawn phenomenon?": "Mengatasi efek dawn phenomenon melibatkan penyesuaian dosis insulin basal atau penggunaan obat lain yang bekerja semalam, serta menjaga pola makan dan aktivitas yang konsisten.",
                    "Apa itu efek Somogyi?": "Efek Somogyi adalah peningkatan kadar glukosa darah setelah episode hipoglikemia di malam hari, sebagai respons tubuh yang berlebihan untuk meningkatkan kadar glukosa darah.",
                    "Bagaimana cara mengatasi efek Somogyi?": "Mengatasi efek Somogyi melibatkan pemantauan kadar glukosa darah malam hari, menghindari dosis insulin berlebihan sebelum tidur, dan memastikan asupan makanan yang cukup untuk mencegah hipoglikemia.",
                    "Apa itu diabetes insipidus?": "Diabetes insipidus adalah kondisi yang ditandai oleh ketidakmampuan ginjal untuk mempertahankan air, menyebabkan produksi urin berlebihan dan rasa haus yang ekstrem, yang tidak terkait dengan kadar glukosa darah.",
                    "Apa penyebab diabetes insipidus?": "Penyebab termasuk kerusakan pada kelenjar pituitari atau hipotalamus yang menghasilkan hormon antidiuretik (ADH), atau masalah pada ginjal yang tidak merespon ADH dengan baik.",
                    "Bagaimana cara mendiagnosis diabetes insipidus?": "Diagnosis melibatkan tes deprivasi air, pengukuran kadar ADH dalam darah, dan pencitraan otak untuk memeriksa kerusakan pada kelenjar pituitari atau hipotalamus.",
                    "Bagaimana cara mengobati diabetes insipidus?": "Pengobatan melibatkan penggunaan desmopressin (analog ADH), dan menjaga hidrasi yang baik dengan mengonsumsi cukup cairan untuk mengimbangi kehilangan urin.",
                    "Apa itu sindrom ovarium polikistik (PCOS) dan hubungannya dengan diabetes?": "PCOS adalah kondisi hormonal pada wanita yang ditandai dengan ketidakseimbangan hormon reproduksi, resistensi insulin, dan risiko meningkat untuk diabetes tipe 2.",
                    "Bagaimana cara mengelola PCOS untuk mencegah diabetes?": "Pengelolaan melibatkan penurunan berat badan, diet sehat, olahraga, dan penggunaan obat seperti metformin untuk meningkatkan sensitivitas insulin.",
                    "Apa itu resistensi insulin?": "Resistensi insulin adalah kondisi di mana sel-sel tubuh tidak merespons insulin dengan baik, menyebabkan kadar glukosa darah tinggi dan peningkatan risiko diabetes tipe 2.",
                    "Apa saja tanda dan gejala resistensi insulin?": "Tanda dan gejala meliputi peningkatan berat badan terutama di area perut, kelelahan, sering merasa lapar, dan peningkatan kadar insulin dalam darah.",
                    "Bagaimana cara mengatasi resistensi insulin?": "Mengatasi resistensi insulin melibatkan penurunan berat badan, diet sehat rendah karbohidrat sederhana, olahraga, dan penggunaan obat seperti metformin jika diperlukan.",
                    "Apa itu hiperlipidemia dan hubungannya dengan diabetes?": "Hiperlipidemia adalah kondisi di mana kadar lipid (kolesterol dan trigliserida) dalam darah tinggi, yang sering dikaitkan dengan diabetes dan meningkatkan risiko penyakit kardiovaskular.",
                    "Bagaimana cara mengelola hiperlipidemia pada penderita diabetes?": "Pengelolaan melibatkan perubahan gaya hidup seperti diet rendah lemak jenuh, olahraga, penurunan berat badan, dan penggunaan obat penurun lipid seperti statin.",
                    "Apa itu trigliserida dan mengapa penting untuk dikontrol pada penderita diabetes?": "Trigliserida adalah jenis lemak dalam darah yang dapat meningkatkan risiko penyakit jantung jika kadarnya terlalu tinggi, penting untuk dikontrol melalui diet, olahraga, dan obat-obatan jika diperlukan.",
                    "Apa itu HDL dan LDL kolesterol?": "HDL (high-density lipoprotein) adalah kolesterol 'baik' yang membantu menghilangkan kolesterol dari arteri, sedangkan LDL (low-density lipoprotein) adalah kolesterol 'jahat' yang dapat menumpuk di arteri dan menyebabkan penyakit jantung.",
                    "Bagaimana cara meningkatkan kadar HDL kolesterol?": "Meningkatkan kadar HDL melibatkan diet sehat yang tinggi asam lemak omega-3, berolahraga secara teratur, berhenti merokok, dan mengonsumsi alkohol dalam jumlah sedang.",
                    "Apa itu sindrom Cushing dan hubungannya dengan diabetes?": "Sindrom Cushing adalah kondisi yang disebabkan oleh kadar kortisol yang tinggi dalam tubuh, yang dapat menyebabkan resistensi insulin dan meningkatkan risiko diabetes tipe 2.",
                    "Bagaimana cara mendiagnosis sindrom Cushing?": "Diagnosis melibatkan tes urine 24 jam untuk mengukur kadar kortisol, tes darah untuk kortisol dan ACTH, serta pencitraan untuk mendeteksi tumor yang mungkin menyebabkan produksi kortisol berlebih.",
                    "Apa itu glukosa puasa dan bagaimana tesnya dilakukan?": "Glukosa puasa adalah kadar glukosa dalam darah setelah puasa selama setidaknya 8 jam. Tes dilakukan dengan mengambil sampel darah setelah periode puasa tersebut.",
                    "Bagaimana cara kerja terapi kombinasi dalam manajemen diabetes tipe 2?": "Terapi kombinasi melibatkan penggunaan lebih dari satu jenis obat dengan mekanisme kerja berbeda untuk mengontrol kadar glukosa darah secara lebih efektif.",
                    "Apa itu monogenik diabetes dan bagaimana cara mendiagnosisnya?": "Monogenik diabetes adalah bentuk diabetes yang disebabkan oleh mutasi pada satu gen. Diagnosis melibatkan tes genetik untuk mendeteksi mutasi tersebut.",
                    "Apa saja jenis obat oral untuk diabetes tipe 2?": "Jenis obat oral termasuk metformin, sulfonilurea, glitazon, DPP-4 inhibitor, SGLT2 inhibitor, dan GLP-1 agonis.",
            }

                # Normalisasi masukan pengguna
                user_input = user_input.lower()

                # Periksa apakah masukan cocok dengan respons yang telah ditentukan sebelumnya
                for key in responses:
                    if key in user_input:
                        return responses[key]
            
                # Respon jika tidak ditemukan kecocokan
                return "I'm sorry, I don't understand that. Can you please rephrase?"

            #tampilan chatbot
        def main():
            
                #untuk menampilkan histori chat sebelumnya
                if 'history' not in st.session_state:
                    st.session_state.history = []

                #kunci unik untuk input teks untuk mengatur ulang
                input_key = 'input_' + str(len(st.session_state.history))

                #untuk pengguna input prompt
                user_input = st.text_input("Ketikkan pesanmu dibawah ini : ", key=input_key)

                #untuk proses inputan pengguna
                if user_input:
                    response = chatbot_response(user_input)

                    #untuk menambah inputan ke histori
                    st.session_state.history.append((user_input, response))
                    st.experimental_rerun()  #untuk menjalankan kembali aplikasi/untuk mengatur ulang kolom input

                #untuk menampilkan chat
                for user_text, bot_response in st.session_state.history:
                    st.write(f"👤: {user_text}")
                    st.write(f"🤖: {bot_response}")

        if __name__ == "__main__":
                main()

    #halaman Setting
    if(selected == 'Setting'):
        st.title('Setting')
        authenticator.logout()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')