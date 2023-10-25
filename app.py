import academic
import patent
import analyse
import visualise
import streamlit as st

def main():
    st.title("Emerging Technologies Trend Explorer")

    data_source = st.radio("Choose a data source:", ("Academic", "Patent"))

    if data_source == "Academic":
        st.subheader("Academic Data")
        keywords = st.text_input("Enter keywords to search for:")
        max_results = st.number_input("Max number of publications to include:", min_value=1, value=100)

        if st.button("Fetch Academic Data"):
            academic_data = academic.get_academic_data(keywords, max_results)
            st.session_state.academic_data = academic_data  # Store in session_state

        if 'academic_data' in st.session_state:
            academic_data = st.session_state.academic_data

            analyzed_data = analyse.predict_class(academic_data)
            st.subheader("Analyzed Academic Data")
            st.dataframe(analyzed_data)

            st.subheader("Visualizations")
            figure_selected = st.radio('Select a chart to display', ['Bar Chart', 'Time Series', 'Pie Chart'])
            if figure_selected == 'Bar Chart':
                fig = visualise.bar_chart(analyzed_data)
                st.plotly_chart(fig, use_container_width=True)
            elif figure_selected == 'Time Series':
                fig = visualise.time_series(analyzed_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.subheader("Select Year for Pie Chart")
                unique_years = analyzed_data['publish_date'].dt.year.unique()
                sorted_years = sorted(unique_years, reverse=True)
                selected_year = st.selectbox("Choose a year:", sorted_years)
                if selected_year:
                    fig = visualise.pie_chart(analyzed_data, selected_year)
                    st.plotly_chart(fig, use_container_width=True)

    elif data_source == "Patent":
        st.subheader("Patent Data")
        available_categories = patent.get_available_categories()

        with st.expander("Available Categories:"):
            selection = []
            for index, category_name in enumerate(available_categories):
                checkbox = st.checkbox(f"{index+1}.{category_name[-1]}", key=index)
                if checkbox:
                    selection.append(index+1)
            css='''
                <style>
                    [data-testid="stExpander"] div:has(>.streamlit-expanderContent) {
                        overflow: scroll;
                        height: 400px;
                    }
                </style>
                '''
            st.markdown(css, unsafe_allow_html=True)
        selected_categories = ','.join(str(x) for x in selection)
        selected_names = [(index, category_name) for index, category_name in available_categories if index in selection]
        selected_names_str = '\n'.join(f"{index + 1}.{category_name}" for index, category_name in selected_names)
        st.text('Selected Categories: ')
        st.text(selected_names_str)

        start_date = st.date_input("Start Date", None)
        end_date = st.date_input("End Date", None)

        if st.button("Fetch Patent Data"):
            patent_data = patent.get_patent_data(start_date, end_date, selected_categories)
            st.session_state.patent_data = patent_data

        if 'patent_data' in st.session_state and not st.session_state.patent_data.empty:
            patent_data = st.session_state.patent_data

            analyzed_data = analyse.predict_class(patent_data)
            st.subheader("Analyzed Patent Data")
            st.dataframe(analyzed_data)

            st.subheader("Visualizations")
            figure_selected = st.radio('Select a chart to display', ['Bar Chart', 'Time Series', 'Pie Chart'])
            if figure_selected == 'Bar Chart':
                fig = visualise.bar_chart(analyzed_data)
                st.plotly_chart(fig, use_container_width=True)
            elif figure_selected == 'Time Series':
                fig = visualise.time_series(analyzed_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.subheader("Select Year for Pie Chart")

                unique_years = analyzed_data['publish_date'].dt.year.unique()

                sorted_years = sorted(unique_years, reverse=True)
                selected_year = st.selectbox("Choose a year:", sorted_years)
                if selected_year:
                    fig = visualise.pie_chart(analyzed_data, selected_year)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Chosen category/time range has no patent records.")

if __name__ == '__main__':
    main()
