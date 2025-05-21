# 436-Project: Serverless To-Do App
 
This repository demonstrates a full-stack To-Do application with:
- **Backend**: Google Cloud Function `onCreateTodo` (Node.js + Firebase Admin)  
- **Frontend**: React SPA calling the Function  
- **Performance tests**: Locust scripts for load testing  
- **Kubernetes manifests**: Deploy backend & frontend on k8s  
- **VM integration**: MongoDB running on a GCP Compute Engine VM  
 
## Prerequisites
- Node.js v16+ and npm  
- Python 3.8+ and pip  
- Google Cloud SDK (`gcloud`) installed & authenticated  
- A GCP project with billing enabled  
- Docker & kubectl (for k8s steps)  
 
## Quickstart
### 1. Clone & configure  
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd 436-project
gcloud auth login
gcloud config set project <YOUR_PROJECT_ID>
 
## 2. Backend: Cloud Function
cd functions
npm install
# Local test
npm start                     # serves at http://localhost:8080
# Deploy to GCP
gcloud functions deploy onCreateTodo \
 --gen2 \
 --runtime nodejs20 \
 --trigger-http \
 --allow-unauthenticated \
 --region us-central1
Copy the URL that appears (e.g. https://us-central1-…/onCreateTodo)
 
3. Frontend: React
cd ../todo_frontend
# Create .env with:
# REACT_APP_API=<YOUR_FUNCTION_URL>
npm install
npm start                     # opens at http://localhost:3000
 
4. Kubernetes deployment
cd ../k8s
kubectl apply -f namespace.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
Verify with kubectl get pods,svc -n todo-app
 
5. VM Integration (MongoDB)
Ensure your backend-deployment.yaml uses:
env:
 - name: MONGO_URL
   value: "mongodb://<VM_EXTERNAL_IP>:27017/Todo"
 
and that your VM firewall allows port 27017.
 
6. Performance Testing with Locust
cd ../performance
python3 -m venv .venv
source .venv/bin/activate
pip install locust
# Create locustfile.py (see example in this repo)
locust -f locustfile.py --headless -u 100 -r 10 -t 2m --host http://<BACKEND_HOST>:5001 --csv=report
