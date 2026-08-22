from pathlib import Path
from html import escape
from datetime import date
import shutil

ROOT = Path(__file__).parent
OUT = ROOT / "public"
DOMAIN = "https://vietchiphub.com"

PAGES = [
    ("", "Vietnam Electronic Components & Factory Supply", "Source IC chips, power modules, industrial boards and factory surplus in Vietnam with traceable RFQ review.", "Vietnam electronics sourcing"),
    ("rfq", "Electronic Components RFQ Vietnam", "Submit part numbers, quantities and target dates for a traceable sourcing review from Vietnam suppliers.", "Submit an RFQ"),
    ("bom-sourcing", "BOM Sourcing Vietnam", "Structured BOM review for factories, EMS teams and procurement buyers sourcing electronic components in Vietnam.", "BOM sourcing"),
    ("components", "Electronic Components in Vietnam", "Browse sourcing categories for semiconductors, modules, connectors and industrial electronic components.", "Component categories"),
    ("components/mcu-dsp", "MCU & DSP Suppliers Vietnam", "Source STM32, NXP, Microchip, TI DSP and other embedded-control components with lot-code review.", "MCU and DSP"),
    ("components/power-modules", "IGBT & Power Modules Vietnam", "Vietnam sourcing support for IGBT, MOSFET, rectifier and inverter power modules.", "Power modules"),
    ("components/industrial-boards", "Industrial Control Boards Vietnam", "Find PLC, CNC, automation, telecom and factory repair boards through a documented inquiry process.", "Industrial boards"),
    ("components/server-parts", "Server Parts & Data Center Hardware Vietnam", "Source CPU, RAM, SSD, RAID, NIC and server boards from Vietnam inventory channels.", "Server parts"),
    ("obsolete-components", "Obsolete Electronic Components Sourcing", "A controlled sourcing path for discontinued and hard-to-find electronic parts, with authenticity checks.", "Obsolete components"),
    ("factory-surplus", "Vietnam Factory Surplus Electronics", "Connect with factories and warehouses holding reels, trays, boards and excess electronic inventory.", "Factory surplus"),
    ("suppliers", "Vietnam Electronics Supplier Network", "Supplier onboarding for factories, distributors, repair shops and inventory owners.", "Supplier network"),
    ("quality", "Component Quality & Traceability", "Our review checklist covers manufacturer, part number, quantity, date code, packaging, photos and test evidence.", "Quality process"),
    ("cities/ho-chi-minh-city", "Electronic Components Ho Chi Minh City", "RFQ and supplier discovery for electronic components and factory inventory in Ho Chi Minh City.", "Ho Chi Minh City"),
    ("cities/hanoi", "Electronic Components Hanoi", "Connect with electronics suppliers, factories and engineering resources in Hanoi.", "Hanoi"),
    ("cities/bac-ninh", "Electronics Suppliers Bac Ninh", "Component sourcing and factory-surplus discovery around Bac Ninh's electronics manufacturing cluster.", "Bac Ninh"),
    ("cities/hai-phong", "Electronics Suppliers Hai Phong", "Source electronic parts and industrial inventory around Hai Phong manufacturing and logistics zones.", "Hai Phong"),
    ("jobs", "Vietnam Electronics Jobs", "A focused registration route for SMT, QC, repair and electronics engineering talent and employers.", "Electronics jobs"),
    ("about", "About VN Electronics Hub", "VN Electronics Hub connects verified buyer demand with Vietnam electronics supply and technical review.", "About the hub"),
    ("contact", "Contact VN Electronics Hub", "Contact the VN Electronics Hub team for RFQs, inventory, suppliers and partnerships.", "Contact"),
]

