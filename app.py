import streamlit as st
from fpdf import FPDF
from datetime import date
import io

st.title("Gerador de PIE - NR-10")

# Campos de entrada
empresa = st.text_input("Nome da Empresa")
inspetor = st.text_input("Engenheiro Responsável (CREA)")

# Checklist de auditoria
st.subheader("Checklist de Conformidade")
unifilar = st.checkbox("Esquemas Unifilares Atualizados?")
epi = st.checkbox("EPIs com CA válidos?")
aterramento = st.checkbox("Sistema de Aterramento Conforme?")
sinalizacao = st.checkbox("Sinalização de Segurança Presente?")
treinamento = st.checkbox("Treinamento NR-10 da Equipe em Dia?")

observacoes = st.text_area("Observações do Auditor")


def gerar_pdf(empresa, inspetor, itens, observacoes):
    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Prontuário de Instalações Elétricas (PIE)", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Referência: NR-10", ln=True, align="C")
    pdf.ln(6)

    # Dados gerais
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Dados Gerais", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Empresa: {empresa or '-'}", ln=True)
    pdf.cell(0, 7, f"Engenheiro Responsável (CREA): {inspetor or '-'}", ln=True)
    pdf.cell(0, 7, f"Data de emissão: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(6)

    # Checklist
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Checklist de Conformidade", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for descricao, ok in itens:
        marca = "[X]" if ok else "[ ]"
        pdf.cell(0, 7, f"{marca} {descricao}", ln=True)
    pdf.ln(6)

    # Observações
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Observações", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, observacoes or "Nenhuma observação registrada.")
    pdf.ln(10)

    # Assinatura
    pdf.cell(0, 7, "_______________________________________", ln=True)
    pdf.cell(0, 7, f"{inspetor or 'Engenheiro Responsável'} - CREA", ln=True)

    return bytes(pdf.output())


if st.button("Gerar Relatório Final"):
    if not empresa or not inspetor:
        st.error("Preencha o nome da empresa e o engenheiro responsável antes de gerar o relatório.")
    else:
        itens = [
            ("Esquemas Unifilares Atualizados?", unifilar),
            ("EPIs com CA válidos?", epi),
            ("Sistema de Aterramento Conforme?", aterramento),
            ("Sinalização de Segurança Presente?", sinalizacao),
            ("Treinamento NR-10 da Equipe em Dia?", treinamento),
        ]

        pdf_bytes = gerar_pdf(empresa, inspetor, itens, observacoes)

        st.success(f"Relatório de {empresa} gerado para auditoria!")

        st.download_button(
            label="📄 Baixar PIE em PDF",
            data=pdf_bytes,
            file_name=f"PIE_NR10_{empresa.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )
