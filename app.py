import streamlit as st
import numpy as np
import pandas as pd

RI_DICT = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
    11: 1.51, 12: 1.54, 13: 1.56, 14: 1.57, 15: 1.59
}

def calculate_ahp_weights(matrix):
    matrix = np.array(matrix)
    n = matrix.shape[0]
    if n == 1:
        return np.array([1.0]), 1.0, 0.0, 0.0, True
    if np.any(matrix <= 0):
        st.warning(f"矩阵中包含0或负值，请检查输入。将使用1.0代替无效值进行计算。")
        matrix[matrix <= 0] = 1.0
    try:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
    except np.linalg.LinAlgError:
        st.error("计算特征值失败。请检查矩阵数据是否有效（例如，避免所有行/列都为0）。")
        return None, 0, 0, 0, False
    lambda_max = np.max(eigenvalues.real)
    max_eig_index = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, max_eig_index].real
    weights = np.abs(weights)
    weights = weights / np.sum(weights)
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_DICT.get(n, 1.59)
    if ri == 0.00:
        cr = 0.00 if ci == 0.00 else np.inf
    else:
        cr = ci / ri
    is_consistent = (cr < 0.1)
    return weights, lambda_max, ci, cr, is_consistent

def sync_reciprocal(matrix_key, editor_key, index_list, col_list):
    try:
        df_editor_state = st.session_state.get(editor_key, {})
        edited_rows = df_editor_state.get("edited_rows", {})
        df = st.session_state.matrices[matrix_key].copy()
        needs_update = False
        for row_index, changes in edited_rows.items():
            for col_name, new_val in changes.items():
                try:
                    new_val_float = float(new_val)
                    if new_val_float <= 0:
                        continue
                    i = row_index
                    j = col_list.index(col_name)
                    if i == j:
                        if df.iloc[i, j] != 1.0:
                            df.iloc[i, j] = 1.0
                            needs_update = True
                    else:
                        reciprocal_val = 1.0 / new_val_float
                        if not np.isclose(df.iloc[i, j], new_val_float):
                            df.iloc[i, j] = new_val_float
                            needs_update = True
                        if not np.isclose(df.iloc[j, i], reciprocal_val):
                            df.iloc[j, i] = reciprocal_val
                            needs_update = True
                except (ValueError, TypeError, ZeroDivisionError):
                    continue
        if needs_update:
            st.session_state.matrices[matrix_key] = df
    except Exception as e:
        print(f"Error in sync_reciprocal for {matrix_key} (editor key {editor_key}): {e}")

st.set_page_config(layout="wide", page_title="AHP 决策支持工具")
st.title("🎓 《系统工程概论》AHP 决策支持工具 (v2)")
st.write("用于本科毕业去向评价，包含实时敏感性分析和自动倒数功能。")
st.sidebar.header("1. 定义问题")
criteria_input = st.sidebar.text_area(
    "输入准则 (每行一个)",
    "未来发展潜力\n经济收入\n个人兴趣符合度\n工作生活平衡\n稳定性"
)
criteria_list = [c.strip() for c in criteria_input.split('\n') if c.strip()]
n_criteria = len(criteria_list)
alts_input = st.sidebar.text_area(
    "输入方案 (每行一个)",
    "国内读研\n出国留学\n考公务员\n进入国企\n进入私企"
)
alts_list = [a.strip() for a in alts_input.split('\n') if a.strip()]
n_alts = len(alts_list)
if 'matrices' not in st.session_state:
    st.session_state.matrices = {}
st.header("2. 构造判断矩阵")
st.info("请使用 1-9 标度法 (例如: 3, 5, 0.33, 0.2) 填表。 **(新功能)**: 您只需编辑一个值，它的倒数将自动更新。")
tab_list = ["准则层 (C)"] + [f"方案层 (A | {c})" for c in criteria_list]
tabs = st.tabs(tab_list)
with tabs[0]:
    st.subheader(f"准则层矩阵 ( {n_criteria} x {n_criteria} )")
    st.write("比较各【准则】对于【总目标】的重要性：")
    matrix_key_c = 'C'
    if matrix_key_c not in st.session_state.matrices:
        df_c = pd.DataFrame(np.ones((n_criteria, n_criteria)),
                            index=criteria_list,
                            columns=criteria_list)
        st.session_state.matrices[matrix_key_c] = df_c
    df_c = st.session_state.matrices[matrix_key_c]
    editor_key_c = "editor_C"
    edited_df_c = st.data_editor(
        df_c,
        key=editor_key_c,
        on_change=sync_reciprocal,
        args=(matrix_key_c, editor_key_c, criteria_list, criteria_list)
    )
for i, criterion in enumerate(criteria_list):
    with tabs[i + 1]:
        st.subheader(f"方案层矩阵: {criterion} ( {n_alts} x {n_alts} )")
        st.write(f"在【{criterion}】准则下，比较各【方案】的优劣：")
        matrix_key_a = f"A_{i}"
        editor_key_a = f"editor_A_{i}"
        if matrix_key_a not in st.session_state.matrices:
            df_a = pd.DataFrame(np.ones((n_alts, n_alts)),
                                index=alts_list,
                                columns=alts_list)
            st.session_state.matrices[matrix_key_a] = df_a
        df_a = st.session_state.matrices[matrix_key_a]
        edited_df_a = st.data_editor(
            df_a,
            key=editor_key_a,
            on_change=sync_reciprocal,
            args=(matrix_key_a, editor_key_a, alts_list, alts_list)
        )
