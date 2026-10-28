import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

# ==================== DARK THEME CANVAS ====================

def draw_dark_background(canvas_obj, doc_obj):
    """Fundo escuro absoluto (#07090e) desenhado na base de cada página."""
    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor("#07090e"))
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas_obj.restoreState()


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Primeira página é a capa completa; sem cabeçalhos ou rodapés
            return

        self.saveState()

        # Linha divisória superior (Header)
        self.setStrokeColor(colors.HexColor("#1e293b"))
        self.setLineWidth(0.75)
        self.line(1.5 * cm, A4[1] - 1.35 * cm, A4[0] - 1.5 * cm, A4[1] - 1.35 * cm)

        # Cabeçalho - Título em Esmeralda Neon
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#10b981"))
        self.drawString(1.5 * cm, A4[1] - 1.15 * cm, "MILLIONAIRE AFFILIATE TRADERS")

        # Cabeçalho - Autor em Dourado
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#fbbf24"))
        self.drawRightString(A4[0] - 1.5 * cm, A4[1] - 1.15 * cm, "FP TRADER — Felipe Vieira")

        # Linha divisória inferior (Footer)
        self.line(1.5 * cm, 1.4 * cm, A4[0] - 1.5 * cm, 1.4 * cm)

        # Rodapé - Texto descritivo
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(1.5 * cm, 0.95 * cm, "Material educativo gratuito • Trading & Afiliados")

        # Rodapé - Número da página
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawRightString(A4[0] - 1.5 * cm, 0.95 * cm, page_text)

        self.restoreState()


