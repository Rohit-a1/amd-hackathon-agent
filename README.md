# Hybrid Token-Efficient Routing Agent

🚀 **Submission for AMD Developer Hackathon: ACT II - Track 1**

This project is an AI routing agent designed to autonomously complete a variety of natural language tasks while maximizing efficiency and minimizing API token costs. 

## 🧠 The Concept (Smart Routing)
Enterprises want to control AI spend without sacrificing user experience. Not every task needs a premium proprietary model. This agent acts as a **smart router**:
1. **Zero-Token Local Routing:** The agent analyzes the complexity of incoming tasks locally using heuristic/regex patterns. If a task is simple (e.g., basic classification or sentiment analysis), it routes it efficiently.
2. **Dynamic Model Selection:** It dynamically chooses the most cost-effective Fireworks AI model (like an 8B model for simple reasoning and a 70B/complex model for heavy coding/math).
3. **Fluff Reduction:** The agent strips out "conversational fluff" to reduce the number of output tokens, fulfilling tasks exactly as asked.

## 🛠️ Tech Stack
- **Python 3.10**
- **Fireworks AI APIs** (Compatible with MiniMax, Kimi K, and Llama 3.1 models)
- **Docker** (Containerized for standardized evaluation)

## 📦 Running the Agent
The agent reads from `/input/tasks.json` and writes evaluations to `/output/results.json`. It is packaged into a lightweight Docker image compliant with the hackathon's scoring environment (4GB RAM, 2 vCPU).

```bash
# To run locally via Docker
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output rohit098a1/amd-hackathon-agent:latest
```

## 🏆 Hackathon Goals Achieved
- ✅ Reads tasks from `/input/tasks.json` & outputs `/output/results.json`
- ✅ Dynamic environment variable integration (`FIREWORKS_API_KEY`, `ALLOWED_MODELS`)
- ✅ Packaged in an ultra-lightweight Docker image (`linux/amd64`)
- ✅ Smart token routing logic to maximize cost-efficiency without losing accuracy.
