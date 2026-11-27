# Hazem Elerefy

AI engineer in Cairo. I work on computer vision, LLM agents and RAG, and I build the service and the interface around the model, not only the model.

AI Engineer at VO for Technology since October 2026. Before that I was a front-end developer and then a data analyst, so the audit trail and the interface get as much of my attention as the training run.

- Portfolio: [hazemelerefy.tech](https://hazemelerefy.tech)
- LinkedIn: [linkedin.com/in/hazemelerefy](https://linkedin.com/in/hazemelerefy)
- Email: hazemelerefy@gmail.com

## Selected work

### DAFEsteel: steel-surface defect detection

<img src="https://raw.githubusercontent.com/hazemelerefey/DAFEsteel/main/figures/06c_Figure5_Comparison_scratches_103.jpg" alt="Scratch detection, stock YOLOv11n on the left and DAFEGate on the right" width="640">

Graduation project, led a six-person team. Python, PyTorch, YOLOv11n, FastAPI, Docker, Gradio.

Hot-rolled steel moves faster than a person can inspect it, and its six defect classes split into two visual families, thin cracks and textured flaws, that one detector cannot serve equally. I designed a gate inside YOLOv11n with an edge-tuned branch and a texture-tuned branch, fused by channel attention and an additive residual that keeps gradients reaching the backbone.

Result: 81.98 mAP@0.5 on a clean 70/20/10 split of NEU-DET, up 2.63 points over a tuned baseline of 79.35 and about six points over the stock model at 75.8. Recall up 3.55 points. 2.69M parameters at 145 FPS.

Shipped as a Dockerized FastAPI service that takes an image and returns boxes with confidences, with a zero-shot guard that rejects images that are not steel. Live demo on [Hugging Face](https://huggingface.co/spaces/hazemelerefy/DAFEsteel).

[Code](https://github.com/hazemelerefey/DAFEsteel)

### Smart Voicemail Router: Egyptian Arabic voicemail triage

<img src="https://raw.githubusercontent.com/hazemelerefey/smart-voicemail-router/master/assets/svr-banner-light.png" alt="Smart Voicemail Router banner" width="720">

Build lead and architect, seven contributors. Whisper, LangGraph, MARBERTv2, FastAPI, React, PostgreSQL, Docker.

Customer care in Egypt runs on dialect-heavy voicemail triaged by hand, and the routing decision cannot be audited. I built a self-hosted pipeline: Whisper large-v3 transcription, a LangGraph gate that verifies and repairs transcripts and escalates the uncertain ones, four MARBERTv2 classifiers for category, urgency, customer state and churn risk, a deterministic priority score, and routing by skill and live capacity.

Result: combined macro-F1 0.7941 against 0.7113 for a TF-IDF baseline, on a consented corpus of 6,522 voicemails with five seeds, and 89.33% routing agreement. Vocal-tone emotion inference was tried and did not separate classes, so urgency comes from text only.

Product: a bilingual console with full RTL, role-based access, audio encrypted at rest, an immutable audit log and live updates. One-command Docker deploy on CPU or GPU, plus a separate dataset audit tool, used to review 5,196 voicemails before training and not part of the product.

[Code](https://github.com/hazemelerefey/smart-voicemail-router)

### AZZAR: AI work orchestrator

<img src="https://raw.githubusercontent.com/hazemelerefey/azzar-agent/master/docs/assets/feature-01-hero.png" alt="AZZAR AI work orchestrator" width="720">

Owner and sole developer, pre-pilot. TypeScript, PostgreSQL, tRPC, multi-provider LLM, Docker.

Most AI products for business are chat windows. You ask, it answers, and the work is still yours. AZZAR is a mission-based orchestrator that works out the skills a mission needs, routes it to a department agent, and returns research and drafts in Egyptian Arabic, Modern Standard Arabic or English, ready to publish after a quick human review.

It picks a model per department with the owner's own keys, tracks cost per task with spend limits, asks for approval before any publishing or sensitive action, and self-hosts. Six apps and about thirty packages in a TypeScript monorepo with its own agent runtime, manager and gateway. First release is the Marketing agent with manual publishing; wider departments follow the pilot.

[Code](https://github.com/hazemelerefey/azzar-agent)

## Skills

- **Computer vision:** PyTorch, YOLO, object detection, model training and evaluation, OpenCV
- **LLM systems:** LangGraph, LangChain, RAG, agent tool calling, Ollama, OpenAI API, schema-constrained output
- **Speech and language:** Whisper, MARBERTv2, Arabic NLP
- **Backend and delivery:** FastAPI, Docker, PostgreSQL, Redis, tRPC, TypeScript, React, Next.js
- **Data:** Pandas, NumPy, SQL, Power BI

## Earlier work

- **NeuroScope:** a browser tool for arranging neural-network layers and exporting PyTorch or TensorFlow code. [Code](https://github.com/hazemelerefey/NeuroScope)
- **JobPulse:** a job-market dashboard comparing demand, recurring skills, salary signals and remote flexibility.
- **Power BI case studies:** global e-commerce sales tracker, healthcare operations dashboard.

## Education

- **Specialized Diploma in Applied AI and Data Analytics**, Digilians, Ministry of Communications and IT, with the Egyptian Military Academy, September 2026. First cohort of a fully funded nine-month national scholarship.
- **LL.B., Commercial and Corporate Law**, Port Said University, June 2024.
- **Nanodegree, Front-End Web Development**, Egypt FWD and Udacity, April 2022.

## Certifications

- Microsoft Certified: Power BI Data Analyst Associate (PL-300), July 2026
- Microsoft Certified: Azure Data Fundamentals (DP-900), November 2026
- AI Agents Fundamentals, Hugging Face, October 2026
- AI Agent Fundamentals with Azure AI Foundry, Microsoft and Coursera, July 2026

## Languages

Arabic: native. English: upper-intermediate (B2).

Open to AI engineering roles and remote work.
