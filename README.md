# MirrorOS Final Private API

**Proprietary prediction engine with LLM-powered natural language extraction.**

## Architecture

### LLM Extraction Pipeline
- **Phase 1**: Goal analysis and domain classification
- **Phase 2**: Variable extraction and categorization  
- **Phase 3**: Integer standardization for heuristics

### Core Components
- `lm_extractor.py` - GPT-4o powered natural language processing
- `prediction_engine.py` - Monte carlo heuristics  
- `fred_integration.py` - Federal Reserve economic data
- `server.py` - Clean Flask API server

## Deployment
- AWS ECS Fargate
- Docker containerized
- Auto-scaling production ready

## Security
⚠️ **PRIVATE REPOSITORY** - Contains proprietary algorithms and API keys