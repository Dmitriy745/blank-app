import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Настройка страницы
st.set_page_config(page_title="Учет расходов", page_icon="💰", layout="wide")

# Заголовок приложения
st.title("")
st.markdown("---")

# Функция для загрузки данных из CSV файла
def load_data():
    if os.path.exists("index.csv"):
        try:
            df = pd.read_csv("index.csv")
            # Преобразование даты в правильный формат
            df['дата'] = pd.to_datetime(df['дата'])
            return df
        except:
            return pd.DataFrame(columns=['дата', 'сумма'])
    else:
        return pd.DataFrame(columns=['дата', 'сумма'])

# Функция для сохранения данных в CSV файл
def save_data(date, amount):
    new_row = {'дата': date, 'сумма': amount}
    
    # Создаем новый DataFrame с новой записью
    new_df = pd.DataFrame([new_row])
    
    # Если файл существует, добавляем к существующим данным
    if os.path.exists("index.csv"):
        existing_df = pd.read_csv("index.csv")
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
    
    # Сохраняем в CSV
    updated_df.to_csv("index.csv", index=False)

# Основной интерфейс
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Добавление записи")
    
    # Элементы ввода
    selected_date = st.date_input(
        "Выберите дату:",
        value=datetime.now(),
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now()
    )
    
    amount = st.number_input(
        "Введите колличество:",
        min_value=0.0,
        max_value=1000000.0,
        value=0.0,
        step=100.0
    )
    
    # Кнопка для добавления записи
    if st.button("💾 Записать в файл", type="primary"):
        if amount > 0:
            save_data(selected_date.strftime("%Y-%m-%d"), amount)
            st.success(f"✅ Запись добавлена: {selected_date.strftime('%d.%m.%Y')} - {amount:.2f} руб.")
            
            # Обновляем данные для отображения
            st.rerun()
        else:
            st.warning("⚠️ Введите сумму больше 0")

with col2:
    st.header("📊 Диаграмма")
    
    # Загружаем данные
    df = load_data()
    
    if not df.empty:
        # Сортируем по дате для правильного отображения на графике
        df = df.sort_values('дата')
        
        # Создаем интерактивную диаграмму
        fig = px.line(
            df, 
            x='дата', 
            y='сумма',
            title='Динамика',
            labels={'дата': 'Дата', 'сумма': 'Клики'},
            markers=True
        )
        
        # Настраиваем внешний вид графика
        fig.update_traces(
            line=dict(color='#FF4B4B', width=3),
            marker=dict(size=8, color='#FF4B4B')
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Дополнительная информация
        st.subheader("📋 История записей")
        
        # Отображаем данные в таблице с форматированием даты
        display_df = df.copy()
        display_df['дата'] = display_df['дата'].dt.strftime('%d.%m.%Y')
        display_df['сумма'] = display_df['сумма'].apply(lambda x: f"{x:.2f} руб.")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Статистика
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Всего записей", len(df))
        
        with col_stat2:
            total_amount = df['сумма'].sum()
            st.metric("Общее колличество", f"{total_amount:.2f} руб.")
        
        with col_stat3:
            avg_amount = df['сумма'].mean()
            st.metric("Средняя", f"{avg_amount:.2f} руб.")
            
    else:
        st.info("📈 Данные отсутствуют. Добавьте первую запись, чтобы увидеть диаграмму.")

# Боковая панель с дополнительными функциями
with st.sidebar:
    st.header("⚙️ Управление данными")
    
    # Просмотр сырых данных
    if st.button("📄 Просмотреть файл index.csv"):
        df = load_data()
        if not df.empty:
            st.write("Содержимое файла index.csv:")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Файл index.csv пуст или не существует")
    
    # Очистка данных
    if st.button("🗑️ Очистить все данные", type="secondary"):
        if os.path.exists("index.csv"):
            os.remove("index.csv")
            st.success("Все данные очищены!")
            st.rerun()
        else:
            st.info("Файл index.csv не существует")
    
    st.markdown("---")
    st.markdown("### Инструкция:")
    st.markdown("""
    1. Выберите дату
    2. Введите сумму
    3. Нажмите «Записать в файл»
    4. Диаграмма обновится автоматически
    """)

# Футер
st.markdown("---")
st.markdown("**")
