import json

notebook = {
    'cells': [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '# JPAIS Sovereign Legal AI - Interactive Exploration\n',
                'This notebook interacts directly with your local bare-metal stack:\n',
                '- **Neo4j:** Relational and hierarchical regulatory graph\n',
                '- **Qdrant:** 768-dimensional legal vector collections\n',
                '- **Ollama (Qwen 2.5 3B):** Local GPU inference on Quadro T2000'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# 1. Query Neo4j Knowledge Graph\n',
                'from neo4j import GraphDatabase\n',
                'driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "JpaisLegalGraph2026!"))\n',
                'with driver.session() as session:\n',
                '    result = session.run("""\n',
                '        MATCH (r:Regulation)-[:CONTAINS]->(a:Article)-[:REFERENCES]->(lc:LegalConcept)\n',
                '        RETURN r.title AS reg_title, a.article_number AS art_num, a.content AS content, lc.canonical_name AS concept\n',
                '    """)\n',
                '    for row in result:\n',
                '        print(f"=== {row.get(\'reg_title\')} ===")\n',
                '        print(f"{row.get(\'art_num\')} (Konsep: {row.get(\'concept\')}):")\n',
                '        print(f"  {row.get(\'content\')}")\n',
                'driver.close()'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# 2. Inspect Qdrant Vector Collections & Payload Statistics\n',
                'from qdrant_client import QdrantClient\n',
                'client = QdrantClient(host="127.0.0.1", port=6333)\n',
                'collections = client.get_collections().collections\n',
                'print(f"Total Collections: {len(collections)}")\n',
                'for col in collections:\n',
                '    info = client.get_collection(col.name)\n',
                '    print(f" - {col.name:<25}: {info.points_count} points | Vector Dim: {info.config.params.vectors.size}")'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# 3. Test Local GPU Inference via Ollama\n',
                'import ollama\n',
                'prompt = "Jelaskan mengapa asas kepastian hukum dan keterlacakan (traceability) krusial dalam penerapan AI di sektor peradilan (maksimal 3 butir kalimat):"\n',
                'response = ollama.generate(model="qwen2.5:3b", prompt=prompt, options={"temperature": 0.2})\n',
                'print(response["response"])\n'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# 4. Execute End-to-End Hybrid Search & Grounded Drafting\n',
                'import sys\n',
                'sys.path.append("/home/ai/JPAIS/projects/jpais_core")\n',
                'from pipeline import JPAISCorePipeline\n',
                '\n',
                'pipeline = JPAISCorePipeline()\n',
                'query = "Berapa lama jangka waktu wajib penyimpanan catatan asal-usul data sistem AI pengadilan?"\n',
                'print(pipeline.hybrid_search_and_draft(query))\n',
                'pipeline.close()'
            ]
        }
    ],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3 (ipykernel)',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.14.0'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

with open('/home/ai/JPAIS/notebooks/01_jpais_exploration.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('Successfully generated: /home/ai/JPAIS/notebooks/01_jpais_exploration.ipynb')
