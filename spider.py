from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

def get_calendar_position(year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    thedate = datetime(year, month, day)
    weekday = thedate.weekday()  # 0表示星期一，6表示星期日

    # 计算给定日期所在的周和列位置
    first_day = datetime(year, month, 1)
    first_weekday = (first_day.weekday() + 1) % 7 + 1
    position = 1 + ((day - 1) // 7) + (((day - 1) % 7 + first_weekday) // 8)
    column = (weekday + 1) % 7 + 1

    return position, column

def monthStr(month):

    month_mapping = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }
    return month_mapping[month]


def calculate_interval(start_year, start_month, start_day, end_year, end_month, end_day):
    # 创建开始日期和结束日期的datetime对象
    start_date = datetime(start_year, start_month, start_day)
    end_date = datetime(end_year, end_month, end_day)

    # 计算日期间隔
    delta = end_date - start_date

    # 计算365天的乘积来比较
    nine_years_in_days = 9 * 365

    if delta.days <= nine_years_in_days:
        # 如果间隔小于等于9年，返回原始的开始日期年、月、日
        return str(start_year), str(start_month).zfill(2), str(start_day).zfill(2)
    else:
        # 如果间隔大于9年，返回结束日期九年前的年、月、日
        new_end_date = end_date - timedelta(days=nine_years_in_days)
        return str(new_end_date.year), str(new_end_date.month).zfill(2), str(new_end_date.day).zfill(2)

j=1

while j<=50:
    driver = webdriver.Chrome()

    urlForStation = "https://www.ncei.noaa.gov/cdo-web/datatools/lcd"

    driver.get(urlForStation)

    driver.implicitly_wait(100)

    selectElement = Select(driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div[1]/div/select'))

    selectElement.select_by_visible_text('State')

    selectElement = Select(driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div[2]/div[3]/select'))

    selectElement.select_by_visible_text('Washington')
    # 上面做了一个界面的选取 选了一个 界面 然后选中 州 和 华盛顿
    if j>25 :
        i = j-25
    else:
        i = j
    if j>25:
        nextpageButton=driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/ul[1]/li[3]/a")
        nextpageButton.click()
    #因为 华盛顿 只有 50个station 25个一页 所以大于25的要切到下一页

    spanElement=driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/table/tbody/tr[{}]/td[1]/div/div[3]/span[1]'.format(i))
    beginDate = spanElement.get_attribute('innerHTML')
    spanElement=driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/table/tbody/tr[{}]/td[1]/div/div[3]/span[2]'.format(i))
    endDate = spanElement.get_attribute('innerHTML')

    #查看当前这一个station的开始日期和结束日期


    buttonElement = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/table/tbody/tr[{}]/td[2]/input'.format(i))
    buttonElement.click()
    # add to cart
    buttonElement = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/a/span')
    buttonElement.click()


    # 进入购物车

    driver.refresh()
    #要刷新一下页面 模拟点击会出现bug

    csv = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[1]/div/div/div/div[2]/input')
    csv.click()
    #选中csv格式

    date_input = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/input')
    date_input.click()

    #把开始 结束 的年月日提取出来
    byear, bmonth, bday = beginDate.split("-")
    eyear, emonth, eday = endDate.split("-")

    #做了一个计算，控制开始日期和结束日期在九年之内
    byear, bmonth, bday = calculate_interval(int(byear), int(bmonth), int(bday), int(eyear), int(emonth), int(eday))


    #首先先选到开始的日期
    #选到开始的年 直接用就可以 选月 需要转化，因为原来是数字，选的时候是jan 这种缩写，day则需要在确定年和月后，具体定某一行某一列，这里需要一个函数来算
    selectYear=Select(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[1]/span/div/div/div/select[1]'))
    selectYear.select_by_visible_text(byear)
    selectMonth =Select(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[1]/span/div/div/div/select[2]'))
    bmonthName = monthStr(bmonth)
    selectMonth.select_by_visible_text(bmonthName)
    position, column = get_calendar_position(int(byear), int(bmonth), int(bday))
    Daybutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[1]/span/div/table/tbody/tr[{}]/td[{}]".format(position,column),)
    Daybutton.click()

    #同理，结束也算一下
    selectYear = Select(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[2]/span/div/div/div/select[1]'))
    selectYear.select_by_visible_text(eyear)
    selectMonth = Select(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[2]/span/div/div/div/select[2]'))
    emonthName = monthStr(emonth)
    selectMonth.select_by_visible_text(emonthName)
    position, column = get_calendar_position(int(eyear), int(emonth), int(eday))
    Daybutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[2]/span/div/table/tbody/tr[{}]/td[{}]".format(position, column), )
    Daybutton.click()

    #点那个日期确定
    button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/div/div/div/div/div/div[4]/form/button[1]")
    button.click()


    #点continue
    continuebutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[1]/div[6]/button")
    continuebutton.click()

    input1=driver.find_element_by_xpath("/html/body/div/div[2]/div/form/div/div[3]/input[1]")
    input2=driver.find_element_by_xpath("/html/body/div/div[2]/div/form/div/div[3]/input[2]")
    input1.send_keys("szf010626@126.com")
    input2.send_keys("szf010626@126.com")

    submitbutton= driver.find_element_by_xpath("/html/body/div/div[2]/div/form/div/div[4]/input")
    submitbutton.click()

    driver.quit()
    j=j+1