# import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# ## Hisseler ##

# def stocks_table():

#     url = 'https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx'
#     stocks_df = pd.read_html(url)[2]

#     stocks_df['Hisse'] = stocks_df['Hisse'].str.replace('  \u200b', '')
#     stocks_df['Son Fiyat (TL)'] = stocks_df['Son Fiyat (TL)'].str.replace(',', '').str.replace('.', '')
#     stocks_df['Son Fiyat (TL)'] = pd.to_numeric(stocks_df['Son Fiyat (TL)']) 
#     stocks_df['Son Fiyat (TL)'] = stocks_df['Son Fiyat (TL)'] / 100

#     return stocks_df

# def fetch_current_stock_price(stock):

#     stock_df = stocks_table()
#     return stock_df[stock_df['Hisse'] == stock.upper()]['Son Fiyat (TL)'].iloc[0]


# ## Dovizler ##


# def currency_table():

#     banka_alis_fiyatlari = []
#     banka_satis_fiyatlari = []
#     doviz_isimleri = ['USD','EUR','ALT','GBP','CHF','AUD','CAD','CNY','DKK','JPY','NOK','SAR','SEK']

#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     driver = webdriver.Chrome(options=chrome_options)

#     driver.get('https://webforms.garantibbva.com.tr/currency-convertor/?lang=tr')
#     driver.implicitly_wait(20)

#     shadow_root = (driver
#                    .find_element(By.CSS_SELECTOR, '[id="cells-template-home"]').shadow_root
#                    .find_element(By.CSS_SELECTOR, 'currency-converter-page').shadow_root
#                    )

#     # Banka Alis Satis Fiyatlari

#     currency_table_cell = shadow_root.find_elements(By.CSS_SELECTOR, '.currencyTableOtherColumns.cell')
    
#     for i, element in enumerate(currency_table_cell, start=1):
#         value = element.text.strip()
#         if i % 2 == 0:
#             banka_satis_fiyatlari.append(value)
#         else:
#             banka_alis_fiyatlari.append(value)
        
#     df_doviz = pd.DataFrame()

#     df_doviz['Doviz Cinsi'] = doviz_isimleri
#     df_doviz['Banka Alis'] = banka_alis_fiyatlari
#     df_doviz['Banka Satis'] = banka_satis_fiyatlari

#     df_doviz['Banka Alis'] = df_doviz['Banka Alis'].str.replace(',', '.').astype(float)
#     df_doviz['Banka Satis'] = df_doviz['Banka Satis'].str.replace(',', '.').astype(float)

#     driver.quit() 

#     return df_doviz


# def fetch_currency_current_sell_price(currency):

#     currency_df = currency_table()
#     return currency_df[currency_df['Doviz Cinsi'] == currency.upper()]['Banka Alis'].iloc[0]

# def fetch_currency_current_buy_price(currency):

#     currency_df = currency_table()
#     return currency_df[currency_df['Doviz Cinsi'] == currency.upper()]['Banka Satis'].iloc[0]

# !pip list

import pandas as pd
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def fetch_current_stock_price(stock):
    
    stock_name = f"{stock.upper()}.IS"
    stock_val = yf.Ticker(stock_name)
    hist = stock_val.history(period="1d", interval="1m")
    last_price = hist['Close'].iloc[-1] if not hist.empty else None
    
    return round(last_price, 2)
    

def currency_table():
    
    banka_alis_fiyatlari = []
    banka_satis_fiyatlari = []
    doviz_isimleri = ['USD', 'EUR', 'ALT', 'GBP', 'CHF', 'AUD', 'CAD', 'CNY', 'DKK', 'JPY', 'NOK', 'SAR', 'SEK']
    
    driver = get_driver()
    try:
        driver.get('https://webforms.garantibbva.com.tr/currency-convertor/?lang=tr')
        driver.implicitly_wait(20)
        shadow_root = (driver.find_element(By.CSS_SELECTOR, '[id="cells-template-home"]').shadow_root.find_element(By.CSS_SELECTOR, 'currency-converter-page').shadow_root)
        currency_table_cells = shadow_root.find_elements(By.CSS_SELECTOR, '.currencyTableOtherColumns.cell')
        
        for i, element in enumerate(currency_table_cells, start=1):
            value = element.text.strip().replace(',', '.')
            if i % 2 == 0:
                banka_satis_fiyatlari.append(float(value))
            else:
                banka_alis_fiyatlari.append(float(value))
    finally:
        driver.quit()
    
    df_doviz = pd.DataFrame({
        'Doviz Cinsi': doviz_isimleri,
        'Banka Alis': banka_alis_fiyatlari,
        'Banka Satis': banka_satis_fiyatlari
    })
    return df_doviz

def fetch_currency_current_sell_price(currency):
    currency_df = currency_table()
    return currency_df.loc[currency_df['Doviz Cinsi'].str.upper() == currency.upper(), 'Banka Alis'].iloc[0]

def fetch_currency_current_buy_price(currency):
    currency_df = currency_table()
    return currency_df.loc[currency_df['Doviz Cinsi'].str.upper() == currency.upper(), 'Banka Satis'].iloc[0]


