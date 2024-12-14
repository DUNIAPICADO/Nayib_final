import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Page configuration with improved styling
st.set_page_config(
    page_title="Northwind Analysis", 
    page_icon=":bar_chart:", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 20px;
    }
    .filter-container {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stMetric {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Function to execute queries safely
def execute_query(query, params=None):
    """
    Execute a SQL query safely, creating a new connection for each query
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
    
    Returns:
        pandas.DataFrame: Result of the query
    """
    try:
        # Create a new connection for each query
        conn = sqlite3.connect("data/Northwind_small.sqlite")
        
        # Execute query with optional parameters
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    finally:
        # Ensure connection is closed
        if 'conn' in locals():
            conn.close()

# Function to load sales by country data
def load_sales_by_country():
    """Load sales data grouped by country"""
    query = """
    SELECT cu.Country, 
           ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalSales,
           COUNT(DISTINCT o.Id) AS TotalOrders
    FROM [Order] o
    JOIN Customer cu ON o.CustomerId = cu.Id
    JOIN OrderDetail od ON o.Id = od.OrderId
    GROUP BY cu.Country
    ORDER BY TotalSales DESC
    """
    return execute_query(query)

# Function to load profit by category
def load_profit_by_category():
    """Load profit data grouped by product category"""
    query = """
    SELECT c.CategoryName, 
           ROUND(SUM(od.UnitPrice * od.Quantity) - 
           SUM(od.UnitPrice * od.Quantity * od.Discount), 2) AS Profit
    FROM OrderDetail od
    JOIN Product p ON od.ProductId = p.Id
    JOIN Category c ON p.CategoryId = c.Id
    GROUP BY c.CategoryName
    ORDER BY Profit DESC
    """
    return execute_query(query)

# Function to load top-selling products
def load_top_selling_products():
    """Load top-selling products by quantity"""
    query = """
    SELECT p.ProductName, 
           SUM(od.Quantity) AS TotalSold,
           ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalRevenue
    FROM OrderDetail od
    JOIN Product p ON od.ProductId = p.Id
    GROUP BY p.ProductName
    ORDER BY TotalSold DESC
    LIMIT 10
    """
    return execute_query(query)

# Main Streamlit app
def main():
    # Title with custom styling
    st.markdown('<h1 class="main-header">🚀 Northwind Sales Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Load data
    sales_by_country = load_sales_by_country()
    profit_by_category = load_profit_by_category()
    top_selling_products = load_top_selling_products()

    # Filters Container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    # Create filter columns
    filter_col1, filter_col2 = st.columns(2)

    # Country Filter
    with filter_col1:
        selected_countries = st.multiselect(
            "🌍 Select Countries", 
            options=sales_by_country['Country'].dropna().unique(),
            default=sales_by_country['Country'].dropna().unique()[:5],
            key='country_filter'
        )

    # Category Filter
    with filter_col2:
        selected_categories = st.multiselect(
            "📦 Select Product Categories", 
            options=profit_by_category['CategoryName'].unique(),
            default=profit_by_category['CategoryName'].unique(),
            key='category_filter'
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Filtering data based on selections
    filtered_country_sales = sales_by_country[sales_by_country['Country'].isin(selected_countries)]
    filtered_category_profit = profit_by_category[profit_by_category['CategoryName'].isin(selected_categories)]

    # Create visualizations
    col1, col2 = st.columns(2)

    # Sales by Country - Interactive Plotly Bar Chart
    with col1:
        st.subheader("🌍 Sales by Country")
        if not filtered_country_sales.empty:
            fig_country_sales = px.bar(
                filtered_country_sales, 
                x='Country', 
                y='TotalSales', 
                title='Sales Distribution by Country',
                labels={'TotalSales': 'Total Sales', 'Country': 'Country'},
                color='TotalSales',
                color_continuous_scale='viridis'
            )
            fig_country_sales.update_layout(height=400)
            st.plotly_chart(fig_country_sales, use_container_width=True)
        else:
            st.warning("No data available for selected countries")

    # Profit by Category - Interactive Plotly Pie Chart
    with col2:
        st.subheader("📦 Profit by Category")
        if not filtered_category_profit.empty:
            fig_category_profit = px.pie(
                filtered_category_profit, 
                values='Profit', 
                names='CategoryName',
                title='Profit Distribution by Product Category',
                hole=0.3
            )
            fig_category_profit.update_layout(height=400)
            st.plotly_chart(fig_category_profit, use_container_width=True)
        else:
            st.warning("No data available for selected categories")

    # Top Selling Products
    st.subheader("🏆 Top 10 Selling Products")
    st.dataframe(
        top_selling_products.style.background_gradient(cmap='Blues'), 
        use_container_width=True
    )

    # Quick Insights
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.metric("🌐 Total Countries", len(sales_by_country))
    
    with insights_col2:
        st.metric("📁 Total Product Categories", len(profit_by_category))

# Run the app
if __name__ == "__main__":
    main()