# Stripe Integration Test 2023

Uses API version 2022-11-15

## Setup

1. Clone repository
2. Set up environment

```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```
pip3 install -r requirements.txt
```

4. Set up a Stripe account with the following product, price, and coupon:

| Type    | ID                  |
| ------- | ------------------- |
| Product | prod_N8GtP4kfDmf5Wn |
| Price   | sku_GOdUWWauNOfRgU  |
| Coupon  | 2020LOVE            |

5. Set up project settings proper stripe API keys

```
cd src
cp env.example .env
nano -w src/.env
```

6. Migrate database

```
python3 manage.py makemigrations
python3 manage.py migrate
```

7. Run

```
python3 manage.py runserver
```

8. Test

Go to [http://localhost:8000](http://localhost:8000)

Test with credit card number `4242424242424242`
