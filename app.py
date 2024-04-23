import streamlit as st
import joblib
import scraped_prices

bank_balance = joblib.load("bank_balance.pkl")
currency_balance = joblib.load("currency_balance.pkl")
stock_balance = joblib.load("stock_balance.pkl")

stock_prices = {
        'tabgd': scraped_prices.fetch_current_stock_price('tabgd'),
        'orge': scraped_prices.fetch_current_stock_price('orge'),
        'kmpur': scraped_prices.fetch_current_stock_price('kmpur'),
        'odine': scraped_prices.fetch_current_stock_price('odine')
    }

currency_prices = {
        'usd': scraped_prices.fetch_currency_current_sell_price('usd'),
        'alt' : scraped_prices.fetch_currency_current_sell_price('alt'),
    }

toplam = 0
stock_toplam = 0
currency_toplam = 0

col_hisseler, col_doviz, col_balans_toplam = st.columns([2,2,1])

with col_hisseler:
    
    st.markdown('<span style="font-size: 35px; font-weight: bold;">HİSSE</span>', unsafe_allow_html=True)
    
    for stock, stock_amount in stock_balance.items():
        
        st.markdown(f'<span style="font-size: 24px; font-weight: bold;">{stock.upper()}</span>', unsafe_allow_html=True)
        qty_stock = st.number_input('Adet:', value=stock_amount, min_value=0, key=f'stock_{stock}')
        
        stock_balance[stock] = qty_stock
        unit_price_stock = stock_prices[stock]
        total_value_stock = round(qty_stock * unit_price_stock, 2)
        
        st.write(f'Birim Fiyat: {unit_price_stock}')
        st.write(f'Toplan Değer: {total_value_stock}')
        
        toplam += total_value_stock
        stock_toplam += total_value_stock
        
        joblib.dump(stock_balance, "stock_balance.pkl")
        st.write("\n")
        
    formatted_stock_toplam = "{:,.2f}".format(stock_toplam)
    st.markdown(f'<span style="font-size: 23px; font-weight: bold;">Hisse Toplam: {formatted_stock_toplam}</span>', unsafe_allow_html=True)
    
with col_doviz:
    
    st.markdown('<span style="font-size: 35px; font-weight: bold;">DÖVİZ</span>', unsafe_allow_html=True)
    
    for currency, currency_amount in currency_balance.items():
        
        st.markdown(f'<span style="font-size: 24px; font-weight: bold;">{currency.upper()}</span>', unsafe_allow_html=True)
        qty_currency = st.number_input('Adet:', value=float(currency_amount), min_value=0.0, step = 0.01, key=f'currency_{currency}')
        
        currency_balance[currency] = qty_currency
        unit_price_currency = currency_prices[currency]
        total_value_currency = round(qty_currency * unit_price_currency, 2)
        
        st.write(f'Birim Fiyat: {unit_price_currency}')
        st.write(f'Toplan Değer: {total_value_currency}')
        
        toplam += total_value_currency
        currency_toplam += total_value_currency
        
        joblib.dump(currency_balance, "currency_balance.pkl")
        st.write("\n")
                
    formatted_currency_toplam = "{:,.2f}".format(currency_toplam)
    st.markdown(f'<span style="font-size: 23px; font-weight: bold;">Döviz Toplam: {formatted_currency_toplam}</span>', unsafe_allow_html=True)
    
with col_balans_toplam:

    st.markdown(f'<span style="font-size: 24px; font-weight: bold;">BANKA HESABI</span>', unsafe_allow_html=True)
    bank_balance_value = st.number_input('Banka Balansı:', value=float(bank_balance), min_value=0.0, step = 0.01, key=f'bank_balans')
    joblib.dump(bank_balance_value, "bank_balance.pkl") 

    st.write('\n')
    
    genel_toplam = toplam + bank_balance_value
    formatted_genel_toplam = "{:,.2f}".format(genel_toplam)
    st.markdown(f'<span style="font-size: 30px; font-weight: bold;">GENEL TOPLAM</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size: 23px; font-weight: bold;">₺ {formatted_genel_toplam}</span>', unsafe_allow_html=True)
    
    st.write('\n')
    
    if st.button("Refresh Page", key="refresh_button"):
        st.experimental_rerun()