VI_PAGES = [
    ("", "Nguồn linh kiện điện tử và vật tư nhà máy tại Việt Nam", "Tìm IC, module công suất, bo mạch công nghiệp và hàng tồn kho nhà máy tại Việt Nam qua quy trình RFQ có thể truy xuất.", "Nguồn cung điện tử Việt Nam"),
    ("rfq", "Gửi yêu cầu báo giá linh kiện điện tử", "Gửi mã linh kiện, số lượng và thời hạn để đội ngũ kiểm tra nhu cầu và kết nối nguồn cung phù hợp tại Việt Nam.", "Gửi yêu cầu báo giá"),
    ("bom-sourcing", "Tìm nguồn cung BOM tại Việt Nam", "Rà soát BOM có cấu trúc cho nhà máy, EMS và bộ phận mua hàng tìm linh kiện tại Việt Nam.", "Tìm nguồn cung BOM"),
    ("components", "Linh kiện điện tử tại Việt Nam", "Danh mục nguồn cung bán dẫn, module, đầu nối và linh kiện điện tử công nghiệp.", "Danh mục linh kiện"),
    ("components/mcu-dsp", "Nhà cung cấp MCU và DSP tại Việt Nam", "Tìm nguồn STM32, NXP, Microchip, TI DSP và linh kiện điều khiển nhúng, có kiểm tra mã lô.", "MCU và DSP"),
    ("components/power-modules", "IGBT và module công suất tại Việt Nam", "Hỗ trợ tìm IGBT, MOSFET, bộ chỉnh lưu và module công suất biến tần tại Việt Nam.", "Module công suất"),
    ("components/industrial-boards", "Bo mạch điều khiển công nghiệp tại Việt Nam", "Tìm bo PLC, CNC, tự động hóa, viễn thông và bo sửa chữa nhà máy theo quy trình có hồ sơ.", "Bo mạch công nghiệp"),
    ("components/server-parts", "Linh kiện máy chủ và trung tâm dữ liệu", "Tìm CPU, RAM, SSD, RAID, NIC và bo máy chủ từ các kênh tồn kho tại Việt Nam.", "Linh kiện máy chủ"),
    ("obsolete-components", "Tìm linh kiện điện tử ngừng sản xuất", "Quy trình kiểm soát cho linh kiện hiếm hoặc đã ngừng sản xuất, chú trọng kiểm tra tính xác thực.", "Linh kiện khó tìm"),
    ("factory-surplus", "Hàng tồn kho điện tử nhà máy Việt Nam", "Kết nối với nhà máy và kho có cuộn linh kiện, khay, bo mạch và hàng điện tử dư thừa.", "Hàng tồn kho nhà máy"),
    ("suppliers", "Mạng lưới nhà cung cấp điện tử Việt Nam", "Đăng ký dành cho nhà máy, nhà phân phối, xưởng sửa chữa và chủ sở hữu hàng tồn kho.", "Mạng lưới nhà cung cấp"),
    ("quality", "Chất lượng và truy xuất nguồn gốc linh kiện", "Danh sách kiểm tra gồm hãng, mã linh kiện, số lượng, date code, đóng gói, hình ảnh và bằng chứng thử nghiệm.", "Quy trình chất lượng"),
    ("cities/ho-chi-minh-city", "Linh kiện điện tử tại TP. Hồ Chí Minh", "Tiếp nhận RFQ và tìm nhà cung cấp linh kiện, hàng tồn kho nhà máy tại TP. Hồ Chí Minh.", "TP. Hồ Chí Minh"),
    ("cities/hanoi", "Linh kiện điện tử tại Hà Nội", "Kết nối nhà cung cấp, nhà máy và nguồn lực kỹ thuật điện tử tại Hà Nội.", "Hà Nội"),
    ("cities/bac-ninh", "Nhà cung cấp điện tử tại Bắc Ninh", "Tìm linh kiện và hàng tồn kho quanh cụm sản xuất điện tử Bắc Ninh.", "Bắc Ninh"),
    ("cities/hai-phong", "Nhà cung cấp điện tử tại Hải Phòng", "Tìm linh kiện và hàng công nghiệp quanh các khu sản xuất, logistics Hải Phòng.", "Hải Phòng"),
    ("jobs", "Việc làm điện tử tại Việt Nam", "Kênh đăng ký cho nhân sự SMT, QC, sửa chữa, kỹ sư điện tử và doanh nghiệp tuyển dụng.", "Việc làm điện tử"),
    ("about", "Giới thiệu VN Electronics Hub", "Nền tảng kết nối nhu cầu mua hàng đủ điều kiện với nguồn cung điện tử và quy trình kiểm tra kỹ thuật tại Việt Nam.", "Giới thiệu"),
    ("contact", "Liên hệ VN Electronics Hub", "Liên hệ về RFQ, hàng tồn kho, nhà cung cấp và hợp tác.", "Liên hệ"),
]

