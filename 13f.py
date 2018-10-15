import urllib

url='https://www.sec.gov/Archives/edgar/data/1280200/000108514618002323/form13fInfoTable.xml'

def load_xml(url):
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()

    return data.decode("utf-8") 

def end_token(xml, start):
    return xml.find('</', start)

def get_opr(xml, idx):
    opr = []
    while True:
        infotbl = xml.find('<infoTable>', idx)
        if infotbl == -1:
            break
        idx = infotbl + 1
        issuer = xml.find('Issuer>', infotbl)
        value = xml.find('value>', infotbl)
        shares = xml.find('sshPrnamt>', infotbl)
        decisin = xml.find('Discretion>', infotbl)

        s_name = xml[issuer + 7:end_token(xml, issuer)]
        s_value = float(xml[value + 6:end_token(xml, value)])
        s_quant = float(xml[shares + 10:end_token(xml, shares)])
        s_opr = xml[decisin + 11:end_token(xml,decisin)]

        opr.append('' + s_opr + ' ' + s_name + ' @ ' + "{:.2f}".format((s_value * 1000) / s_quant))
    return opr

xml = load_xml(url)
opr = get_opr(xml, 0)

for i in range(0, len(opr)):
    print(opr[i])
