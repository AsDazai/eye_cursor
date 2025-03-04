from flask import Flask, request, Response, redirect, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(_name_)

# Language options mapping
LANGUAGES = {
    "1": "english",
    "2": "marathi",
    "3": "hindi"
}

# Voice language codes mapping for Twilio
VOICE_LANGUAGES = {
    "english": "en-IN",
    "marathi": "mr-IN",
    "hindi": "hi-IN"
}

# Service menus for each language
SERVICE_MENU = {
    "english": ("Please select the service you need: "
                "For Financial Assistance and Farmer Welfare, press 1. "
                "For Irrigation, Mechanization and Resource Management, press 2. "
                "For Crop Production and Food Security, press 3. "
                "For Sustainable and Modern Agriculture, press 4."),
    "marathi": ("कृपया तुम्हाला आवश्यक सेवा निवडा: "
                "आर्थिक सहाय्य आणि शेतकरी कल्याणासाठी, 1 दाबा. "
                "सिंचन, यांत्रिकीकरण आणि संसाधन व्यवस्थापनासाठी, 2 दाबा. "
                "पीक उत्पादन आणि अन्न सुरक्षेसाठी, 3 दाबा. "
                "शाश्वत आणि आधुनिक शेतीसाठी, 4 दाबा."),
    "hindi": ("कृपया अपनी आवश्यक सेवा चुनें: "
              "वित्तीय सहायता और किसान कल्याण के लिए, 1 दबाएं। "
              "सिंचाई, मशीनीकरण और संसाधन प्रबंधन के लिए, 2 दबाएं। "
              "फसल उत्पादन और खाद्य सुरक्षा के लिए, 3 दबाएं। "
              "सतत और आधुनिक कृषि के लिए, 4 दबाएं।")
}