ZH_PAGES = [
    ("", "越南电子元器件与工厂供应链", "在越南寻找芯片、功率模块、工业板卡和工厂库存，通过可追溯的询价流程对接供应。", "越南电子供应链"),
    ("rfq", "提交越南电子元器件询价", "提交型号、数量和交期，由团队人工审核需求并匹配越南供应渠道。", "提交询价"),
    ("bom-sourcing", "越南 BOM 配单与采购", "面向工厂、EMS 和采购团队的结构化 BOM 审核与越南供应链对接。", "BOM 配单"),
    ("components", "越南电子元器件分类", "查询半导体、模块、连接器和工业电子元件的越南供应渠道。", "元器件分类"),
    ("components/mcu-dsp", "越南 MCU 与 DSP 供应", "寻找 STM32、NXP、Microchip、TI DSP 等嵌入式控制元件。", "MCU 与 DSP"),
    ("components/power-modules", "越南 IGBT 与功率模块", "寻找 IGBT、MOSFET、整流器及变频器功率模块。", "功率模块"),
    ("components/industrial-boards", "越南工业控制板卡", "寻找 PLC、CNC、自动化、通信及工厂维修板卡。", "工业板卡"),
    ("components/server-parts", "越南服务器与数据中心配件", "寻找 CPU、内存、SSD、RAID、网卡及服务器板卡。", "服务器配件"),
    ("obsolete-components", "停产与难找电子元件", "为停产和紧缺元件提供受控的寻源与真伪证据审核流程。", "停产元件"),
    ("factory-surplus", "越南工厂电子库存", "对接持有卷盘、托盘、板卡和电子呆滞库存的工厂与仓库。", "工厂库存"),
    ("suppliers", "越南电子供应商网络", "面向工厂、分销商、维修企业及库存持有方的供应商入口。", "供应商网络"),
    ("quality", "元器件质量与可追溯性", "核对品牌、型号、数量、批次日期、包装、照片和测试证据。", "质量流程"),
    ("cities/ho-chi-minh-city", "胡志明市电子元器件", "在胡志明市提交询价并寻找元器件和工厂库存供应。", "胡志明市"),
    ("cities/hanoi", "河内电子元器件", "连接河内的电子供应商、工厂与技术资源。", "河内"),
    ("cities/bac-ninh", "北宁电子供应商", "围绕北宁电子制造集群寻找元器件和工厂库存。", "北宁"),
    ("cities/hai-phong", "海防电子供应商", "围绕海防制造业和物流区寻找电子元件与工业库存。", "海防"),
    ("jobs", "越南电子行业招聘", "面向 SMT、QC、维修、电子工程人才及招聘企业的登记入口。", "电子招聘"),
    ("about", "关于 VN Electronics Hub", "连接真实采购需求与越南电子供应链，并保留技术审核和追溯信息。", "关于平台"),
    ("contact", "联系 VN Electronics Hub", "就询价、库存、供应商和合作事宜联系我们。", "联系我们"),
]

CSS = """
:root{--ink:#081a2d;--muted:#5d6b78;--blue:#0757d9;--cyan:#00a8b5;--paper:#f4f7fb;--line:#dce5ef;--white:#fff;--orange:#ffb547}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--white);line-height:1.6}a{color:inherit;text-decoration:none}.wrap{width:min(1160px,calc(100% - 36px));margin:auto}.top{background:#061321;color:#c9d8e8;font-size:.82rem;padding:7px 0}.top .wrap,.nav,.hero-grid,.split,.foot-grid{display:flex;justify-content:space-between;align-items:center;gap:24px}.nav{height:76px}.brand{font-weight:850;font-size:1.28rem;letter-spacing:-.03em}.brand i{color:var(--cyan);font-style:normal}.links{display:flex;gap:22px;font-size:.94rem;font-weight:650}.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 18px;border-radius:10px;background:var(--blue);color:#fff;font-weight:750;border:1px solid var(--blue)}.btn.alt{background:transparent;color:var(--ink);border-color:#b9c8d8}.hero{background:radial-gradient(circle at 78% 18%,#0a63c5 0,#08294d 31%,#061524 72%);color:white;padding:80px 0 68px;overflow:hidden}.hero-grid{align-items:flex-start}.hero-copy{max-width:720px}.eyebrow{color:#77e3ea;text-transform:uppercase;letter-spacing:.13em;font-weight:800;font-size:.76rem}.hero h1{font-size:clamp(2.3rem,5vw,4.7rem);line-height:1.02;letter-spacing:-.055em;margin:16px 0 20px}.hero p{font-size:1.13rem;color:#d5e2ee;max-width:670px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.hero .alt{color:white;border-color:#66809a}.signal{min-width:280px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:18px;padding:24px;backdrop-filter:blur(10px)}.signal b{display:block;font-size:2rem}.signal span{color:#b9ccdf;font-size:.9rem}.trust{border-bottom:1px solid var(--line);padding:17px 0;color:#425366}.trust .wrap{display:flex;gap:28px;flex-wrap:wrap;font-size:.88rem;font-weight:700}section{padding:68px 0}.soft{background:var(--paper)}h2{font-size:clamp(1.8rem,3vw,2.8rem);letter-spacing:-.04em;line-height:1.1;margin:0 0 12px}.lead{color:var(--muted);max-width:720px;margin:0 0 30px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:#fff;border:1px solid var(--line);border-radius:15px;padding:24px;box-shadow:0 9px 30px rgba(11,35,61,.05)}.card .tag{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);font-weight:850}.card h3{font-size:1.18rem;margin:10px 0 6px}.card p{color:var(--muted);font-size:.92rem;margin:0}.card a{display:inline-block;color:var(--blue);font-weight:750;margin-top:15px}.split{align-items:flex-start}.steps{counter-reset:s}.step{position:relative;padding:0 0 26px 52px}.step:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:34px;height:34px;border-radius:9px;background:#e4efff;color:var(--blue);display:grid;place-items:center;font-weight:850}.step h3{margin:0}.step p{margin:4px 0;color:var(--muted)}.panel{background:#0b2744;color:#fff;border-radius:18px;padding:30px;max-width:430px}.panel p{color:#c9d9e8}.check{display:flex;gap:10px;margin:12px 0}.check:before{content:"✓";color:#69e1df;font-weight:900}.faq details{border-top:1px solid var(--line);padding:17px 0}.faq summary{font-weight:800;cursor:pointer}.faq p{color:var(--muted)}.cta{background:linear-gradient(120deg,#0757d9,#008d9b);color:#fff;border-radius:22px;padding:38px;display:flex;align-items:center;justify-content:space-between;gap:30px}.cta h2{max-width:650px}.cta .btn{background:white;color:#064aa4;border-color:white}footer{background:#061321;color:#c1cfdd;padding:48px 0}.foot-grid{align-items:flex-start}.foot-links{display:grid;grid-template-columns:repeat(2,1fr);gap:8px 30px;font-size:.9rem}.legal{margin-top:34px;padding-top:18px;border-top:1px solid #27394b;font-size:.78rem;color:#8295a8}.crumb{font-size:.82rem;color:#6b7c8f;margin-bottom:22px}.pagehero{padding:58px 0;background:linear-gradient(145deg,#eef5ff,#f6fbfc)}.pagehero h1{font-size:clamp(2.2rem,4vw,3.8rem);line-height:1.05;letter-spacing:-.05em;max-width:850px;margin:10px 0 18px}.pagehero p{max-width:740px;color:#516273;font-size:1.08rem}.notice{border-left:4px solid var(--orange);background:#fff9ec;padding:16px 18px;border-radius:5px;color:#5c4a23}.form{display:grid;grid-template-columns:1fr 1fr;gap:14px}.form input,.form textarea,.form select{width:100%;padding:13px;border:1px solid #b8c6d5;border-radius:8px;font:inherit}.form textarea,.full{grid-column:1/-1}.small{font-size:.79rem;color:var(--muted)}@media(max-width:820px){.links{display:none}.hero-grid,.split,.foot-grid,.cta{flex-direction:column}.signal{width:100%}.grid{grid-template-columns:1fr}.hero{padding-top:54px}.form{grid-template-columns:1fr}.form>*{grid-column:1}.nav{height:66px}section{padding:50px 0}}
"""

