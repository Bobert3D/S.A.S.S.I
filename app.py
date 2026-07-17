import streamlit as st
from sassi_engine import scan_code


def main():
    st.set_page_config(page_title="S.A.S.S.I Gatekeeper", page_icon="🤖", layout="centered")

    st.title("S.A.S.S.I Gatekeeper")
    st.write("Submit Python code and let S.A.S.S.I scan it for syntax issues and banned operations.")

    code_input = st.text_area("Python code to scan", height=300)

    if st.button("Scan code"):
        if not code_input.strip():
            st.warning("Please enter some code before scanning.")
        else:
            result = scan_code(code_input)
            if result["ok"]:
                st.success(result["summary"])
                with st.expander("View syntax tree scan details"):
                    for line in result["details"]:
                        st.code(line, language=None)
            elif result["status"] == "rejected":
                st.error(result["summary"])
                st.write("Details:")
                for line in result["details"]:
                    st.write(line)
            else:
                st.error(result["summary"])
                st.write("Details:")
                for line in result["details"]:
                    st.write(line)


if __name__ == "__main__":
    main()
