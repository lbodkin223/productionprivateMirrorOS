# MirrorOS Final Private API - Claude Manifest

## Project Overview
**MirrorOS Final Private API** - FRED-enhanced LLM-powered prediction service for goal achievement probability analysis.

## Key Components

### Core Files
- `server.py` - Flask API server with prediction endpoint and health checks
- `lm_extractor.py` - Multi-phase LLM extraction system (Claude/GPT-4o)
- `fred_integration.py` - FRED economic data integration for market-aware predictions
- `requirements.txt` - Dependencies including Flask, OpenAI, fredapi, pandas
- `Dockerfile` - Container configuration for AWS ECS deployment
- `buildspec.yml` - AWS CodeBuild configuration for CI/CD

### Environment & Deployment
- **AWS ECS**: Deployed on `mirroros-production-cluster` as `mirroros-private-api-service`
- **API Gateway**: `https://yyk4197cr6.execute-api.us-east-2.amazonaws.com/prod/api`
- **Environment**: Production with FRED API key integration
- **Docker Registry**: ECR repository `423636639115.dkr.ecr.us-east-2.amazonaws.com/mirroros-private-api`

## API Architecture

### Prediction Pipeline
1. **Input**: `POST /predict` with goal and context
2. **Phase 1**: LLM goal analysis and domain classification
3. **Phase 2**: Variable extraction and categorization
4. **Phase 3**: Integer standardization (qualitative → quantitative)
5. **FRED Enhancement**: Economic data adjustment for career/finance goals
6. **Output**: JSON response with probability, confidence intervals, analysis

### Key Features
- Multi-domain support (career, finance, fitness, dating, academic, business, travel)
- Natural language processing with company name normalization
- Economic factor integration via FRED API
- Confidence intervals and risk assessment
- Chain-of-thought explanations

## Development Commands

### Local Testing
```bash
python server.py  # Start local development server
```

### Docker Deployment
```bash
# Manual deployment (when CodeBuild fails)
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 423636639115.dkr.ecr.us-east-2.amazonaws.com
docker build -t mirroros-private-api-latest .
docker tag mirroros-private-api-latest:latest 423636639115.dkr.ecr.us-east-2.amazonaws.com/mirroros-private-api:latest
docker push 423636639115.dkr.ecr.us-east-2.amazonaws.com/mirroros-private-api:latest
aws ecs update-service --cluster mirroros-production-cluster --service mirroros-private-api-service --force-new-deployment
```

### Health Monitoring
```bash
# Check ECS service status
aws ecs describe-services --cluster mirroros-production-cluster --services mirroros-private-api-service

# Check target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-east-2:423636639115:targetgroup/mirroros-private-tg/0cfd102ace7cae3d

# Test API health
curl https://yyk4197cr6.execute-api.us-east-2.amazonaws.com/prod/api/health
```

## Environment Variables
- `OPENAI_API_KEY` - GPT-4o access for LLM extraction
- `ANTHROPIC_API_KEY` - Claude access (primary LLM)
- `FRED_API_KEY=3f4a3669dcef7d3509b06a2bde989993` - Economic data access
- `FLASK_ENV=production` - Runtime environment
- `PORT=8080` - Container port

## Known Issues & Solutions
- **CodeBuild buildspec detection**: Use manual Docker deployment if automated builds fail
- **Company name variations**: Phase 2 LLM extraction handles "OpenAI"/"open ai" normalization
- **Health check failures**: Usually resolved by fresh Docker image deployment