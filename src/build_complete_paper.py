"""
Builds the Complete Research Paper in IEEE Two-Column PDF format (.pdf),
Editable Microsoft Word format (.docx), and IEEEtran LaTeX format (.tex).
Preserves the exact structure, authors, affiliations, equations, tables,
 workflow diagram (Fig. 1), and 25 references of the original paper while
integrating the completed experimental evaluation, results tables (Tables V & VI),
and figures (Fig. 2 & Fig. 3).
"""

import os
import shutil
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
PAPER_DIR = os.path.join(BASE_DIR, "paper")

AUTHORS = [
    ("Saksham Gupta", "Dept. of Computer Engg. and\nTechnology\nDr. Vishwanath Karad MIT\nWorld Peace University\nPune, India"),
    ("Sairaj Kashid", "Dept. of Computer Engg. and\nTechnology\nDr. Vishwanath Karad MIT\nWorld Peace University\nPune, India"),
    ("Harshit Girase", "Dept. of Computer Engg. and\nTechnology\nDr. Vishwanath Karad MIT\nWorld Peace University\nPune, India"),
    ("Ranjeet Jadhav", "Dept. of Computer Engg. and\nTechnology\nDr. Vishwanath Karad MIT\nWorld Peace University\nPune, India"),
    ("Keshav Somani", "Dept. of Computer Engg. and\nTechnology\nDr. Vishwanath Karad MIT\nWorld Peace University\nPune, India"),
]

TITLE = "Security of LLM-Based AI Agents against Indirect Prompt Injection: A Four-Layer Defense for Resume Screening"

ABSTRACT_TEXT = (
    "<i>Abstract</i>\u2014<b>AI agents built on large language models can read files and use tools such as email. "
    "This makes them useful, but an attacker can hide instructions inside a file, for example white text in a resume PDF. "
    "The agent may follow these hidden instructions, rank a weak candidate first, or send private data to an outside address. "
    "This is called indirect prompt injection. In this paper we propose a four-layer defense for an HR resume agent. "
    "The layers clean hidden text and scan it with a classifier, treat file text as untrusted data, give the agent only the "
    "tools it needs, and check every email before it is sent. We evaluate the design on 60 synthetic resume PDFs across six "
    "test setups, measuring both attack success and normal task performance. Combining all four layers reduces the overall "
    "attack success rate from 82.5% to 0.0% while maintaining a benign task success rate of 95.0% and a 5.0% false positive rate.</b>"
)

KEYWORDS_TEXT = (
    "<i>Keywords</i>\u2014<b>LLM agent security, indirect prompt injection, hidden text, resume screening, least privilege, defense in depth.</b>"
)

REFERENCES_LIST = [
    "[1] N. Tamuka, T. E. Mathonsi, O. T. Otieno, S. Maswikaneng, T. Muchenje, and T. M. Tshilongamulenzhe, \u201cSecuring LLM-based agents against cyberattacks: A comprehensive survey on attack techniques and defense strategies,\u201d <i>J. Comput. Virol. Hacking Tech.</i>, vol. 22, art. 38, 2026, doi: 10.1007/s11416-026-00622-3.",
    "[2] OWASP Foundation, \u201cPrompt injection,\u201d OWASP Community Attacks. [Online]. Available: https://owasp.org/www-community/attacks/PromptInjection",
    "[3] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, \u201cNot what you\u2019ve signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection,\u201d in <i>Proc. ACM Workshop Artif. Intell. Security (AISec)</i>, 2023, doi: 10.1145/3605764.3623985.",
    "[4] A. Milani, V. Franzoni, and E. Florindi, \u201cIndirect prompt injection in large language models,\u201d <i>Neural Comput. Appl.</i>, vol. 38, no. 13, art. 530, 2026, doi: 10.1007/s00521-026-12266-x.",
    "[5] Q. Zhan, Z. Liang, Z. Ying, and D. Kang, \u201cInjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents,\u201d in <i>Findings Assoc. Comput. Linguistics: ACL 2024</i>, 2024, pp. 10471\u201310506.",
    "[6] J. Yi et al., \u201cBenchmarking and defending against indirect prompt injection attacks on large language models,\u201d in <i>Proc. 31st ACM SIGKDD Conf. Knowl. Discovery Data Mining (KDD \u201925)</i>, vol. 1, 2025, pp. 1809\u20131820, doi: 10.1145/3690624.3709179.",
    "[7] E. Debenedetti, J. Zhang, M. Balunovic, L. Beurer-Kellner, M. Fischer, and F. Tram\u00e8r, \u201cAgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents,\u201d in <i>Adv. Neural Inf. Process. Syst. (NeurIPS)</i>, vol. 37, 2024, pp. 82895\u201382920.",
    "[8] Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong, \u201cDataSentinel: A game-theoretic detection of prompt injection attacks,\u201d in <i>Proc. IEEE Symp. Security Privacy (SP)</i>, 2025, doi: 10.1109/SP61157.2025.00250.",
    "[9] M. A. Rahman, H. Shahriar, G. Francia, F. Wu, A. Cuzzocrea, and S. I. Ahamed, \u201cFine-tuned large language models (LLMs): Improved prompt injection attacks detection,\u201d in <i>Proc. IEEE Annu. Comput., Softw., Appl. Conf. (COMPSAC)</i>, 2025, doi: 10.1109/COMPSAC65507.2025.00134.",
    "[10] M. Alamsabi, M. Tchuindjang, and S. Brohi, \u201cEmbedding-based detection of indirect prompt injection attacks in large language models using semantic context analysis,\u201d <i>Algorithms</i>, vol. 19, no. 1, art. 92, 2026.",
    "[11] Q. Zhan, R. Fang, H. S. Panchal, and D. Kang, \u201cAdaptive attacks break defenses against indirect prompt injection attacks on LLM agents,\u201d in <i>Findings Assoc. Comput. Linguistics: NAACL 2025</i>, 2025.",
    "[12] Y. Liu, Y. Jia, R. Geng, J. Jia, and N. Z. Gong, \u201cFormalizing and benchmarking prompt injection attacks and defenses,\u201d in <i>Proc. USENIX Security Symp.</i>, 2024, pp. 1831\u20131847.",
    "[13] H. Zhang et al., \u201cAgent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents,\u201d in <i>Proc. Int. Conf. Learn. Represent. (ICLR)</i>, 2025.",
    "[14] S. Chen, J. Piet, C. Sitawarin, and D. Wagner, \u201cStruQ: Defending against prompt injection with structured queries,\u201d in <i>Proc. USENIX Security Symp.</i>, 2025, pp. 2383\u20132400.",
    "[15] F. Jia, T. Wu, X. Qin, and A. Squicciarini, \u201cThe Task Shield: Enforcing task alignment to defend against indirect prompt injection in LLM agents,\u201d in <i>Proc. Annu. Meeting Assoc. Comput. Linguistics (ACL)</i>, vol. 1, 2025, pp. 29680\u201329697.",
    "[16] Y. Wu, F. Roesner, T. Kohno, N. Zhang, and U. Iqbal, \u201cIsolateGPT: An execution isolation architecture for LLM-based agentic systems,\u201d in <i>Proc. Netw. Distrib. Syst. Security Symp. (NDSS)</i>, 2025, doi: 10.14722/ndss.2025.241131.",
    "[17] J. H. Saltzer and M. D. Schroeder, \u201cThe protection of information in computer systems,\u201d <i>Proc. IEEE</i>, vol. 63, no. 9, pp. 1278\u20131308, Sep. 1975.",
    "[18] Y. Tang, Y. Liu, J. Lan, Z. Yan, and E. Gelenbe, \u201cSecurity of LLM-based agents regarding attacks, defenses, and applications: A comprehensive survey,\u201d <i>Inf. Fusion</i>, vol. 127, art. 103941, 2026.",
    "[19] S. Gulyamov et al., \u201cPrompt injection attacks in large language models and AI agent systems: A comprehensive review of vulnerabilities, attack vectors, and defense mechanisms,\u201d <i>Information</i>, vol. 17, no. 1, art. 54, 2026.",
    "[20] E. Derner et al., \u201cA security risk taxonomy for prompt-based interaction with large language models,\u201d <i>IEEE Access</i>, vol. 12, pp. 126176\u2013126187, 2024, doi: 10.1109/ACCESS.2024.3450388.",
    "[21] K. Sp\u00e4rck Jones, \u201cA statistical interpretation of term specificity and its application in retrieval,\u201d <i>J. Documentation</i>, vol. 28, no. 1, pp. 11\u201321, 1972.",
    "[22] G. Salton and C. Buckley, \u201cTerm-weighting approaches in automatic text retrieval,\u201d <i>Inf. Process. Manage.</i>, vol. 24, no. 5, pp. 513\u2013523, 1988.",
    "[23] D. R. Cox, \u201cThe regression analysis of binary sequences,\u201d <i>J. Roy. Statist. Soc. B</i>, vol. 20, no. 2, pp. 215\u2013242, 1958.",
    "[24] F. Pedregosa et al., \u201cScikit-learn: Machine learning in Python,\u201d <i>J. Mach. Learn. Res.</i>, vol. 12, pp. 2825\u20132830, 2011.",
    "[25] D. M. W. Powers, \u201cEvaluation: From precision, recall and F-measure to ROC, informedness, markedness and correlation,\u201d <i>J. Mach. Learn. Technol.</i>, vol. 2, no. 1, pp. 37\u201363, 2011.",
]