# Scheme details mapping
SCHEME_DETAILS = {
    "english": {
        "1": {  # Financial Assistance & Farmer Welfare
            "prompt": ("For Financial Assistance and Farmer Welfare, please select: "
                       "For PM-Kisan Samman Nidhi (PM-KISAN), press 1. "
                       "For Kisan Credit Card (KCC) Scheme , press 2. "
                       "For Rashtriya Krishi Vikas Yojana (RKVY), press 3. "
                       "Pradhan Mantri Fasal Bima Yojana (PMFBY), press 4. "
                       "PM Kisan Maan Dhan Yojana (PM-KMY), press 5."
                       "Paramparagat Krishi Vikas Yojana (PKVY),press 6."
                       "Agriculture Infrastructure Fund (AIF),press7." ),
            "schemes": {
                "1": "For PM-Kisan Samman Nidhi (PM-KISAN): ₹6,000 annual financial assistance for farmers. PM-Kisan Samman Nidhi (PM-KISAN) is a government scheme that provides ₹6,000 per year to eligible farmers in three equal installments of ₹2,000. The amount is directly transferred to their bank accounts to support agricultural and personal expenses. The scheme aims to ensure financial stability for farmers and help them buy seeds, fertilizers, and other essentials. All landholding farmer families can apply online or through Common Service Centers (CSCs). By offering direct income support, PM-KISAN helps improve farmers' livelihoods and promotes agricultural growth.Scheme website: [https://pmkisan.gov.in/](https://pmkisan.gov.in/) ",
                "2": "For Kisan Credit Card (KCC) Scheme: The Kisan Credit Card (KCC) scheme provides farmers with affordable credit to meet their agricultural needs. The scheme offers short-term credit for crop production, post-harvest expenses, and consumption needs. Farmers can use the KCC to buy seeds, fertilizers, pesticides, and other inputs. The card also covers expenses for farm maintenance, irrigation, and other agricultural activities. By providing timely credit at low interest rates, the KCC scheme helps farmers manage their finances and improve agricultural productivity.Scheme website: [https://www.myscheme.gov.in/schemes/kcc](https://www.myscheme.gov.in/schemes/kcc)",
                "3": "For Rashtriya Krishi Vikas Yojana (RKVY): The Rashtriya Krishi Vikas Yojana (RKVY) is a government scheme that aims to promote agricultural growth and development. The scheme provides financial assistance to states for implementing various agricultural projects and initiatives. RKVY supports activities such as crop diversification, infrastructure development, and technology adoption in agriculture. By funding state-specific projects, the scheme helps improve farm productivity, income, and sustainability. Farmers can benefit from RKVY by participating in training programs, demonstrations, and other capacity-building activities.Scheme website: [https://rkvy.da.gov.in/](https://rkvy.da.gov.in/)",
                "4": "Pradhan Mantri Fasal Bima Yojana (PMFBY): The Pradhan Mantri Fasal Bima Yojana (PMFBY) is a crop insurance scheme that provides financial protection to farmers against crop losses due to natural calamities. The scheme covers risks such as drought, flood, hailstorm, pest infestation, and other weather-related events. PMFBY offers insurance coverage for all food and oilseed crops, as well as commercial and horticultural crops. By paying a nominal premium, farmers can insure their crops and receive compensation for yield losses. PMFBY aims to safeguard farmers' income and ensure food security in the country.Scheme website: [https://pmfby.gov.in/](https://pmfby.gov.in/)",
                "5": "PM Kisan Maan Dhan Yojana (PM-KMY): The Pradhan Mantri Kisan Maan Dhan Yojana (PM-KMY) is a pension scheme for small and marginal farmers. The scheme provides a monthly pension of ₹3,000 to farmers after the age of 60. Farmers can join the scheme by contributing a nominal amount during their working years. PM-KMY aims to provide financial security to farmers in their old age and support their families. By enrolling in the scheme, farmers can secure their future and enjoy a dignified retirement.Scheme website: [https://pmkmy.gov.in/](https://pmkmy.gov.in/)",
                "6": "Paramparagat Krishi Vikas Yojana (PKVY): Paramparagat Krishi Vikas Yojana (PKVY) promotes organic farming by providing financial support to farmers. It helps in training, certification, and marketing of organic products. Farmers get ₹50,000 per hectare over three years to switch to organic farming. The goal is to reduce chemical use and improve soil health and crop quality.Scheme website: [https://pgsindia-ncof.gov.in/pkvy/index.aspx](https://pgsindia-ncof.gov.in/pkvy/index.aspx)",
                "7": "Agriculture Infrastructure Fund (AIF): Agriculture Infrastructure Fund (AIF) is a ₹1 lakh crore government scheme to support farm infrastructure development. It provides low-interest loans for building cold storage, warehouses, processing units, and supply chains. Farmers, FPOs, and agribusinesses can benefit from subsidized interest rates and financial support to improve agricultural productivity and reduce post-harvest losses.Scheme website: [https://agriinfra.dac.gov.in/](https://agriinfra.dac.gov.in/)"
            },
            "num_digits": 1
        },
        "2": {  # Irrigation, Mechanization & Resource Management
            "prompt": ("For Irrigation, Mechanization and Resource Management, please select: "
                       "For Pradhan Mantri Krishi Sinchayee Yojana (PMKSY),press 1."                       
                       "Rashtriya Krishi Vikas Yojana (RKVY),press 2."
                       "Rainfed Area Development (RAD),press 3."
                       "Accelerated Irrigation Benefits Programme (AIBP),press 4."
                       "National Mission on Agricultural Extension and Technology (NMAET),press 5."
                       "National Innovations on Climate Resilient Agriculture (NICRA),press 6."
                       "Command Area Development & Water Management (CADWM),press 7."
                       ),
            "schemes": {
              "1": "For Pradhan Mantri Krishi Sinchayee Yojana (PMKSY): The Pradhan Mantri Krishi Sinchayee Yojana (PMKSY) is a government scheme to improve irrigation facilities for farmers. It aims to provide water to every farm through better water management and efficient use. The scheme funds projects like canal development, drip irrigation, and rainwater harvesting. Farmers benefit from subsidies on irrigation equipment and techniques. PMKSY helps reduce water wastage and increase crop productivity. State governments and local bodies implement the projects. This scheme ensures better water availability for farming and supports sustainable agriculture. Scheme website: [https://pmksy.gov.in/](https://pmksy.gov.in/)",
              "2": "For Rashtriya Krishi Vikas Yojana (RKVY): Rashtriya Krishi Vikas Yojana (RKVY) is a government scheme that provides financial support to improve farming infrastructure, technology, and productivity. It helps farmers with modern equipment, irrigation facilities, and storage solutions. The scheme also promotes innovation, crop diversification, and value-added farming to increase farmers' income. Scheme website: [https://rkvy.da.gov.in/](https://rkvy.da.gov.in/)",
              "3": "For Rainfed Area Development (RAD): Rainfed Area Development (RAD) is a scheme under the National Mission for Sustainable Agriculture (NMSA) that focuses on rainwater harvesting, soil conservation, and efficient irrigation in rainfed areas. It helps farmers adopt integrated farming systems like crop-livestock-horticulture to improve productivity. The scheme promotes drought-resistant crops and better water management to ensure sustainable farming. Scheme website: [https://nmsa.gov.in/](https://nmsa.gov.in/)",
              "4": "For Accelerated Irrigation Benefits Programme (AIBP): Accelerated Irrigation Benefits Programme (AIBP) is a government scheme that aims to complete ongoing irrigation projects to provide better water access to farmers. It focuses on building canals, dams, and water storage systems to improve irrigation coverage. The scheme helps in reducing farmers' dependence on rainfall and ensures a stable water supply for agriculture. Scheme website: [https://jalshakti-dowr.gov.in/programmes/aibp](https://jalshakti-dowr.gov.in/programmes/aibp)",
              "5": "For National Mission on Agricultural Extension and Technology (NMAET): National Mission on Agricultural Extension and Technology (NMAET) is a government scheme that promotes modern farming techniques, mechanization, and efficient irrigation. It helps farmers adopt advanced equipment, better seeds, and resource management practices. The scheme also provides training and support to improve agricultural productivity and sustainability. Scheme website: [https://agricoop.nic.in/en/nmaet](https://agricoop.nic.in/en/nmaet)",
              "6": "For National Innovations on Climate Resilient Agriculture (NICRA): National Innovations on Climate Resilient Agriculture (NICRA) is a government initiative that helps farmers adapt to climate change by using water-efficient irrigation, soil conservation, and weather-based farming techniques. It promotes drought-resistant crops, rainwater harvesting, and climate-smart technologies to reduce risks from extreme weather. The scheme aims to improve agricultural sustainability and productivity in changing climate conditions. Scheme website: [https://www.nicra-icar.in/](https://www.nicra-icar.in/)",
              "7": "For Command Area Development & Water Management (CADWM): Command Area Development & Water Management (CADWM) is a government scheme that aims to improve water-use efficiency in irrigated areas. It focuses on canal lining, drip and sprinkler irrigation, and better water management practices. The scheme helps farmers get a reliable water supply, reduce water wastage, and increase crop productivity. Scheme website: [https://cadwm.gov.in/](https://cadwm.gov.in/)"
            },
            "num_digits": 1
        },
        "3": {  # Crop Production & Food Security
            "prompt": ("For Crop Production and Food Security, please select: "
                       "Green Revolution  Krishonnati Yojana,press 1."
                       "Mission for Integrated Development of Horticulture (MIDH),press 2."
                       "National Mission on Sustainable Agriculture (NMSA),press 3."
                       "National Programme for Organic Production (NPOP) ,press 4."),
            "schemes": {
               "1": "For Green Revolution Krishonnati Yojana: Green Revolution Krishonnati Yojana aims to enhance crop productivity through modern farming techniques, high-yield seeds, and better irrigation methods. It includes various sub-schemes like NFSM, MIDH, and RKVY to promote sustainable agriculture. The focus is on increasing food grain production, pest management, and agricultural mechanization. It helps farmers adopt scientific and technological advancements to improve their income and productivity. Scheme website: [https://agricoop.nic.in/en/krishonnati-yojana](https://agricoop.nic.in/en/krishonnati-yojana)",
               "2": "For Mission for Integrated Development of Horticulture (MIDH): Mission for Integrated Development of Horticulture (MIDH) promotes the cultivation of fruits, vegetables, spices, medicinal plants, and flowers. It provides financial support for irrigation, cold storage, post-harvest management, and marketing. The scheme encourages the use of modern technology to improve horticultural productivity. It helps farmers get better market access and value addition for their produce. Scheme website: [https://midh.gov.in/](https://midh.gov.in/)",
               "3": "For National Mission on Sustainable Agriculture (NMSA): National Mission on Sustainable Agriculture (NMSA) focuses on climate-resilient agriculture to help farmers cope with changing weather patterns. It promotes soil health management, water conservation, and organic farming. The scheme supports efficient irrigation systems like drip and sprinkler irrigation to save water. It helps in improving crop yield while maintaining environmental sustainability. Scheme website: [https://nmsa.gov.in/](https://nmsa.gov.in/)",
               "4": "For National Programme for Organic Production (NPOP): National Programme for Organic Production (NPOP) promotes organic farming by providing certification and support for organic product exports. It ensures that farmers follow strict organic farming standards for domestic and international markets. The scheme helps in reducing chemical fertilizer use and improving soil health. It also provides market access for organic farmers, increasing their income and sustainability. Scheme website: [https://apeda.gov.in/apedawebsite/organic/index.htm](https://apeda.gov.in/apedawebsite/organic/index.htm)"
                        }
            },
            "num_digits": 1
        },
        "4": {  # Sustainable & Modern Agriculture
            "prompt": "There are no schemes currently listed under Sustainable and Modern Agriculture.",
            "schemes": {},
            "num_digits": 0
        }
    },
    "marathi": {
        "1": {  
            "prompt": ("आर्थिक सहाय्य आणि शेतकरी कल्याणासाठी कृपया निवडा: "
                       "प्रधानमंत्री किसान सन्मान निधी (PM-KISAN) साठी, 1 दाबा. "
                       "किसान क्रेडिट कार्ड (KCC) योजना साठी, 2 दाबा. "
                       "राष्ट्रीय कृषी विकास योजना (RKVY) साठी, 3 दाबा. "
                       "प्रधानमंत्री पीक विमा योजना (PMFBY) साठी, 4 दाबा. "
                       "PM किसान मानधन योजना (PM-KMY) साठी, 5 दाबा. "
                       "परंपरागत कृषी विकास योजना (PKVY) साठी, 6 दाबा. "
                       "कृषी पायाभूत सुविधा निधी (AIF) साठी, 7 दाबा."),
            "schemes": {
                "1": "प्रधानमंत्री कृषि सिंचाई योजना (PMKSY): प्रधानमंत्री कृषि सिंचाई योजना (PMKSY) ही सरकारी योजना आहे जी शेतकऱ्यांसाठी सिंचन सुविधा सुधारण्यासाठी राबवली जाते. यामध्ये पाण्याचे प्रभावी व्यवस्थापन आणि कार्यक्षम उपयोग सुनिश्चित केला जातो. योजनेअंतर्गत कालवे विकास, ठिबक सिंचन आणि पावसाचे पाणी साठवण्याच्या प्रकल्पांना अनुदान दिले जाते. शेतकऱ्यांना सिंचन उपकरणे आणि आधुनिक तंत्रज्ञानावर अनुदान मिळते. PMKSY शेतकऱ्यांना पाण्याचा योग्य वापर करण्यास मदत करते आणि पीक उत्पादनक्षमता वाढवते. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://pmksy.gov.in/) येथे भेट द्या.",
                "2": "राष्ट्रीय कृषी विकास योजना (RKVY): राष्ट्रीय कृषी विकास योजना (RKVY) ही एक सरकारी योजना आहे जी शेती पायाभूत सुविधा, आधुनिक तंत्रज्ञान आणि उत्पादनक्षमता सुधारण्यासाठी आर्थिक सहाय्य पुरवते. या योजनेअंतर्गत शेतकऱ्यांना आधुनिक उपकरणे, सिंचन सुविधा आणि साठवणूक उपाय मिळतात. तसेच, पीक विविधीकरण, नाविन्यपूर्ण शेती तंत्रज्ञान आणि मूल्यवर्धित शेतीला प्रोत्साहन दिले जाते, जेणेकरून शेतकऱ्यांचे उत्पन्न वाढू शकेल. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://rkvy.nic.in/) येथे भेट द्या.",
                "3": "रैनफेड एरिया डेव्हलपमेंट (RAD): रैनफेड एरिया डेव्हलपमेंट (RAD) ही राष्ट्रीय शाश्वत कृषी अभियान (NMSA) अंतर्गत येणारी योजना आहे जी कोरडवाहू भागातील शेतकऱ्यांसाठी जलसंधारण, मृदासंवर्धन आणि कार्यक्षम सिंचन सुविधा पुरवते. योजनेद्वारे शेतकऱ्यांना एकात्मिक शेती पद्धती स्वीकारण्यास मदत केली जाते, जसे की पीक-जनावर-फलोद्यान यासारख्या मिश्रित शेती पद्धती. RAD शेतकऱ्यांना दुष्काळ प्रतिरोधक पिके, योग्य पाणी व्यवस्थापन आणि शाश्वत शेतीसाठी मदत करते. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://nmsa.gov.in/) येथे भेट द्या.",
                "4": "गतीमान सिंचन लाभ कार्यक्रम (AIBP): गतीमान सिंचन लाभ कार्यक्रम (AIBP) हा सरकारी उपक्रम आहे, जो प्रलंबित सिंचन प्रकल्प पूर्ण करण्यासाठी आणि शेतकऱ्यांना अधिक पाणी उपलब्ध करून देण्यासाठी सुरू करण्यात आला आहे. या योजनेद्वारे कालवे, धरणे आणि पाणी साठवणूक यंत्रणा उभारणीसाठी मदत केली जाते. AIBP अंतर्गत, सिंचन क्षमता वाढवण्यासाठी राज्य सरकारांना आर्थिक सहाय्य दिले जाते, जेणेकरून शेतकऱ्यांचे पावसावर अवलंबित्व कमी होईल. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://mowr.gov.in/) येथे भेट द्या.",
                "5": "राष्ट्रीय कृषी विस्तार आणि तंत्रज्ञान अभियान (NMAET): राष्ट्रीय कृषी विस्तार आणि तंत्रज्ञान अभियान (NMAET) ही आधुनिक शेती तंत्रज्ञान, यांत्रिकीकरण आणि कार्यक्षम सिंचन पद्धतींना प्रोत्साहन देणारी सरकारी योजना आहे. शेतकऱ्यांना अत्याधुनिक उपकरणे, सुधारित बियाणे आणि संसाधन व्यवस्थापन तंत्रज्ञानाचा अवलंब करण्यास मदत केली जाते. योजनेच्या माध्यमातून प्रशिक्षण आणि सहाय्य पुरवले जाते, ज्यामुळे शेतकऱ्यांची उत्पादकता आणि शाश्वत शेतीसाठी क्षमता वाढते. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://agricoop.nic.in/) येथे भेट द्या.",
                "6": "राष्ट्रीय हवामान लवचिक शेती नवकल्पना (NICRA): राष्ट्रीय हवामान लवचिक शेती नवकल्पना (NICRA) हा सरकारी उपक्रम आहे, जो शेतकऱ्यांना हवामान बदलाशी जुळवून घेण्यासाठी मदत करतो. या योजनेद्वारे पाणी कार्यक्षम सिंचन, मृदा संवर्धन आणि हवामानानुसार शेती पद्धतींचा अवलंब केला जातो. NICRA अंतर्गत दुष्काळ प्रतिरोधक पिके, पावसाच्या पाण्याचे संकलन आणि हवामान सुसंगत तंत्रज्ञान विकसित केले जाते, जेणेकरून हवामानातील बदलांमुळे होणारे धोके कमी करता येतील. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://icar.org.in/) येथे भेट द्या.",
                "7": "आदेशित क्षेत्र विकास आणि जल व्यवस्थापन (CADWM): आदेशित क्षेत्र विकास आणि जल व्यवस्थापन (CADWM) ही योजना सिंचन क्षेत्रांमध्ये पाण्याचा कार्यक्षम वापर सुधारण्यासाठी राबवली जाते. या योजनेअंतर्गत कालवे अस्तरीकरण, ठिबक आणि तुषार सिंचन तंत्रज्ञानाचा अवलंब आणि उत्तम जलव्यवस्थापन पद्धतींना प्रोत्साहन दिले जाते. CADWM शेतकऱ्यांना स्थिर पाणीपुरवठा मिळवून देण्यास, पाण्याची नासाडी कमी करण्यास आणि पीक उत्पादन वाढवण्यास मदत करते. अधिक माहितीसाठी, [अधिकृत संकेतस्थळ](https://mowr.gov.in/) येथे भेट द्या."
                    }
            }
            },
            "num_digits": 1
        
        "2": {  
            "prompt": ("सिंचन, यांत्रिकीकरण आणि संसाधन व्यवस्थापनासाठी कृपया निवडा: "
                       "प्रधानमंत्री कृषी सिंचन योजना (PMKSY) साठी, 1 दाबा. "
                       "राष्ट्रीय कृषी विकास योजना (RKVY) साठी, 2 दाबा. "
                       "रेनफेड एरिया डेव्हलपमेंट (RAD) साठी, 3 दाबा. "
                       "प्रगतीशील सिंचन लाभ कार्यक्रम (AIBP) साठी, 4 दाबा. "
                       "राष्ट्रीय कृषी विस्तार आणि तंत्रज्ञान अभियान (NMAET) साठी, 5 दाबा. "
                       "राष्ट्रीय हवामान अनुकूल शेती नवप्रवर्तन (NICRA) साठी, 6 दाबा. "
                       "आदेशित क्षेत्र विकास आणि जल व्यवस्थापन (CADWM) साठी, 7 दाबा."),
            "schemes": {
                "1": "हरितक्रांती कृषोन्नती योजना: ही योजना आधुनिक शेती तंत्रज्ञान, उच्च उत्पादकता असलेली बियाणे आणि सुधारित सिंचन पद्धतींचा वापर करून शेती उत्पादन वाढवण्यास मदत करते. अधिक माहितीसाठी भेट द्या: https://agricoop.nic.in/",
                 "2": "समन्वित फलोत्पादन विकास मिशन (MIDH): फळे, भाजीपाला, मसाले, औषधी वनस्पती आणि फुलशेती उत्पादन वाढवण्यासाठी आर्थिक सहाय्य पुरवणारी योजना. अधिक माहितीसाठी भेट द्या: https://midh.gov.in/",
                 "3": "राष्ट्रीय शाश्वत कृषी अभियान (NMSA): हवामान बदलाशी जुळवून घेण्यासाठी मृदा आरोग्य व्यवस्थापन, पाणी संवर्धन आणि सेंद्रिय शेतीला प्रोत्साहन देणारी योजना. अधिक माहितीसाठी भेट द्या: https://nmsa.gov.in/",
                 "4": "राष्ट्रीय सेंद्रिय उत्पादन कार्यक्रम (NPOP): सेंद्रिय शेतीसाठी प्रमाणपत्र, निर्यात सहाय्य आणि सेंद्रिय उत्पादनांची विक्रीस मदत करणारी योजना. अधिक माहितीसाठी भेट द्या: https://apeda.gov.in/apedawebsite/organic/index.htm",
                 "5": "प्रगतीशील सिंचन लाभ कार्यक्रम (AIBP): सिंचन प्रकल्प पूर्णत्वासाठी निधी देणारी ही योजना आहे, ज्यामुळे जास्त शेतीक्षेत्र सिंचनाखाली येईल. अधिक माहितीसाठी भेट द्या: https://jalshakti-dowr.gov.in/schemes/accelerated-irrigation-benefit-programme",
                 "6": "राष्ट्रीय कृषी विस्तार आणि तंत्रज्ञान अभियान (NMAET): आधुनिक शेती तंत्रज्ञान आणि साधनसामग्रीसाठी शेतकऱ्यांना प्रशिक्षण दिले जाते. अधिक माहितीसाठी भेट द्या: https://agricoop.nic.in/",
                "7": "राष्ट्रीय हवामान अनुकूल शेती नवप्रवर्तन (NICRA): हवामान बदलासह शेतीला अनुकूल करण्यासाठी सेंद्रिय शेती आणि जलव्यवस्थापनाला प्रोत्साहन देते. अधिक माहितीसाठी भेट द्या: https://www.nicra-icar.in/"
            },
            "num_digits": 1
        },
       "3": {  
            "prompt": ("पीक उत्पादन आणि अन्न सुरक्षा यासाठी कृपया निवडा: "
                       "हरितक्रांती कृषोन्नती योजना, 1 दाबा. "
                       "समग्र बागायती विकास अभियान (MIDH), 2 दाबा. "
                       "राष्ट्रीय शाश्वत शेती अभियान (NMSA), 3 दाबा. "
                       "राष्ट्रीय सेंद्रिय उत्पादन कार्यक्रम (NPOP), 4 दाबा."),
            "schemes": {
                "1": "हरितक्रांती कृषोन्नती योजना: हरितक्रांती कृषोन्नती योजनेचा उद्देश आधुनिक शेती तंत्रज्ञान, उच्च उत्पन्न देणाऱ्या बियाण्यांचा वापर आणि उत्तम सिंचन पद्धतींच्या माध्यमातून पीक उत्पादकता वाढवणे आहे. या योजनेत NFSM, MIDH आणि RKVY सारख्या उपयोजना आहेत ज्या शाश्वत शेतीला चालना देतात. अन्नधान्य उत्पादन वाढवणे, कीड व्यवस्थापन आणि यांत्रिकीकरणाला प्रोत्साहन देणे यावर भर दिला जातो. ही योजना शेतकऱ्यांना वैज्ञानिक आणि तांत्रिक प्रगती आत्मसात करून उत्पन्न आणि उत्पादकता सुधारण्यास मदत करते. अधिक माहितीसाठी भेट द्या: https://agricoop.nic.in/",
                "2": "समग्र बागायती विकास अभियान (MIDH): समग्र बागायती विकास अभियान (MIDH) फळे, भाज्या, मसाले, औषधी वनस्पती आणि फुलांची शेती प्रोत्साहन देते. सिंचन, कोल्ड स्टोरेज, काढणीपश्चात व्यवस्थापन आणि विपणनासाठी आर्थिक मदत दिली जाते. आधुनिक तंत्रज्ञानाचा वापर करून बागायती उत्पादन वाढवण्यास ही योजना मदत करते. शेतकऱ्यांना चांगल्या बाजारपेठेचा आणि मूल्यवर्धनाचा लाभ मिळावा हा उद्देश आहे. अधिक माहितीसाठी भेट द्या: https://midh.gov.in/",
                "3": "राष्ट्रीय शाश्वत शेती अभियान (NMSA): राष्ट्रीय शाश्वत शेती अभियान (NMSA) हवामान अनुकूल शेतीवर लक्ष केंद्रित करते, जेणेकरून शेतकरी बदलत्या हवामानाशी जुळवून घेऊ शकतील. मृदा आरोग्य व्यवस्थापन, जलसंधारण आणि सेंद्रिय शेतीला प्रोत्साहन दिले जाते. ठिबक व तुषार सिंचनासारखी कार्यक्षम सिंचन प्रणाली समर्थित केली जाते, ज्यामुळे पाण्याची बचत होते. या योजनेमुळे पर्यावरण संतुलन राखून पीक उत्पादन वाढवता येते. अधिक माहितीसाठी भेट द्या: https://nmsa.gov.in/",
                 "4": "राष्ट्रीय सेंद्रिय उत्पादन कार्यक्रम (NPOP): राष्ट्रीय सेंद्रिय उत्पादन कार्यक्रम (NPOP) शेतकऱ्यांना सेंद्रिय उत्पादनाचे प्रमाणपत्र आणि निर्यात सुविधांसाठी मदत करतो. शेतकऱ्यांनी सेंद्रिय शेतीचे कठोर निकष पाळावेत याची खात्री केली जाते. या योजनेमुळे रासायनिक खतांचा वापर कमी होतो आणि मृदा आरोग्य सुधारते. तसेच, सेंद्रिय शेतकऱ्यांना बाजारपेठ उपलब्ध करून देऊन त्यांचे उत्पन्न आणि शाश्वतता वाढवणे हे उद्दिष्ट आहे. अधिक माहितीसाठी भेट द्या: https://apeda.gov.in/apedawebsite/organic/index.htm"
            },
            "num_digits": 1
        },
        "4": {  
            "prompt": "शाश्वत आणि आधुनिक शेतीअंतर्गत सध्या कोणत्याही योजना सूचीबद्ध नाहीत.",
            "schemes": {},
            "num_digits": 0
        }

    "hindi": {
       "1": {  
            "prompt": ("आर्थिक सहायता और किसान कल्याण के लिए कृपया चयन करें: "
                       "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) के लिए, 1 दबाएं। "
                       "किसान क्रेडिट कार्ड (KCC) योजना के लिए, 2 दबाएं। "
                       "राष्ट्रीय कृषि विकास योजना (RKVY) के लिए, 3 दबाएं। "
                       "प्रधानमंत्री फसल बीमा योजना (PMFBY) के लिए, 4 दबाएं। "
                       "PM किसान मानधन योजना (PM-KMY) के लिए, 5 दबाएं। "
                       "परंपरागत कृषि विकास योजना (PKVY) के लिए, 6 दबाएं। "
                       "कृषि अवसंरचना निधि (AIF) के लिए, 7 दबाएं।"),
            "schemes": {
               "1": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN): इस योजना के तहत पात्र किसानों को प्रति वर्ष ₹6,000 की आर्थिक सहायता दी जाती है। यह राशि चार महीने के अंतराल पर ₹2,000 की तीन किश्तों में सीधे उनके बैंक खाते में जमा की जाती है। इस योजना का उद्देश्य किसानों को आर्थिक स्थिरता प्रदान करना और उन्हें बीज, खाद और अन्य कृषि आवश्यकताओं को पूरा करने में सहायता करना है। अधिक जानकारी के लिए: https://pmkisan.gov.in/",
               "2": "किसान क्रेडिट कार्ड (KCC) योजना: KCC योजना किसानों को कम ब्याज दर पर ऋण प्रदान करती है। यह ऋण बीज, खाद, कीटनाशक, सिंचाई और अन्य कृषि आवश्यकताओं के लिए उपयोग किया जा सकता है। यह योजना किसानों की त्वरित आर्थिक आवश्यकताओं को पूरा करने और कृषि उत्पादकता बढ़ाने में मदद करती है। अधिक जानकारी के लिए: https://www.nabard.org/",
               "3": "राष्ट्रीय कृषि विकास योजना (RKVY): RKVY योजना के तहत कृषि विकास के विभिन्न परियोजनाओं को वित्तीय सहायता दी जाती है। इसमें फसल विविधीकरण, आधुनिक कृषि तकनीकों का उपयोग, बुनियादी ढांचे का विकास और अनुसंधान के लिए धनराशि प्रदान की जाती है, जिससे कृषि उत्पादकता और किसानों की आय में वृद्धि होती है। अधिक जानकारी के लिए: https://rkvy.nic.in/",
               "4": "प्रधानमंत्री फसल बीमा योजना (PMFBY): PMFBY एक फसल बीमा योजना है, जो प्राकृतिक आपदाओं के कारण फसल को हुए नुकसान की भरपाई करती है। इसमें सूखा, बाढ़, ओलावृष्टि, कीट हमले और जलवायु परिवर्तन से होने वाले नुकसान को कवर किया जाता है। किसान कम प्रीमियम का भुगतान कर अपनी फसलों को सुरक्षित कर सकते हैं। अधिक जानकारी के लिए: https://pmfby.gov.in/",
               "5": "PM किसान मानधन योजना (PM-KMY): यह योजना छोटे और सीमांत किसानों के लिए एक पेंशन योजना है। इसमें किसानों को 60 वर्ष की आयु के बाद प्रति माह ₹3,000 की पेंशन दी जाती है। किसान इस योजना में मामूली आर्थिक योगदान देकर भविष्य के लिए वित्तीय सुरक्षा प्राप्त कर सकते हैं। अधिक जानकारी के लिए: https://maandhan.in/",
               "6": "परंपरागत कृषि विकास योजना (PKVY): यह योजना जैविक खेती को प्रोत्साहित करती है। किसानों को प्रशिक्षण, प्रमाणन और जैविक उत्पादों के विपणन के लिए वित्तीय सहायता दी जाती है। तीन वर्षों के लिए प्रति हेक्टेयर ₹50,000 की सहायता प्रदान की जाती है, जिससे किसान रासायनिक खादों का उपयोग कम करके जैविक खेती कर सकें। अधिक जानकारी के लिए: https://pgsindia-ncof.gov.in/",
               "7": "कृषि अवसंरचना निधि (AIF): इस योजना के तहत किसानों को कोल्ड स्टोरेज, गोदाम, प्रसंस्करण इकाइयों और आपूर्ति श्रृंखला के विकास के लिए रियायती ब्याज दरों पर ऋण प्रदान किया जाता है। इससे कृषि उत्पादन को बढ़ाने और कटाई के बाद होने वाले नुकसान को कम करने में मदद मिलती है। अधिक जानकारी के लिए: https://agriinfra.dac.gov.in/"
            },
            "num_digits": 1
        },
        "2": {  
            "prompt": ("सिंचाई, यंत्रीकरण और संसाधन प्रबंधन के लिए कृपया चयन करें: "
                       "प्रधानमंत्री कृषि सिंचाई योजना (PMKSY) के लिए, 1 दबाएं। "
                       "राष्ट्रीय कृषि विकास योजना (RKVY) के लिए, 2 दबाएं। "
                       "रेनफेड एरिया डेवलपमेंट (RAD) के लिए, 3 दबाएं। "
                       "तेजी से सिंचाई लाभ कार्यक्रम (AIBP) के लिए, 4 दबाएं। "
                       "राष्ट्रीय कृषि विस्तार और प्रौद्योगिकी अभियान (NMAET) के लिए, 5 दबाएं। "
                       "राष्ट्रीय जलवायु अनुकूल कृषि नवाचार (NICRA) के लिए, 6 दबाएं। "
                       "कमांड क्षेत्र विकास और जल प्रबंधन (CADWM) के लिए, 7 दबाएं।"),
            "schemes": {
                 "1": "प्रधानमंत्री कृषि सिंचाई योजना (PMKSY): इस योजना का उद्देश्य 'हर खेत को पानी' उपलब्ध कराना है। इसमें ड्रिप और स्प्रिंकलर सिंचाई सहित जल संरक्षण तकनीकों का उपयोग किया जाता है। अधिक जानकारी के लिए: https://pmksy.gov.in/",
                 "2": "राष्ट्रीय कृषि विकास योजना (RKVY): यह योजना कृषि अवसंरचना, प्रौद्योगिकी और उत्पादन में सुधार के लिए वित्तीय सहायता प्रदान करती है। अधिक जानकारी के लिए: https://rkvy.nic.in/",
                 "3": "रेनफेड एरिया डेवलपमेंट (RAD): यह योजना वर्षा आधारित क्षेत्रों में जल संरक्षण, मृदा संरक्षण और जल प्रबंधन के लिए सहायता प्रदान करती है। अधिक जानकारी के लिए: https://nmsa.gov.in/",
                 "4": "तेजी से सिंचाई लाभ कार्यक्रम (AIBP): यह योजना अधूरे सिंचाई परियोजनाओं को पूरा करने के लिए धनराशि प्रदान करती है, जिससे अधिक कृषि भूमि को सिंचाई के तहत लाया जा सके। अधिक जानकारी के लिए: https://jalshakti-dowr.gov.in/programmes/accelerated-irrigation-benefit-programme",
                 "5": "राष्ट्रीय कृषि विस्तार और प्रौद्योगिकी अभियान (NMAET): इस योजना के तहत किसानों को आधुनिक कृषि तकनीक और उपकरणों के उपयोग के लिए प्रशिक्षण दिया जाता है। अधिक जानकारी के लिए: https://agricoop.nic.in/en/Majorprogrammes/NMAET",
                 "6": "राष्ट्रीय जलवायु अनुकूल कृषि नवाचार (NICRA): यह योजना जलवायु परिवर्तन के अनुकूल कृषि पद्धतियों को प्रोत्साहित करती है, जिसमें जैविक खेती और जल प्रबंधन शामिल हैं। अधिक जानकारी के लिए: https://www.nicra-icar.in/",
                 "7": "कमांड क्षेत्र विकास और जल प्रबंधन (CADWM): यह योजना सिंचाई और जल प्रबंधन में सुधार के लिए ड्रिप, स्प्रिंकलर सिंचाई और जल संरक्षण को बढ़ावा देती है। अधिक जानकारी के लिए: https://cadwm.gov.in/"
            },
            "num_digits": 1
        },
        "3": {  
        "prompt": ("फसल उत्पादन और खाद्य सुरक्षा के लिए, कृपया चुनें: "
                   "ग्रीन रेवोल्यूशन कृषोन्नति योजना, प्रेस 1। "
                   "एकीकृत बागवानी विकास मिशन (MIDH), प्रेस 2। "
                   "राष्ट्रीय सतत कृषि मिशन (NMSA), प्रेस 3। "
                   "राष्ट्रीय जैविक उत्पादन कार्यक्रम (NPOP), प्रेस 4।"),
        "schemes": {
            "1": "ग्रीन रेवोल्यूशन कृषोन्नति योजना: ग्रीन रेवोल्यूशन कृषोन्नति योजना आधुनिक कृषि तकनीकों, उच्च उपज वाले बीजों और बेहतर सिंचाई विधियों के माध्यम से फसल उत्पादकता बढ़ाने का लक्ष्य रखती है। इसमें NFSM, MIDH और RKVY जैसी विभिन्न उप-योजनाएं शामिल हैं, जो सतत कृषि को बढ़ावा देती हैं। इसका मुख्य उद्देश्य खाद्यान्न उत्पादन बढ़ाना, कीट प्रबंधन और कृषि यंत्रीकरण को प्रोत्साहित करना है। यह योजना किसानों को वैज्ञानिक और तकनीकी प्रगति अपनाने में मदद करती है, जिससे उनकी आय और उत्पादकता में सुधार होता है। अधिक जानकारी के लिए: https://agricoop.nic.in/en/majorprogrammes/green-revolution",
            "2": "एकीकृत बागवानी विकास मिशन (MIDH): एकीकृत बागवानी विकास मिशन (MIDH) फलों, सब्जियों, मसालों, औषधीय पौधों और फूलों की खेती को बढ़ावा देता है। यह सिंचाई, कोल्ड स्टोरेज, कटाई के बाद प्रबंधन और विपणन के लिए वित्तीय सहायता प्रदान करता है। यह योजना आधुनिक तकनीक के उपयोग को बढ़ावा देती है ताकि बागवानी उत्पादकता में सुधार हो सके। यह किसानों को बेहतर बाजार पहुंच और उनके उत्पादों के मूल्य संवर्धन में सहायता करता है। अधिक जानकारी के लिए: https://midh.gov.in/",
            "3": "राष्ट्रीय सतत कृषि मिशन (NMSA): राष्ट्रीय सतत कृषि मिशन (NMSA) जलवायु-लचीली कृषि पर केंद्रित है ताकि किसान बदलते मौसम के प्रभावों से निपट सकें। यह मृदा स्वास्थ्य प्रबंधन, जल संरक्षण और जैविक खेती को बढ़ावा देता है। योजना ड्रिप और स्प्रिंकलर सिंचाई जैसे कुशल सिंचाई प्रणालियों का समर्थन करती है ताकि पानी की बचत हो सके। यह फसल उत्पादन में वृद्धि करते हुए पर्यावरणीय स्थिरता बनाए रखने में सहायता करता है। अधिक जानकारी के लिए: https://nmsa.gov.in/",
            "4": "राष्ट्रीय जैविक उत्पादन कार्यक्रम (NPOP): राष्ट्रीय जैविक उत्पादन कार्यक्रम (NPOP) जैविक खेती को बढ़ावा देने के लिए प्रमाणन और जैविक उत्पादों के निर्यात के लिए समर्थन प्रदान करता है। यह सुनिश्चित करता है कि किसान घरेलू और अंतरराष्ट्रीय बाजारों के लिए सख्त जैविक खेती मानकों का पालन करें। यह योजना रासायनिक उर्वरकों के उपयोग को कम करने और मृदा स्वास्थ्य सुधारने में मदद करती है। यह जैविक किसानों को बाजार में पहुंच प्रदान करती है, जिससे उनकी आय और स्थिरता बढ़ती है। अधिक जानकारी के लिए: https://apeda.gov.in/apedawebsite/organic/"
        },
        "num_digits": 1
    },
    "4": {  
        "prompt": "टिकाऊ और आधुनिक कृषि के तहत वर्तमान में कोई योजना सूचीबद्ध नहीं है।",
        "schemes": {},
        "num_digits": 0
        }
    }