CARDS = [
    ("MCU / DSP", "STM32, NXP, Microchip and TI embedded-control sourcing.", "/components/mcu-dsp/"),
    ("Power Modules", "IGBT, MOSFET and inverter power components.", "/components/power-modules/"),
    ("Industrial Boards", "PLC, CNC, telecom and automation repair boards.", "/components/industrial-boards/"),
    ("Server Parts", "CPU, RAM, SSD, RAID, NIC and server boards.", "/components/server-parts/"),
    ("Factory Surplus", "Reels, trays, boxed components and excess boards.", "/factory-surplus/"),
    ("Obsolete Parts", "Hard-to-find parts with a controlled review path.", "/obsolete-components/"),
]

def nav():
    return '<div class="top"><div class="wrap"><span>Vietnam electronics supply-chain platform</span><span>Buyer RFQ · Supplier inventory · Factory services</span></div></div><header class="wrap nav"><a class="brand" href="/"><i>VN</i> Electronics Hub</a><nav class="links"><a href="/components/">Components</a><a href="/bom-sourcing/">BOM Sourcing</a><a href="/factory-surplus/">Surplus</a><a href="/suppliers/">Suppliers</a><a href="/quality/">Quality</a></nav><a class="btn" href="/rfq/">Submit RFQ</a></header>'

def footer():
    return f'''<footer><div class="wrap"><div class="foot-grid"><div><div class="brand"><i>VN</i> Electronics Hub</div><p>Connecting qualified demand with Vietnam's electronics supply chain.</p></div><div class="foot-links"><a href="/rfq/">Submit RFQ</a><a href="/suppliers/">List inventory</a><a href="/quality/">Quality process</a><a href="/contact/">Contact</a><a href="/about/">About</a><a href="/jobs/">Jobs</a></div></div><div class="legal">© {date.today().year} VN Electronics Hub. Independent B2B sourcing platform. Product availability and authenticity require supplier documentation and buyer verification.</div></div></footer>'''

