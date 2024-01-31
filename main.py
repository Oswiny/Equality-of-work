import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

url = "https://www.numbeo.com/cost-of-living/prices_by_country.jsp?displayCurrency=USD&itemId=105"
result = requests.get(url).text
soup = BeautifulSoup(result, 'html.parser')

script_tag = soup.findAll('script')[15]

data_start = script_tag.text.find("data.addRows") + len("data.addRows")
data_end = script_tag.text.find(";", data_start)
data_text = script_tag.text[data_start:data_end].strip()

country_data = eval(data_text)

update_tag = soup.findAll('p')[-2]
update_start = update_tag.text.find("Last Update:")
update_end = update_tag.text.find("CST", update_start) + len("CST")
update_text = update_tag.text[update_start:update_end].strip()
print(update_text)

global item_price
correct_input = 0
while not correct_input:
    try:
        item_price = float(input("Enter item price: "))
    except ValueError:
        print("Your input contains non-numeric characters")
        continue
    if item_price < 0:
        print("Do not enter negative values!")
    elif item_price == 0:
        print("Do not enter 0 as value!")
    else:
        break

country_names = list()
for data in country_data:
    country_names.append(data[0])

country_avg_monthly_salary = list()
for data in country_data:
    country_avg_monthly_salary.append(data[1])

monthly_hours_worked = 173.33
country_avg_hourly_salary = list()
for data in country_avg_monthly_salary:
    country_avg_hourly_salary.append(data / monthly_hours_worked)

country_needed_hours = list()
for data in country_avg_hourly_salary:
    country_needed_hours.append(float(round(item_price / data, 1)))


def graph_hours_of_work_bar(pcountry_names, pcountry_needed_hours, pitem_price):
    print("Input was accepted")
    fig, ax = plt.subplots(figsize=(20, 40))
    chart = plt.barh(pcountry_names, pcountry_needed_hours, color=['skyblue', 'lightcoral'], height=0.7)

    plt.bar_label(chart, fontsize=10, fmt="%.1f", label_type="edge", fontweight="bold")
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    ax.spines[["right", "top", "bottom"]].set_visible(False)
    # ax.xaxis.set_visible(False)
    plt.title(f"Hours Needed to Work for a ${pitem_price} Product", fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("neededworkhours.png")


def graph_price_equality_bar(pcountry_names, pcountry_avg_hourly_salary, pcountry_needed_hours, pitem_price):
    correct_input = 0
    index = 0
    while not correct_input:
        base_country = input("Enter your base country (for list of countries type 'help'): ")
        if base_country == "help":
            for name in pcountry_names:
                print(name)
            continue
        for name in pcountry_names:
            if name == base_country:
                correct_input = 1
                print("Input was accepted")
                break
            else:
                index += 1
        if correct_input == 1:
            break
        index = 0
        print("There seems to be error please try again")

    base_country_hours = pcountry_needed_hours[index]
    pcountry_names.pop(index)
    pcountry_avg_hourly_salary.pop(index)

    country_equal_price = list()
    for hourly_salary in pcountry_avg_hourly_salary:
        country_equal_price.append(base_country_hours * hourly_salary)

    fig, ax = plt.subplots(figsize=(50, 80))
    chart = plt.barh(pcountry_names, country_equal_price, color=['skyblue', 'lightcoral'], height=0.7)

    plt.bar_label(chart, fontsize=30, fmt="%.1f", label_type="edge", fontweight="bold")
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    ax.spines[["right", "top", "bottom"]].set_visible(False)
    # ax.xaxis.set_visible(False)
    plt.title(
        f"Estimating the Cost of a ${pitem_price} Product in Different Countries with Equal Work Hours in the {base_country}",
        fontsize=30)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.tight_layout()
    plt.savefig("priceequality.png")


correct_input = 0
while not correct_input:
    choose_graph = input("Do you want 'price equality' graph or 'needed work hours' graph: ")
    if choose_graph == "price equality":
        graph_price_equality_bar(country_names, country_avg_hourly_salary, country_needed_hours, item_price)
        break
    elif choose_graph == "needed work hours":
        graph_hours_of_work_bar(country_names, country_needed_hours, item_price)
        break
    else:
        print("There seems to be an error try again")