@app.route("/ivr", methods=["GET", "POST"])
def ivr_menu():
    """Initial language selection menu."""
    resp = VoiceResponse()
    gather = resp.gather(num_digits=1, action="/handle-language", method="POST")
    # Using a default English voice for the combined message
    gather.say("Welcome to Krushimitra. For deatiled info please visit krushimitra.ai . Please select your preferred language. "
               "For English, press 1. "
               "मराठीसाठी 2 दाबा. "
               "हिंदी के लिए 3 दबाएं.", language="en-IN")
    resp.redirect("/ivr")
    return Response(str(resp), mimetype="application/xml")  

@app.route("/handle-language", methods=["GET", "POST"])
def handle_language():
    """Handle language selection and present service options."""
    selected_digit = request.values.get("Digits", None)
    language = LANGUAGES.get(selected_digit)
    resp = VoiceResponse()
    if not language:
        resp.say("Invalid selection.", language="en-US")
        resp.redirect("/ivr")
        return Response(str(resp), mimetype="application/xml")
    
    # Present service menu based on language with appropriate voice.
    gather = resp.gather(num_digits=1,
                         action=f"/handle-service?language={language}",
                         method="POST")
    gather.say(SERVICE_MENU[language], language=VOICE_LANGUAGES[language])
    # If no input, repeat the service menu.
    resp.redirect(f"/handle-language?language={language}")
    return Response(str(resp), mimetype="application/xml")

