# Веб-презентация "Возможности data.table в R"
# Демонстрация основных функций для работы с данными
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(
    page_title="Возможности data.table в R",
    page_icon="📊",
    layout="wide"
)

# Главный заголовок
st.title("📊 Возможности пакета data.table в R")
st.markdown("### Демонстрация основных функций для работы с данными")

# Боковая панель с навигацией
st.sidebar.title("Навигация")
sections = [
    "Введение",
    "Синтаксис data.table", 
    "Фильтрация данных",
    "Индексация",
    "SQL-подобные запросы",
    "IF-THEN-ELSE операции",
    "Объединение данных",
    "Производительность",
    "Заключение"
]

selected_section = st.sidebar.selectbox("Выберите раздел:", sections)

# Создание тестовых данных (имитация данных Санкт-Петербурга)
@st.cache_data
def create_sample_data():
    np.random.seed(123)
    
    # Районы Санкт-Петербурга
    districts = ["Центральный", "Невский", "Василеостровский", "Петроградский", 
                "Красногвардейский", "Московский", "Фрунзенский", "Приморский"]
    
    # Типы мест размещения Wi-Fi
    location_types = ["Парк", "Библиотека", "Музей", "Торговый центр", 
                     "Станция метро", "Больница", "Школа", "Университет"]
    
    # Создаем датасет Wi-Fi зон
    wifi_zones = pd.DataFrame({
        'id': range(1, 501),
        'district': np.random.choice(districts, 500),
        'location_type': np.random.choice(location_types, 500),
        'address': [f"ул. {np.random.choice(['Невский пр.', 'Литейный пр.', 'Садовая ул.', 'Московский пр.', 'Ленинский пр.'])}, {np.random.randint(1, 201)}" for _ in range(500)],
        'latitude': np.random.uniform(59.8, 60.1, 500),
        'longitude': np.random.uniform(30.1, 30.5, 500),
        'speed_mbps': np.random.choice([10, 25, 50, 100], 500, p=[0.3, 0.4, 0.2, 0.1]),
        'is_active': np.random.choice([True, False], 500, p=[0.9, 0.1]),
        'installation_year': np.random.randint(2015, 2025, 500),
        'users_per_day': np.random.randint(10, 501, 500)
    })
    
    # Создаем данные о видеокамерах
    cameras = pd.DataFrame({
        'camera_id': range(1, 301),
        'district': np.random.choice(districts, 300),
        'camera_type': np.random.choice(["Дорожная", "Дворовая", "Парковая", "Транспортная"], 300),
        'address': [f"ул. {np.random.choice(['Невский пр.', 'Литейный пр.', 'Садовая ул.', 'Московский пр.', 'Ленинский пр.'])}, {np.random.randint(1, 201)}" for _ in range(300)],
        'latitude': np.random.uniform(59.8, 60.1, 300),
        'longitude': np.random.uniform(30.1, 30.5, 300),
        'resolution': np.random.choice(["HD", "Full HD", "4K"], 300, p=[0.2, 0.6, 0.2]),
        'is_working': np.random.choice([True, False], 300, p=[0.95, 0.05]),
        'installation_year': np.random.randint(2010, 2025, 300)
    })
    
    return wifi_zones, cameras

wifi_zones, cameras = create_sample_data()