def shell(title, desc, path, body, schema="WebPage"):
    canonical = DOMAIN + ("/" if not path else f"/{path}/")
    data = '{"@context":"https://schema.org","@type":"%s","name":"%s","url":"%s","description":"%s","isPartOf":{"@type":"WebSite","name":"VN Electronics Hub","url":"%s"}}' % (schema, escape(title), canonical, escape(desc), DOMAIN)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | VN Electronics Hub</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{data}</script><link rel="stylesheet" href="/assets/site.css"></head><body>{nav()}{body}{footer()}</body></html>'''

def card_grid():
    return '<div class="grid">' + ''.join(f'<article class="card"><span class="tag">Sourcing lane</span><h3>{t}</h3><p>{d}</p><a href="{u}">View category →</a></article>' for t,d,u in CARDS) + '</div>'

def inquiry_form():
    return '''<form class="form" name="component-rfq" method="POST" data-netlify="true" action="/thank-you/"><input type="hidden" name="form-name" value="component-rfq"><input name="company" aria-label="Company" placeholder="Company name" required><input name="contact" aria-label="Contact" placeholder="Email / WhatsApp / Zalo" required><input name="part_number" aria-label="Part number" placeholder="Part number / BOM title" required><input name="quantity" aria-label="Quantity" placeholder="Quantity"><select name="urgency" aria-label="Urgency"><option>Required date</option><option>Within 7 days</option><option>Within 30 days</option><option>Planning / forecast</option></select><select name="condition" aria-label="Condition"><option>Required condition</option><option>New and original</option><option>Tested / refurbished acceptable</option><option>Open to alternatives</option></select><textarea name="details" rows="5" placeholder="Manufacturer, package, date code, target price, delivery city and documentation requirements"></textarea><button class="btn full" type="submit">Send RFQ for manual review</button><p class="small full">No automatic quote is issued. A reviewer checks the request, supplier evidence and commercial fit before follow-up.</p></form>'''

def home():
    body = '''<main><section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><div class="eyebrow">Vietnam electronics sourcing</div><h1>Find components and factory supply with a traceable RFQ.</h1><p>For factories, EMS teams, repair businesses and procurement buyers sourcing ICs, power modules, industrial boards, server parts and verified surplus in Vietnam.</p><div class="actions"><a class="btn" href="/rfq/">Submit part numbers</a><a class="btn alt" href="/suppliers/">List supplier inventory</a></div></div><aside class="signal"><span>Structured intake for</span><b>Part numbers</b><span>Manufacturer · Quantity · Date code · Packaging · Delivery</span><hr><span>Human review before supplier introduction</span></aside></div></section><div class="trust"><div class="wrap"><span>✓ Evidence-first sourcing</span><span>✓ Vietnam supplier discovery</span><span>✓ BOM & alternative review</span><span>✓ Buyer-controlled approval</span></div></div><section class="soft"><div class="wrap"><h2>Focused sourcing lanes</h2><p class="lead">Start with a category or send a structured RFQ. Every inquiry retains the original manufacturer and part-number requirements.</p>''' + card_grid() + '''</div></section><section><div class="wrap split"><div><h2>A clearer path from requirement to supplier</h2><p class="lead">The platform organizes evidence before introducing inventory, reducing incomplete quotes and mismatched parts.</p><div class="steps"><div class="step"><h3>Submit requirement</h3><p>Part number, manufacturer, quantity, package, target date and destination.</p></div><div class="step"><h3>Review evidence</h3><p>Photos, labels, lot/date code, packaging, test reports and supplier identity where available.</p></div><div class="step"><h3>Confirm commercial fit</h3><p>Buyer approves condition, documentation, inspection and transaction terms.</p></div></div></div><aside class="panel"><span class="eyebrow">Risk controls</span><h2>Not a blind parts marketplace.</h2><div class="check">No claim of authenticity without evidence</div><div class="check">No automatic substitute approval</div><div class="check">No hidden change to buyer specifications</div><div class="check">Independent inspection encouraged</div></aside></div></section><section class="soft"><div class="wrap"><h2>Manufacturing regions</h2><p class="lead">Use regional pages to identify the right electronics cluster and logistics route.</p><div class="grid"><article class="card"><h3>Bac Ninh</h3><p>Electronics manufacturing, suppliers and factory inventory.</p><a href="/cities/bac-ninh/">Explore Bac Ninh →</a></article><article class="card"><h3>Hanoi</h3><p>Engineering, distribution and northern Vietnam procurement.</p><a href="/cities/hanoi/">Explore Hanoi →</a></article><article class="card"><h3>Ho Chi Minh City</h3><p>Distribution, repair, trading and southern industrial demand.</p><a href="/cities/ho-chi-minh-city/">Explore HCMC →</a></article></div></div></section><section><div class="wrap cta"><h2>Have a part number, BOM or factory inventory list?</h2><a class="btn" href="/rfq/">Start a structured review</a></div></section></main>'''
    return shell(PAGES[0][1], PAGES[0][2], "", body, "WebSite")

def detail(path,title,desc,heading):
    if path == "rfq":
        content = f'''<section class="pagehero"><div class="wrap"><div class="crumb"><a href="/">Home</a> / RFQ</div><span class="eyebrow">Buyer intake</span><h1>{heading}</h1><p>{desc}</p></div></section><section><div class="wrap split"><div style="flex:1"><h2>Send a complete requirement</h2>{inquiry_form()}</div><aside class="panel"><h2>Include when available</h2><div class="check">Exact manufacturer and part number</div><div class="check">Package, grade and acceptable date code</div><div class="check">Quantity and target delivery date</div><div class="check">Destination and inspection needs</div></aside></div></section>'''
    else:
        related = card_grid() if path in ("components","bom-sourcing") else '''<div class="grid"><article class="card"><h3>Requirement capture</h3><p>Exact specifications stay attached to the inquiry.</p></article><article class="card"><h3>Evidence review</h3><p>Supplier claims are separated from verified documents.</p></article><article class="card"><h3>Buyer approval</h3><p>Substitutions and condition changes require buyer approval.</p></article></div>'''
        content = f'''<section class="pagehero"><div class="wrap"><div class="crumb"><a href="/">Home</a> / {escape(heading)}</div><span class="eyebrow">Vietnam supply chain</span><h1>{escape(title)}</h1><p>{escape(desc)}</p><div class="actions"><a class="btn" href="/rfq/">Submit requirement</a><a class="btn alt" href="/quality/">Review quality process</a></div></div></section><section><div class="wrap"><h2>{escape(heading)} sourcing workflow</h2><p class="lead">VN Electronics Hub is an inquiry and supplier-discovery platform. Availability, provenance and commercial terms must be confirmed for each transaction.</p>{related}</div></section><section class="soft"><div class="wrap split"><div><h2>What buyers should provide</h2><p class="lead">Manufacturer, exact part number, package, grade, quantity, acceptable date code, required documents, delivery city and target date.</p><p class="notice">Technical and compatibility information is for sourcing support only. Buyers remain responsible for engineering validation, inspection and final approval.</p></div><aside class="panel"><h2>Need a fast review?</h2><p>Send the highest-priority lines first. The team can structure the rest of the BOM after confirming fit.</p><a class="btn" href="/rfq/">Open RFQ form</a></aside></div></section><section><div class="wrap faq"><h2>Common questions</h2><details><summary>Does the platform guarantee authenticity?</summary><p>No. We organize supplier evidence and recommend appropriate inspection; final acceptance belongs to the buyer.</p></details><details><summary>Can alternative parts be proposed?</summary><p>Yes, but alternatives are clearly marked and require engineering and buyer approval.</p></details><details><summary>Can suppliers submit stock?</summary><p>Yes. Inventory owners can use the supplier route and provide labels, quantities, condition and location.</p></details></div></section>'''
    return shell(title,desc,path,"<main>"+content+"</main>")

def localized_page(lang, prefix, path, title, desc, heading):
    vi = lang == "vi"
    labels = ({
        "supply": "Chuỗi cung ứng điện tử Việt Nam", "home": "Trang chủ", "components": "Linh kiện",
        "bom": "Tìm nguồn BOM", "surplus": "Hàng tồn kho", "suppliers": "Nhà cung cấp", "quality": "Chất lượng",
        "rfq": "Gửi RFQ", "intro": "Kết nối nhu cầu mua hàng thực với nguồn cung Việt Nam bằng quy trình có hồ sơ và kiểm tra bằng chứng.",
        "start": "Gửi yêu cầu", "process": "Xem quy trình chất lượng", "need": "Thông tin người mua cần cung cấp",
        "needtext": "Hãng sản xuất, mã linh kiện chính xác, quy cách đóng gói, cấp chất lượng, số lượng, date code chấp nhận được, chứng từ, địa điểm giao hàng và thời hạn.",
        "warning": "Thông tin kỹ thuật chỉ hỗ trợ tìm nguồn. Người mua chịu trách nhiệm xác nhận kỹ thuật, kiểm định và phê duyệt cuối cùng.",
        "steps": [("Ghi nhận yêu cầu", "Giữ nguyên mã linh kiện, thông số, số lượng và thời hạn."), ("Kiểm tra bằng chứng", "Tách rõ tuyên bố của nhà cung cấp với tài liệu đã kiểm tra."), ("Người mua phê duyệt", "Mọi thay thế hoặc thay đổi tình trạng hàng phải được chấp thuận.")],
        "formtitle": "Gửi yêu cầu đầy đủ", "company": "Tên công ty", "contact": "Email / WhatsApp / Zalo", "part": "Mã linh kiện / tên BOM", "qty": "Số lượng", "details": "Hãng, quy cách, date code, giá mục tiêu, nơi giao hàng và yêu cầu chứng từ", "send": "Gửi RFQ để kiểm tra thủ công",
        "disclaimer": "Không phát hành báo giá tự động. Đội ngũ sẽ kiểm tra yêu cầu và bằng chứng trước khi phản hồi.",
    } if vi else {
        "supply": "越南电子供应链", "home": "首页", "components": "元器件", "bom": "BOM 配单", "surplus": "工厂库存", "suppliers": "供应商", "quality": "质量流程",
        "rfq": "提交询价", "intro": "以保留原始需求和供应证据的方式，对接真实采购需求与越南电子供应链。",
        "start": "提交需求", "process": "查看质量流程", "need": "采购方需要提供", "needtext": "品牌、准确型号、封装、等级、数量、可接受批次、所需文件、交付城市和目标日期。",
        "warning": "技术与兼容信息仅用于寻源支持。采购方负责工程验证、检验和最终批准。",
        "steps": [("记录原始需求", "保留准确型号、规格、数量和交期。"), ("审核供应证据", "区分供应商声明与已经核验的文件。"), ("采购方确认", "替代料及状态变化必须获得采购方批准。")],
        "formtitle": "提交完整采购需求", "company": "公司名称", "contact": "邮箱 / WhatsApp / 微信", "part": "型号 / BOM 名称", "qty": "数量", "details": "品牌、封装、批次、目标价、交付地点和文件要求", "send": "提交人工审核", "disclaimer": "平台不会自动报价。团队会先核对需求、供应证据与合作条件。",
    })
    route = (f"/{prefix}/" if not path else f"/{prefix}/{path}/") if prefix else ("/" if not path else f"/{path}/")
    canonical = DOMAIN + route
    alternates = f'<link rel="alternate" hreflang="vi" href="{DOMAIN}/{path + "/" if path else ""}"><link rel="alternate" hreflang="en" href="{DOMAIN}/en/{path + "/" if path else ""}"><link rel="alternate" hreflang="zh-Hans" href="{DOMAIN}/zh/{path + "/" if path else ""}"><link rel="alternate" hreflang="x-default" href="{DOMAIN}/{path + "/" if path else ""}">'
    base = f"/{prefix}" if prefix else ""
    language = '<div class="top"><div class="wrap"><span>'+labels["supply"]+'</span><span><a href="'+('/'+path+'/' if path else '/')+'">VI</a> · <a href="/en/'+(path+'/' if path else '')+'">EN</a> · <a href="/zh/'+(path+'/' if path else '')+'">中文</a></span></div></div>'
    header = f'''{language}<header class="wrap nav"><a class="brand" href="{base}/"><i>VN</i> Electronics Hub</a><nav class="links"><a href="{base}/components/">{labels['components']}</a><a href="{base}/bom-sourcing/">{labels['bom']}</a><a href="{base}/factory-surplus/">{labels['surplus']}</a><a href="{base}/suppliers/">{labels['suppliers']}</a><a href="{base}/quality/">{labels['quality']}</a></nav><a class="btn" href="{base}/rfq/">{labels['rfq']}</a></header>'''
    if path == "rfq":
        core = f'''<section class="pagehero"><div class="wrap"><div class="crumb"><a href="{base}/">{labels['home']}</a> / RFQ</div><span class="eyebrow">{labels['supply']}</span><h1>{escape(title)}</h1><p>{escape(desc)}</p></div></section><section><div class="wrap"><h2>{labels['formtitle']}</h2><form class="form" name="component-rfq-{lang}" method="POST" data-netlify="true" action="{base}/thank-you/"><input type="hidden" name="form-name" value="component-rfq-{lang}"><input name="company" placeholder="{labels['company']}" required><input name="contact" placeholder="{labels['contact']}" required><input name="part_number" placeholder="{labels['part']}" required><input name="quantity" placeholder="{labels['qty']}"><textarea class="full" name="details" rows="5" placeholder="{labels['details']}"></textarea><button class="btn full" type="submit">{labels['send']}</button><p class="small full">{labels['disclaimer']}</p></form></div></section>'''
    elif not path:
        core = f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><div class="eyebrow">{labels['supply']}</div><h1>{escape(title)}</h1><p>{escape(desc)}</p><div class="actions"><a class="btn" href="{base}/rfq/">{labels['start']}</a><a class="btn alt" href="{base}/suppliers/">{labels['suppliers']}</a></div></div><aside class="signal"><span>RFQ</span><b>BOM · IC · MCU</b><span>IGBT · Bo mạch / 板卡 · Linh kiện / 元器件</span></aside></div></section><section class="soft"><div class="wrap"><h2>{labels['components']}</h2><p class="lead">{labels['intro']}</p><div class="grid">{''.join(f'<article class="card"><h3>{escape(t)}</h3><p>{escape(d)}</p><a href="{base}/{p}/">{labels["start"]} →</a></article>' for p,t,d,h in (VI_PAGES if vi else ZH_PAGES)[4:10])}</div></div></section><section><div class="wrap cta"><h2>{labels['intro']}</h2><a class="btn" href="{base}/rfq/">{labels['rfq']}</a></div></section>'''
    else:
        core = f'''<section class="pagehero"><div class="wrap"><div class="crumb"><a href="{base}/">{labels['home']}</a> / {escape(heading)}</div><span class="eyebrow">{labels['supply']}</span><h1>{escape(title)}</h1><p>{escape(desc)}</p><div class="actions"><a class="btn" href="{base}/rfq/">{labels['start']}</a><a class="btn alt" href="{base}/quality/">{labels['process']}</a></div></div></section><section><div class="wrap"><h2>{escape(heading)}</h2><p class="lead">{labels['intro']}</p><div class="grid">{''.join(f'<article class="card"><h3>{a}</h3><p>{b}</p></article>' for a,b in labels['steps'])}</div></div></section><section class="soft"><div class="wrap"><h2>{labels['need']}</h2><p class="lead">{labels['needtext']}</p><p class="notice">{labels['warning']}</p></div></section>'''
    schema = '{"@context":"https://schema.org","@type":"WebPage","inLanguage":"%s","name":"%s","url":"%s","description":"%s"}' % (lang, escape(title), canonical, escape(desc))
    foot = f'''<footer><div class="wrap"><div class="brand"><i>VN</i> Electronics Hub</div><p>{labels['intro']}</p><div class="legal">© {date.today().year} VN Electronics Hub</div></div></footer>'''
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | VN Electronics Hub</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{canonical}"><script type="application/ld+json">{schema}</script><link rel="stylesheet" href="/assets/site.css"></head><body>{header}<main>{core}</main>{foot}</body></html>'''

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT/"assets").mkdir(parents=True,exist_ok=True)
    (OUT/"assets/site.css").write_text(CSS,encoding="utf-8")
    for path,title,desc,heading in PAGES:
        target = OUT/"en" if not path else OUT/"en"/path
        target.mkdir(parents=True,exist_ok=True)
        english = home() if not path else detail(path,title,desc,heading)
        original_url = DOMAIN + ('/' if not path else f'/{path}/')
        english_url = DOMAIN + ('/en/' if not path else f'/en/{path}/')
        english = english.replace(original_url, english_url)
        english = english.replace('href="/', 'href="/en/')
        english = english.replace('href="/en/assets/', 'href="/assets/')
        english = english.replace('action="/en/thank-you/"', 'action="/en/thank-you/"')
        english = english.replace('<body>', '<body><div class="top"><div class="wrap"><span>Vietnam electronics supply chain</span><span><a href="/'+(path+'/' if path else '')+'">VI</a> · <a href="/en/'+(path+'/' if path else '')+'">EN</a> · <a href="/zh/'+(path+'/' if path else '')+'">中文</a></span></div></div>')
        (target/"index.html").write_text(english,encoding="utf-8")
    for lang, prefix, pages in (("vi", "", VI_PAGES), ("zh", "zh", ZH_PAGES)):
        for path,title,desc,heading in pages:
            target = OUT if not path and not prefix else (OUT/prefix if not path else OUT/prefix/path) if prefix else OUT/path
            target.mkdir(parents=True,exist_ok=True)
            (target/"index.html").write_text(localized_page(lang,prefix,path,title,desc,heading),encoding="utf-8")
    thanks = OUT/"thank-you"; thanks.mkdir(exist_ok=True)
    (thanks/"index.html").write_text('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Đã nhận RFQ | VN Electronics Hub</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css"></head><body><main><section class="pagehero"><div class="wrap"><h1>Đã nhận yêu cầu báo giá</h1><p>Yêu cầu của bạn đã vào hàng chờ kiểm tra thủ công.</p><a class="btn" href="/">Về trang chủ</a></div></section></main></body></html>',encoding="utf-8")
    for prefix, lang, title, message in (("en","en","RFQ received","Your request is queued for manual review."),("zh","zh","询价已收到","您的需求已进入人工审核队列。")):
        t = OUT/prefix/"thank-you"; t.mkdir(parents=True,exist_ok=True)
        (t/"index.html").write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | VN Electronics Hub</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css"></head><body><main><section class="pagehero"><div class="wrap"><h1>{title}</h1><p>{message}</p><a class="btn" href="/{prefix}/">VN Electronics Hub</a></div></section></main></body></html>',encoding="utf-8")
    urls = [DOMAIN+('/' if not p else f'/{p}/') for p,*_ in VI_PAGES]
    urls += [DOMAIN+f'/{prefix}/'+('' if not p else f'{p}/') for prefix,pages in (("en",PAGES),("zh",ZH_PAGES)) for p,*_ in pages]
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n' for u in urls)+'</urlset>\n',encoding="utf-8")
    (OUT/"robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n',encoding="utf-8")
    (ROOT/"netlify.toml").write_text('[build]\n  publish = "public"\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Content-Type-Options = "nosniff"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n    Permissions-Policy = "camera=(), microphone=(), geolocation=()"\n',encoding="utf-8")

if __name__ == "__main__": build()
