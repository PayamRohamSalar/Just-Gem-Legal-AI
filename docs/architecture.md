# معماری سیستم دستیار هوشمند حقوقی

## ۱. نمای کلی

[cite_start]معماری این سیستم بر پایه الگوی **Retrieval-Augmented Generation (RAG)** بنا شده است[cite: 78]. این الگو به ما اجازه می‌دهد تا قدرت مدل‌های زبانی بزرگ (LLMs) را با یک پایگاه دانش تخصصی و قابل اعتماد ترکیب کنیم. به جای تکیه بر دانش عمومی و غیرقابل کنترل مدل، سیستم ابتدا اطلاعات مرتبط را از اسناد حقوقی استخراج کرده و سپس از مدل برای تولید یک پاسخ منسجم و مستند بر اساس آن اطلاعات استفاده می‌کند.

[cite_start]این رویکرد تضمین می‌کند که پاسخ‌ها همیشه مبتنی بر منابع معتبر بوده و از "هالوسینیشن" (تولید اطلاعات نادرست) جلوگیری می‌شود[cite: 7].

## ۲. جریان داده (Data Flow)

جریان پردازش یک درخواست در سیستم به صورت زیر است:


<style>#mermaid-1754645291648{font-family:sans-serif;font-size:16px;fill:#333;}#mermaid-1754645291648 .error-icon{fill:#552222;}#mermaid-1754645291648 .error-text{fill:#552222;stroke:#552222;}#mermaid-1754645291648 .edge-thickness-normal{stroke-width:2px;}#mermaid-1754645291648 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1754645291648 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1754645291648 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1754645291648 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1754645291648 .marker{fill:#333333;}#mermaid-1754645291648 .marker.cross{stroke:#333333;}#mermaid-1754645291648 svg{font-family:sans-serif;font-size:16px;}#mermaid-1754645291648 .label{font-family:sans-serif;color:#333;}#mermaid-1754645291648 .label text{fill:#333;}#mermaid-1754645291648 .node rect,#mermaid-1754645291648 .node circle,#mermaid-1754645291648 .node ellipse,#mermaid-1754645291648 .node polygon,#mermaid-1754645291648 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1754645291648 .node .label{text-align:center;}#mermaid-1754645291648 .node.clickable{cursor:pointer;}#mermaid-1754645291648 .arrowheadPath{fill:#333333;}#mermaid-1754645291648 .edgePath .path{stroke:#333333;stroke-width:1.5px;}#mermaid-1754645291648 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1754645291648 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1754645291648 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1754645291648 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1754645291648 .cluster text{fill:#333;}#mermaid-1754645291648 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:sans-serif;font-size:12px;background:hsl(80,100%,96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1754645291648:root{--mermaid-font-family:sans-serif;}#mermaid-1754645291648:root{--mermaid-alt-font-family:sans-serif;}#mermaid-1754645291648 flowchart{fill:apa;}</style>