# Раздел: Введение
if selected_section == "Введение":
    st.header("🎯 Что такое data.table?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **data.table** - это пакет R, который предоставляет расширенную версию `data.frame` с:
        
        - 🚀 **Высокой производительностью** для больших данных
        - 📝 **Лаконичным синтаксисом** для манипуляций с данными  
        - 🔍 **SQL-подобными операциями**
        - ⚡ **Эффективной индексацией**
        - 💾 **Экономией памяти** через модификацию по ссылке
        """)
        
        st.info("💡 В этой презентации мы используем Python/pandas для демонстрации концепций data.table")
    
    with col2:
        st.metric("Версия data.table", "1.14.8")
        st.metric("Строк данных Wi-Fi", len(wifi_zones))
        st.metric("Строк данных камер", len(cameras))
    
    st.subheader("📊 Обзор данных")
    
    tab1, tab2 = st.tabs(["Wi-Fi зоны", "Видеокамеры"])
    
    with tab1:
        st.write("**Данные о Wi-Fi зонах Санкт-Петербурга:**")
        st.dataframe(wifi_zones.head(10), use_container_width=True)
        
    with tab2:
        st.write("**Данные о видеокамерах Санкт-Петербурга:**")
        st.dataframe(cameras.head(10), use_container_width=True)

# Раздел: Синтаксис data.table
elif selected_section == "Синтаксис data.table":
    st.header("📝 Основной синтаксис data.table")
    
    st.markdown("""
    ### Структура DT[i, j, by]
    
    Основная структура data.table выглядит как **`DT[i, j, by]`**, где:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **i** - строки
        
        Эквивалент WHERE в SQL
        
        Фильтрация и выбор строк
        """)
    
    with col2:
        st.success("""
        **j** - столбцы
        
        Эквивалент SELECT в SQL
        
        Выбор и вычисление столбцов
        """)
    
    with col3:
        st.warning("""
        **by** - группировка
        
        Эквивалент GROUP BY в SQL
        
        Группировка для агрегации
        """)
    
    st.markdown("### Примеры синтаксиса:")
    
    code_examples = {
        "Выбор строк": "DT[district == 'Центральный']",
        "Выбор столбцов": "DT[, .(address, speed_mbps)]", 
        "Группировка": "DT[, .N, by = district]",
        "Комбинированный": "DT[is_active == TRUE, .(avg_speed = mean(speed_mbps)), by = district]"
    }
    
    for title, code in code_examples.items():
        st.code(f"# {title}\n{code}", language="r")

# Раздел: Фильтрация данных
elif selected_section == "Фильтрация данных":
    st.header("🔍 Фильтрация данных")
    
    st.subheader("Простая фильтрация")
    
    # Интерактивные фильтры
    col1, col2 = st.columns(2)
    
    with col1:
        selected_district = st.selectbox("Выберите район:", ["Все"] + sorted(wifi_zones['district'].unique()))
        min_speed = st.slider("Минимальная скорость (Мбит/с):", 0, 100, 25)
    
    with col2:
        selected_type = st.selectbox("Тип локации:", ["Все"] + sorted(wifi_zones['location_type'].unique()))
        only_active = st.checkbox("Только активные зоны", value=True)
    
    # Применяем фильтры
    filtered_data = wifi_zones.copy()
    
    if selected_district != "Все":
        filtered_data = filtered_data[filtered_data['district'] == selected_district]
    
    if selected_type != "Все":
        filtered_data = filtered_data[filtered_data['location_type'] == selected_type]
    
    filtered_data = filtered_data[filtered_data['speed_mbps'] >= min_speed]
    
    if only_active:
        filtered_data = filtered_data[filtered_data['is_active'] == True]
    
    st.write(f"**Результат фильтрации: {len(filtered_data)} записей**")
    st.dataframe(filtered_data, use_container_width=True)
    
    # Код data.table
    st.subheader("Эквивалентный код в data.table:")
    
    filter_conditions = []
    if selected_district != "Все":
        filter_conditions.append(f"district == '{selected_district}'")
    if selected_type != "Все":
        filter_conditions.append(f"location_type == '{selected_type}'")
    filter_conditions.append(f"speed_mbps >= {min_speed}")
    if only_active:
        filter_conditions.append("is_active == TRUE")
    
    filter_code = " & ".join(filter_conditions)
    st.code(f"wifi_zones[{filter_code}]", language="r")

# Раздел: Индексация
elif selected_section == "Индексация":
    st.header("⚡ Индексация для ускорения операций")
    
    st.markdown("""
    ### Зачем нужна индексация?
    
    data.table использует **бинарный поиск** для быстрого доступа к данным:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Без индекса:**
        - Линейный поиск O(n)
        - Медленно на больших данных
        - Проверяет каждую строку
        """)
    
    with col2:
        st.markdown("""
        **С индексом:**
        - Бинарный поиск O(log n)
        - Быстро на любых данных
        - Умный поиск по отсортированным данным
        """)
    
    # Демонстрация производительности
    st.subheader("📈 Демонстрация производительности")
    
    sizes = [1000, 10000, 100000, 1000000]
    linear_times = [s * 0.001 for s in sizes]  # Имитация линейного времени
    binary_times = [np.log2(s) * 0.0001 for s in sizes]  # Имитация логарифмического времени
    
    performance_df = pd.DataFrame({
        'Размер данных': sizes,
        'Без индекса (мс)': linear_times,
        'С индексом (мс)': binary_times
    })
    
    fig = px.line(performance_df, x='Размер данных', y=['Без индекса (мс)', 'С индексом (мс)'],
                  title="Сравнение производительности поиска",
                  log_x=True, log_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Создание индексов в data.table:")
    
    st.code("""
# Создание первичного ключа
setkey(wifi_zones, district)

# Поиск по ключу (очень быстро)
wifi_zones["Центральный"]

# Множественные ключи
setkey(wifi_zones, district, location_type)
wifi_zones[.("Центральный", "Библиотека")]

# Вторичные индексы
setindex(wifi_zones, speed_mbps)
wifi_zones[speed_mbps == 100, on = "speed_mbps"]
    """, language="r")

# Раздел: SQL-подобные запросы
elif selected_section == "SQL-подобные запросы":
    st.header("🗄️ SQL-подобные запросы")
    
    st.subheader("Группировка и агрегация")
    
    # Статистика по районам
    district_stats = wifi_zones.groupby('district').agg({
        'id': 'count',
        'speed_mbps': ['mean', 'max'],
        'is_active': 'sum',
        'users_per_day': 'mean'
    }).round(1)
    
    district_stats.columns = ['Количество зон', 'Средняя скорость', 'Макс скорость', 'Активных зон', 'Средн. пользователей/день']
    district_stats = district_stats.sort_values('Количество зон', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(district_stats, use_container_width=True)
    
    with col2:
        fig = px.bar(district_stats.reset_index(), 
                     x='district', y='Количество зон',
                     title="Wi-Fi зоны по районам")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Эквивалентный SQL и data.table код:")
    
    tab1, tab2 = st.tabs(["SQL", "data.table"])
    
    with tab1:
        st.code("""
SELECT district,
       COUNT(*) as count,
       AVG(speed_mbps) as avg_speed,
       MAX(speed_mbps) as max_speed,
       SUM(is_active) as active_count
FROM wifi_zones
GROUP BY district
ORDER BY count DESC;
        """, language="sql")
    
    with tab2:
        st.code("""
wifi_zones[, .(
  count = .N,
  avg_speed = mean(speed_mbps),
  max_speed = max(speed_mbps),
  active_count = sum(is_active)
), by = district][order(-count)]
        """, language="r")
    
    # Сложные запросы
    st.subheader("Сложные агрегации")
    
    complex_stats = wifi_zones.groupby(['district', 'location_type']).agg({
        'id': 'count',
        'speed_mbps': 'mean',
        'users_per_day': 'mean',
        'installation_year': lambda x: (x >= 2020).sum()
    }).round(1)
    
    complex_stats.columns = ['Всего зон', 'Средняя скорость', 'Средн. пользователей', 'Современных зон']
    complex_stats = complex_stats.reset_index()
    complex_stats = complex_stats.sort_values('Всего зон', ascending=False).head(15)
    
    st.dataframe(complex_stats, use_container_width=True)

# Раздел: IF-THEN-ELSE операции
elif selected_section == "IF-THEN-ELSE операции":
    st.header("🔀 IF-THEN-ELSE операции")
    
    st.subheader("Создание категорий")
    
    # Добавляем категории
    wifi_with_categories = wifi_zones.copy()
    
    # Категория скорости
    wifi_with_categories['speed_category'] = pd.cut(
        wifi_with_categories['speed_mbps'], 
        bins=[0, 25, 50, 100], 
        labels=['Низкая', 'Средняя', 'Высокая'],
        include_lowest=True
    )
    
    # Рейтинг зон
    def calculate_rating(row):
        if row['speed_mbps'] >= 50 and row['users_per_day'] >= 200:
            return 'Отличная'
        elif row['speed_mbps'] >= 25 and row['users_per_day'] >= 100:
            return 'Хорошая'
        elif row['speed_mbps'] >= 10 and row['users_per_day'] >= 50:
            return 'Удовлетворительная'
        else:
            return 'Требует улучшения'
    
    wifi_with_categories['zone_rating'] = wifi_with_categories.apply(calculate_rating, axis=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Распределение по категориям скорости:**")
        speed_dist = wifi_with_categories['speed_category'].value_counts()
        fig1 = px.pie(values=speed_dist.values, names=speed_dist.index, 
                      title="Категории скорости Wi-Fi")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.write("**Распределение по рейтингу зон:**")
        rating_dist = wifi_with_categories['zone_rating'].value_counts()
        fig2 = px.bar(x=rating_dist.index, y=rating_dist.values,
                      title="Рейтинг Wi-Fi зон")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Код data.table для условных операций:")
    
    st.code("""
# Простые условия
wifi_zones[, speed_category := ifelse(speed_mbps >= 50, "Высокая", 
                                     ifelse(speed_mbps >= 25, "Средняя", "Низкая"))]

# Сложные условия с fcase
wifi_zones[, zone_rating := fcase(
  speed_mbps >= 50 & users_per_day >= 200, "Отличная",
  speed_mbps >= 25 & users_per_day >= 100, "Хорошая", 
  speed_mbps >= 10 & users_per_day >= 50, "Удовлетворительная",
  default = "Требует улучшения"
)]

# Условные вычисления в группах
wifi_zones[, .(
  excellent_pct = sum(zone_rating == "Отличная") / .N * 100
), by = district]
    """, language="r")
    
    # Показываем результат
    st.subheader("Результат категоризации:")
    st.dataframe(wifi_with_categories[['address', 'district', 'speed_mbps', 'users_per_day', 'speed_category', 'zone_rating']].head(10), use_container_width=True)

# Раздел: Объединение данных
elif selected_section == "Объединение данных":
    st.header("🔗 Объединение данных (Joins)")
    
    # Создаем данные о районах
    district_info = pd.DataFrame({
        'district': wifi_zones['district'].unique(),
        'population': np.random.randint(100000, 500000, len(wifi_zones['district'].unique())),
        'area_km2': np.random.randint(10, 50, len(wifi_zones['district'].unique())),
        'budget_millions': np.random.randint(50, 200, len(wifi_zones['district'].unique()))
    })
    
    st.subheader("Данные о районах:")
    st.dataframe(district_info, use_container_width=True)
    
    # Объединяем данные
    wifi_summary = wifi_zones.groupby('district').agg({
        'id': 'count',
        'speed_mbps': 'mean',
        'users_per_day': 'sum'
    }).round(1)
    wifi_summary.columns = ['wifi_count', 'avg_speed', 'total_users']
    
    # Merge с информацией о районах
    merged_data = wifi_summary.merge(district_info, on='district', how='inner')
    
    # Вычисляем дополнительные метрики
    merged_data['wifi_density'] = (merged_data['wifi_count'] / merged_data['area_km2']).round(2)
    merged_data['users_per_1000_pop'] = (merged_data['total_users'] / merged_data['population'] * 1000).round(1)
    
    st.subheader("Результат объединения с дополнительными метриками:")
    st.dataframe(merged_data, use_container_width=True)
    
    # Визуализация
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.scatter(merged_data, x='population', y='wifi_count',
                         size='budget_millions', hover_name='district',
                         title="Зависимость количества Wi-Fi от населения")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(merged_data, x='district', y='wifi_density',
                     title="Плотность Wi-Fi зон по районам")
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Код data.table для объединения:")
    
    st.code("""
# Создаем агрегированные данные
wifi_summary <- wifi_zones[, .(
  wifi_count = .N,
  avg_speed = mean(speed_mbps),
  total_users = sum(users_per_day)
), by = district]

# Inner join
merged_data <- wifi_summary[district_info, on = "district"]

# Добавляем вычисляемые столбцы
merged_data[, wifi_density := wifi_count / area_km2]
merged_data[, users_per_1000_pop := total_users / population * 1000]
    """, language="r")

# Раздел: Производительность
elif selected_section == "Производительность":
    st.header("🚀 Производительность data.table")
    
    st.markdown("""
    ### Почему data.table быстрый?
    
    1. **Модификация по ссылке** - оператор `:=` изменяет данные без копирования
    2. **Умная индексация** - автоматическое создание и использование индексов
    3. **Оптимизированный C код** - критические операции написаны на C
    4. **Параллельные вычисления** - автоматическое использование нескольких ядер
    """)
    
    # Сравнение производительности
    st.subheader("📊 Сравнение с другими пакетами")
    
    # Имитация бенчмарков
    benchmark_data = pd.DataFrame({
        'Операция': ['Группировка', 'Фильтрация', 'Объединение', 'Сортировка'],
        'base R (сек)': [2.5, 1.8, 4.2, 3.1],
        'dplyr (сек)': [1.2, 0.9, 2.1, 1.5],
        'data.table (сек)': [0.3, 0.2, 0.5, 0.4]
    })
    
    fig = px.bar(benchmark_data, x='Операция', 
                 y=['base R (сек)', 'dplyr (сек)', 'data.table (сек)'],
                 title="Сравнение производительности (1M строк)",
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Масштабируемость
    st.subheader("📈 Масштабируемость")
    
    sizes = [1000, 10000, 100000, 1000000, 10000000]
    base_r_times = [s * 0.000001 for s in sizes]
    data_table_times = [s * 0.0000002 for s in sizes]
    
    scaling_df = pd.DataFrame({
        'Размер данных': sizes,
        'base R': base_r_times,
        'data.table': data_table_times
    })
    
    fig2 = px.line(scaling_df, x='Размер данных', y=['base R', 'data.table'],
                   title="Масштабируемость (время выполнения)",
                   log_x=True, log_y=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("💡 Советы по оптимизации:")
    
    tips = [
        "Используйте `setkey()` для часто фильтруемых столбцов",
        "Применяйте `:=` для модификации данных без копирования", 
        "Используйте `.SD` для операций над подмножествами столбцов",
        "Комбинируйте операции в одном вызове `DT[...]`",
        "Используйте `fread()` и `fwrite()` для быстрого I/O"
    ]
    
    for i, tip in enumerate(tips, 1):
        st.write(f"{i}. {tip}")

# Раздел: Заключение
elif selected_section == "Заключение":
    st.header("🎯 Заключение")
    
    st.subheader("Основные преимущества data.table:")
    
    advantages = [
        ("🚀", "Высокая производительность", "Особенно на больших данных"),
        ("📝", "Лаконичный синтаксис", "DT[i, j, by] покрывает большинство операций"),
        ("💾", "Эффективная память", "Модификация по ссылке с оператором :="),
        ("🗄️", "SQL-подобные операции", "Привычный синтаксис для работы с данными"),
        ("⚡", "Мощная индексация", "Автоматическая оптимизация запросов"),
        ("🔧", "Богатые возможности", "От простой фильтрации до сложных аналитических операций")
    ]
    
    for emoji, title, description in advantages:
        st.write(f"{emoji} **{title}** - {description}")
    
    st.subheader("📈 Статистика нашего анализа:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Всего Wi-Fi зон", len(wifi_zones))
    
    with col2:
        active_zones = wifi_zones['is_active'].sum()
        st.metric("Активных зон", active_zones, f"{active_zones/len(wifi_zones)*100:.1f}%")
    
    with col3:
        avg_speed = wifi_zones['speed_mbps'].mean()
        st.metric("Средняя скорость", f"{avg_speed:.1f} Мбит/с")
    
    with col4:
        total_users = wifi_zones['users_per_day'].sum()
        st.metric("Всего пользователей/день", f"{total_users:,}")
    
    st.subheader("🔗 Полезные ресурсы:")
    
    resources = [
        "[Официальная документация data.table](https://rdatatable.gitlab.io/data.table/)",
        "[Шпаргалка по data.table](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/datatable_Cheat_Sheet_R.pdf)",
        "[Advanced R - data.table](http://adv-r.had.co.nz/Performance.html#data-table)",
        "[Введение в data.table](https://www.listendata.com/2016/10/r-data-table.html)"
    ]
    
    for resource in resources:
        st.markdown(f"- {resource}")
    
    st.success("✅ Презентация завершена! data.table - мощный инструмент для эффективной работы с данными в R.")

# Футер
st.markdown("---")
st.markdown("*Презентация создана с использованием Streamlit и демонстрирует концепции пакета data.table*")