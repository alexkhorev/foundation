import streamlit as st
from openpyxl import load_workbook

from core.extractor.extractor import extract_data_from_sheet
from core.calculate import MainCalculation


def main():
    st.title(
        'Calculation of a capped pile'
    )
    st.header(
        'Input data'
    )

    with open(r'templates\template.xlsx', 'rb') as file:
        st.sidebar.download_button(':material/download: Download Template',
                                   file, file_name='template.xlsx',
                                   use_container_width=True)
    file = st.sidebar.file_uploader('Upload', type=['xls', 'xlsx'], label_visibility='collapsed')
    with open('templates/img.png', 'rb') as image_file:
        st.image(image_file.read())
    if file:
        st.toast('File successfully uploaded', icon='🔥')

        workbook = load_workbook(file, data_only=True)
        pile_data = extract_data_from_sheet(workbook['PileData'], 'PileData')
        load_data = extract_data_from_sheet(workbook['LoadData'], 'LoadData')
        foundation_data = extract_data_from_sheet(workbook['FoundationData'], 'FoundationData')

        result = MainCalculation().calculate(pile_data, load_data, foundation_data)

        if result.get('is_passed'):
            st.success('Calculation successful')

            st.markdown(
                '### Result'
            )

            st.markdown('The condition is true:')
            st.latex(
                fr'M_y \le \frac{{\gamma_cM_u}}{{\gamma_n}} \Rightarrow {result['calculation_variables']['first_state_load'][0]:.2f} < {result['calculation_variables']['sum_moment_with_coefficient']:.2f}')

            st.markdown('All calculations are listed below.')

            st.markdown(
                f'The ultimate overturning moment by bearing capacity of the ground $M_u$ is found from the equilibrium equation $\Sigma M=0$. For this purpose we find the moments included in the general equation of equilibrium:'
            )
            st.markdown(
                '1. Ultimate moment on bearing capacity of the ground $M_u$ from the equation of equilibrium'
            )
            st.latex(
                fr'M_u = M^г_{{к}} + M^г_{{св.в.}} + M^г_{{св.н.}} + M^в_{{к.у.}} + M^в_{{ос.}} + M^{{тр}}_{{к.у.}} = {result['calculation_variables']['sum_moment']:.2f}\:кНм')

            st.markdown(
                '2. Reactive moment of lateral rebound along the height of the widening slab'
            )
            st.latex(
                fr'М^г_{{к}} = \sigma_{{кр}}Db(L - \frac{{b}}{{2}}) = {result['calculation_variables']['side_cap_moment']:.2f}\:кНм')

            st.markdown(
                '3. Reactive moment of lateral rebound of the strut above the point "0" of conditional rotation of the strut in the ground at the depth $Z_0$. If the point "0" is located at the level of the bottom of the widening slab or higher, the reactive moment of the lateral support of the post above the point "0" is assumed to be equal to zero.'
            )

            st.latex(
                fr'M^г_{{ст.в.}} = \sigma_{{кр}}d(Z_0 - b)(L - \frac{{b}}{{2}} - \frac{{Z_0}}{{2}}) = {result['calculation_variables']['top_side_moment']:.2f}\:кНм')
            st.latex(
                fr'A = \left[b(L-\frac{{b^2}}{{2}})(\alpha-1)+\frac{{\pi d^2}}{{12}}(1+\frac{{1}}{{4}}(\alpha^2-1)(2\alpha-1)) + \beta \frac{{\pi d}}{{4}}(\alpha^2 - 1)(L-b)\right] = {result['calculation_variables']['coefficients'][0]:.2f}\:м^2')
            st.latex(fr'\alpha = D/d = {result['calculation_variables']['alpha']:.1f}')
            st.latex(fr'\beta = \frac{{f_{{тр}}}}{{\sigma_{{кр}}}} = {result['calculation_variables']['betta']:.2f}')
            st.latex(
                fr'B = \left[b(\alpha - 1) + \beta \frac{{\pi d}}{{4}}\alpha^2\right] = {result['calculation_variables']['coefficients'][1]:.2f}\:м^2')
            st.latex(fr'Z_0 = \sqrt{{H^2 + 0.5C}} - H = {result['calculation_variables']['pivot_depth']:.2f}\:м')
            st.latex(
                fr'C = \left[L^2 + 2H(L-B) - 2LB + 2A\right] = {result['calculation_variables']['coefficients'][2]:.2f}\:м^2')

            st.markdown(
                '4. Reactive moment of lateral rebound of the strut below the point "0" of conditional rotation of the strut in the ground at the depth $Z_0$.'
            )
            st.latex(
                fr'M^г_{{св.н.}} = -\sigma_{{кр}}d \frac{{(L-Z_0)^2}}{{2}} = {result['calculation_variables']['bottom_side_moment']:.2f}\:кНм')

            st.markdown(
                '5. Reactive moment of the vertical pushback acting over the area of the widening plate'
            )
            st.latex(
                fr'M^в_{{к.у.}} = (D^2 - \frac{{\pi d^2}}{{4}})\sigma_{{кр}} \frac{{2\alpha - 1}}{{6}}= {result['calculation_variables']['vert_cap_moment']:.2f}\:кНм'
            )

            st.markdown(
                '6.	Reactive moment of the vertical backstop acting on the base area of the pile'
            )
            st.latex(
                fr'M^в_{{ос.}} = \frac{{\pi d^3}}{{12}}\sigma_{{кр}} = {result['calculation_variables']['vert_pile_moment']:.2f}\:кНм'
            )

            st.markdown(
                '7.	Reactive moment of friction forces arising at the contact of the base of the widening plate with the soil'
            )
            st.latex(
                fr'M^{{тр}}_{{к.у.}} = (D^2 - \frac{{\pi d^2}}{{4}})f_{{тр}}(L-b) = {result['calculation_variables']['contact_moment']:.2f}\:кНм'
            )


        else:
            st.error('Calculation failed')

            st.markdown('The condition is false:')
            st.latex(
                fr'M_y \le \frac{{\gamma_cM_u}}{{\gamma_n}} \Rightarrow {result['calculation_variables']['first_state_load'][0]:.2f} > {result['calculation_variables']['sum_moment_with_coefficient']:.2f}')



if __name__=="__main__":
    main()