def build_pdf():
    pdf_filename = r"c:\Users\felip\Downloads\Meus Ebooks\Millionaire Affiliate Traders\Millionaire_Affiliate_Traders_FP_Trader.pdf"
    cover_image_path = r"c:\Users\felip\Downloads\Meus Ebooks\Millionaire Affiliate Traders\capa_ebook.png"

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()

    # ==================== PALETA DE CORES TEMA ESCURO ====================
    bg_surface = colors.HexColor("#0d1527")      # Fundo de cards/tabelas (Navy/Slate profundo)
    bg_elevated = colors.HexColor("#111c33")     # Linhas alternadas de tabelas
    border_slate = colors.HexColor("#1e293b")    # Bordas e grids elegantes
    
    accent_emerald = colors.HexColor("#00e676")  # Verde Neon vibrante
    accent_green = colors.HexColor("#10b981")    # Esmeralda moderna
    accent_gold = colors.HexColor("#fbbf24")     # Dourado âmbar luxuoso
    accent_cyan = colors.HexColor("#38bdf8")     # Ciano brilhante para links e destaques
    
    text_white = colors.HexColor("#ffffff")      # Branco puro para títulos
    text_body = colors.HexColor("#e2e8f0")       # Slate 200 de alto contraste e leitura suave
    text_bullets = colors.HexColor("#cbd5e1")    # Slate 300 para listas
    text_muted = colors.HexColor("#94a3b8")      # Slate 400
    
    # Cores de caixas de destaque
    dica_bg = colors.HexColor("#062419")         # Fundo verde floresta escuro
    dica_border = colors.HexColor("#059669")     # Borda esmeralda
    dica_text = colors.HexColor("#d1fae5")       # Texto menta claro
    
    alerta_bg = colors.HexColor("#260b0b")       # Fundo vermelho vinho escuro
    alerta_border = colors.HexColor("#dc2626")   # Borda vermelha
    alerta_text = colors.HexColor("#fca5a5")     # Texto coral suave
    
    table_header_bg = colors.HexColor("#064e3b") # Fundo de cabeçalho de tabela

    # ==================== ESTILOS TIPOGRÁFICOS ====================
    title_style = ParagraphStyle(
        'DocTitleDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=text_white,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitleDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=accent_gold,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'ChapterH1Dark',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=text_white,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2Dark',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15.5,
        textColor=accent_green,
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=text_body,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=text_bullets,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3.5
    )

    link_style = ParagraphStyle(
        'LinkTextDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12.5,
        textColor=accent_cyan
    )

    table_header_style = ParagraphStyle(
        'TableHeaderDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=text_white
    )

    table_cell_style = ParagraphStyle(
        'TableCellDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=text_body
    )

    table_gold_style = ParagraphStyle(
        'TableGoldDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12.5,
        textColor=accent_gold
    )

    table_green_style = ParagraphStyle(
        'TableGreenDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12.5,
        textColor=accent_green
    )

    table_cyan_style = ParagraphStyle(
        'TableCyanDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12.5,
        textColor=accent_cyan
    )

    callout_text = ParagraphStyle(
        'CalloutRedDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=alerta_text
    )

    callout_green_text = ParagraphStyle(
        'CalloutGreenDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=dica_text
    )

    story = []

    # ==================== PÁGINA 1: CAPA OFICIAL ====================
    if os.path.exists(cover_image_path):
        story.append(Spacer(1, 0.6 * cm))
        story.append(Image(cover_image_path, width=18.0 * cm, height=24.1 * cm))
    else:
        story.append(Spacer(1, 4 * cm))
        story.append(Paragraph("MILLIONAIRE AFFILIATE TRADERS", title_style))
        story.append(Paragraph("O guia gratuito para começar no mercado de afiliados de corretoras", subtitle_style))
        story.append(Paragraph("FP TRADER — Felipe Vieira", h2_style))

    story.append(PageBreak())

    # ==================== PÁGINA 2: BOAS-VINDAS & SUMÁRIO ====================
    story.append(Paragraph("BOAS-VINDAS", title_style))
    story.append(Paragraph("Mensagem do Autor — FP TRADER (Felipe Vieira)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph("<b>Seja muito bem-vindo ao Millionaire Affiliate Traders!</b>", body_style))
    story.append(Paragraph(
        "Este material foi criteriosamente desenvolvido para você que deseja conhecer o mercado de afiliados "
        "de corretoras e aprender como iniciar sua jornada na divulgação de plataformas globais de trading.",
        body_style
    ))
    story.append(Paragraph(
        "Aqui você encontrará informações introdutórias fundamentais sobre <b>opções binárias, criptomoedas e Forex</b>, "
        "além de links diretos para os principais programas de afiliados mundiais e orientações práticas para "
        "começar a construir sua própria rede de indicações e subafiliados.",
        body_style
    ))
    story.append(Paragraph(
        "Meu objetivo é compartilhar conhecimento, facilitar seu acesso aos programas oficiais e ajudar você a "
        "compreender os primeiros passos desse ecossistema.",
        body_style
    ))

    # Box Dica de Ouro
    dica_data = [[
        Paragraph("💡 <b>Princípio Fundamental:</b> Você não precisa começar sabendo tudo. O segredo é estudar, conhecer a fundo as regras de cada plataforma e desenvolver suas estratégias com consistência, ética e responsabilidade.", callout_green_text)
    ]]
    dica_table = Table(dica_data, colWidths=[18 * cm])
    dica_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), dica_bg),
        ('BOX', (0,0), (-1,-1), 1, dica_border),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(dica_table)
    story.append(Spacer(1, 10))

    # Sumário Box
    story.append(Paragraph("SUMÁRIO DO MATERIAL", h2_style))
    sumario_data = [
        [Paragraph("<b>Capítulo 01</b>", table_gold_style), Paragraph("Entenda o Mercado de Afiliados e Subafiliados", table_cell_style)],
        [Paragraph("<b>Capítulo 02</b>", table_gold_style), Paragraph("Opções Binárias & Plataformas (Avalon, IQ Option, Exnova, Vyon)", table_cell_style)],
        [Paragraph("<b>Capítulo 03</b>", table_gold_style), Paragraph("Criptomoedas (Binance, Bybit)", table_cell_style)],
        [Paragraph("<b>Capítulo 04</b>", table_gold_style), Paragraph("Forex — Mercado Cambial (Fotmarkets, Exness)", table_cell_style)],
        [Paragraph("<b>Capítulo 05</b>", table_gold_style), Paragraph("Como Construir sua Rede de Afiliados (Instagram, TikTok, YT, Telegram)", table_cell_style)],
        [Paragraph("<b>Capítulo 06</b>", table_gold_style), Paragraph("Plano de Ação Prático para Iniciantes (Roteiro de 7 Dias)", table_cell_style)],
        [Paragraph("<b>Canais</b>", table_green_style), Paragraph("Contatos Oficiais, Comunidade & Aviso Regulatório", table_cell_style)],
    ]
    sumario_table = Table(sumario_data, colWidths=[3.5 * cm, 14.5 * cm])
    sumario_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [bg_surface, bg_elevated]),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sumario_table)

    story.append(PageBreak())

    # ==================== PÁGINA 3: CAPÍTULO 1 ====================
    story.append(Paragraph("CAPÍTULO 1 — ENTENDA O MERCADO DE AFILIADOS", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph("O que é um afiliado?", h2_style))
    story.append(Paragraph(
        "Um afiliado é um parceiro que divulga produtos ou serviços de uma empresa utilizando links de indicação "
        "exclusivos ou mecanismos de rastreamento com identificadores únicos (tags e cookies).",
        body_style
    ))
    story.append(Paragraph(
        "Dependendo do programa, a empresa remunera o afiliado com base em diferentes modelos:",
        body_style
    ))
    story.append(Paragraph("• <b>CPA (Custo por Aquisição):</b> Remuneração fixa por cadastro com primeiro depósito aprovado.", bullet_style))
    story.append(Paragraph("• <b>Revenue Share (RevShare):</b> Participação percentual contínua na receita gerada pelo usuário indicado.", bullet_style))
    story.append(Paragraph("• <b>Modelos Híbridos:</b> Combinação de taxa fixa inicial com percentual de receita contínua.", bullet_style))

    story.append(Paragraph("O que é um subafiliado?", h2_style))
    story.append(Paragraph(
        "Alguns programas oferecem uma estrutura de parceiros em níveis. Nela, você pode indicar novos afiliados "
        "para participarem da divulgação da corretora. Quando esses parceiros geram comissões, você recebe uma "
        "porcentagem proporcional pelo suporte e recrutamento prestados (geralmente entre 5% e 10% da comissão gerada).",
        body_style
    ))

    story.append(Paragraph("Passo a Passo para Iniciar:", h2_style))
    passos_data = [
        [Paragraph("<b>1. Escolha:</b>", table_cyan_style), Paragraph("Defina o programa de afiliados alinhado com seu nicho e audiência.", table_cell_style)],
        [Paragraph("<b>2. Requisitos:</b>", table_cyan_style), Paragraph("Leia os termos de aprovação, tráfego aceito e políticas contra fraudes.", table_cell_style)],
        [Paragraph("<b>3. Cadastro:</b>", table_cyan_style), Paragraph("Preencha suas informações reais e confirme sua identidade.", table_cell_style)],
        [Paragraph("<b>4. Tracking:</b>", table_cyan_style), Paragraph("Organize seus links personalizados com parâmetros de rastreamento (SubIDs).", table_cell_style)],
        [Paragraph("<b>5. Conteúdo:</b>", table_cyan_style), Paragraph("Crie materiais educativos focados em gerar valor genuíno para o público.", table_cell_style)],
        [Paragraph("<b>6. Análise:</b>", table_cyan_style), Paragraph("Monitore métricas de cliques, conversões e comissões no painel oficial.", table_cell_style)],
    ]
    passos_table = Table(passos_data, colWidths=[3.2 * cm, 14.8 * cm])
    passos_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [bg_surface, bg_elevated]),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(passos_table)
    story.append(Spacer(1, 10))

    # Alerta Regulatório
    aviso_data = [[
        Paragraph("⚠️ <b>Atenção:</b> Não existe garantia de aprovação automática, geração de comissões ou lucros fáceis. O sucesso depende da qualidade da sua entrega, seriedade e consistência ao longo do tempo.", callout_text)
    ]]
    aviso_table = Table(aviso_data, colWidths=[18 * cm])
    aviso_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), alerta_bg),
        ('BOX', (0,0), (-1,-1), 1, alerta_border),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(aviso_table)

    story.append(PageBreak())

    # ==================== PÁGINA 4: CAPÍTULO 2 ====================
    story.append(Paragraph("CAPÍTULO 2 — OPÇÕES BINÁRIAS", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph(
        "Opções binárias são derivativos nos quais o resultado da operação depende de uma condição prefixada: "
        "se a cotação de determinado ativo estará acima ou abaixo do preço de entrada em uma data/horário de expiração.",
        body_style
    ))
    story.append(Paragraph("O que é indispensável estudar antes de operar ou divulgar?", h2_style))
    story.append(Paragraph("• Leitura básica de gráficos, velas japonesas (Candlesticks) e ação do preço (Price Action)", bullet_style))
    story.append(Paragraph("• Zonas de Suporte e Resistência, linhas de tendência e canais de volatilidade", bullet_style))
    story.append(Paragraph("• Gerenciamento estrito de banca (nunca arrisque mais do que 1% a 2% por entrada)", bullet_style))
    story.append(Paragraph("• Diferenças práticas entre a conta demo (treinamento) e a conta real", bullet_style))
    story.append(Paragraph("• Condições de saque, regras de compliance e taxas cobradas", bullet_style))

    story.append(Paragraph("Programas de Afiliados e Plataformas:", h2_style))

    # Tabela de Plataformas Binárias
    broker_data = [
        [
            Paragraph("<b>Plataforma</b>", table_header_style),
            Paragraph("<b>Finalidade</b>", table_header_style),
            Paragraph("<b>Link de Acesso Oficial (Clique para abrir)</b>", table_header_style)
        ],
        [
            Paragraph("<b>AVALON</b>", table_gold_style),
            Paragraph("Afiliados (Parceiros)", table_cell_style),
            Paragraph('<link href="https://partner.avalonbroker.com/auth/signup?ref_id=749575&amp;afftrack=EbookMAT"><font color="#38bdf8"><u>partner.avalonbroker.com (Cadastro Afiliado)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>AVALON</b>", table_gold_style),
            Paragraph("Operações (Trader)", table_cell_style),
            Paragraph('<link href="https://trade.avalonbroker.com/register?aff=749575&amp;aff_model=revenue&amp;afftrack=ebookMAT"><font color="#38bdf8"><u>trade.avalonbroker.com (Conta Trader)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>AFFSTORE</b>", table_gold_style),
            Paragraph("Hub de Afiliados Global", table_cell_style),
            Paragraph('<link href="https://affstore.com/?ref_id=384570&amp;afftrack=ebookMAT"><font color="#38bdf8"><u>affstore.com (Painel Geral de Afiliados)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>IQ OPTION</b>", table_gold_style),
            Paragraph("Operações (Trader)", table_cell_style),
            Paragraph('<link href="https://affiliate.iqoption.net/redir/?aff=384570&amp;aff_model=revenue&amp;afftrack=ebookMAT"><font color="#38bdf8"><u>iqoption.com (Registro de Trader)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>EXNOVA</b>", table_gold_style),
            Paragraph("Operações (Trader)", table_cell_style),
            Paragraph('<link href="https://trade.exnova.com/pwa?aff=384570&amp;aff_model=revenue&amp;afftrack=ebookMAT"><font color="#38bdf8"><u>exnova.com (Cadastro Trader)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>SABIOTRADE</b>", table_gold_style),
            Paragraph("Mesa Proprietária", table_cell_style),
            Paragraph('<link href="https://sabiotrade.com/?aff=384570&amp;aff_model=revenue&amp;afftrack=ebookMAT"><font color="#38bdf8"><u>sabiotrade.com (Acesso à Plataforma)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>QUADCODE</b>", table_gold_style),
            Paragraph("Tráfego de Afiliados", table_cell_style),
            Paragraph('<link href="https://quadcode.com/lp/affiliate_traffic?utm_source=384570&amp;utm_medium=ebookMAT"><font color="#38bdf8"><u>quadcode.com (Affiliate Traffic)</u></font></link>', link_style)
        ],
    ]
    broker_table = Table(broker_data, colWidths=[3.2 * cm, 4.0 * cm, 10.8 * cm])
    broker_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(broker_table)
    story.append(Spacer(1, 10))

    # VYON TRADE ESPECIAL
    story.append(Paragraph("Vyon Trade — Procedimento Passo a Passo:", h2_style))
    story.append(Paragraph("1. Crie sua conta inicial na corretora: <link href='https://vyontrade.com/register?refid=B4iIAiC34c'><font color='#38bdf8'><u>vyontrade.com/register</u></font></link>", bullet_style))
    story.append(Paragraph("2. Conclua a validação e ativação da conta solicitada pela plataforma.", bullet_style))
    story.append(Paragraph("3. Acesse a área de estatísticas de parceiros: <link href='https://partners.vyontrade.com/estatisticas'><font color='#38bdf8'><u>partners.vyontrade.com/estatisticas</u></font></link>", bullet_style))
    story.append(Paragraph("4. Utilize o mesmo e-mail e senha cadastrados na corretora para entrar no painel.", bullet_style))
    story.append(Paragraph("5. Localize seu link de indicação e acompanhe seus relatórios de desempenho.", bullet_style))

    story.append(PageBreak())

    # ==================== PÁGINA 5: CAPÍTULO 3 & 4 ====================
    story.append(Paragraph("CAPÍTULO 3 — CRIPTOMOEDAS", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph(
        "Criptomoedas são ativos digitais descentralizados conhecidos pela alta liquidez e volatilidade expressiva. "
        "Antes de operar ou indicar corretoras de criptomoedas, tenha total clareza sobre:",
        body_style
    ))
    story.append(Paragraph("• Como funcionam os depósitos em reais (PIX) e retiradas para carteiras pessoais (cold/hot wallets)", bullet_style))
    story.append(Paragraph("• A importância inegociável da autenticação de dois fatores (2FA via app autenticador)", bullet_style))
    story.append(Paragraph("• Diferenciação precisa de redes de envio (ex: Bitcoin vs ERC20 vs BEP20 vs Tron TRC20)", bullet_style))
    story.append(Paragraph("• Estrutura de taxas Maker/Taker e custos de saque em blockchain", bullet_style))

    crypto_data = [
        [
            Paragraph("<b>Corretora</b>", table_header_style),
            Paragraph("<b>Destaques</b>", table_header_style),
            Paragraph("<b>Link Oficial com Benefícios</b>", table_header_style)
        ],
        [
            Paragraph("<b>BINANCE</b>", table_gold_style),
            Paragraph("Maior exchange do mundo em volume e segurança máxima", table_cell_style),
            Paragraph('<link href="https://www.binance.com/register?ref=234579621"><font color="#38bdf8"><u>binance.com (Ref: 234579621)</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>BYBIT</b>", table_gold_style),
            Paragraph("Líder em contratos futuros e campanhas atrativas", table_cell_style),
            Paragraph('<link href="https://www.bybit.com/invite?ref=Q8Z4YP8&amp;medium=referral&amp;utm_campaign=evergreen"><font color="#38bdf8"><u>bybit.com (Convite: Q8Z4YP8)</u></font></link>', link_style)
        ],
    ]
    crypto_table = Table(crypto_data, colWidths=[3.2 * cm, 5.0 * cm, 9.8 * cm])
    crypto_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(crypto_table)
    story.append(Spacer(1, 12))

    # CAPÍTULO 4 - FOREX
    story.append(Paragraph("CAPÍTULO 4 — FOREX (MERCADO CAMBIAL)", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph(
        "O mercado Forex (Foreign Exchange) é o maior e mais líquido mercado financeiro global. "
        "Nele, são negociados pares de moedas como EUR/USD, GBP/USD e USD/JPY. Conceitos obrigatórios:",
        body_style
    ))
    story.append(Paragraph("• <b>Pips e Spread:</b> A menor fração de variação do par e o custo operacional de entrada", bullet_style))
    story.append(Paragraph("• <b>Lotes:</b> Tamanho do contrato negociado (Standard 1.0, Mini 0.1, Micro 0.01)", bullet_style))
    story.append(Paragraph("• <b>Alavancagem:</b> Potencializa o poder de compra, mas multiplica igualmente o risco de perdas", bullet_style))
    story.append(Paragraph("• <b>Stop-Loss & Take-Profit:</b> Ordens automáticas de proteção e encerramento", bullet_style))

    forex_data = [
        [
            Paragraph("<b>Corretora</b>", table_header_style),
            Paragraph("<b>Características</b>", table_header_style),
            Paragraph("<b>Link de Registro Oficial</b>", table_header_style)
        ],
        [
            Paragraph("<b>FOTMARKETS</b>", table_gold_style),
            Paragraph("Suporte dedicado e ambiente ágil para novos traders", table_cell_style),
            Paragraph('<link href="https://secure.fot.co/links/go/1630"><font color="#38bdf8"><u>secure.fot.co/links/go/1630</u></font></link>', link_style)
        ],
        [
            Paragraph("<b>EXNESS</b>", table_gold_style),
            Paragraph("Uma das mais prestigiadas do mundo, saques automáticos", table_cell_style),
            Paragraph('<link href="https://one.exnessonelink.com/a/k1ha2y86gr"><font color="#38bdf8"><u>one.exnessonelink.com/a/k1ha2y86gr</u></font></link>', link_style)
        ],
    ]
    forex_table = Table(forex_data, colWidths=[3.2 * cm, 5.0 * cm, 9.8 * cm])
    forex_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(forex_table)

    story.append(PageBreak())

    # ==================== PÁGINA 6: CAPÍTULO 5 ====================
    story.append(Paragraph("CAPÍTULO 5 — COMO CONSTRUIR SUA REDE DE AFILIADOS", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    story.append(Paragraph(
        "Cadastrar-se nos programas é apenas a primeira etapa. Para construir resultados consistentes como afiliado "
        "e estruturar uma rede sólida, você precisa dominar os principais canais de tráfego orgânico e pago:",
        body_style
    ))

    canais_data = [
        [
            Paragraph("<b>Canal</b>", table_header_style),
            Paragraph("<b>Melhor Abordagem Prática</b>", table_header_style)
        ],
        [
            Paragraph("<b>📷 Instagram</b>", table_gold_style),
            Paragraph("Carrosséis explicativos sobre termos de mercado, Reels rápidos com dicas operacionais e link estratégico na Bio oferecendo este ebook gratuito.", table_cell_style)
        ],
        [
            Paragraph("<b>🎵 TikTok</b>", table_cyan_style),
            Paragraph("Vídeos dinâmicos desmistificando o mercado para leigos. Foque em tutoriais de como criar conta e primeiros passos. Nunca faça promessas de ganhos irreais.", table_cell_style)
        ],
        [
            Paragraph("<b>▶️ YouTube</b>", table_gold_style),
            Paragraph("O canal mais forte para conversão duradoura. Crie tutoriais passo a passo da interface das plataformas, análises de taxas e comparativos transparentes.", table_cell_style)
        ],
        [
            Paragraph("<b>✈️ Telegram</b>", table_cyan_style),
            Paragraph("Canal de relacionamento direto para nutrir a comunidade, enviar materiais complementares, relatórios e tirar dúvidas frequentes dos novos membros.", table_cell_style)
        ],
        [
            Paragraph("<b>📁 Google Drive</b>", table_gold_style),
            Paragraph("Mantenha o PDF deste ebook hospedado em pasta pública para distribuição fácil para leads que não utilizam o Telegram.", table_cell_style)
        ],
    ]
    canais_table = Table(canais_data, colWidths=[3.5 * cm, 14.5 * cm])
    canais_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(canais_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Boas Práticas e Compliance na Divulgação:", h2_style))
    story.append(Paragraph("✔ <b>Transparência:</b> Declare abertamente que você utiliza links de parceiro e que poderá receber comissões.", bullet_style))
    story.append(Paragraph("✔ <b>Zero Spam:</b> Nunca envie mensagens não solicitadas ou links soltos em grupos públicos.", bullet_style))
    story.append(Paragraph("✔ <b>Sem Promessas Falsas:</b> Fuja de expressões como 'ganhos garantidos' ou 'dinheiro fácil'. Elas destroem sua reputação e causam banimento nos programas.", bullet_style))
    story.append(Paragraph("✔ <b>Acompanhamento:</b> Use os painéis analíticos para ver quais canais trazem cliques mais qualificados.", bullet_style))

    story.append(PageBreak())

    # ==================== PÁGINA 7: CAPÍTULO 6, CONTATOS & AVISO ====================
    story.append(Paragraph("CAPÍTULO 6 — PLANO DE AÇÃO PARA INICIANTES", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_green, spaceBefore=4, spaceAfter=12))

    cronograma_data = [
        [Paragraph("<b>Dia</b>", table_header_style), Paragraph("<b>Meta Prática da Primeira Semana</b>", table_header_style)],
        [Paragraph("<b>Dia 01</b>", table_green_style), Paragraph("Estude a fundo as regras dos programas de afiliados e modelos de comissão (CPA vs RevShare).", table_cell_style)],
        [Paragraph("<b>Dia 02</b>", table_green_style), Paragraph("Escolha 2 ou 3 corretoras do guia e leia integralmente os termos de uso de parceiro.", table_cell_style)],
        [Paragraph("<b>Dia 03</b>", table_green_style), Paragraph("Realize seus cadastros com seus dados reais e envie a documentação de KYC para aprovação.", table_cell_style)],
        [Paragraph("<b>Dia 04</b>", table_green_style), Paragraph("Organize seus links de indicação, crie seus parâmetros de tracking e guarde em uma planilha.", table_cell_style)],
        [Paragraph("<b>Dia 05</b>", table_green_style), Paragraph("Produza seu primeiro conteúdo educativo (carrossel no Instagram ou vídeo explicativo no TikTok).", table_cell_style)],
        [Paragraph("<b>Dia 06</b>", table_green_style), Paragraph("Publique a apresentação do seu canal e disponibilize este ebook gratuito como isca digital.", table_cell_style)],
        [Paragraph("<b>Dia 07</b>", table_green_style), Paragraph("Analise as dúvidas recebidas dos seus seguidores e planeje os conteúdos da semana seguinte.", table_cell_style)],
    ]
    cronograma_table = Table(cronograma_data, colWidths=[2.5 * cm, 15.5 * cm])
    cronograma_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cronograma_table)
    story.append(Spacer(1, 10))

    # CONTATOS OFICIAIS
    story.append(Paragraph("CONTATOS OFICIAIS & COMUNIDADE", h2_style))
    contatos_data = [
        [
            Paragraph("💬 <b>WhatsApp Oficial:</b>", table_gold_style),
            Paragraph('<link href="https://wa.me/5532984167034"><font color="#38bdf8"><u>+55 32 98416-7034 (Clique para conversar no WhatsApp)</u></font></link>', link_style)
        ],
        [
            Paragraph("✈️ <b>Telegram:</b>", table_cyan_style),
            Paragraph('<link href="https://t.me/chefe_fp_vieira"><font color="#38bdf8"><u>@chefe_fp_vieira (Mensagem direta no Telegram)</u></font></link>', link_style)
        ],
        [
            Paragraph("📸 <b>Instagram:</b>", table_green_style),
            Paragraph('<link href="https://instagram.com/f.vieiraaaa"><font color="#38bdf8"><u>@f.vieiraaaa (Siga e envie direct no Instagram)</u></font></link>', link_style)
        ],
    ]
    contatos_table = Table(contatos_data, colWidths=[4.8 * cm, 13.2 * cm])
    contatos_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [bg_surface, bg_elevated]),
        ('GRID', (0,0), (-1,-1), 0.5, border_slate),
        ('BOX', (0,0), (-1,-1), 1, border_slate),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(contatos_table)
    story.append(Spacer(1, 10))

    # AVISO IMPORTANTE FINAL
    aviso_final = (
        "<b>AVISO LEGAL:</b> Este material tem finalidade estritamente educativa e informativa. "
        "Não representa recomendação de investimento, aconselhamento financeiro ou garantia de rentabilidade. "
        "Os mercados de Opções Binárias, Forex e Criptomoedas envolvem risco real de perda do capital investido. "
        "Os links contêm códigos de afiliado pelos quais o autor poderá receber comissões."
    )
    aviso_box_data = [[Paragraph(aviso_final, callout_text)]]
    aviso_box = Table(aviso_box_data, colWidths=[18 * cm])
    aviso_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), alerta_bg),
        ('BOX', (0,0), (-1,-1), 1, alerta_border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(aviso_box)

    # Build Document com tema escuro (onFirstPage e onLaterPages)
    doc.build(
        story,
        canvasmaker=NumberedCanvas,
        onFirstPage=draw_dark_background,
        onLaterPages=draw_dark_background
    )
    print("PDF successfully generated at:", pdf_filename)


if __name__ == "__main__":
    build_pdf()
