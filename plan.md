Create a deliberately vulnerable MCP (Model Context Protocol) security training application for students, developers, AppSec engineers, and security professionals.

The application must be educational, safe to run locally, and designed as a hands-on lab for learning MCP security flaws. It should NOT target real systems, real credentials, production APIs, or external services.

Project goal:
Build a vulnerable MCP-based application that demonstrates common MCP and agentic AI security risks mapped to the OWASP MCP Top 10 and OWASP Top 10 for LLM Applications 2025.

Use references from:
- OWASP MCP Top 10
- OWASP Top 10 for LLM Applications 2025
- MCP security best practices
- Agentic AI security patterns
- Prompt injection, tool poisoning, excessive agency, insecure tool design, secret exposure, unsafe defaults, and context leakage examples

Application requirements:
1. Create a complete working vulnerable MCP app.
2. Include a simple web interface for learners.
3. Include MCP server code and client/agent code.
4. Include intentionally vulnerable tools.
5. Include sample attack scenarios.
6. Include test data only, with fake users, fake tokens, and fake documents.
7. Clearly mark the application as intentionally vulnerable.
8. Do not include real exploit targets, real secrets, or harmful payloads.
9. The vulnerable app and the solution guide must be separate.

Suggested tech stack:
- Python
- FastAPI or Flask for the web interface
- MCP Python SDK / FastMCP
- SQLite or local JSON files for fake data
- Simple frontend using HTML/CSS/JavaScript
- Optional Docker setup for easy local deployment

Create the following structure:

/mcp-vulnerable-lab
  /vulnerable-app
    /mcp_server
    /agent_client
    /web_ui
    /data
    /docs
    README.md
    docker-compose.yml
  /solution-guide
    README.md
    mitigations.md
    secure-code-examples
    detection-rules
    testing-checklists
  /references
    owasp-mapping.md

The vulnerable app should include at least 10 labs:

Lab 1: Prompt Injection Against MCP Tools
- User tricks the agent into ignoring instructions and calling an unsafe tool.
- Map to OWASP LLM01 Prompt Injection and relevant OWASP MCP risk.

Lab 2: Tool Poisoning
- A malicious MCP tool description manipulates the agent into choosing it.
- Demonstrate how tool metadata can influence agent behavior.

Lab 3: Excessive Tool Permissions
- A tool has access to more actions than required.
- Example: read, write, delete, export when only read is needed.

Lab 4: Secret Exposure
- Fake API keys or tokens are stored in config, logs, or tool responses.
- Learners identify how secrets leak through MCP context.

Lab 5: Insecure Authentication and Authorization
- A user can access another fake user’s records through weak checks.

Lab 6: Context Poisoning
- A fake document or tool response injects hidden instructions into the agent context.

Lab 7: Unsafe Tool Execution
- A tool accepts unsafe user-controlled input and performs risky local actions in a sandboxed way.

Lab 8: Insecure Output Handling
- Tool output is trusted and rendered directly in the UI.
- Demonstrate safe, non-harmful HTML/script-style output handling issues.

Lab 9: Insufficient Logging and Monitoring
- Important MCP tool calls are not logged.
- Learners add logging, audit trails, and alerting.

Lab 10: Unsafe Default Configuration
- Debug mode, broad tool access, verbose errors, and permissive CORS are enabled by default.

For each lab, include:
- Learning objective
- OWASP MCP Top 10 mapping
- OWASP LLM Top 10 mapping
- Vulnerable code
- Step-by-step student exercise
- Expected observation
- Hints
- Secure solution in the separate solution-guide folder only
- Defensive checklist
- Optional detection rule or log query

The solution guide must include:
1. Explanation of the vulnerability
2. Why it matters in MCP/agentic AI systems
3. Secure coding fix
4. Before-and-after code snippets
5. Recommended controls:
   - least privilege tools
   - allowlisted tool calls
   - schema validation
   - output encoding
   - secret management
   - human approval gates
   - audit logging
   - rate limiting
   - tool identity verification
   - secure defaults
6. Detection ideas
7. Discussion questions for students

The web interface should include:
- Home page explaining the lab
- List of all 10 vulnerabilities
- Individual lab pages
- “Run vulnerable scenario” button
- Display of agent reasoning summary, tool selected, tool input, and tool output
- Warning banner: “This app is intentionally vulnerable. Use only locally.”
- Instructor mode toggle to show hints
- No solution shown inside the vulnerable app

Add a README with:
- Project overview
- Safety disclaimer
- Setup steps
- How to run locally
- Docker instructions
- Lab flow
- Target audience
- Learning outcomes
- OWASP mappings
- Contribution guide

Important safety constraints:
- Use only fake data.
- Do not connect to real email, GitHub, cloud, filesystem, Slack, Jira, or production APIs.
- Any dangerous behavior must be simulated.
- Command execution examples must be sandboxed or mocked.
- No malware, credential theft, persistence, evasion, or real-world exploitation code.
- The goal is education and defense.

Output expected:
- Complete project code
- Folder structure
- README files
- Vulnerable MCP server
- Agent client
- Web UI
- Fake dataset
- 10 lab modules
- Separate solution guide
- OWASP mapping table
- Instructor notes
- Student exercise sheets
- Optional Docker setup