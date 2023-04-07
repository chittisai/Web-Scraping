import requests  # form pip install requests
from bs4 import BeautifulSoup  # from pip install bs4
import xlsxwriter  # from pip install XlsxWriter

# reads html file
def read(path):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content


# returns the list of doctors profiles
def get_data_of_all(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    provider_cards = soup.find_all(
        "div", {"class": "NewProviderCard__Wrapper-sc-12vowct-0"}
    )
    lists = []
    for card in provider_cards:
        s = card.find("a", href=True)
        lists.append("https://intake.steerhealth.io" + s["href"])
    return lists


# returns each doctor's information in dictionary
def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    name = soup.find("b")
    details = soup.find_all("span")

    if (
        name != None
        and details != None
        and len(details) >= 5
        and len(details[2].text.split(",")) >= 2
    ):
        name = name.text
        spec = details[1].text
        city = details[2].text.split(",")[0]
        state = details[2].text.split(",")[1]
        phn = details[5].text
        addr = details[3].text

        dictData = {
            "Full Name": name,
            "Speciality": spec,
            "Full Address": addr,
            "City": city,
            "State": state,
            "Phone": phn,
        }
        return dictData
    else:
        return None


# makes excel file of list of dictionaries of doctor information
def make_excel(doctor_list):
    workbook = xlsxwriter.Workbook("DoctorInfo.xlsx")
    worksheet = workbook.add_worksheet("Info")

    worksheet.write(0, 0, " ")
    worksheet.write(0, 1, "Full Name")
    worksheet.write(0, 2, "Speciality")
    worksheet.write(0, 3, "Full Address")
    worksheet.write(0, 4, "City")
    worksheet.write(0, 5, "State")
    worksheet.write(0, 6, "Phone")

    for index, entry in enumerate(doctor_list):
        worksheet.write(index + 1, 0, str(index))
        worksheet.write(index + 1, 1, entry["Full Name"])
        worksheet.write(index + 1, 2, entry["Speciality"])
        worksheet.write(index + 1, 3, entry["Full Address"])
        worksheet.write(index + 1, 4, entry["City"])
        worksheet.write(index + 1, 5, entry["State"])
        worksheet.write(index + 1, 6, entry["Phone"])

    workbook.close()


# path to the html file in computer
# Note: I have done this because no library is able to get the information of each and every tag
file_path = "C:/Users/chitti sai/Desktop/index.html"

html = read(file_path)

listOfDoctors = get_data_of_all(html)

doctorsInfo = []
for doctor in listOfDoctors:
    data = get_info(doctor)
    if data != None:
        doctorsInfo.append(data)

make_excel(doctorsInfo)