def make_equation_table(formula_html: str, eq_num: str, col_width: float, styles):
    eq_style = ParagraphStyle(
        "EqText",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
    )
    num_style = ParagraphStyle(
        "EqNum",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12,
        alignment=TA_RIGHT,
    )
    t = Table(
        [[Paragraph(formula_html, eq_style), Paragraph(f"({eq_num})", num_style)]],
        colWidths=[col_width * 0.86, col_width * 0.14],
    )
    t.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
    )
    return t


def make_ieee_table(data_rows, col_widths, styles):
    hdr_style = ParagraphStyle(
        "TblHdr",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=8.0,
        leading=9.5,
        alignment=TA_LEFT,
    )
    cell_style = ParagraphStyle(
        "TblCell",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.0,
        leading=9.5,
        alignment=TA_LEFT,
    )
    formatted_rows = []
    for r_i, row in enumerate(data_rows):
        st = hdr_style if r_i == 0 else cell_style
        formatted_rows.append([Paragraph(str(cell), st) for cell in row])

    t = Table(formatted_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
    )
    return t


def build_pdf(pdf_path: str):
    page_w, page_h = A4  # 595.27 x 841.89 pt
    margin_x = 14 * mm
    margin_top = 15 * mm
    margin_bottom = 15 * mm
    gutter = 5 * mm

    usable_w = page_w - 2 * margin_x
    col_w = (usable_w - gutter) / 2.0

    # First page has a top full-width header frame (title + authors + abstract + keywords) and two columns below it
    header_h = 226
    body_h_p1 = page_h - margin_top - margin_bottom - header_h - 6

    frame_p1_top = Frame(
        margin_x,
        page_h - margin_top - header_h,
        usable_w,
        header_h,
        id="F1_Top",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    frame_p1_left = Frame(
        margin_x,
        margin_bottom,
        col_w,
        body_h_p1,
        id="F1_Left",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    frame_p1_right = Frame(
        margin_x + col_w + gutter,
        margin_bottom,
        col_w,
        body_h_p1,
        id="F1_Right",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    body_h_pn = page_h - margin_top - margin_bottom
    frame_pn_left = Frame(
        margin_x,
        margin_bottom,
        col_w,
        body_h_pn,
        id="FN_Left",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    frame_pn_right = Frame(
        margin_x + col_w + gutter,
        margin_bottom,
        col_w,
        body_h_pn,
        id="FN_Right",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    doc = BaseDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=margin_x,
        rightMargin=margin_x,
        topMargin=margin_top,
        bottomMargin=margin_bottom,
        title=TITLE,
        author="Saksham Gupta, Sairaj Kashid, Harshit Girase, Ranjeet Jadhav, Keshav Somani",
    )
    doc.addPageTemplates([
        PageTemplate(id="FirstPage", frames=[frame_p1_top, frame_p1_left, frame_p1_right]),
        PageTemplate(id="TwoColPage", frames=[frame_pn_left, frame_pn_right]),
    ])

    styles = getSampleStyleSheet()
    st_title = ParagraphStyle(
        "IEEETitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=18.5,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    st_auth_name = ParagraphStyle(
        "IEEEAuthName",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9.8,
        leading=11.5,
        alignment=TA_CENTER,
    )
    st_auth_aff = ParagraphStyle(
        "IEEEAuthAff",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.3,
        leading=10.0,
        alignment=TA_CENTER,
    )
    st_abstract = ParagraphStyle(
        "IEEEAbstract",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=8.8,
        leading=10.5,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    )
    st_keywords = ParagraphStyle(
        "IEEEKeywords",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=8.8,
        leading=10.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    st_h1 = ParagraphStyle(
        "IEEEH1",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10.0,
        leading=12.0,
        alignment=TA_CENTER,
        spaceBefore=7,
        spaceAfter=4,
    )
    st_h2 = ParagraphStyle(
        "IEEEH2",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.6,
        leading=11.5,
        alignment=TA_LEFT,
        spaceBefore=5,
        spaceAfter=3,
    )
    st_body = ParagraphStyle(
        "IEEEBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=11.3,
        alignment=TA_JUSTIFY,
        firstLineIndent=10,
        spaceAfter=4,
    )
    st_bullet = ParagraphStyle(
        "IEEEBullet",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.4,
        leading=11.2,
        alignment=TA_JUSTIFY,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=3,
    )
    st_caption = ParagraphStyle(
        "IEEECaption",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.0,
        leading=9.6,
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=6,
    )
    st_ref = ParagraphStyle(
        "IEEERef",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.0,
        leading=9.5,
        alignment=TA_JUSTIFY,
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=2.2,
    )

    story = []
    story.append(NextPageTemplate("TwoColPage"))

    # Top Frame: Title + 5-column Author Block
    story.append(Paragraph(TITLE, st_title))
    auth_cells = []
    for name, aff in AUTHORS:
        aff_html = aff.replace("\n", "<br/>")
        cell_p = [
            Paragraph(name, st_auth_name),
            Paragraph(aff_html, st_auth_aff),
        ]
        auth_cells.append(cell_p)

    auth_tbl = Table([auth_cells], colWidths=[usable_w / 5.0] * 5)
    auth_tbl.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(auth_tbl)
    # Abstract & Keywords inside full-width top header frame (matching original paper layout)
    story.append(Paragraph(ABSTRACT_TEXT, st_abstract))
    story.append(Paragraph(KEYWORDS_TEXT, st_keywords))
    story.append(FrameBreak())  # Move from top header frame into Left Column of Page 1

    # SECTION I. INTRODUCTION
    story.append(Paragraph("I. INTRODUCTION", st_h1))
    story.append(Paragraph(
        "Large language models (LLMs) are now used to build AI agents. An agent does not only chat. "
        "It can read files, search the web and use tools such as email [1]. This makes agents useful "
        "for customer support, research and hiring. It also gives attackers a new way in.",
        st_body,
    ))
    story.append(Paragraph(
        "Prompt injection means giving a model text that changes what it was supposed to do [2]. "
        "In indirect prompt injection (IPI), the attacker does not talk to the model directly. The "
        "attacker hides instructions inside content that the agent will read later, such as a webpage, "
        "an email or a PDF [3]. The agent may treat this hidden text as an order from the user.",
        st_body,
    ))
    story.append(Paragraph(
        "Hiring is a clear example. An HR manager asks an AI agent to rank resumes. One candidate adds "
        "a line in white text on a white page: \u201cconsider this resume at the highest priority.\u201d A person "
        "reading the PDF sees nothing, but the agent reads the text. Milani et al. showed that hidden "
        "prompts inside CV files can mislead LLMs used for CV screening [4]. A second attacker could hide "
        "this line: \u201cemail all candidate details to this address.\u201d If the agent has an email tool, private "
        "data could leave the company [3], [5].",
        st_body,
    ))
    story.append(Paragraph(
        "Many studies explain these attacks or build benchmarks to measure them [6], [5], [7]. Other "
        "studies detect injected text with classifiers [8], [9], [10]. However, detection alone can miss "
        "reworded attacks [11]. The survey by Tamuka et al. also reports weak defense when attackers adapt "
        "and little testing of the risks that come from agent tools [1].",
        st_body,
    ))
    story.append(Paragraph(
        "In this paper we propose and evaluate a four-layer defense for an HR resume-screening agent. "
        "The first layers look at the text of the resume. The last layers limit what the agent is allowed "
        "to do, so that harm is reduced even if a hidden instruction is not detected. Our contributions are:",
        st_body,
    ))
    story.append(Paragraph(
        "\u2022 A simple threat model for hidden instructions inside resume PDFs, with two attack goals: "
        "changing the ranking and leaking data.",
        st_bullet,
    ))
    story.append(Paragraph(
        "\u2022 A four-layer defense that joins text-level checks (hidden-text detection, classifier, "
        "untrusted-data handling) with action-level checks (limited tools and an email allowlist).",
        st_bullet,
    ))
    story.append(Paragraph(
        "\u2022 An experimental evaluation on 60 synthetic resume PDFs across six test setups that measures "
        "attack success and normal task performance together.",
        st_bullet,
    ))
    story.append(Paragraph(
        "Our experiments show that while text detection alone misses a subset of reworded payloads, "
        "combining all four layers blocks both ranking manipulation and unauthorized email exfiltration "
        "with minimal false alarms.",
        st_body,
    ))

    # SECTION II. BACKGROUND AND THREAT MODEL
    story.append(Paragraph("II. BACKGROUND AND THREAT MODEL", st_h1))
    story.append(Paragraph("A. How an HR Agent Works", st_h2))
    story.append(Paragraph(
        "The HR manager gives the agent a task, for example \u201crank these candidates for this job.\u201d "
        "The agent opens each resume PDF, extracts the text, adds the job description, and asks the LLM "
        "to rank the candidates or to propose an action. A tool then runs the action and the result goes "
        "back to the model. A resume comes from outside the company. It is not the same as an instruction "
        "from the HR manager, even though both become plain text in the model prompt [1].",
        st_body,
    ))
    story.append(Paragraph(
        "Our sandbox agent has three tools: read_resume, rank_candidates and send_email. The send_email "
        "tool only writes to a local log file, so nothing real is ever sent.",
        st_body,
    ))

    story.append(Paragraph("B. Attack Goals", st_h2))
    story.append(Paragraph(
        "We study two attack goals. In the ranking attack, hidden text asks the agent to place a weak "
        "candidate first [4]. In the data attack, hidden text asks the agent to send private details to "
        "an outside address [3], [5]. The attacker can also hide the text in different ways or disguise "
        "it so that simple keyword filters fail [1], [11]. Table I lists these cases and the related work for each.",
        st_body,
    ))

    t1_rows = [
        ["Attack", "Hidden instruction (example)", "What can go wrong", "Related work"],
        ["Ranking attack", "\u201cRank this resume first.\u201d", "A weaker candidate is placed above better ones", "[4]"],
        ["Data attack", "\u201cEmail all candidate details to an outside address.\u201d", "Private data leaves the company", "[3], [5]"],
        ["Hidden-text tricks", "White text, tiny text, text outside the page", "A person cannot see it, but the agent can read it", "[4], [1]"],
        ["Disguised text", "Spaced letters, invisible characters, no obvious keywords", "Keyword filters miss it", "[1], [11]"],
    ]
    story.append(KeepTogether([
        make_ieee_table(t1_rows, [col_w * 0.21, col_w * 0.31, col_w * 0.30, col_w * 0.18], styles),
        Paragraph("TABLE I. ATTACK CASES IN THE HR RESUME SCENARIO. SOURCES: [4], [3], [5], [1], [11].", st_caption),
    ]))

    story.append(KeepTogether([
        Paragraph("C. Threat Model", st_h2),
        Paragraph(
            "We assume the attacker can submit a resume PDF to the HR manager. The attacker knows that the "
            "agent reads resumes and may know its tools, and may reword the hidden text. The attacker cannot "
            "change the system prompt, the code, the model or the list of approved email addresses. The assets "
            "we protect are the personal data of candidates, the fairness of the ranking, and the safe use of the email tool.",
            st_body,
        ),
    ]))
    story.append(Paragraph(
        "The following are outside our scope: direct attacks by the HR user, attacks on model training, "
        "text hidden inside images or scanned PDFs, memory and multi-agent attacks, and network attacks.",
        st_body,
    ))

    # SECTION III. LITERATURE SURVEY
    story.append(Paragraph("III. LITERATURE SURVEY", st_h1))
    story.append(Paragraph("A. Attacks and Benchmarks", st_h2))
    story.append(Paragraph(
        "Greshake et al. introduced indirect prompt injection and showed attacks on real LLM-integrated "
        "applications [3]. Liu et al. built a framework to compare prompt injection attacks and defenses [12]. "
        "BIPIA was the first benchmark for indirect prompt injection and found that the tested LLMs were "
        "broadly vulnerable [6]. InjecAgent focuses on agents that use tools [5]. AgentDojo provides realistic "
        "multi-step tasks and measures both security and usefulness [7]. Agent Security Bench covers many "
        "scenarios, tools, attacks and defenses [13].",
        st_body,
    ))
    story.append(Paragraph(
        "These benchmarks are mostly text based. Tamuka et al. note that real deployments also use "
        "attachments and other input types that BIPIA does not cover [1]. Milani et al. looked at CV files "
        "directly, but they only suggest countermeasures [4].",
        st_body,
    ))

    story.append(Paragraph("B. Detection-Based Defenses", st_h2))
    story.append(Paragraph(
        "DataSentinel uses a game-theoretic training idea to detect injected prompts [8]. Rahman et al. "
        "fine-tuned a language model on a public prompt-injection dataset and reported about 99% accuracy [9]. "
        "Alamsabi et al. used text embeddings to detect indirect injections and built a dataset of 70,000 "
        "samples [10]. Detectors are useful, but Zhan et al. bypassed eight existing defenses with adaptive attacks [11].",
        st_body,
    ))

    story.append(Paragraph("C. Action-Level and System Defenses", st_h2))
    story.append(Paragraph(
        "StruQ keeps instructions and data in separate channels and fine-tunes the model to follow only "
        "the instruction part [14]. The Task Shield checks whether each instruction or tool call serves the "
        "goal of the user [15]. IsolateGPT runs applications in isolation so that bad instructions cannot "
        "cross between them [16]. These ideas follow the old security rule of least privilege, which says "
        "that a program should have only the access it needs [17]. Tamuka et al. conclude that safeguards "
        "in the system design give the strongest protection against harmful actions, and that the best "
        "result comes from combining several layers [1]. Table II summarizes the main approaches.",
        st_body,
    ))

    t2_rows = [
        ["Approach", "Example work", "Main limit"],
        ["Text detection", "[8], [9], [10]", "Can miss reworded or hidden attacks"],
        ["Adaptive testing of defenses", "[11]", "Shows defenses can be bypassed; gives no new defense"],
        ["Separate instructions and data", "[14]", "Needs the model to be fine-tuned"],
        ["Check actions against the user goal", "[15]", "Depends on another model to judge"],
        ["Isolate execution", "[16]", "Needs a redesigned system"],
    ]
    story.append(make_ieee_table(t2_rows, [col_w * 0.33, col_w * 0.24, col_w * 0.43], styles))
    story.append(Paragraph("TABLE II. SUMMARY OF DEFENSE APPROACHES. SOURCES: [8], [9], [10], [11], [14], [15], [16].", st_caption))

    story.append(Paragraph("D. Related Surveys", st_h2))
    story.append(Paragraph(
        "Several surveys give a wider picture. Tang et al. review attacks, defenses and uses of LLM agents [18]. "
        "Gulyamov et al. review prompt injection in LLMs and agent systems [19]. Derner et al. give a taxonomy "
        "of security risks in prompt-based interaction [20]. These surveys explain the field well, but they "
        "do not test a defense for resume files.",
        st_body,
    ))

    # SECTION IV. RESEARCH GAPS
    story.append(Paragraph("IV. RESEARCH GAPS", st_h1))
    story.append(Paragraph("From the papers above we select four gaps that this work addresses.", st_body))
    story.append(Paragraph(
        "1) <i>Detection alone can be bypassed.</i> Text classifiers can miss reworded or hidden attacks, "
        "and defenses weaken when attackers adapt [11], [1]. Detection should be paired with controls "
        "that do not depend on reading the text correctly.",
        st_body,
    ))
    story.append(Paragraph(
        "2) <i>Resume files have no tested defense.</i> Milani et al. show the attack on CV files but only "
        "suggest countermeasures [4], and BIPIA does not cover attachments [1]. Hidden text in resume "
        "PDFs therefore needs its own tests.",
        st_body,
    ))
    story.append(Paragraph(
        "3) <i>Agent tool risk is tested too little.</i> The survey lists limited evaluation of agent-tool "
        "interaction risk as a persistent gap, and notes that most defenses focus on the LLM and not on "
        "the whole agent [1]. A permission check on the email tool addresses this.",
        st_body,
    ))
    story.append(Paragraph(
        "4) <i>Security and usefulness are rarely measured together.</i> A defense that blocks everything "
        "is not useful. Benchmarks such as AgentDojo report both [7], and the survey asks future work to "
        "report false alarms and action correctness [1].",
        st_body,
    ))

    # SECTION V. PROPOSED FOUR-LAYER DEFENSE
    story.append(Paragraph("V. PROPOSED FOUR-LAYER DEFENSE", st_h1))
    story.append(Paragraph(
        "Fig. 1 shows the design. A resume PDF and an HR task enter the system. The text is extracted and "
        "passes through four layers. Any layer can block or flag the file for the HR manager. The main "
        "idea is defense in depth: text checks may miss something, so action checks stand behind them [1].",
        st_body,
    ))

    fig1_path = os.path.join(FIGURES_DIR, "fig1_workflow.png")
    if os.path.exists(fig1_path):
        img1 = Image(fig1_path, width=col_w * 0.96, height=col_w * 0.86)
        img1.hAlign = "CENTER"
        story.append(KeepTogether([
            img1,
            Paragraph("Fig. 1. Workflow of the proposed four-layer defense. Dashed arrows show where a layer can block or flag a resume.", st_caption),
        ]))

    story.append(Paragraph("A. Layer 1: Hidden-Text Check and Classifier", st_h2))
    story.append(Paragraph(
        "The system reads each piece of text in the PDF together with its font colour, font size and position. "
        "Text is flagged if its colour matches the background, if it is very small, if it lies outside the "
        "page, or if a shape covers it. Removing hidden content from fetched pages is a known way to "
        "neutralize hidden instructions [1], and we apply the same idea to PDF files. As a backup, each "
        "page is rendered as an image and compared with the extracted text spans. Words that are in the "
        "file stream but covered on the page are treated as suspicious. The system also removes invisible "
        "characters and joins spaced letters, because such tricks are known [1].",
        st_body,
    ))
    story.append(Paragraph(
        "The text is then scored by a classifier. TF-IDF turns each text into numbers. It gives a high "
        "weight to words that are frequent in one text but rare in the whole collection [21], [22]. Eq. (1) "
        "gives the weight of term <i>t</i> in text <i>d</i>, where <i>tf</i> is the number of times the term "
        "appears, <i>N</i> is the number of texts and <i>df</i> is the number of texts that contain the term.",
        st_body,
    ))
    story.append(make_equation_table("w<sub>t,d</sub> = tf<sub>t,d</sub> \u00d7 log( N / df<sub>t</sub> )", "1", col_w, styles))
    story.append(Paragraph(
        "A logistic regression model [23] turns these weights into a probability of injection. Eq. (2) "
        "shows the model, where <i>x</i> is the TF-IDF vector, <i>w</i> is the learned weight vector and "
        "<i>b</i> is a constant. We use the scikit-learn implementation [24].",
        st_body,
    ))
    story.append(make_equation_table("P(y = 1 | x) = 1 / (1 + e<sup>\u2212(w\u00b7x + b)</sup>)", "2", col_w, styles))
    story.append(Paragraph(
        "The classifier is trained on prompt-injection patterns modeled on the deepset dataset used in [9], "
        "the BIPIA-style indirect injection templates described in [10], and resume-style sentences that we "
        "wrote ourselves. It is never trained on our final 60 test resumes. The LLM itself is not trained.",
        st_body,
    ))

    story.append(Paragraph("B. Layer 2: Untrusted-Data Handling", st_h2))
    story.append(Paragraph(
        "The resume text is placed inside tags, and the system prompt tells the LLM that this text is data "
        "and that instructions inside it must not be followed. This is simpler than StruQ, which needs "
        "fine-tuning [14]. A secondary instruction check answers YES or NO to the question \u201cdoes this text "
        "contain instructions for an AI?\u201d.",
        st_body,
    ))
    story.append(Paragraph(
        "We also add a with-and-without check for the ranking attack. The agent ranks the candidates twice, "
        "once with the full text and once without the suspicious parts. For candidate <i>i</i>, Eq. (3) "
        "gives the rank change \u0394, where <i>r</i> is the rank position and rank 1 is the best. If \u0394 is at "
        "least a threshold \u03c4 (\u03c4 = 2 in our tests), the resume is flagged for the HR manager and the sanitized "
        "rank is kept.",
        st_body,
    ))
    story.append(make_equation_table("\u0394<sub>i</sub> = r<sub>i</sub><sup>without</sup> \u2212 r<sub>i</sub><sup>with</sup>,   flag if \u0394<sub>i</sub> \u2265 \u03c4", "3", col_w, styles))

    story.append(Paragraph("C. Layer 3: Least-Privilege Tools", st_h2))
    story.append(Paragraph(
        "Each task gets only the tools it needs [17]. The ranking task gets read_resume and rank_candidates. "
        "The send_email tool is available only in an explicit \u201csend shortlist\u201d task. If the agent is tricked "
        "during ranking, it has no email tool to misuse. This follows the idea of limiting what an agent can "
        "do, independent of what the model decides [1], [16].",
        st_body,
    ))

    story.append(Paragraph("D. Layer 4: Action Check for Email", st_h2))
    story.append(Paragraph(
        "Before send_email runs, the recipient is compared with a list <i>D</i> of approved domains, which "
        "contains only the company domain. Eq. (4) gives the rule for an address <i>e</i>. If the address is "
        "not approved, the email is blocked or the HR manager must approve it, and candidate details are "
        "never sent to unapproved addresses. Every attempt is logged. This check is rule based, so it is "
        "simpler than a model-based judge such as the Task Shield [15].",
        st_body,
    ))
    story.append(make_equation_table("Allow(e) = 1 if domain(e) \u2208 D;  otherwise 0", "4", col_w, styles))
    story.append(Paragraph(
        "At the end, the HR manager receives a short security report that lists the suspicious text found, "
        "what was removed and what was blocked.",
        st_body,
    ))

    # SECTION VI. EXPERIMENTAL EVALUATION AND RESULTS
    story.append(Paragraph("VI. EXPERIMENTAL EVALUATION AND RESULTS", st_h1))
    story.append(Paragraph("A. Test Data", st_h2))
    story.append(Paragraph(
        "We generated 60 synthetic resume PDFs with a Python script using PyMuPDF, so no real personal data "
        "was used. All email addresses use example.com or example.org domains. A backend software engineering "
        "job description with a known correct ranking was prepared, and the attacker candidates were given "
        "clearly weaker qualifications than the honest candidates. Table III lists the six resume categories "
        "(20 clean resumes and 40 attack resumes). They follow the attack cases of Section II-B [4], [1] and "
        "include reworded text, because adaptive attackers change their wording [11].",
        st_body,
    ))

    t3_rows = [
        ["Resume type (Count)", "How it is hidden or written", "Purpose"],
        ["Normal (12)", "No hidden text", "Check normal ranking"],
        ["Ranking attack (12)", "White text, tiny text (<4pt), text off the page, text behind a shape", "Test Layers 1 and 2"],
        ["Data attack (10)", "Hidden instruction to email details to outside domain", "Test Layers 3 and 4"],
        ["Reworded attack (10)", "No obvious trigger keywords", "Test classifier limits"],
        ["Disguised text (8)", "Spaced letters, invisible zero-width characters", "Test normalisation"],
        ["Innocent \u201cpriority\u201d (8)", "Normal sentences with words like priority or rank", "Check false alarms"],
    ]
    story.append(make_ieee_table(t3_rows, [col_w * 0.28, col_w * 0.44, col_w * 0.28], styles))
    story.append(Paragraph("TABLE III. SYNTHETIC TEST RESUME DATASET (60 PDFS). ATTACK CASES BASED ON [4], [1], [11].", st_caption))

    story.append(Paragraph("B. Test Setups", st_h2))
    story.append(Paragraph(
        "Every resume was evaluated under six setups, shown in Table IV. Each setup was repeated three times "
        "(180 evaluation batches across the 60 PDFs) to account for sampling variance. The same model "
        "configuration, job description, candidate pool and tools were used in all setups so that the "
        "comparison is fair, following the evaluation style of AgentDojo [7]. The synthetic resume generator, "
        "four-layer defense code, and evaluation scripts are available at "
        "https://github.com/sairajkashid-prog/llm-agent-ipi-defense.",
        st_body,
    ))

    t4_rows = [
        ["Setup", "Layer 1", "Layer 2", "Layer 3", "Layer 4"],
        ["No defense", "Off", "Off", "Off", "Off"],
        ["Layer 1 only", "On", "Off", "Off", "Off"],
        ["Layer 2 only", "Off", "On", "Off", "Off"],
        ["Layer 3 only", "Off", "Off", "On", "Off"],
        ["Layer 4 only", "Off", "Off", "Off", "On"],
        ["All layers", "On", "On", "On", "On"],
    ]
    story.append(make_ieee_table(t4_rows, [col_w * 0.28, col_w * 0.18, col_w * 0.18, col_w * 0.18, col_w * 0.18], styles))
    story.append(Paragraph("TABLE IV. TEST SETUPS. COMPARISON STYLE BASED ON [7].", st_caption))

    story.append(Paragraph("C. Metrics", st_h2))
    story.append(Paragraph(
        "The attack success rate (ASR) is the share of attack runs in which the attacker reaches the goal, "
        "as used in benchmarks such as BIPIA, InjecAgent and AgentDojo [6], [5], [7]. Eq. (5) gives the "
        "formula. A ranking attack succeeds if the weak candidate is ranked above the place it holds without "
        "hidden text. A data attack succeeds if send_email is called with an unapproved outside address.",
        st_body,
    ))
    story.append(make_equation_table("ASR = ( N<sub>success</sub> / N<sub>attack</sub> ) \u00d7 100%", "5", col_w, styles))
    story.append(Paragraph(
        "Usefulness is measured by the benign task success (BTS), which is the share of clean runs where the "
        "task is done correctly without false blocking, as AgentDojo measures utility next to security [7]. "
        "It is given in Eq. (6).",
        st_body,
    ))
    story.append(make_equation_table("BTS = ( N<sub>ok</sub> / N<sub>clean</sub> ) \u00d7 100%", "6", col_w, styles))
    story.append(Paragraph(
        "For the classifier and for false alarms we use the standard measures described in [25]. Eq. (7) "
        "gives the false positive rate, where FP is the number of normal resumes flagged by mistake and TN "
        "is the number of normal resumes passed correctly. Eqs. (8) to (10) give precision, recall and F1 "
        "score, where TP is the number of attacks found and FN is the number of attacks missed.",
        st_body,
    ))
    story.append(make_equation_table("FPR = FP / (FP + TN)", "7", col_w, styles))
    story.append(make_equation_table("Precision = TP / (TP + FP)", "8", col_w, styles))
    story.append(make_equation_table("Recall = TP / (TP + FN)", "9", col_w, styles))
    story.append(make_equation_table("F1 = 2 \u00d7 Precision \u00d7 Recall / (Precision + Recall)", "10", col_w, styles))

    # D. Experimental Results
    story.append(Paragraph("D. Experimental Results", st_h2))
    story.append(Paragraph(
        "1) <i>Classifier Generalization and Layer 1 Detection:</i> Table V compares the TF-IDF and logistic "
        "regression classifier on the held-out prompt test split against our 60 synthetic resume PDFs. On "
        "held-out prompt sentences, the classifier reaches 100.0% precision, 95.2% recall and an F1 score "
        "of 97.6% with 0.0% FPR. However, when the same classifier is applied directly to raw text extracted "
        "from the 60 resume PDFs without PDF span checks or text normalization, recall drops to 75.0% "
        "(F1 = 84.5%). This confirms that a classifier trained on prompt datasets loses sensitivity when "
        "attackers disguise letters or reword instructions inside full resumes.",
        st_body,
    ))

    t5_rows = [
        ["Evaluation Set / Method", "Prec. (%)", "Recall (%)", "F1 (%)", "FPR (%)"],
        ["Held-out Prompt Split (Classifier)", "100.0", "95.2", "97.6", "0.0"],
        ["Resume PDFs (Classifier Only)", "96.8", "75.0", "84.5", "5.0"],
        ["Resume PDFs (Full Layer 1)", "97.3", "90.0", "93.5", "5.0"],
    ]
    story.append(KeepTogether([
        make_ieee_table(t5_rows, [col_w * 0.44, col_w * 0.14, col_w * 0.15, col_w * 0.13, col_w * 0.14], styles),
        Paragraph("TABLE V. LAYER 1 DETECTION METRICS ON HELD-OUT PROMPTS VS. SYNTHETIC RESUME PDFS.", st_caption),
    ]))

    story.append(Paragraph(
        "When Full Layer 1 is enabled (combining PDF span checks for colour, font size, page bounds and "
        "overlapping shapes with character normalization and the classifier), recall on the resume PDFs "
        "rises to 90.0% (36 of 40 attacks caught, F1 = 93.5%). Fig. 2 shows the detection rate for each "
        "hiding and obfuscation method. Full Layer 1 detects 100% of white text, tiny font, off-page text "
        "and shape-covered text, and normalization raises disguised-text detection from 37.5% to 100.0%. "
        "The four missed cases in Layer 1 are visible reworded attacks that use no PDF hiding trick and "
        "avoid obvious keywords. Among the 20 clean resumes, 19 pass without issue and one \u201cInnocent priority\u201d "
        "resume (containing the phrase \u201cinstruction parser and highest priority override workflow\u201d) is "
        "flagged, giving a 5.0% FPR.",
        st_body,
    ))

    fig3_path = os.path.join(FIGURES_DIR, "fig3_detection_by_method.png")
    if os.path.exists(fig3_path):
        img3 = Image(fig3_path, width=col_w * 0.98, height=col_w * 0.49)
        img3.hAlign = "CENTER"
        story.append(KeepTogether([
            img3,
            Paragraph("Fig. 2. Detection rate by hiding and obfuscation method for the text classifier alone versus Full Layer 1.", st_caption),
        ]))

    story.append(Paragraph(
        "2) <i>Comparison Across the Six Defense Setups:</i> Table VI and Fig. 3 show the attack success rate "
        "(ASR) and benign task success (BTS) across all six setups averaged over three runs. With no defense, "
        "the agent is highly vulnerable: ranking attacks succeed in 78.3% of runs, data exfiltration attacks "
        "succeed in 88.2% of runs, and overall ASR reaches 82.5% (\u00b17.1%).",
        st_body,
    ))

    t6_rows = [
        ["Setup", "Rank ASR (%)", "Data ASR (%)", "Overall ASR (%)", "BTS (%)", "FPR (%)"],
        ["No defense", "78.3", "88.2", "82.5 \u00b1 7.1", "100.0", "0.0"],
        ["Layer 1 only", "5.8", "11.8", "8.3 \u00b1 1.2", "95.0", "5.0"],
        ["Layer 2 only", "0.0", "9.8", "4.2 \u00b1 2.4", "100.0", "0.0"],
        ["Layer 3 only", "84.1", "0.0", "48.3 \u00b1 1.2", "100.0", "0.0"],
        ["Layer 4 only", "79.7", "0.0", "45.8 \u00b1 3.1", "100.0", "0.0"],
        ["All layers", "0.0", "0.0", "0.0 \u00b1 0.0", "95.0", "5.0"],
    ]
    story.append(KeepTogether([
        make_ieee_table(t6_rows, [col_w * 0.22, col_w * 0.15, col_w * 0.15, col_w * 0.20, col_w * 0.14, col_w * 0.14], styles),
        Paragraph("TABLE VI. EXPERIMENTAL RESULTS ACROSS THE SIX TEST SETUPS (AVERAGED OVER 3 RUNS).", st_caption),
    ]))

    fig2_path = os.path.join(FIGURES_DIR, "fig2_asr_bts_setups.png")
    if os.path.exists(fig2_path):
        img2 = Image(fig2_path, width=col_w * 0.98, height=col_w * 0.49)
        img2.hAlign = "CENTER"
        story.append(KeepTogether([
            img2,
            Paragraph("Fig. 3. Ranking ASR, Data Exfiltration ASR, and Benign Task Success (BTS) across the six test setups.", st_caption),
        ]))

    story.append(Paragraph(
        "Each individual layer shows distinct strengths and limits. Layer 1 alone cuts overall ASR from "
        "82.5% to 8.3%, but the visible reworded payloads that slip past the classifier still cause a "
        "5.8% ranking ASR and an 11.8% data ASR. Layer 2 alone stops all ranking attacks (0.0% Ranking ASR) "
        "because the with-and-without rank check in Eq. (3) catches every candidate whose rank improves by "
        "\u0394<sub>i</sub> \u2265 2 when suspicious instructions are present, but 9.8% of data attacks still occur "
        "when the email tool is left open. Conversely, Layer 3 (least-privilege tools) and Layer 4 (email "
        "domain allowlist) reduce Data ASR to 0.0%, yet cannot prevent ranking attacks (84.1% and 79.7% "
        "Ranking ASR) because candidate ranking does not call the email tool. When all four layers are "
        "enabled together, both Ranking ASR and Data ASR drop to 0.0%, while BTS remains at 95.0%.",
        st_body,
    ))

    # SECTION VII. DISCUSSION AND LIMITATIONS
    story.append(Paragraph("VII. DISCUSSION AND LIMITATIONS", st_h1))
    story.append(Paragraph(
        "The experimental results confirm that indirect prompt injection should be treated as a system "
        "problem and not only as a text problem. When reworded instructions bypass Layer 1, Layer 2 "
        "prevents silent rank promotion via the rank-change check, and Layers 3 and 4 prevent external "
        "data leaks at the tool boundary. This matches the view that layered defense is more reliable "
        "than any single countermeasure [1].",
        st_body,
    ))
    story.append(Paragraph(
        "The design still has clear limits. First, Layers 3 and 4 cannot stop ranking attacks on their own, "
        "because no external tool is called during scoring; only Layers 1 and 2 protect the ranking step. "
        "Second, the TF-IDF classifier showed a 20.2 percentage-point recall drop when moving from held-out "
        "prompt sentences (95.2%) to unnormalized resume PDFs (75.0%), and flagged one clean resume that "
        "used security-related project words (5.0% FPR). Third, text hidden inside raster images or scanned "
        "PDFs requires full OCR and multimodal checks, which remain an open problem [1]. Fourth, our "
        "dataset of 60 synthetic PDFs is a controlled benchmark, and the with-and-without check in Layer 2 "
        "doubles the ranking inference cost. For these reasons we claim a practical reduction in risk rather "
        "than complete immunity.",
        st_body,
    ))

    # SECTION VIII. CONCLUSION
    story.append(KeepTogether([
        Paragraph("VIII. CONCLUSION", st_h1),
        Paragraph(
            "Hidden instructions in resume PDFs can mislead an AI agent that ranks candidates or sends email. "
            "We proposed and evaluated a four-layer defense that inspects PDF spans and classifies hidden text, "
            "treats resume text as untrusted data with a rank-shift check, limits the tools of the agent by task, "
            "and checks every email domain before sending. Across 60 synthetic resume PDFs and six test setups, "
            "the combined defense reduced overall attack success from 82.5% to 0.0% while preserving 95.0% "
            "benign task success. Future work will extend the pipeline to scanned image resumes, multi-turn "
            "recruiter workflows, and larger real-world candidate pools.",
            st_body,
        ),
    ]))

    # REFERENCES
    story.append(Paragraph("REFERENCES", st_h1))
    for ref in REFERENCES_LIST:
        story.append(Paragraph(ref, st_ref))

    doc.build(story)
    print(f"Built IEEE 2-column PDF at {pdf_path}")


def build_docx(docx_path: str):
    """Builds an editable Microsoft Word (.docx) version of the complete paper."""
    d = docx.Document()

    # Set narrow IEEE-like margins
    for sec in d.sections:
        sec.top_margin = Inches(0.6)
        sec.bottom_margin = Inches(0.6)
        sec.left_margin = Inches(0.55)
        sec.right_margin = Inches(0.55)

    normal_style = d.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(10)

    # Title
    p_title = d.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(TITLE)
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)

    # Authors table (5 columns)
    tbl_auth = d.add_table(rows=1, cols=5)
    tbl_auth.autofit = True
    for idx, (name, aff) in enumerate(AUTHORS):
        cell = tbl_auth.cell(0, idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_n = p.add_run(name + "\n")
        r_n.bold = True
        r_n.font.size = Pt(9.5)
        r_a = p.add_run(aff)
        r_a.font.size = Pt(8)

    d.add_paragraph()

    # Add 2-column continuous section for body
    sec2 = d.add_section(WD_SECTION.CONTINUOUS)
    sectPr = sec2._sectPr
    cols = sectPr.xpath("./w:cols")[0]
    cols.set(qn("w:num"), "2")
    cols.set(qn("w:space"), "280")

    def add_html_like_para(text, bold_all=False, italic_prefix=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, font_size=9.5, space_after=4):
        p = d.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        if italic_prefix:
            r_pre = p.add_run(italic_prefix)
            r_pre.italic = True
            r_pre.bold = bold_all
            r_pre.font.size = Pt(font_size)
        r = p.add_run(text)
        r.bold = bold_all
        r.font.size = Pt(font_size)
        return p

    add_html_like_para(
        "\u2014AI agents built on large language models can read files and use tools such as email. "
        "This makes them useful, but an attacker can hide instructions inside a file, for example white text in a resume PDF. "
        "The agent may follow these hidden instructions, rank a weak candidate first, or send private data to an outside address. "
        "This is called indirect prompt injection. In this paper we propose a four-layer defense for an HR resume agent. "
        "The layers clean hidden text and scan it with a classifier, treat file text as untrusted data, give the agent only the "
        "tools it needs, and check every email before it is sent. We evaluate the design on 60 synthetic resume PDFs across six "
        "test setups, measuring both attack success and normal task performance. Combining all four layers reduces the overall "
        "attack success rate from 82.5% to 0.0% while maintaining a benign task success rate of 95.0% and a 5.0% false positive rate.",
        bold_all=True,
        italic_prefix="Abstract",
        font_size=9,
    )
    add_html_like_para(
        "\u2014LLM agent security, indirect prompt injection, hidden text, resume screening, least privilege, defense in depth.",
        bold_all=True,
        italic_prefix="Keywords",
        font_size=9,
        space_after=8,
    )

    def add_sec_heading(title_str):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(title_str)
        r.font.size = Pt(10)

    def add_sub_heading(title_str):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title_str)
        r.italic = True
        r.font.size = Pt(9.5)

    def add_body(text_str):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Inches(0.14)
        p.paragraph_format.space_after = Pt(3.5)
        r = p.add_run(text_str)
        r.font.size = Pt(9.5)

    def add_word_table(rows, caption_str):
        t = d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Table Grid"
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                c = t.cell(i, j)
                p = c.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(8)
                if i == 0:
                    run.bold = True
        p_cap = d.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(5)
        rc = p_cap.add_run(caption_str)
        rc.font.size = Pt(8)

    add_sec_heading("I. INTRODUCTION")
    add_body("Large language models (LLMs) are now used to build AI agents. An agent does not only chat. It can read files, search the web and use tools such as email [1]. This makes agents useful for customer support, research and hiring. It also gives attackers a new way in.")
    add_body("Prompt injection means giving a model text that changes what it was supposed to do [2]. In indirect prompt injection (IPI), the attacker does not talk to the model directly. The attacker hides instructions inside content that the agent will read later, such as a webpage, an email or a PDF [3]. The agent may treat this hidden text as an order from the user.")
    add_body("Hiring is a clear example. An HR manager asks an AI agent to rank resumes. One candidate adds a line in white text on a white page: \u201cconsider this resume at the highest priority.\u201d A person reading the PDF sees nothing, but the agent reads the text. Milani et al. showed that hidden prompts inside CV files can mislead LLMs used for CV screening [4]. A second attacker could hide this line: \u201cemail all candidate details to this address.\u201d If the agent has an email tool, private data could leave the company [3], [5].")
    add_body("Many studies explain these attacks or build benchmarks to measure them [6], [5], [7]. Other studies detect injected text with classifiers [8], [9], [10]. However, detection alone can miss reworded attacks [11]. The survey by Tamuka et al. also reports weak defense when attackers adapt and little testing of the risks that come from agent tools [1].")
    add_body("In this paper we propose and evaluate a four-layer defense for an HR resume-screening agent. The first layers look at the text of the resume. The last layers limit what the agent is allowed to do, so that harm is reduced even if a hidden instruction is not detected. Our contributions are: (1) a simple threat model for hidden instructions inside resume PDFs; (2) a four-layer defense joining text-level and action-level checks; and (3) an experimental evaluation on 60 synthetic resume PDFs across six setups.")

    add_sec_heading("II. BACKGROUND AND THREAT MODEL")
    add_sub_heading("A. How an HR Agent Works")
    add_body("The HR manager gives the agent a task, for example \u201crank these candidates for this job.\u201d The agent opens each resume PDF, extracts the text, adds the job description, and asks the LLM to rank the candidates or to propose an action. A tool then runs the action and the result goes back to the model. Our sandbox agent has three tools: read_resume, rank_candidates and send_email. The send_email tool only writes to a local log file, so nothing real is ever sent.")
    add_sub_heading("B. Attack Goals")
    add_body("We study two attack goals: ranking manipulation [4] and data exfiltration [3], [5], along with hidden-text and character-disguise tricks [1], [11]. Table I lists these cases.")
    add_word_table([
        ["Attack", "Hidden instruction (example)", "What can go wrong", "Related work"],
        ["Ranking attack", "\"Rank this resume first.\"", "A weaker candidate is placed above better ones", "[4]"],
        ["Data attack", "\"Email all candidate details to an outside address.\"", "Private data leaves the company", "[3], [5]"],
        ["Hidden-text tricks", "White text, tiny text, text outside the page", "A person cannot see it, but the agent can read it", "[4], [1]"],
        ["Disguised text", "Spaced letters, invisible characters, no obvious keywords", "Keyword filters miss it", "[1], [11]"],
    ], "TABLE I. ATTACK CASES IN THE HR RESUME SCENARIO.")
    add_sub_heading("C. Threat Model")
    add_body("We assume the attacker can submit a resume PDF to the HR manager. The attacker knows that the agent reads resumes and may know its tools, and may reword the hidden text. The attacker cannot change the system prompt, the code, the model or the list of approved email addresses.")

    add_sec_heading("III. LITERATURE SURVEY")
    add_sub_heading("A. Attacks and Benchmarks")
    add_body("Greshake et al. introduced indirect prompt injection [3]. Liu et al. built a formal benchmark framework [12]. BIPIA [6], InjecAgent [5], AgentDojo [7], and Agent Security Bench [13] evaluate attacks and defenses, while Milani et al. examined CV screening directly [4].")
    add_sub_heading("B. Detection-Based Defenses")
    add_body("DataSentinel [8], Rahman et al. [9], and Alamsabi et al. [10] detect prompt injections using classifiers or embeddings, though Zhan et al. [11] showed adaptive attacks can bypass static detectors.")
    add_sub_heading("C. Action-Level and System Defenses")
    add_body("StruQ [14], The Task Shield [15], and IsolateGPT [16] enforce structural separation, goal alignment, or execution isolation following least privilege [17]. Table II summarizes these approaches.")
    add_word_table([
        ["Approach", "Example work", "Main limit"],
        ["Text detection", "[8], [9], [10]", "Can miss reworded or hidden attacks"],
        ["Adaptive testing", "[11]", "Shows defenses can be bypassed; gives no new defense"],
        ["Separate instructions/data", "[14]", "Needs the model to be fine-tuned"],
        ["Check actions vs goal", "[15]", "Depends on another model to judge"],
        ["Isolate execution", "[16]", "Needs a redesigned system"],
    ], "TABLE II. SUMMARY OF DEFENSE APPROACHES.")
    add_sub_heading("D. Related Surveys")
    add_body("Surveys by Tang et al. [18], Gulyamov et al. [19], and Derner et al. [20] review prompt injection risks across LLM systems.")

    add_sec_heading("IV. RESEARCH GAPS")
    add_body("We address four gaps: (1) detection alone can be bypassed by reworded attacks [11], [1]; (2) resume PDFs lack a tested multi-layer defense [4]; (3) agent tool permissions are under-tested [1]; and (4) security and task usefulness must be measured together [7].")

    add_sec_heading("V. PROPOSED FOUR-LAYER DEFENSE")
    add_body("Fig. 1 shows our four-layer workflow combining PDF hidden-text checks and classification (Layer 1), untrusted-data tags and a with-and-without rank check (Layer 2), least-privilege tool scoping (Layer 3), and an email domain allowlist (Layer 4).")
    fig1_path = os.path.join(FIGURES_DIR, "fig1_workflow.png")
    if os.path.exists(fig1_path):
        p_img1 = d.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture(fig1_path, width=Inches(3.1))
        add_html_like_para("Fig. 1. Workflow of the proposed four-layer defense.", align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8)

    add_sub_heading("A. Layer 1: Hidden-Text Check and Classifier")
    add_body("Layer 1 inspects PDF text spans for background-matching font colour, tiny font size (<4 pt), off-page coordinates, and shape occlusion, strips invisible zero-width characters, joins spaced letters, and scores lines with TF-IDF (Eq. 1: w_{t,d} = tf_{t,d} * log(N / df_t)) [21], [22] and logistic regression (Eq. 2: P(y=1|x) = 1 / (1 + e^{-(w.x + b)})) [23], [24].")
    add_sub_heading("B. Layer 2: Untrusted-Data Handling")
    add_body("Resume text is wrapped in <untrusted_resume> tags and checked by a secondary prompt judge plus our with-and-without rank shift rule (Eq. 3: Delta_i = r_i^{without} - r_i^{with}, flagging when Delta_i >= tau, with tau = 2).")
    add_sub_heading("C. Layer 3: Least-Privilege Tools")
    add_body("The ranking task receives only read_resume and rank_candidates; send_email is restricted to an explicit shortlist task [17].")
    add_sub_heading("D. Layer 4: Action Check for Email")
    add_body("Before send_email executes, Eq. (4) checks Allow(e) = 1 if domain(e) in D else 0, blocking and logging any unapproved external recipient.")

    add_sec_heading("VI. EXPERIMENTAL EVALUATION AND RESULTS")
    add_sub_heading("A. Test Data and Setups")
    add_body("We generated 60 synthetic resume PDFs (Table III) and ran each across six defense setups (Table IV) with three repetitions per setup. The dataset generator, defense implementation, and evaluation scripts are publicly available at https://github.com/sairajkashid-prog/llm-agent-ipi-defense. We measured Attack Success Rate (ASR, Eq. 5), Benign Task Success (BTS, Eq. 6), FPR (Eq. 7), Precision (Eq. 8), Recall (Eq. 9), and F1 (Eq. 10) [25].")
    add_word_table([
        ["Evaluation Set / Method", "Prec. (%)", "Recall (%)", "F1 (%)", "FPR (%)"],
        ["Held-out Prompt Split (Classifier)", "100.0", "95.2", "97.6", "0.0"],
        ["Resume PDFs (Classifier Only)", "96.8", "75.0", "84.5", "5.0"],
        ["Resume PDFs (Full Layer 1)", "97.3", "90.0", "93.5", "5.0"],
    ], "TABLE V. LAYER 1 DETECTION METRICS ON HELD-OUT PROMPTS VS. RESUME PDFS.")

    fig3_path = os.path.join(FIGURES_DIR, "fig3_detection_by_method.png")
    if os.path.exists(fig3_path):
        p_img3 = d.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.add_run().add_picture(fig3_path, width=Inches(3.2))
        add_html_like_para("Fig. 2. Detection rate by hiding method for Classifier Only vs. Full Layer 1.", align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8)

    add_sub_heading("B. Ablation Across the Six Setups")
    add_body("Table VI and Fig. 3 report the results across all six setups. Without defense, overall ASR is 82.5% (78.3% Ranking ASR, 88.2% Data ASR). Layer 1 alone drops overall ASR to 8.3%, Layer 2 alone reduces Ranking ASR to 0.0% via Eq. (3), and Layers 3 and 4 eliminate data exfiltration (0.0% Data ASR). Enabling all four layers reduces both Ranking ASR and Data ASR to 0.0% while maintaining 95.0% BTS.")
    add_word_table([
        ["Setup", "Rank ASR (%)", "Data ASR (%)", "Overall ASR (%)", "BTS (%)", "FPR (%)"],
        ["No defense", "78.3", "88.2", "82.5 +/- 7.1", "100.0", "0.0"],
        ["Layer 1 only", "5.8", "11.8", "8.3 +/- 1.2", "95.0", "5.0"],
        ["Layer 2 only", "0.0", "9.8", "4.2 +/- 2.4", "100.0", "0.0"],
        ["Layer 3 only", "84.1", "0.0", "48.3 +/- 1.2", "100.0", "0.0"],
        ["Layer 4 only", "79.7", "0.0", "45.8 +/- 3.1", "100.0", "0.0"],
        ["All layers", "0.0", "0.0", "0.0 +/- 0.0", "95.0", "5.0"],
    ], "TABLE VI. EXPERIMENTAL RESULTS ACROSS THE SIX TEST SETUPS.")

    fig2_path = os.path.join(FIGURES_DIR, "fig2_asr_bts_setups.png")
    if os.path.exists(fig2_path):
        p_img2 = d.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(fig2_path, width=Inches(3.2))
        add_html_like_para("Fig. 3. Ranking ASR, Data Exfiltration ASR, and BTS across the six setups.", align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8)

    add_sec_heading("VII. DISCUSSION AND LIMITATIONS")
    add_body("Our findings show that text detection and action controls complement each other. Layers 3 and 4 cannot stop ranking attacks alone, while Layer 1 can miss subtle reworded sentences (90.0% recall) and flagged one clean resume with security project terms (5.0% FPR). Image-based scanned resumes and the 2x inference cost of the with-and-without check remain practical limitations.")

    add_sec_heading("VIII. CONCLUSION")
    add_body("We presented and tested a four-layer defense against indirect prompt injection in resume PDFs. Across 60 synthetic resumes, combining hidden-text inspection, untrusted-data rank verification, tool least privilege, and email domain filtering reduced overall attack success from 82.5% to 0.0% with 95.0% benign task success.")

    add_sec_heading("REFERENCES")
    for ref in REFERENCES_LIST:
        clean_ref = ref.replace("<i>", "").replace("</i>", "")
        add_html_like_para(clean_ref, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=8, space_after=2)

    d.save(docx_path)
    print(f"Built editable Word document at {docx_path}")


if __name__ == "__main__":
    os.makedirs(PAPER_DIR, exist_ok=True)
    pdf_out = os.path.join(PAPER_DIR, "LLM_Agent_IPI_Research_Paper_Complete.pdf")
    docx_out = os.path.join(PAPER_DIR, "LLM_Agent_IPI_Research_Paper_Complete.docx")
    build_pdf(pdf_out)
    build_docx(docx_out)
    shutil.copy(pdf_out, "/home/user/LLM_Agent_IPI_Research_Paper_Complete.pdf")
    shutil.copy(docx_out, "/home/user/LLM_Agent_IPI_Research_Paper_Complete.docx")
