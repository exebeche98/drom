import random
from time import sleep
from matplotlib.pyplot import table
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

ua = UserAgent()
headers = {
    "Accept": "*/*",
    "User-Agent": ua.random
}
def create_empty_table(path, column_names):
    with open(path, "w", encoding= "UTF-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((column_names))

def page_request(page_number):
    '''
    Take page withs ads
    '''
    try:
        url = f"https://auto.drom.ru/region70/all/page{page_number}"
        req = requests.get(url, headers = headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        print(f"Page {page_number} download successful")
        return soup
    except:
        print(f"Page {page_number} download failed")
        return False      

def get_table_info(index, table_head):
    try:
        info = table_head[index].find('td')
        #print(f"{index} {info.text}")
        return info.text
    except:
        print(f"Exeption for index {index}")
        return None
    
def get_base_info(ref):
    car_list = []
    req = requests.get(ref, headers = headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    table_head = soup.find(class_ = "css-xalqz7 eppj3wm0").find_all("tr")#.find_all("th")

    car_list.append(get_table_info(0, table_head)) # Engine
    car_list.append(get_table_info(1, table_head)) # Power
    car_list.append(get_table_info(3, table_head)) # Transmission
    car_list.append(get_table_info(4, table_head)) # wheel_drive
    car_list.append(get_table_info(5, table_head)) # color
    car_list.append(get_table_info(6, table_head)) # mileage
    car_list.append(get_table_info(7, table_head)) # steering_wheel
    
    
    gibdd_info = soup.find(class_ = "css-p3p0wz efk53ec0")
    if(gibdd_info is not None):
        gibdd_info = gibdd_info.find_all(class_ = "css-13qo6o5 ev29ov71")
        car_registration_records = gibdd_info[1].text.split(' ')[0]
    else:
        car_registration_records = None

    car_list.append(car_registration_records) # car_registration_records
    print(car_list)
    return car_list

def get_car_info(soup_):
    item_text = soup_.text

    # 0Name, 1Year, 2Enginge|Fuel|Volume, 3Power, 4Transmission, 5Wheel_drive, 6color, 7millage, 8steeringwheel, 9regestration records
    car_list = [] # for single car
    car_href = soup_.get("href") # ref to full car ad
    car_list.append(str(item_text).split(',')[0]) # Name
    car_list.append(str(item_text).split(',')[1][1:5]) # Year
    
    req = requests.get(car_href, headers = headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    car_list += get_base_info(car_href)
    
    print(car_list)
    
    return car_list



def main():
    table_path = "data/cars_data.csv"
    colum_names = ['Name', 'Year', 'Engine', 'Power', 'Transmission', 'Wheel_drive' ,
                    'Color', 'Mileage', 'Steering_wheel', 'Registration records count']
    create_empty_table(table_path,colum_names)
    page_number = 0

    while(True):
        soup = page_request(page_number)

        if(soup == False):
            break
        else:
            all_cars_hrefs = soup.find_all(class_ = "css-1ctbluq ewrty961")
            
            cars_info = []
            for index, item in enumerate(all_cars_hrefs):
                car_info = get_car_info(item)
                cars_info.insert(0, car_info)
                print(f"Car {index} on page {page_number} is done successfuly")

            with open(table_path, "a", encoding= "UTF-8-sig", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(cars_info)

            print(f"Page {page_number} is finished")
            page_number +=1



if __name__ == '__main__':
    main()
    