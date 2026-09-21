from app.schemas.report import Financials, KeyPerson, ReportData

_MOCK_DATA: dict[str, ReportData] = {
    "microsoft": ReportData(
        overview=(
            "Microsoft Corporation is a global technology company headquartered in Redmond, "
            "Washington. It develops, licenses, and supports software, services, devices, and "
            "solutions across cloud computing, productivity, and gaming."
        ),
        key_people=[
            KeyPerson(name="Satya Nadella", title="Chairman & CEO"),
            KeyPerson(name="Amy Hood", title="Executive Vice President & CFO"),
            KeyPerson(name="Brad Smith", title="Vice Chair & President"),
        ],
        news=[
            "Microsoft expands Azure AI infrastructure with new data center regions across Europe and Asia.",
            "Copilot integration deepens across Microsoft 365 suite, driving enterprise adoption.",
            "Microsoft and OpenAI extend partnership with multi-year investment commitment.",
        ],
        financials=Financials(
            revenue="$245.1B (FY2024)",
            employee_count="228,000+",
            market_cap="~$3.1T",
            yoy_growth="16%",
        ),
        risks=[
            "Intense competition in cloud from AWS and Google Cloud.",
            "Regulatory scrutiny over AI products and acquisitions in the EU and US.",
            "Cybersecurity threats targeting enterprise customers.",
        ],
    ),
    "google": ReportData(
        overview=(
            "Alphabet Inc. (Google) is a multinational technology conglomerate headquartered in "
            "Mountain View, California. Its core business is online advertising, complemented by "
            "cloud computing, hardware, and AI research through Google DeepMind."
        ),
        key_people=[
            KeyPerson(name="Sundar Pichai", title="CEO, Alphabet & Google"),
            KeyPerson(name="Ruth Porat", title="SVP & Chief Investment Officer"),
            KeyPerson(name="Demis Hassabis", title="CEO, Google DeepMind"),
        ],
        news=[
            "Google launches Gemini Ultra across Workspace products for enterprise customers.",
            "Alphabet reports strong Q3 2024 results driven by Search and YouTube ad revenue.",
            "Google Cloud surpasses $10B quarterly revenue milestone for the first time.",
        ],
        financials=Financials(
            revenue="$307.4B (FY2024)",
            employee_count="181,000+",
            market_cap="~$2.1T",
            yoy_growth="14%",
        ),
        risks=[
            "Antitrust rulings in the US and EU threatening Search distribution agreements.",
            "AI-generated search results risk cannibalizing core advertising revenue.",
            "Increasing competition in cloud AI from Microsoft Azure and AWS.",
        ],
    ),
    "amazon": ReportData(
        overview=(
            "Amazon.com, Inc. is a multinational technology and e-commerce company headquartered "
            "in Seattle, Washington. It operates the world's largest online marketplace, AWS cloud "
            "platform, and a growing advertising and logistics business."
        ),
        key_people=[
            KeyPerson(name="Andy Jassy", title="President & CEO"),
            KeyPerson(name="Brian Olsavsky", title="SVP & CFO"),
            KeyPerson(name="Adam Selipsky", title="CEO, Amazon Web Services"),
        ],
        news=[
            "AWS announces new generative AI services including Amazon Bedrock enhancements.",
            "Amazon expands same-day delivery network to 20 additional US metro areas.",
            "Amazon advertising revenue grows 19% year-over-year, approaching $50B annually.",
        ],
        financials=Financials(
            revenue="$620.1B (FY2024)",
            employee_count="1,500,000+",
            market_cap="~$2.2T",
            yoy_growth="11%",
        ),
        risks=[
            "Labor relations and unionization efforts across fulfillment centers.",
            "Regulatory pressure on AWS market dominance and data practices.",
            "Thin margins in retail segment vulnerable to macroeconomic downturns.",
        ],
    ),
    "apple": ReportData(
        overview=(
            "Apple Inc. is a multinational technology company headquartered in Cupertino, "
            "California. It designs and sells consumer electronics, software, and services, "
            "with the iPhone as its flagship product alongside Mac, iPad, and Apple Services."
        ),
        key_people=[
            KeyPerson(name="Tim Cook", title="CEO"),
            KeyPerson(name="Luca Maestri", title="SVP & CFO"),
            KeyPerson(name="Craig Federighi", title="SVP Software Engineering"),
        ],
        news=[
            "Apple Intelligence features roll out to iPhone 16 and compatible iPhone 15 Pro models.",
            "App Store faces new compliance requirements under EU Digital Markets Act.",
            "Apple Vision Pro expands to additional international markets.",
        ],
        financials=Financials(
            revenue="$391.0B (FY2024)",
            employee_count="161,000+",
            market_cap="~$3.4T",
            yoy_growth="2%",
        ),
        risks=[
            "Heavy revenue concentration in iPhone segment.",
            "Ongoing EU regulatory actions targeting App Store fees and sideloading.",
            "Supply chain dependency on manufacturing partners in China.",
        ],
    ),
    "salesforce": ReportData(
        overview=(
            "Salesforce, Inc. is a cloud-based software company headquartered in San Francisco, "
            "California. It provides customer relationship management (CRM) software and enterprise "
            "applications focused on sales, service, marketing, and commerce."
        ),
        key_people=[
            KeyPerson(name="Marc Benioff", title="Chair & CEO"),
            KeyPerson(name="Amy Weaver", title="President & CFO"),
            KeyPerson(name="Brian Millham", title="President & COO"),
        ],
        news=[
            "Salesforce launches Agentforce, an autonomous AI agent platform for enterprise workflows.",
            "Salesforce acquires Informatica in a deal valued at approximately $11.3B.",
            "Einstein AI features see accelerated adoption across Sales Cloud and Service Cloud.",
        ],
        financials=Financials(
            revenue="$34.9B (FY2024)",
            employee_count="72,000+",
            market_cap="~$270B",
            yoy_growth="11%",
        ),
        risks=[
            "Intensifying CRM competition from Microsoft Dynamics and emerging AI-native vendors.",
            "Customer spending scrutiny on SaaS subscriptions in a tighter enterprise budget environment.",
            "Integration complexity following multiple large acquisitions.",
        ],
    ),
}

_GENERIC_RESPONSE = ReportData(
    overview="No detailed research data is available for this company at this time.",
    key_people=[],
    news=[],
    financials=Financials(
        revenue=None,
        employee_count=None,
        market_cap=None,
        yoy_growth=None,
    ),
    risks=[],
)


def get_mock_research(company_name: str) -> ReportData:
    normalized = company_name.lower().strip()
    if normalized in _MOCK_DATA:
        return _MOCK_DATA[normalized]
    for key in _MOCK_DATA:
        if key in normalized or normalized in key:
            return _MOCK_DATA[key]
    return _GENERIC_RESPONSE