@app.route("/handle-service", methods=["GET", "POST"])
def handle_service():
    """Handle service selection and present scheme details or further selection."""
    language = request.args.get("language")
    service_digit = request.values.get("Digits", None)
    resp = VoiceResponse()

    if language not in SERVICE_MENU or service_digit not in SCHEME_DETAILS.get(language, {}):
        resp.say("Invalid selection. Please try again.", language=VOICE_LANGUAGES.get(language, "en-US"))
        resp.redirect("/ivr")
        return Response(str(resp), mimetype="application/xml")
    
    scheme_info = SCHEME_DETAILS[language][service_digit]
    # Check if further scheme selection is needed.
    if scheme_info["num_digits"] > 0 and scheme_info["schemes"]:
        gather = resp.gather(num_digits=1,
                             action=f"/handle-scheme?language={language}&service={service_digit}",
                             method="POST")
        gather.say(scheme_info["prompt"], language=VOICE_LANGUAGES[language])
        resp.redirect(f"/handle-service?language={language}")
    else:
        # No further input required, just speak the message.
        resp.say(scheme_info["prompt"], language=VOICE_LANGUAGES[language])
        resp.hangup()
        
    return Response(str(resp), mimetype="application/xml")

@app.route("/handle-scheme", methods=["GET", "POST"])
def handle_scheme():
    """Handle selection of a specific scheme and announce details."""
    language = request.args.get("language")
    service_digit = request.args.get("service")
    scheme_digit = request.values.get("Digits", None)
    resp = VoiceResponse()
    
    try:
        scheme_desc = SCHEME_DETAILS[language][service_digit]["schemes"][scheme_digit]
    except KeyError:
        resp.say("Invalid selection. Please try again.", language=VOICE_LANGUAGES.get(language, "en-US"))
        resp.redirect(f"/handle-service?language={language}")
        return Response(str(resp), mimetype="application/xml")
    
    resp.say(scheme_desc, language=VOICE_LANGUAGES[language])
    resp.hangup()
    return Response(str(resp), mimetype="application/xml")

if _name_ == "_main_":
    app.run(debug=True)