st.header("3. 计算结果与一致性检验")
criteria_weights = None
all_alt_weights = []
all_consistent = True
if st.button("🚀 开始计算"):
    results_container = st.container()
    results_container.subheader("准则层 (C) 计算结果")
    try:
        matrix_c = st.session_state.matrices['C'].values.astype(float)
        c_weights, c_lambda, c_ci, c_cr, c_consistent = calculate_ahp_weights(matrix_c)
        if c_weights is not None:
            results_container.write(f"最大特征值 $\lambda_{{max}}$: {c_lambda:.4f}")
            results_container.write(f"CI: {c_ci:.4f}")
            results_container.write(f"CR: {c_cr:.4f}")
            if c_consistent:
                results_container.success("准则层矩阵通过一致性检验 (CR < 0.1)")
                criteria_weights = c_weights
            else:
                results_container.error("警告: 准则层矩阵未通过一致性检验 (CR >= 0.1)，请重新调整！")
                all_consistent = False
            df_c_weights = pd.DataFrame(c_weights, index=criteria_list, columns=["权重"])
            results_container.dataframe(df_c_weights.style.format("{:.3%}"))
        else:
            all_consistent = False
        results_container.subheader("方案层 (A) 计算结果")
        alt_weights_matrix = []
        for i, criterion in enumerate(criteria_list):
            matrix_key = f"A_{i}"
            matrix_a = st.session_state.matrices[matrix_key].values.astype(float)
            a_weights, a_lambda, a_ci, a_cr, a_consistent = calculate_ahp_weights(matrix_a)
            if a_weights is not None:
                alt_weights_matrix.append(a_weights)
                with results_container.expander(f"查看 {criterion} 准则的计算详情"):
                    st.write(f"最大特征值 $\lambda_{{max}}$: {a_lambda:.4f}")
                    st.write(f"CI: {a_ci:.4f}")
                    st.write(f"CR: {a_cr:.4f}")
                    if a_consistent:
                        st.success(f"矩阵 (A | {criterion}) 通过一致性检验 (CR < 0.1)")
                    else:
                        st.error(f"警告: 矩阵 (A | {criterion}) 未通过一致性检验 (CR >= 0.1)！")
                        all_consistent = False
            else:
                all_consistent = False
        st.header("4. 总排序结果")
        if criteria_weights is not None and len(alt_weights_matrix) == n_criteria:
            A_matrix = np.array(alt_weights_matrix).T
            C_vector = criteria_weights.reshape(-1, 1)
            final_scores = A_matrix @ C_vector
            final_scores = final_scores.flatten()
            df_final = pd.DataFrame({
                "方案": alts_list,
                "最终得分": final_scores
            }).sort_values(by="最终得分", ascending=False)
            st.dataframe(df_final.style.format({"最终得分": "{:.4f}"}))
            st.bar_chart(df_final.set_index("方案"))
            st.session_state['final_results'] = {
                'A_matrix': A_matrix,
                'C_weights_original': C_vector,
                'alts_list': alts_list,
                'criteria_list': criteria_list
            }
        elif not all_consistent:
            st.warning("由于一个或多个矩阵未通过一致性检验或计算出错，总排序未执行。")
        else:
            st.warning("计算未完成，无法显示总排序。")
    except Exception as e:
        st.error(f"计算出错: {e}")
        st.exception(e)
st.header("5. ⚡ 实时敏感性分析")
st.write("拖动下面的滑块，实时调整【准则层】的权重，观察最终排序的变化。")
if 'final_results' in st.session_state:
    results = st.session_state['final_results']
    A_matrix = results['A_matrix']
    C_weights_original = results['C_weights_original'].flatten()
    alts_list = results['alts_list']
    criteria_list_from_results = results.get('criteria_list', criteria_list)
    if len(criteria_list_from_results) != len(C_weights_original):
        st.warning("准则列表与权重不匹配，敏感性分析可能不准确。请重新定义准则并计算。")
    else:
        new_weights = []
        st.write("调整准则权重 (注意：总和将自动归一化):")
        cols = st.columns(len(criteria_list_from_results))
        for i, criterion in enumerate(criteria_list_from_results):
            with cols[i]:
                default_val = float(C_weights_original[i])
                weight = st.slider(criterion, 0.0, 1.0, default_val, 0.01, key=f"slider_{i}")
                new_weights.append(weight)
        new_weights_array = np.array(new_weights)
        sum_weights = np.sum(new_weights_array)
        if sum_weights > 0:
            new_weights_normalized = new_weights_array / sum_weights
        else:
            new_weights_normalized = np.zeros_like(new_weights_array)
        new_final_scores = A_matrix @ new_weights_normalized.reshape(-1, 1)
        new_final_scores = new_final_scores.flatten()
        df_new_final = pd.DataFrame({
            "方案": alts_list,
            "调整后得分": new_final_scores
        }).sort_values(by="调整后得分", ascending=False)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**调整后的排序**")
            st.dataframe(df_new_final.style.format({"调整后得分": "{:.4f}"}))
        with col2:
            st.write("**归一化权重**")
            df_new_weights = pd.DataFrame({
                "准则": criteria_list_from_results,
                "新权重": new_weights_normalized
            })
            st.bar_chart(df_new_weights.set_index("准则"))
        st.write("---")
        st.subheader("实时排序变化图")
        st.bar_chart(df_new_final.set_index("方案"))
else:
    st.info("请先点击上方的「🚀 开始计算」按钮，以生成总排序结果，然后再进行敏感性分析。")