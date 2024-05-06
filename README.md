# Step-1: Build docker image
```bash
docker build -t rest-apis .
```

# Step-2: Checking docker images
```bash
docker images
```

# Step-3: Running the image normal and detached mode
```bash
docker run -p 5989:5000 rest-apis
```

```bash
docker run -dp 5989:5000 rest-apis
```

# Step-4: Checking Running Containers
```bash
docker ps
```

# Step-5: Checking all the containers
```bash
docker ps -a
```

# Step-6: Stopping container
```bash
docker stop "container_id"
```

# Step-7: Resuming container
```bash
docker start "container_id"
```

# Step-8: Restarting container
```bash
docker restart "container_id"
```

# Step-9: Removing container
```bash
docker remove "container_id"
```

# Step-10: Removing images
```bash
docker rmi rest-apis
```

# Step-11: File debug True
```bash
docker run -dp 5958:5000 -w /app -v "%cd%:/app" rest-apis
```

# To fix pip issues

# Step-1:
```bash
python -m ensurepip
```

# Step-2:
```bash
python -m pip install -U pip
```

# Connecting to Microsoft SQL Server

# Step-1:
```bash
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')
```