DB = {

    "Ferrari": {
        "SF90 Stradale": {"v":["Base"], "p":[750.0], "f":["Hybrid"], "seg":"Supercar"},
        "296 GTB":       {"v":["Base"], "p":[540.0], "f":["Hybrid"], "seg":"Supercar"},
        "Roma":          {"v":["Base"], "p":[376.0], "f":["Petrol"], "seg":"Grand Tourer"},
        "Purosangue":    {"v":["Base"], "p":[1050.0], "f":["Petrol"], "seg":"Super SUV"}
    },
    "Bugatti": {
        "Chiron":        {"v":["Base", "Pur Sport", "Super Sport"], "p":[1920.0, 2400.0, 2800.0], "f":["Petrol"], "seg":"Hypercar"}
    },
    "Koenigsegg": {
        "Jesko":         {"v":["Absolut", "Attack"], "p":[2400.0, 2600.0], "f":["Petrol"], "seg":"Hypercar"},
        "Gemera":        {"v":["Base"], "p":[1600.0], "f":["Hybrid"], "seg":"Hypercar"}
    },
    # VOLUME
    "Maruti Suzuki": {
        "Alto K10":     {"v":["STD","LXI","VXI","ZXI","ZXI+"],               "p":[3.99,4.26,4.79,5.45,5.83], "f":["Petrol","CNG"],          "seg":"Hatchback"},
        "Swift":        {"v":["LXI","VXI","ZXI","ZXI+"],                     "p":[6.49,7.49,8.49,9.64],      "f":["Petrol","CNG"],          "seg":"Hatchback"},
        "Baleno":       {"v":["Sigma","Delta","Zeta","Alpha"],                "p":[6.61,7.45,8.45,9.88],      "f":["Petrol","CNG"],          "seg":"Hatchback"},
        "Dzire":        {"v":["LXI","VXI","ZXI","ZXI+"],                     "p":[6.79,7.81,8.85,9.93],      "f":["Petrol","CNG"],          "seg":"Sedan"},
        "Fronx":        {"v":["Sigma","Delta","Zeta","Alpha"],                "p":[7.51,9.04,11.41,13.06],    "f":["Petrol","CNG"],          "seg":"Coupe SUV"},
        "Brezza":       {"v":["LXI","VXI","ZXI","ZXI+"],                     "p":[8.34,10.49,12.52,14.14],   "f":["Petrol","CNG"],          "seg":"SUV"},
        "Ertiga":       {"v":["LXI","VXI","ZXI","ZXI+"],                     "p":[8.69,10.44,12.09,13.08],   "f":["Petrol","CNG"],          "seg":"MPV"},
        "Grand Vitara": {"v":["Sigma","Delta","Zeta","Alpha","Alpha+ Hybrid"],"p":[10.70,13.45,16.45,18.99,19.99],"f":["Petrol","Hybrid"],  "seg":"SUV"},
        "Jimny":        {"v":["Zeta","Alpha"],                                "p":[12.74,15.05],              "f":["Petrol"],                "seg":"Off-Road SUV"},
    },
    "Hyundai": {
        "i20":          {"v":["Era","Magna","Sportz","Asta","Asta(O)"],       "p":[7.04,8.27,9.84,11.12,12.10],"f":["Petrol","Diesel","CNG"],"seg":"Hatchback"},
        "Venue":        {"v":["E","S","S+","SX","SX+","SX(O)"],              "p":[7.94,9.53,10.47,12.08,13.12,13.57],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Creta":        {"v":["E","EX","S","S+","SX","SX(O)"],               "p":[11.00,12.50,14.25,16.50,18.75,20.15],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Creta Electric":{"v":["Executive","Smart","Prime","Excellence"],    "p":[17.99,18.99,21.40,23.50],  "f":["EV"],                    "seg":"Electric SUV"},
        "Alcazar":      {"v":["Prestige","Platinum","Signature"],            "p":[14.99,18.18,20.17],        "f":["Petrol","Diesel"],       "seg":"3-Row SUV"},
        "Tucson":       {"v":["Platinum","Signature 2WD","Signature AWD"],   "p":[26.93,32.25,34.59],        "f":["Petrol","Diesel"],       "seg":"Premium SUV"},
        "Ioniq 5":      {"v":["RWD Standard","RWD Long Range","AWD"],        "p":[44.95,46.95,60.45],        "f":["EV"],                    "seg":"Electric SUV"},
    },
    "Tata": {
        "Tiago":        {"v":["XE","XM","XT","XZ","XZ+"],                    "p":[5.60,6.20,7.25,8.10,8.45], "f":["Petrol","CNG"],          "seg":"Hatchback"},
        "Punch":        {"v":["Pure","Adventure","Accomplished","Creative"],  "p":[6.13,7.49,8.49,10.20],     "f":["Petrol","CNG"],          "seg":"Micro SUV"},
        "Tiago EV":     {"v":["XT","XZ","XZ+","XZ+ LR"],                    "p":[8.69,9.99,11.49,12.04],    "f":["EV"],                    "seg":"Electric Hatchback"},
        "Punch EV":     {"v":["Smart","Adventure","Empowered","Empowered+"], "p":[10.99,13.49,14.49,15.49],  "f":["EV"],                    "seg":"Electric SUV"},
        "Nexon":        {"v":["Smart","Pure","Creative","Fearless","Fearless+"],"p":[8.10,10.49,12.99,14.29,15.50],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Nexon EV":     {"v":["Smart","Creative","Fearless","Fearless+"],    "p":[12.49,15.49,17.49,19.00],  "f":["EV"],                    "seg":"Electric SUV"},
        "Curvv EV":     {"v":["Creative","Fearless","Fearless+"],            "p":[17.49,19.99,21.99],        "f":["EV"],                    "seg":"Electric Coupe SUV"},
        "Harrier":      {"v":["Smart","Pure","Creative","Fearless","Fearless+"],"p":[14.99,17.99,20.99,23.49,26.44],"f":["Petrol","Diesel"],"seg":"Premium SUV"},
        "Safari":       {"v":["Smart+","Creative","Fearless","Fearless+","Gold"],"p":[16.19,21.49,24.49,26.49,27.34],"f":["Petrol","Diesel"],"seg":"3-Row SUV"},
    },
    "Mahindra": {
        "XUV 3XO":      {"v":["MX1","MX2","MX3","AX5 L","AX7 L"],           "p":[7.99,9.48,11.54,14.98,15.49],"f":["Petrol","Diesel"],     "seg":"SUV"},
        "Thar ROXX":    {"v":["MX1","MX3","AX5 L","AX7 L","AX7 AWD L"],     "p":[12.99,15.49,18.79,20.49,22.49],"f":["Petrol","Diesel"],   "seg":"Off-Road SUV"},
        "Scorpio N":    {"v":["Z2","Z4","Z6","Z8","Z8 AWD"],                 "p":[13.85,15.50,18.29,21.99,24.54],"f":["Petrol","Diesel"],   "seg":"SUV"},
        "XUV700":       {"v":["MX","AX3","AX5","AX7","AX7 AWD"],            "p":[13.99,17.99,20.99,24.99,26.70],"f":["Petrol","Diesel"],   "seg":"Premium SUV"},
        "BE 6":         {"v":["Pack One","Pack Two","Pack Three"],           "p":[18.90,23.90,26.90],        "f":["EV"],                    "seg":"Electric Coupe SUV"},
        "XEV 9e":       {"v":["Pack One","Pack Two","Pack Three"],           "p":[21.90,26.90,30.50],        "f":["EV"],                    "seg":"Electric SUV"},
    },
    "Kia": {
        "Sonet":        {"v":["HTE","HTK","HTK+","HTX","HTX+","GTX+"],       "p":[7.99,9.89,11.75,13.19,15.09,15.89],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Seltos":       {"v":["HTK","HTK+","HTX","HTX+","GTX","GTX+"],       "p":[10.90,13.45,15.45,17.29,18.89,20.65],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Carens":       {"v":["Premium","Luxury","Luxury+","X-Line"],        "p":[10.45,14.67,17.49,18.20],  "f":["Petrol","Diesel","CNG"], "seg":"MPV"},
        "EV6":          {"v":["RWD Standard","RWD Long Range","AWD"],        "p":[60.97,63.97,65.97],        "f":["EV"],                    "seg":"Electric GT"},
    },
    "Toyota": {
        "Glanza":       {"v":["E","S","G","V"],                              "p":[6.73,7.59,8.47,10.03],     "f":["Petrol","CNG"],          "seg":"Hatchback"},
        "Hyryder":      {"v":["E","S","G","V Hybrid","V Hybrid AWD"],        "p":[10.73,12.62,14.64,17.99,19.44],"f":["Petrol","Hybrid"],  "seg":"SUV"},
        "Innova Hycross":{"v":["G","V","VX","ZX"],                          "p":[19.77,23.00,26.50,30.05],  "f":["Petrol","Hybrid"],       "seg":"Premium MPV"},
        "Fortuner":     {"v":["4x2 MT","4x2 AT","Legender 4x4"],            "p":[33.43,37.99,50.31],        "f":["Petrol","Diesel"],       "seg":"Premium SUV"},
        "Camry Hybrid": {"v":["Hybrid"],                                     "p":[48.08],                    "f":["Hybrid"],                "seg":"Executive Sedan"},
    },
    "Honda": {
        "Amaze":        {"v":["S MT","V MT","V CVT","VX CVT"],               "p":[7.21,9.03,9.88,11.08],     "f":["Petrol","CNG"],          "seg":"Sedan"},
        "Elevate":      {"v":["V MT","V CVT","SV CVT","ZX CVT"],             "p":[11.69,13.77,15.15,15.96],  "f":["Petrol"],                "seg":"SUV"},
        "City":         {"v":["V MT","V CVT","ZX MT","ZX CVT"],              "p":[11.73,13.55,15.09,15.97],  "f":["Petrol"],                "seg":"Sedan"},
        "City e:HEV":   {"v":["ZX Hybrid"],                                  "p":[19.59],                    "f":["Hybrid"],                "seg":"Hybrid Sedan"},
    },
    "Volkswagen": {
        "Taigun":       {"v":["Comfortline","Highline","Topline","GT Plus"],  "p":[11.69,14.53,17.17,20.43],  "f":["Petrol"],                "seg":"SUV"},
        "Virtus":       {"v":["Comfortline","Highline","Topline","GT Plus"],  "p":[11.56,14.12,16.78,19.41],  "f":["Petrol"],                "seg":"Sedan"},
        "Tiguan":       {"v":["Elegance","R-Line"],                          "p":[35.17,48.97],              "f":["Petrol"],                "seg":"Premium SUV"},
    },
    "Skoda": {
        "Kushaq":       {"v":["Active","Ambition","Style","Monte Carlo"],     "p":[11.09,14.39,17.49,19.49],  "f":["Petrol"],                "seg":"SUV"},
        "Slavia":       {"v":["Active","Ambition","Style","Monte Carlo"],     "p":[10.69,14.19,17.09,18.49],  "f":["Petrol"],                "seg":"Sedan"},
        "Kodiaq":       {"v":["Style","Sportline"],                          "p":[46.89,48.89],              "f":["Petrol"],                "seg":"Premium SUV"},
        "Superb":       {"v":["Laurin & Klement"],                           "p":[54.49],                    "f":["Petrol"],                "seg":"Premium Sedan"},
    },
    "MG": {
        "Hector":       {"v":["Style","Super","Smart Pro","Savvy Pro"],       "p":[13.99,16.30,18.20,21.99],  "f":["Petrol","CNG","Diesel"], "seg":"SUV"},
        "Windsor EV":   {"v":["Excite","Essence","Exclusive"],               "p":[13.50,14.50,15.50],        "f":["EV"],                    "seg":"Electric SUV"},
        "ZS EV":        {"v":["Excite Pro","Essence Pro"],                   "p":[18.98,25.88],              "f":["EV"],                    "seg":"Electric SUV"},
        "Gloster":      {"v":["Super 2WD","Savvy 2WD","Savvy AWD"],          "p":[37.80,44.00,45.00],        "f":["Diesel"],                "seg":"Premium SUV"},
    },
    "Renault": {
        "Kiger":        {"v":["RXE","RXL","RXT","RXZ","RXZ Turbo"],          "p":[5.99,7.49,8.55,10.50,11.23],"f":["Petrol"],              "seg":"SUV"},
        "Triber":       {"v":["RXE","RXL","RXT","RXZ"],                      "p":[6.00,6.99,7.82,8.65],      "f":["Petrol","CNG"],          "seg":"MPV"},
    },
    "Nissan": {
        "Magnite":      {"v":["XE","XL","XV","XV Premium","Turbo XV(O)"],     "p":[5.99,7.09,8.69,10.99,11.39],"f":["Petrol"],              "seg":"SUV"},
    },
    "Citroen": {
        "C3":           {"v":["Live","Feel","Shine"],                         "p":[6.16,7.59,9.19],           "f":["Petrol"],                "seg":"Hatchback"},
        "C3 Aircross":  {"v":["Feel","Feel+ AT","Shine AT"],                  "p":[9.99,13.32,14.49],         "f":["Petrol"],                "seg":"SUV"},
        "eC3":          {"v":["Feel","Shine"],                                "p":[11.50,12.90],              "f":["EV"],                    "seg":"Electric Hatchback"},
    },
    # LUXURY
    "BMW": {
        "3 Series":     {"v":["320i Sport","330i M Sport","M340i"],          "p":[46.90,57.90,72.90],        "f":["Petrol"],                "seg":"Luxury Sedan"},
        "5 Series":     {"v":["520i Luxury","530i M Sport"],                 "p":[67.90,72.90],              "f":["Petrol"],                "seg":"Executive Sedan"},
        "7 Series":     {"v":["740i Luxury","740Ld Luxury","760i xDrive"],   "p":[172,195,253],              "f":["Petrol","Diesel"],       "seg":"Ultra Luxury Sedan"},
        "X1":           {"v":["sDrive18i xLine","sDrive18i M Sport"],        "p":[46.50,56.90],              "f":["Petrol"],                "seg":"Luxury SUV"},
        "X3":           {"v":["xDrive20i","xDrive20d","xDrive30i M Sport"],  "p":[69.90,73.90,90.90],        "f":["Petrol","Diesel"],       "seg":"Luxury SUV"},
        "X5":           {"v":["xDrive40i M Sport","xDrive40d M Sport"],      "p":[93.90,98.90],              "f":["Petrol","Diesel"],       "seg":"Luxury SUV"},
        "iX":           {"v":["xDrive40","xDrive50 Sport"],                  "p":[121,140],                  "f":["EV"],                    "seg":"Electric Luxury SUV"},
    },
    "Mercedes-Benz": {
        "A-Class":      {"v":["A 200 Progressive","A 220 4MATIC"],           "p":[45.50,53.00],              "f":["Petrol"],                "seg":"Luxury Hatchback"},
        "C-Class":      {"v":["C 200","C 220d","C 300d AMG"],               "p":[57.00,62.00,68.00],        "f":["Petrol","Diesel"],       "seg":"Luxury Sedan"},
        "E-Class":      {"v":["E 200","E 220d","E 350d AMG"],               "p":[78.50,84.50,95.00],        "f":["Petrol","Diesel"],       "seg":"Executive Sedan"},
        "S-Class":      {"v":["S 450d","S 500","Maybach S 680"],            "p":[169,220,350],              "f":["Petrol","Diesel"],       "seg":"Ultra Luxury Sedan"},
        "GLA":          {"v":["GLA 200","GLA 220d AMG"],                    "p":[49.90,56.50],              "f":["Petrol","Diesel"],       "seg":"Luxury SUV"},
        "GLC":          {"v":["GLC 220d","GLC 300d AMG"],                   "p":[68.00,80.00],              "f":["Diesel"],                "seg":"Luxury SUV"},
        "GLE":          {"v":["GLE 300d","GLE 450","AMG GLE 53"],           "p":[97.00,110,150],            "f":["Petrol","Diesel"],       "seg":"Luxury SUV"},
        "EQS":          {"v":["EQS 450+","AMG EQS 53"],                     "p":[155,245],                  "f":["EV"],                    "seg":"Electric Luxury Sedan"},
    },
    "Audi": {
        "A4":           {"v":["35 TFSI Premium","45 TFSI Technology"],       "p":[47.34,54.65],              "f":["Petrol"],                "seg":"Luxury Sedan"},
        "A6":           {"v":["45 TFSI","55 TFSI"],                         "p":[63.99,73.99],              "f":["Petrol"],                "seg":"Executive Sedan"},
        "Q3":           {"v":["35 TFSI Premium","40 TFSI Technology"],       "p":[44.89,52.89],              "f":["Petrol"],                "seg":"Luxury SUV"},
        "Q5":           {"v":["45 TFSI","55 TFSI quattro"],                  "p":[67.97,84.15],              "f":["Petrol"],                "seg":"Luxury SUV"},
        "Q7":           {"v":["45 TFSI Technology","55 TFSI quattro"],       "p":[91.83,105],                "f":["Petrol"],                "seg":"Luxury SUV"},
        "e-tron":       {"v":["50 quattro","55 quattro"],                    "p":[114,120],                  "f":["EV"],                    "seg":"Electric Luxury SUV"},
    },
    "Volvo": {
        "XC40":         {"v":["B4 Plus Dark","B4 Plus","B4 Ultimate"],       "p":[57.90,62.90,67.90],        "f":["Petrol"],                "seg":"Luxury SUV"},
        "XC60":         {"v":["B5 Plus Dark","B5 Plus","B6 Ultimate"],       "p":[68.90,73.90,83.90],        "f":["Petrol"],                "seg":"Luxury SUV"},
        "XC90":         {"v":["B6 Plus Dark","B6 Plus 7S","Ultimate 7S"],    "p":[103,107,115],              "f":["Petrol"],                "seg":"Luxury 3-Row SUV"},
        "EX40":         {"v":["Single Motor","Twin Motor"],                  "p":[55.90,63.90],              "f":["EV"],                    "seg":"Electric Luxury SUV"},
    },
    # ULTRA LUXURY
    "Jeep": {
        "Compass":      {"v":["Sport","Longitude","Trailhawk","Model S 4x4"],"p":[20.49,22.99,28.29,30.39],  "f":["Petrol","Diesel"],       "seg":"Premium SUV"},
        "Meridian":     {"v":["Longitude 2WD","Limited 4WD","Overland 4WD"], "p":[29.90,33.50,37.00],        "f":["Diesel"],                "seg":"3-Row SUV"},
        "Wrangler":     {"v":["Unlimited Sport","Unlimited Sahara","Rubicon"],"p":[56.95,62.45,67.65],       "f":["Petrol"],                "seg":"Off-Road Icon"},
    },
    "BYD": {
        "Atto 3":       {"v":["Standard","Extended Range"],                  "p":[33.99,37.99],              "f":["EV"],                    "seg":"Electric SUV"},
        "Seal":         {"v":["Excellence RWD","Performance AWD"],           "p":[41.00,53.00],              "f":["EV"],                    "seg":"Electric Sedan"},
        "eMAX 7":       {"v":["7-Seater"],                                   "p":[26.90],                    "f":["EV"],                    "seg":"Electric MPV"},
    },
    "Porsche": {
        "Macan":        {"v":["Base","S","GTS","Turbo"],                     "p":[89.42,104,114,138],        "f":["Petrol"],                "seg":"Luxury SUV"},
        "Cayenne":      {"v":["Base","S","GTS","Turbo GT"],                  "p":[129,147,193,298],          "f":["Petrol"],                "seg":"Luxury SUV"},
        "911":          {"v":["Carrera","Carrera S","GT3","Turbo S"],        "p":[221,264,379,439],          "f":["Petrol"],                "seg":"Sports Car"},
        "Taycan":       {"v":["RWD","4S","GTS","Turbo","Turbo S"],           "p":[187,209,230,274,314],      "f":["EV"],                    "seg":"Electric Luxury Sedan"},
    },
    "Land Rover": {
        "Defender":     {"v":["90 S","110 S","110 HSE","110 X","130 HSE"],   "p":[107,119,150,198,235],      "f":["Diesel","Petrol"],       "seg":"Luxury Off-Road"},
        "Discovery":    {"v":["S","HSE","HSE Luxury"],                       "p":[98.30,115,145],            "f":["Diesel"],                "seg":"Luxury SUV"},
        "Range Rover Sport":{"v":["Dynamic SE","HSE Dynamic","Autobiography"],"p":[163,193,219],             "f":["Petrol","Diesel"],       "seg":"Luxury SUV"},
        "Range Rover":  {"v":["SE LWB","HSE LWB","Autobiography LWB","SV LWB"],"p":[239,290,365,465],       "f":["Petrol","Diesel"],       "seg":"Ultra Luxury SUV"},
    },
}
