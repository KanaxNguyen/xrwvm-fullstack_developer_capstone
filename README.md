# xrwvm-fullstack_developer_capstone

## Best Cars Dealership Reviews

Best Cars is a Django and React full-stack capstone application for browsing
dealerships across the United States, filtering dealers by state, reading
sentiment-labelled customer reviews, registering and signing in, and posting a
vehicle purchase review.

The repository includes a self-contained JSON fallback for dealer and review
data, a Django admin interface for car makes and models, a React frontend,
automated tests, and a GitHub Actions workflow.

### Run locally

```bash
cd server
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
cd frontend && npm ci && npm run build && cd ..
python manage.py runserver
```

Demo administrator: `root` / `RootPass123!`
